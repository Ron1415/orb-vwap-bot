"""Statistics shared by the backtest, the live review and the pages."""
from __future__ import annotations

import math

import config as C
from engine import hhmm

LABELS = {
    "or_opposite": "Stop: other side of range", "or_mid": "Stop: middle of range", "vwap": "Stop: VWAP",
    "signal_bar": "Stop: signal bar",
    "r1": "Target 1R", "r2": "Target 2R", "r3": "Target 3R", "or_width": "Target: range width",
    "eod": "Hold to 3:55 PM", "half_r1_trail_vwap": "Half at 1R, trail VWAP", "trail_vwap": "Trail VWAP",
}


def variant_name(rules: dict) -> str:
    return f"{LABELS[rules['stop']]}; {LABELS[rules['target']]}"


def stats(trades: list[dict], sessions: int | None = None, key: str = "r_net") -> dict:
    n = len(trades)
    if n == 0:
        return {"n": 0}
    rs = [t[key] for t in trades]
    avg = sum(rs) / n
    sd = math.sqrt(sum((r - avg) ** 2 for r in rs) / (n - 1)) if n > 1 else 0.0
    wins = sum(r for r in rs if r > 0)
    losses = -sum(r for r in rs if r < 0)
    eq = peak = dd = 0.0
    for t in trades:
        eq += t["r_sized"]
        peak = max(peak, eq)
        dd = min(dd, eq - peak)
    out = {
        "n": n, "win": round(sum(r > 0 for r in rs) / n * 100, 1), "avg": round(avg, 3),
        "se": round(sd / math.sqrt(n), 3) if n > 1 else None,
        "t": round(avg / (sd / math.sqrt(n)), 2) if n > 1 and sd > 0 else None,
        "pf": round(wins / losses, 2) if losses > 0 else None,
        "total": round(sum(rs), 2), "sized_total": round(sum(t["r_sized"] for t in trades), 2),
        "max_dd": round(dd, 2), "avg_pct": round(sum(t["pct_net"] for t in trades) / n, 4),
    }
    if sessions:
        out["per_week"] = round(n / sessions * 5, 2)
    return out


def halves(trades: list[dict], dates: list[str]) -> list[dict]:
    if not dates:
        return []
    mid = dates[len(dates) // 2]
    a = [t for t in trades if t["date"] < mid]
    b = [t for t in trades if t["date"] >= mid]
    return [{"label": f"{dates[0]} to {mid}", **stats(a)}, {"label": f"{mid} to {dates[-1]}", **stats(b)}]


def by_key(trades: list[dict], fn, order=None) -> list[dict]:
    groups: dict = {}
    for t in trades:
        groups.setdefault(fn(t), []).append(t)
    keys = order or sorted(groups, key=lambda k: (k is None, str(k)))
    return [{"label": str(k), **stats(groups[k])} for k in keys if k in groups]


def buckets(trades: list[dict], feature: str) -> list[dict]:
    vals = sorted(t[feature] for t in trades if t.get(feature) is not None)
    if len(vals) < 8:
        return []
    cuts = [vals[int(len(vals) * q)] for q in (0.25, 0.5, 0.75)]
    fmt = (lambda v: hhmm(v)) if feature == "signal_min" else (lambda v: f"{v:.3g}")
    edges = [None] + cuts + [None]
    out = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        grp = [t for t in trades if t.get(feature) is not None
               and (lo is None or t[feature] >= lo) and (hi is None or t[feature] < hi)]
        label = (f"under {fmt(hi)}" if lo is None else f"{fmt(lo)} and over" if hi is None else f"{fmt(lo)} to {fmt(hi)}")
        out.append({"label": label, **stats(grp)})
    return out


def daily_load(trades: list[dict]) -> dict:
    """How trades stack up on the same day (all ETFs together): counts and the day's total R (size-weighted)."""
    days: dict = {}
    for t in trades:
        d = days.setdefault(t["date"], [0, 0.0])
        d[0] += 1
        d[1] += t["r_sized"]
    if not days:
        return {}
    counts = [v[0] for v in days.values()]
    totals = sorted(v[1] for v in days.values())
    return {"days_with_trades": len(days), "avg_trades_per_day": round(sum(counts) / len(days), 2),
            "max_trades_per_day": max(counts), "share_days_3plus": round(sum(c >= 3 for c in counts) / len(days) * 100, 1),
            "worst_day_r": round(totals[0], 2), "best_day_r": round(totals[-1], 2),
            "worst_5pct_day_r": round(totals[max(0, int(len(totals) * 0.05) - 1)], 2)}


def breakdowns(trades: list[dict]) -> dict:
    out = {
        "ETF": by_key(trades, lambda t: t.get("symbol", C.SYMBOL), C.SYMBOLS),
        "Side": by_key(trades, lambda t: t["side"], ["long", "short"]),
        "Exit": by_key(trades, lambda t: t["exit_reason"]),
        "Signal hour": by_key(trades, lambda t: hhmm(t["signal_min"] // 30 * 30)),
        "Weekday": by_key(trades, lambda t: t["weekday"], ["Mon", "Tue", "Wed", "Thu", "Fri"]),
        "With daily trend (close vs 20-day)": by_key(trades, lambda t: "with" if (t["side"] == "long") == t["above_sma20"] else "against"),
        "With first 15-min candle": by_key(trades, lambda t: "with" if (t["side"] == "long") == t["or_candle_up"] else "against"),
        "Month": by_key(trades, lambda t: t["date"][:7]),
    }
    for f in C.BUCKET_FEATURES:
        b = buckets(trades, f)
        if b:
            out[f"Quartiles: {f}"] = b
    return out


def equity(trades: list[dict]) -> list[list]:
    eq, out = 0.0, []
    for t in trades:
        eq += t["r_sized"]
        out.append([t["date"], round(eq, 3)])
    return out
