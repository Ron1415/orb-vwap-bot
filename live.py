"""Live paper trading (no broker). Runs every few minutes in the session.

- live/today.json: today's range, VWAP, last price and each strategy's status for the dashboard.
- live/paper_trades.json: one record per day per strategy (v1 control, v2 candle, v3 candle + volume),
  followed with the backtest rules. At the end of the day, the control record also stores what every
  test variant would have done.
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
FIELDS = ("strategy", "side", "entry", "stop", "target", "exit_reason", "r_net")


def _load() -> list:
    try:
        out = json.loads(TRADES.read_text())
    except Exception:
        return []
    for t in out:
        t.setdefault("strategy", "v1 control")      # records from before November 4
    return out


def _save(trades: list) -> None:
    LIVE.mkdir(exist_ok=True)
    TRADES.write_text(json.dumps(trades, indent=1, default=str))


def scan(final: bool = False) -> dict:
    now = dt.datetime.now(data.NY)
    date = now.strftime("%Y-%m-%d")
    bars, src = data.today_bars()
    bars = E.rth(bars)
    info = {"date": date, "checked": now.strftime("%H:%M ET"), "source": src, "bars": len(bars), "errors": data.ERRORS[:3]}
    LIVE.mkdir(exist_ok=True)
    if not bars:
        info["status"] = "Market closed or no data yet"
        TODAY.write_text(json.dumps(info, indent=1))
        return info
    vw = E.session_vwap(bars)
    orr = E.opening_range(bars, C.RULES["or_minutes"])
    info.update({"last": round(bars[-1].c, 2), "last_bar": E.hhmm(bars[-1].minute), "vwap": round(vw[-1], 2)})
    if orr:
        info.update({"or_high": round(orr[0], 2), "or_low": round(orr[1], 2),
                     "first_candle": "up" if orr[3] >= orr[2] else "down"})
    ctx = E.daily_context(data.yahoo_daily(C.SYMBOL), date)
    trades = _load()
    info["strategies"] = {}
    for name in C.STRATEGIES:
        tr, status = E.run_strategy(bars, ctx, name)
        rec = next((t for t in trades if t["date"] == date and t["strategy"] == name), None)
        if tr:
            tr.update({"date": date, "strategy": name})
            if rec is None:
                tr["detected"] = now.strftime("%H:%M ET")
                trades.append(tr)
                rec = tr
            else:
                rec.update({k: v for k, v in tr.items() if k != "detected"})
            if final and name == "v1 control":
                rec["variants"] = {}
                for vname, r in backtest.variants().items():
                    vt, _ = E.run_day(bars, ctx, r)
                    if vt and vname != "Baseline":
                        rec["variants"][vname] = vt["r_net"]
        info["strategies"][name] = {"status": status, **({k: rec[k] for k in FIELDS} if rec else {})}
    info["status"] = info["strategies"]["v1 control"]["status"]
    _save(trades)
    TODAY.write_text(json.dumps(info, indent=1, default=str))
    if final:
        (LIVE / "review.md").write_text(review.live_review(trades))
    return info
