"""Plain-English review files (review.md) for the backtest and the live paper trades."""
from __future__ import annotations

import config as C


def _s(st: dict) -> str:
    if not st or not st.get("n"):
        return "no trades"
    se = f" ±{st['se']:.2f}" if st.get("se") else ""
    pf = f", profit factor {st['pf']}" if st.get("pf") else ""
    wk = f", {st['per_week']} per week" if st.get("per_week") else ""
    return f"{st['n']} trades{wk}, {st['win']}% win, {st['avg']:+.2f}R{se} per trade{pf}, max drawdown {st['max_dd']}R"


def candidates(summary: dict) -> list[dict]:
    out = []
    for row in summary["grid"]:
        for f, st in row["cells"].items():
            if st.get("n", 0) < C.MIN_TRADES_TO_JUDGE:
                continue
            ha = st.get("half_avgs") or [None, None]
            out.append({"variant": row["variant"], "filter": f, **st,
                        "steady": all(h is not None and h > 0 for h in ha) and (st.get("recent_avg") or 0) > 0})
    return sorted(out, key=lambda x: x["avg"], reverse=True)


def backtest_review(s: dict) -> str:
    b = s["baseline"]
    L = [f"# ETF ORB-15 + VWAP: backtest review", "",
         f"Generated {s['generated']}. ETFs traded: {', '.join(s.get('symbols') or [C.SYMBOL])}; watch only: {', '.join(s.get('watch_symbols') or []) or 'none'}. Main candidate: {s.get('main_strategy', '-')}. Data: {s['source']}. {s['sessions']} sessions, {s['first']} to {s['last']}. "
         f"Results are net of {C.COST_PER_SHARE_PER_SIDE * 100:.0f} cent per share per side.", ""]
    if s.get("errors"):
        L += ["**Data warnings:** " + "; ".join(s["errors"]), ""]
    L += ["## Baseline (version 1)",
          "Range 9:30-9:45; first 5-minute close outside the range on the same side of VWAP, before 11:30; "
          "entry at the next bar's open; stop at the other side of the range; target 2R; exit 3:55 PM; one trade a day.", "",
          f"- **All:** {_s(b['all'])}", f"- **Gross of costs:** {b['gross'].get('avg', 0):+.2f}R per trade",
          f"- **Last 6 months:** {_s(b['recent'])}"]
    for h in b["halves"]:
        L.append(f"- **{h['label']}:** {_s(h)}")
    L.append(f"- **Size-weighted total (longs 1x, shorts 0.5x):** {b['all'].get('sized_total', 0)}R")
    L.append("- **Days without a trade:** " + (", ".join(f"{k} {v}" for k, v in b["status"].items() if k != "trade") or "none"))
    if s.get("strategies"):
        L += ["", "## The paper-traded strategies",
              f"The candle and volume factors were found on {s['factors_found_from']} onward. Earlier sessions "
              f"({s.get('out_of_sample_sessions', 0)}) are out of sample: the fair test of v2 and v3.", "",
              "| Strategy | Out of sample | Found period | Last 6 months | All |", "|---|---|---|---|---|"]
        cell = lambda st: (f"{st['n']} trades, {st['avg']:+.2f}R, t {st.get('t') or '-'}, PF {st.get('pf') or '-'}"
                           if st.get("n") else "no trades")
        for name, st in s["strategies"].items():
            L.append(f"| {name} | {cell(st['out_of_sample'])} | {cell(st['in_sample'])} | {cell(st['recent'])} | {cell(st['all'])} |")
        for name, st in s["strategies"].items():
            if st.get("watch_shorts", {}).get("n"):
                L.append(f"- **{name}, watch-only shorts (not counted):** all {cell(st['watch_shorts'])}; "
                         f"out of sample {cell(st['watch_shorts_oos'])}")
        for name, st in s["strategies"].items():
            if st.get("watch_symbols", {}).get("n"):
                L.append(f"- **{name}, watch-only ETFs {', '.join(s.get('watch_symbols') or [])} (not counted):** {cell(st['watch_symbols'])}")
        for name, st in s["strategies"].items():
            if st.get("by_symbol_oos"):
                L.append(f"- **{name} by ETF, out of sample:** " + "; ".join(f"{r['label']} {r.get('avg', 0):+.2f}R (n={r['n']})" for r in st["by_symbol_oos"]))
            d = st.get("daily_load") or {}
            if d:
                L.append(f"- **{name} same-day load:** {d['avg_trades_per_day']} trades a day on average, up to {d['max_trades_per_day']}; "
                         f"3+ trades on {d['share_days_3plus']}% of trading days; worst day {d['worst_day_r']}R, worst 5% of days {d['worst_5pct_day_r']}R or less")
        for name, st in s["strategies"].items():
            L.append(f"- **{name} by year:** " + "; ".join(f"{r['label']} {r.get('avg', 0):+.2f}R (n={r['n']})" for r in st["by_year"]))
    L += ["", "## Best variant and filter combinations (at least "
          f"{C.MIN_TRADES_TO_JUDGE} trades)", "",
          "| Variant | Filter | Trades | Win | Avg R | ±SE | PF | Halves | Last 6 mo | Steady |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    cands = candidates(s)
    for c in cands[:12]:
        ha = " / ".join(f"{h:+.2f}" if h is not None else "-" for h in c["half_avgs"])
        L.append(f"| {c['variant']} | {c['filter']} | {c['n']} | {c['win']}% | {c['avg']:+.2f} | {c.get('se') or '-'} | "
                 f"{c.get('pf') or '-'} | {ha} | {(c.get('recent_avg') or 0):+.2f} | {'yes' if c['steady'] else 'no'} |")
    L += ["", "## Reading the evidence", ""]
    cells = sum(1 for row in s["grid"] for st in row["cells"].values() if st.get("n", 0) >= C.MIN_TRADES_TO_JUDGE)
    # About 1 cell in 40 shows t >= 2 by luck alone, so with this many cells the bar is t >= 3.
    good = [c for c in cands if c["steady"] and (c.get("t") or 0) >= 3 and c["avg"] >= 0.1]
    if good:
        g = good[0]
        L.append(f"- **Candidate:** {g['variant']} with filter \"{g['filter']}\": {g['avg']:+.2f}R per trade "
                 f"(t = {g['t']}), positive in both halves and in the last 6 months. Paper trade before any change.")
    else:
        L.append("- **No combination is clearly positive** (needs +0.10R or more, t of 3 or more, both halves and "
                 "the last 6 months positive). Do not automate yet.")
    L.append(f"- {cells} cells were compared; about {max(1, round(cells / 40))} would reach t = 2 by luck alone, which is why the bar is t = 3.")
    L.append("- Many combinations are tested, so the best one is partly luck. Treat a winner as a hypothesis to "
             "confirm on paper trades, not as proof.")
    L += ["", "## Baseline breakdowns", ""]
    for name, rows in b["breakdowns"].items():
        if name == "Month":
            continue
        L.append(f"**{name}:** " + "; ".join(f"{r['label']} {r.get('avg', 0):+.2f}R (n={r['n']})" for r in rows))
        L.append("")
    return "\n".join(L) + "\n"


def live_review(trades: list[dict]) -> str:
    import analysis as A
    L = ["# ETF ORB-15 + VWAP: live paper review", ""]
    closed = [t for t in trades if t.get("exit_reason") not in (None, "open")]
    for name in C.STRATEGIES:
        mine = [t for t in closed if t.get("strategy", "v1 control") == name]
        L.append(f"- **{name}:** {_s(A.stats([t for t in mine if not t.get('watch')]))}")
        w = [t for t in mine if t.get("watch")]
        if w:
            L.append(f"  - watch-only shorts (not counted): {_s(A.stats(w))}")
    closed = [t for t in closed if t.get("strategy", "v1 control") == "v1 control"]
    by_v: dict = {}
    for t in closed:
        for v, r in (t.get("variants") or {}).items():
            by_v.setdefault(v, []).append(r)
    if by_v:
        L += ["", "| Variant | Trades | Avg R | Total R |", "|---|---|---|---|"]
        for v, rs in sorted(by_v.items(), key=lambda x: -sum(x[1]) / len(x[1])):
            L.append(f"| {v} | {len(rs)} | {sum(rs) / len(rs):+.2f} | {sum(rs):+.2f} |")
    L.append("")
    L.append("Compare these with the backtest after about 40 paper trades.")
    return "\n".join(L) + "\n"
