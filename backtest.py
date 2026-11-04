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


def _status_key(tr, st: str) -> str:
    return "trade" if tr else ("skipped: " + st.split("skipped, ")[1] if "skipped, " in st
                               else "no breakout before cutoff" if st.startswith("No breakout")
                               else "no bar to enter" if "no bar to enter" in st else st)


def _sorted(trades: list) -> list:
    return sorted(trades, key=lambda t: (t["date"], t["signal_min"], t["symbol"]))


def run_days(market: dict, dates: list[str], fn) -> tuple[list, dict]:
    """fn(bars, ctx) -> (trade, status) for every ETF on every date (one trade per ETF per day)."""
    trades, status = [], {}
    for sym, m in market.items():
        for d in dates:
            if d not in m["by_day"]:
                continue
            tr, st = fn(m["by_day"][d], E.daily_context(m["daily"], d))
            key = _status_key(tr, st)
            status[key] = status.get(key, 0) + 1
            if tr:
                tr["date"], tr["symbol"] = d, sym
                trades.append(tr)
    return _sorted(trades), status


def load_market(days: int) -> tuple[dict, str]:
    market, sources = {}, set()
    for sym in C.SYMBOLS:
        by_day, src = data.history(days, sym)
        if by_day:
            market[sym] = {"by_day": by_day}
            sources.add(src)
        else:
            log.warning("No data for %s", sym)
    return market, ", ".join(sorted(sources))


def run(days: int = C.BACKTEST_DAYS, market: dict | None = None, source: str = "", by_day: dict | None = None) -> dict:
    if by_day is not None:                      # single-symbol call (tests)
        market = {C.SYMBOL: {"by_day": by_day}}
    if market is None:
        market, source = load_market(days)
    for m in market.values():
        m["daily"] = E.daily_from_intraday(m["by_day"])
    ref = market.get(C.SYMBOL) or next(iter(market.values()))
    full = [d for d in sorted(ref["by_day"]) if len(E.rth(ref["by_day"][d])) >= 60]       # skip half days
    # the first DAILY_LOOKBACK calendar days only feed the 20/50-day context
    lead = (dt.date.fromisoformat(full[0]) + dt.timedelta(days=C.DAILY_LOOKBACK)).isoformat() if full else ""
    dates = [d for d in full if d >= lead] if len(full) > 120 else full
    dates = dates[-days:]
    recent = dates[-C.RECENT_DAYS:]
    log.info("%d sessions %s to %s, %d ETFs, from %s", len(dates), dates[0] if dates else "-",
             dates[-1] if dates else "-", len(market), source)

    OUT.mkdir(exist_ok=True)
    rows, grid = [], []
    base_trades, base_status = [], {}
    for name, rules in variants().items():
        trades, status = run_days(market, dates, lambda bars, ctx, r=rules: E.run_day(bars, ctx, r))
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
        trades, _ = run_days(market, dates, lambda bars, ctx, n=name: E.run_strategy(bars, ctx, n))
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
            "by_symbol": A.by_key(trades, lambda t: t["symbol"], [s for s in C.SYMBOLS if s in market]),
            "by_symbol_oos": A.by_key([t for t in trades if t["date"] < cut], lambda t: t["symbol"], [s for s in C.SYMBOLS if s in market]),
            "daily_load": A.daily_load(trades),
            "equity": A.equity(trades),
        }

    rec_base = [t for t in base_trades if recent and t["date"] >= recent[0]]
    summary = {
        "generated": dt.datetime.now(data.NY).strftime("%Y-%m-%d %H:%M ET"),
        "source": source, "errors": data.ERRORS[:5], "symbols": [s for s in C.SYMBOLS if s in market],
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
