"""Builds the GitHub Pages dashboard: site/index.html (self-contained) plus copies of the data files."""
from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

import analysis as A
import config as C
from engine import hhmm

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"


def _j(p: Path, default):
    try:
        return json.loads(p.read_text())
    except Exception:
        return default


def _cls(v):
    if v is None:
        return "na"
    return "pos2" if v >= 0.15 else "pos" if v > 0.03 else "neg2" if v <= -0.15 else "neg" if v < -0.03 else "flat"


def _r(v):
    return "-" if v is None else f"{v:+.2f}"


def _tiles(st: dict, label: str) -> str:
    if not st or not st.get("n"):
        return f"<div class='card'><h3>{label}</h3><p class='muted'>No trades yet.</p></div>"
    items = [("Trades", st["n"]), ("Per week", st.get("per_week", "-")), ("Win rate", f"{st['win']}%"),
             ("Avg R (net)", _r(st["avg"]) + (f" <small>±{st['se']}</small>" if st.get("se") else "")),
             ("Profit factor", st.get("pf") or "-"), ("Max drawdown", f"{st['max_dd']}R")]
    cells = "".join(f"<div class='tile'><span>{k}</span><b>{v}</b></div>" for k, v in items)
    return f"<div class='card'><h3>{label}</h3><div class='tiles'>{cells}</div></div>"


def _equity_svg(eq: list) -> str:
    if len(eq) < 2:
        return ""
    w, h, p = 900, 230, 34
    ys = [e[1] for e in eq] + [0]
    lo, hi = min(ys), max(ys)
    span = (hi - lo) or 1
    X = lambda i: p + i * (w - 2 * p) / (len(eq) - 1)
    Y = lambda v: h - p - (v - lo) * (h - 2 * p) / span
    pts = " ".join(f"{X(i):.1f},{Y(e[1]):.1f}" for i, e in enumerate(eq))
    return (f"<svg viewBox='0 0 {w} {h}' class='eq' role='img' aria-label='Cumulative R'>"
            f"<line x1='{p}' x2='{w - p}' y1='{Y(0):.1f}' y2='{Y(0):.1f}' class='zero'/>"
            f"<polyline points='{pts}' class='line'/>"
            f"<text x='{p}' y='{h - 6}' class='lbl'>{eq[0][0]}</text><text x='{w - p}' y='{h - 6}' text-anchor='end' class='lbl'>{eq[-1][0]}: {eq[-1][1]:+.1f}R</text>"
            f"<text x='{p - 4}' y='{Y(hi):.1f}' text-anchor='end' class='lbl'>{hi:+.0f}</text>"
            f"<text x='{p - 4}' y='{Y(lo):.1f}' text-anchor='end' class='lbl'>{lo:+.0f}</text></svg>")


def _grid(s: dict) -> str:
    fl = s["filters"]
    head = "".join(f"<th>{html.escape(f)}</th>" for f in fl)
    rows = []
    for row in s["grid"]:
        tds = []
        for f in fl:
            c = row["cells"].get(f, {})
            if not c.get("n"):
                tds.append("<td class='na'>-</td>")
                continue
            tip = (f"{c['n']} trades, {c['win']}% win, PF {c.get('pf') or '-'}, halves "
                   f"{' / '.join(_r(x) for x in c.get('half_avgs', []))}, last 6 months {_r(c.get('recent_avg'))} (n={c.get('recent_n')})")
            tds.append(f"<td class='{_cls(c['avg'])} cell' title='{html.escape(tip)}' data-all='{_r(c['avg'])}' "
                       f"data-recent='{_r(c.get('recent_avg'))}' data-cls-all='{_cls(c['avg'])}' data-cls-recent='{_cls(c.get('recent_avg'))}'>"
                       f"<b>{_r(c['avg'])}</b><small>n={c['n']}</small></td>")
        name = "<b>Baseline</b>" if row["variant"] == "Baseline" else html.escape(row["variant"])
        rows.append(f"<tr><th class='rowh'>{name}</th>{''.join(tds)}</tr>")
    return (f"<div class='scroll'><table class='grid'><thead><tr><th>Variant</th>{head}</tr></thead>"
            f"<tbody>{''.join(rows)}</tbody></table></div>")


def _table(rows: list, title: str) -> str:
    body = "".join(f"<tr><td>{html.escape(str(r['label']))}</td><td>{r['n']}</td><td>{r.get('win', '-')}%</td>"
                   f"<td class='{_cls(r.get('avg'))}'>{_r(r.get('avg'))}</td><td>{r.get('pf') or '-'}</td></tr>" for r in rows)
    return (f"<div class='mini'><h4>{html.escape(title)}</h4><table><thead><tr><th></th><th>n</th><th>Win</th><th>Avg R</th><th>PF</th></tr></thead>"
            f"<tbody>{body}</tbody></table></div>")


def _today(t: dict) -> str:
    if not t:
        return "<p class='muted'>No live check yet.</p>"
    kv = [("Status", t.get("status")), ("Range high", t.get("or_high")), ("Range low", t.get("or_low")),
          ("VWAP", t.get("vwap")), ("Last", f"{t.get('last')} ({t.get('last_bar')} bar)" if t.get("last") else None),
          ("Checked", f"{t.get('date')} {t.get('checked')} via {t.get('source')}")]
    tr = t.get("trade")
    if tr:
        kv.insert(1, ("Paper trade", f"{tr['side'].upper()} at {tr['entry']}, stop {tr['stop']}, target {tr['target']}, "
                                    f"{tr['exit_reason']} {_r(tr['r_net'])}R"))
    return "<dl class='kv'>" + "".join(f"<dt>{k}</dt><dd>{html.escape(str(v))}</dd>" for k, v in kv if v is not None) + "</dl>"


def _paper(trades: list) -> str:
    if not trades:
        return "<p class='muted'>No paper trades yet. The bot records the first signal each day.</p>"
    rows = "".join(
        f"<tr><td>{t['date']}</td><td>{t['side']}</td><td>{hhmm(t['signal_min'])}</td><td>{t.get('detected', '-')}</td>"
        f"<td>{t['entry']}</td><td>{t['stop']}</td><td>{t.get('target') or '-'}</td><td>{t['exit']}</td><td>{t['exit_reason']}</td>"
        f"<td class='{_cls(t['r_net'])}'>{_r(t['r_net'])}</td></tr>" for t in reversed(trades[-60:]))
    st = A.stats([t for t in trades if t["exit_reason"] != "open"])
    summ = f"<p>{st['n']} closed, {st.get('win', 0)}% win, {_r(st.get('avg'))}R per trade.</p>" if st.get("n") else ""
    return (summ + "<div class='scroll'><table><thead><tr><th>Date</th><th>Side</th><th>Signal bar</th><th>Seen</th><th>Entry</th>"
            "<th>Stop</th><th>Target</th><th>Exit</th><th>How</th><th>R net</th></tr></thead><tbody>" + rows + "</tbody></table></div>")


CSS = """
:root{--bg:#f7f8fa;--card:#fff;--ink:#1b2430;--muted:#667085;--line:#e3e7ee;--accent:#2f6fde;
--pos:#d8f0df;--pos2:#a9dfb8;--neg:#f8dcdc;--neg2:#efb0b0;--flat:#f1f3f6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11151b;--card:#1a2029;--ink:#e6e9ee;--muted:#98a2b3;
--line:#2a323e;--accent:#6c9cf0;--pos:#1f3a29;--pos2:#2b5a3b;--neg:#43262a;--neg2:#6a3036;--flat:#222a35}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1200px;margin:0 auto;padding:16px}h1{font-size:22px;margin:4px 0}h2{font-size:17px;margin:24px 0 8px}
h3{font-size:14px;margin:0 0 8px;color:var(--muted);font-weight:600}h4{margin:0 0 6px;font-size:13px}
.muted{color:var(--muted)}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin:8px 0}
.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.tile span{display:block;color:var(--muted);font-size:12px}.tile b{font-size:18px}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}th,td{padding:5px 7px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th:first-child,td:first-child{text-align:left}.scroll{overflow-x:auto}
.grid td{min-width:78px}.grid td b{display:block}.grid td small{color:var(--muted)}.rowh{font-weight:400;text-align:left;white-space:normal;min-width:220px}
.pos{background:var(--pos)}.pos2{background:var(--pos2)}.neg{background:var(--neg)}.neg2{background:var(--neg2)}.flat{background:var(--flat)}.na{color:var(--muted)}
.minis{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
.kv{display:grid;grid-template-columns:max-content 1fr;gap:4px 14px;margin:0}.kv dt{color:var(--muted)}.kv dd{margin:0}
.eq{width:100%;height:auto}.eq .line{fill:none;stroke:var(--accent);stroke-width:2}.eq .zero{stroke:var(--line);stroke-dasharray:4 4}.eq .lbl{fill:var(--muted);font-size:12px}
.toggle button{border:1px solid var(--line);background:var(--card);color:var(--ink);padding:4px 10px;border-radius:6px;cursor:pointer}
.toggle button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
pre{white-space:pre-wrap;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;font-size:12.5px}
"""

JS = """
document.querySelectorAll('.toggle button').forEach(b=>b.addEventListener('click',()=>{
 document.querySelectorAll('.toggle button').forEach(x=>x.classList.toggle('on',x===b));
 const k=b.dataset.k;document.querySelectorAll('td.cell').forEach(td=>{
  td.className='cell '+td.dataset['cls'+(k==='all'?'All':'Recent')];td.querySelector('b').textContent=td.dataset[k];});
}));
"""


def build() -> Path:
    s = _j(ROOT / "backtest" / "summary.json", None)
    today = _j(ROOT / "live" / "today.json", {})
    paper = _j(ROOT / "live" / "paper_trades.json", [])
    rev = (ROOT / "backtest" / "review.md").read_text() if (ROOT / "backtest" / "review.md").exists() else ""
    parts = [f"<main><h1>SPY Opening Range + VWAP bot</h1><p class='muted'>Testing phase. Paper trades only; no broker connection.</p>",
             "<h2>Today</h2><div class='card'>" + _today(today) + "</div>",
             "<h2>Live paper trades</h2><div class='card'>" + _paper(paper) + "</div>"]
    if s:
        b = s["baseline"]
        parts += [f"<h2>Backtest</h2><p class='muted'>{s['sessions']} sessions, {s['first']} to {s['last']} ({html.escape(s['source'])}). "
                  f"Generated {s['generated']}. Net of {C.COST_PER_SHARE_PER_SIDE * 100:.0f}¢ per share per side.</p>",
                  "<div class='row'>" + _tiles(b["all"], "Baseline, full period") + _tiles(b["recent"], f"Baseline, last 6 months (from {s.get('recent_first')})") + "</div>",
                  "<div class='card'><h3>Baseline cumulative R (longs 1x, shorts 0.5x)</h3>" + _equity_svg(b["equity"]) + "</div>",
                  "<h2>Side-by-side tests</h2><p class='muted'>Average R per trade, net of costs. Hover a cell for trades, win rate, halves and the last 6 months. "
                  f"Judge only cells with at least {C.MIN_TRADES_TO_JUDGE} trades.</p>"
                  "<div class='toggle'><button class='on' data-k='all'>Full period</button> <button data-k='recent'>Last 6 months</button></div>",
                  "<div class='card'>" + _grid(s) + "</div>",
                  "<h2>Baseline breakdowns</h2><div class='minis'>" + "".join(_table(v, k) for k, v in b["breakdowns"].items()) + "</div>"]
    else:
        parts.append("<h2>Backtest</h2><p class='muted'>Not run yet. Run the workflow with mode <b>backtest</b>.</p>")
    if rev:
        parts.append("<h2>Review file</h2><pre>" + html.escape(rev) + "</pre>")
    parts.append("</main>")
    page = ("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>SPY ORB VWAP Bot</title><style>{CSS}</style></head><body>{''.join(parts)}<script>{JS}</script></body></html>")
    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(page)
    for p in [ROOT / "backtest" / "summary.json", ROOT / "live" / "paper_trades.json", ROOT / "live" / "today.json"]:
        if p.exists():
            shutil.copy(p, SITE / p.name)
    return SITE / "index.html"


if __name__ == "__main__":
    print(build())
