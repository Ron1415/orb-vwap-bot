"""Live paper trading (no broker). Runs every few minutes in the session.

- live/today.json: today's range, VWAP, last price and status for the dashboard.
- live/paper_trades.json: one record per day with a signal, followed with the backtest rules.
- End of day: the final result, plus what every test variant would have done that day.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import backtest
import config as C
import data
import engine as E
import review

ROOT = Path(__file__).resolve().parent
LIVE = ROOT / "live"
TRADES = LIVE / "paper_trades.json"
TODAY = LIVE / "today.json"


def _load() -> list:
    try:
        return json.loads(TRADES.read_text())
    except Exception:
        return []


def _save(trades: list) -> None:
    LIVE.mkdir(exist_ok=True)
    TRADES.write_text(json.dumps(trades, indent=1, default=str))


def _ctx(date: str) -> dict:
    return E.daily_context(data.yahoo_daily(C.SYMBOL), date)


def scan(final: bool = False) -> dict:
    now = dt.datetime.now(data.NY)
    date = now.strftime("%Y-%m-%d")
    bars, src = data.today_bars()
    bars = E.rth(bars)
    info = {"date": date, "checked": now.strftime("%H:%M ET"), "source": src, "bars": len(bars), "errors": data.ERRORS[:3]}
    if not bars:
        info["status"] = "Market closed or no data yet"
        LIVE.mkdir(exist_ok=True)
        TODAY.write_text(json.dumps(info, indent=1))
        return info
    rules = C.RULES
    vw = E.session_vwap(bars)
    orr = E.opening_range(bars, rules["or_minutes"])
    info.update({"last": round(bars[-1].c, 2), "last_bar": E.hhmm(bars[-1].minute), "vwap": round(vw[-1], 2)})
    if orr:
        info.update({"or_high": round(orr[0], 2), "or_low": round(orr[1], 2)})
    ctx = _ctx(date)
    tr, status = E.run_day(bars, ctx, rules)
    info["status"] = status
    trades = _load()
    rec = next((t for t in trades if t["date"] == date), None)
    if tr:
        tr["date"] = date
        if rec is None:
            tr["detected"] = now.strftime("%H:%M ET")
            trades.append(tr)
            rec = tr
        else:
            rec.update({k: v for k, v in tr.items() if k != "detected"})
        info["trade"] = {k: rec[k] for k in ("side", "entry", "stop", "target", "exit_reason", "r_net")}
        if final:
            rec["variants"] = {}
            for name, r in backtest.variants().items():
                vt, _ = E.run_day(bars, ctx, r)
                if vt and name != "Baseline":
                    rec["variants"][name] = vt["r_net"]
        _save(trades)
    elif final:
        info["final"] = True
    TODAY.write_text(json.dumps(info, indent=1, default=str))
    if final:
        (LIVE / "review.md").write_text(review.live_review(trades))
    return info
