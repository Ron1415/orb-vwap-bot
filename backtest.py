"""Backtest: every session re-run with the baseline and every test variant.

Writes backtest/trades.csv.gz (one row per variant per trade), backtest/summary.json
and backtest/review.md. Judge results net of costs, and on the full period and the recent 6 months.
"""
from __future__ import annotations

import csv
import datetime as dt
import gzip
import json
import logging
from pathlib import Path

import analysis as A
import config as C
import data
import engine as E

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "backtest"
log = logging.getLogger("backtest")


def variants() -> dict[str, dict]:
    base = dict(C.RULES)
    out = {"Baseline": base}
    for s in C.TEST_STOPS:
        for t in C.TEST_TARGETS:
            r = dict(base, stop=s, target=t)
            name = A.variant_name(r)
            if s == base["stop"] and t == base["target"]:
                continue                      # same as the baseline
            out[name] = r
    for name, change in C.EXTRA_VARIANTS.items():
        out[name] = dict(base, **change)
    return out


def run_days(by_day: dict, dates: list[str], rules: dict, daily: list[dict]) -> tuple[list, dict]:
    trades, status = [], {}
    for d in dates:
        ctx = E.daily_context(daily, d)
        tr, st = E.run_day(by_day[d], ctx, rules)
        key = "trade" if tr else ("skipped: " + st.split("skipped, ")[1] if "skipped, " in st
                                   else "no breakout before cutoff" if st.startswith("No breakout")
                                   else "no bar to enter" if "no bar to enter" in st else st)
        status[key] = status.get(key, 0) + 1
        if tr:
            tr["date"] = d
            trades.append(tr)
    return trades, status


def run(days: int = C.BACKTEST_DAYS, by_day: dict | None = None, source: str = "") -> dict:
    if by_day is None:
        by_day, source = data.history(days)
    daily = E.daily_from_intraday(by_day)
    full = [d for d in sorted(by_day) if len(E.rth(by_day[d])) >= 60]       # skip half days
    # the first DAILY_LOOKBACK calendar days only feed the 20/50-day context
    lead = (dt.date.fromisoformat(full[0]) + dt.timedelta(days=C.DAILY_LOOKBACK)).isoformat() if full else ""
    dates = [d for d in full if d >= lead] if len(full) > 120 else full
    dates = dates[-days:]
    recent = dates[-C.RECENT_DAYS:]
    log.info("%d sessions %s to %s from %s", len(dates), dates[0] if dates else "-", dates[-1] if dates else "-", source)

    OUT.mkdir(exist_ok=True)
    rows, grid = [], []
    base_trades, base_status = [], {}
    for name, rules in variants().items():
        trades, status = run_days(by_day, dates, rules, daily)
        if name == "Baseline":
            base_trades, base_status = trades, status
        for t in trades:
            rows.append({"variant": name, **t})
        cells = {}
        for fname, fn in C.FILTERS.items():
            sel = [t for t in trades if fn(t)]
            rec = [t for t in sel if t["date"] >= recent[0]] if recent else []
            st = A.stats(sel, len(dates))
            st["recent_avg"] = A.stats(rec).get("avg")
            st["recent_n"] = len(rec)
            h = A.halves(sel, dates)
            st["half_avgs"] = [x.get("avg") for x in h]
            cells[fname] = st
        grid.append({"variant": name, "rules": {k: rules[k] for k in ("or_minutes", "entry", "entry_cutoff", "stop", "target")}, "cells": cells})

    # ---- the strategies paper traded side by side (config.STRATEGIES); watch-only shorts reported apart
    strategies = {}
    cut = C.FACTORS_FOUND_FROM
    oos_dates = [d for d in dates if d < cut]
    ins_dates = [d for d in dates if d >= cut]
    for name in C.STRATEGIES:
        trades = []
        for d in dates:
            tr, _ = E.run_strategy(by_day[d], E.daily_context(daily, d), name)
            if tr:
                tr["date"] = d
                trades.append(tr)
        for t in trades:
            rows.append({"variant": f"Strategy: {name}", **t})
        watch = [t for t in trades if t.get("watch")]
        trades = [t for t in trades if not t.get("watch")]
        strategies[name] = {
            "watch_shorts": A.stats(watch, len(dates)),
            "watch_shorts_oos": A.stats([t for t in watch if t["date"] < cut], len(oos_dates)),
            "all": A.stats(trades, len(dates)),
            "out_of_sample": A.stats([t for t in trades if t["date"] < cut], len(oos_dates)),
            "in_sample": A.stats([t for t in trades if t["date"] >= cut], len(ins_dates)),
            "recent": A.stats([t for t in trades if recent and t["date"] >= recent[0]], len(recent)),
            "by_year": A.by_key(trades, lambda t: t["date"][:4]),
            "by_side": A.by_key(trades, lambda t: t["side"], ["long", "short"]),
            "equity": A.equity(trades),
        }

    rec_base = [t for t in base_trades if recent and t["date"] >= recent[0]]
    summary = {
        "generated": dt.datetime.now(data.NY).strftime("%Y-%m-%d %H:%M ET"),
        "source": source, "errors": data.ERRORS[:5],
        "sessions": len(dates), "first": dates[0] if dates else None, "last": dates[-1] if dates else None,
        "recent_first": recent[0] if recent else None,
        "rules": C.RULES, "cost_per_share_per_side": C.COST_PER_SHARE_PER_SIDE,
        "baseline": {
            "all": A.stats(base_trades, len(dates)), "recent": A.stats(rec_base, len(recent)),
            "gross": A.stats(base_trades, len(dates), key="r_gross"),
            "halves": A.halves(base_trades, dates), "status": base_status,
            "breakdowns": A.breakdowns(base_trades), "equity": A.equity(base_trades),
            "last_trades": base_trades[-15:],
        },
        "filters": list(C.FILTERS), "grid": grid,
        "strategies": strategies, "factors_found_from": cut,
        "out_of_sample_sessions": len(oos_dates), "in_sample_sessions": len(ins_dates),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, default=str))
    if rows:
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with gzip.open(OUT / "trades.csv.gz", "wt", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
    import review
    (OUT / "review.md").write_text(review.backtest_review(summary))
    return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
