"""Rules engine: opening range, session VWAP, the breakout signal and the trade simulation.

Pure functions on lists of Bar (one regular session of 5-minute bars, New York time).
Conservative fills: when one bar touches both the stop and the target, the stop is assumed first.
"""
from __future__ import annotations

from collections import namedtuple

import config as C

Bar = namedtuple("Bar", "ts date minute o h l c v")   # minute = bar START, minutes after midnight NY


def hhmm(m: int) -> str:
    h, mm = divmod(int(m), 60)
    return f"{(h - 1) % 12 + 1}:{mm:02d} {'AM' if h < 12 else 'PM'}"


def rth(bars: list) -> list:
    return [b for b in bars if C.RTH_OPEN <= b.minute < C.RTH_CLOSE]


def session_vwap(bars: list) -> list[float]:
    """VWAP after each bar's close, anchored at 9:30 (typical price x volume)."""
    pv = vol = 0.0
    out = []
    for b in bars:
        tp = (b.h + b.l + b.c) / 3
        v = b.v if b.v > 0 else 1.0
        pv += tp * v
        vol += v
        out.append(pv / vol)
    return out


def opening_range(bars: list, or_minutes: int):
    """(high, low, open, close) of the first or_minutes, or None while it is still forming."""
    end = C.RTH_OPEN + or_minutes
    rng = [b for b in bars if C.RTH_OPEN <= b.minute < end]
    if len(rng) < or_minutes // C.BAR_MINUTES or not any(b.minute >= end for b in bars):
        return None
    return max(b.h for b in rng), min(b.l for b in rng), rng[0].o, rng[-1].c


def find_signal(bars: list, rules: dict, vw: list | None = None):
    """First 5-minute close outside the opening range on the same side of VWAP.

    Returns (signal dict | None, status text). bars must be one session's regular-hours bars.
    """
    orr = opening_range(bars, rules["or_minutes"])
    if orr is None:
        return None, "Opening range forming"
    orh, orl, _, _ = orr
    vw = vw or session_vwap(bars)
    end = C.RTH_OPEN + rules["or_minutes"]
    for i, b in enumerate(bars):
        if b.minute < end:
            continue
        if b.minute >= rules["entry_cutoff"]:
            return None, f"No breakout before {hhmm(rules['entry_cutoff'])}"
        side = None
        if b.c > orh and b.c > vw[i]:
            side = "long"
        elif b.c < orl and b.c < vw[i] and rules.get("allow_shorts", True):
            side = "short"
        if side:
            return {"i": i, "side": side, "orh": orh, "orl": orl, "vwap": vw[i], "minute": b.minute}, \
                f"{side.upper()} signal on the {hhmm(b.minute)} bar"
    return None, "Watching for a breakout"


def _stop_price(sig: dict, bars: list, entry: float, rules: dict) -> float:
    long = sig["side"] == "long"
    buf = entry * rules["stop_buffer_pct"] / 100
    mode = rules["stop"]
    if mode == "or_opposite":
        lvl = sig["orl"] if long else sig["orh"]
    elif mode == "or_mid":
        lvl = (sig["orh"] + sig["orl"]) / 2
    elif mode == "vwap":
        lvl = sig["vwap"]
    elif mode == "signal_bar":
        sb = bars[sig["i"]]
        lvl = sb.l if long else sb.h
    else:
        raise ValueError(mode)
    return lvl - buf if long else lvl + buf


def simulate(bars: list, sig: dict, rules: dict, vw: list | None = None) -> dict | None:
    """Simulate one trade. Returns None when the trade is skipped (no next bar, bad risk).

    r_gross / r_net are per unit of size (size is applied separately as r_sized).
    """
    vw = vw or session_vwap(bars)
    long = sig["side"] == "long"
    d = 1 if long else -1
    if rules["entry"] == "next_open":
        k = sig["i"] + 1
        if k >= len(bars) or bars[k].minute >= rules["eod_exit"]:
            return None
        entry, start = bars[k].o, k          # the entry bar itself can stop or target out
    else:
        entry, start = bars[sig["i"]].c, sig["i"] + 1
    stop = _stop_price(sig, bars, entry, rules)
    risk = (entry - stop) * d
    if risk <= 0:
        return {"skip": "entry beyond stop"}
    risk_pct = risk / entry * 100
    if risk_pct > rules.get(f"max_risk_pct_{sig['side']}", rules["max_risk_pct"]):
        return {"skip": "risk too large"}
    if risk_pct < rules["min_risk_pct"]:
        return {"skip": "risk too small"}

    tgt_mode = rules["target"]
    rmult = {"r1": 1, "r2": 2, "r3": 3}.get(tgt_mode)
    if rmult:
        target = entry + d * rmult * risk
    elif tgt_mode == "or_width":
        target = entry + d * (sig["orh"] - sig["orl"])
    elif tgt_mode == "half_r1_trail_vwap":
        target = entry + d * risk               # the first half
    else:
        target = None                           # eod, trail_vwap
    first_target = target

    open_frac, pnl, cur_stop = 1.0, 0.0, stop
    mfe = mae = 0.0
    exit_px = exit_min = None
    reason = ""
    half_done = False
    for j in range(start, len(bars)):
        b = bars[j]
        if b.minute >= rules["eod_exit"]:
            exit_px, exit_min, reason = bars[j - 1].c, b.minute, "eod"
            break
        fav = (b.h - entry) if long else (entry - b.l)
        adv = (entry - b.l) if long else (b.h - entry)
        mfe, mae = max(mfe, fav / risk), max(mae, adv / risk)
        hit_stop = (b.l <= cur_stop) if long else (b.h >= cur_stop)
        if hit_stop:
            # a gap through the stop fills at the worse open
            px = min(b.o, cur_stop) if long else max(b.o, cur_stop)
            exit_px, exit_min, reason = px, b.minute, ("breakeven" if half_done else "stop")
            break
        if target is not None:
            hit_t = (b.h >= target) if long else (b.l <= target)
            if hit_t:
                px = max(b.o, target) if long else min(b.o, target)
                if tgt_mode == "half_r1_trail_vwap" and not half_done:
                    pnl += 0.5 * (px - entry) * d
                    open_frac, half_done, cur_stop, target = 0.5, True, entry, None
                    # the same bar could still close across VWAP: checked below
                else:
                    exit_px, exit_min, reason = px, b.minute, "target"
                    break
        if tgt_mode in ("trail_vwap",) or (tgt_mode == "half_r1_trail_vwap" and half_done):
            if (b.c < vw[j]) if long else (b.c > vw[j]):
                exit_px, exit_min, reason = b.c, b.minute + C.BAR_MINUTES, "vwap trail"
                break
    if exit_px is None:                          # data ended (live, intraday): mark at the last close
        done = bars[-1].minute + C.BAR_MINUTES >= rules["eod_exit"]
        exit_px, exit_min, reason = bars[-1].c, bars[-1].minute + C.BAR_MINUTES, ("eod" if done else "open")
    pnl += open_frac * (exit_px - entry) * d
    cost = 2 * C.COST_PER_SHARE_PER_SIDE
    size = rules["long_size"] if long else rules["short_size"]
    r_net = (pnl - cost) / risk
    return {
        "side": sig["side"], "signal_min": sig["minute"], "entry_min": bars[start].minute if rules["entry"] == "next_open" else sig["minute"] + C.BAR_MINUTES,
        "entry": round(entry, 4), "stop": round(stop, 4), "target": None if first_target is None else round(first_target, 4),
        "exit": round(exit_px, 4), "exit_min": exit_min, "exit_reason": reason,
        "risk": round(risk, 4), "risk_pct": round(risk_pct, 4),
        "r_gross": round(pnl / risk, 4), "r_net": round(r_net, 4), "pct_net": round((pnl - cost) / entry * 100, 4),
        "size": size, "r_sized": round(r_net * size, 4), "mfe_r": round(mfe, 3), "mae_r": round(mae, 3),
        "half_taken": half_done,
    }


def features(bars: list, sig: dict, ctx: dict, rules: dict) -> dict:
    """Facts at the signal, recorded for the review (no look-ahead)."""
    orh, orl = sig["orh"], sig["orl"]
    _, _, oro, orc = opening_range(bars, rules["or_minutes"])
    sb = bars[sig["i"]]
    or_bars = [b for b in bars if b.minute < C.RTH_OPEN + rules["or_minutes"]]
    avg_v = sum(b.v for b in or_bars) / max(len(or_bars), 1)
    mid = (orh + orl) / 2
    prev_c = ctx.get("prev_close")
    atr = ctx.get("atr14")
    return {
        "side": sig["side"], "signal_min": sig["minute"],
        "or_high": round(orh, 4), "or_low": round(orl, 4),
        "or_width_pct": round((orh - orl) / mid * 100, 4),
        "or_atr": round((orh - orl) / atr, 4) if atr else None,
        "or_candle_up": orc >= oro,
        "gap_pct": round((bars[0].o - prev_c) / prev_c * 100, 4) if prev_c else 0.0,
        "vwap_dist_pct": round((sb.c - sig["vwap"]) / sb.c * 100, 4),
        "breakout_vol_ratio": round(sb.v / avg_v, 3) if avg_v else None,
        "above_sma20": bool(prev_c and ctx.get("sma20") and prev_c > ctx["sma20"]),
        "above_sma50": bool(prev_c and ctx.get("sma50") and prev_c > ctx["sma50"]),
        "weekday": ctx.get("weekday"),
    }


def run_day(bars: list, ctx: dict, rules: dict) -> tuple[dict | None, str]:
    """Signal + simulation + features for one session. Returns (trade or None, status)."""
    bars = rth(bars)
    if not bars:
        return None, "No data"
    vw = session_vwap(bars)
    sig, status = find_signal(bars, rules, vw)
    if not sig:
        return None, status
    tr = simulate(bars, sig, rules, vw)
    if tr is None:
        return None, status + " (no bar to enter)"
    if "skip" in tr:
        return None, f"{status}: skipped, {tr['skip']}"
    f = features(bars, sig, ctx, rules)
    f.update(tr)
    return f, status


def daily_context(daily: list[dict], date: str) -> dict:
    """daily: [{'date','h','l','c'}] sorted. Context from completed days BEFORE date."""
    import datetime as dt
    prior = [d for d in daily if d["date"] < date]
    ctx = {"weekday": dt.date.fromisoformat(date).strftime("%a")}
    if not prior:
        return ctx
    closes = [d["c"] for d in prior]
    ctx["prev_close"] = closes[-1]
    ctx["prev_high"], ctx["prev_low"] = prior[-1]["h"], prior[-1]["l"]
    if len(closes) >= 20:
        ctx["sma20"] = sum(closes[-20:]) / 20
    if len(closes) >= 50:
        ctx["sma50"] = sum(closes[-50:]) / 50
    if len(prior) >= 15:
        trs = []
        for a, b in zip(prior[-15:-1], prior[-14:]):
            trs.append(max(b["h"] - b["l"], abs(b["h"] - a["c"]), abs(b["l"] - a["c"])))
        ctx["atr14"] = sum(trs) / len(trs)
    return ctx


def daily_from_intraday(by_day: dict) -> list[dict]:
    out = []
    for date in sorted(by_day):
        r = rth(by_day[date])
        if r:
            out.append({"date": date, "h": max(b.h for b in r), "l": min(b.l for b in r), "c": r[-1].c})
    return out


def run_strategy(bars: list, ctx: dict, name: str) -> tuple[dict | None, str]:
    """One of config.STRATEGIES for one session: its rules, its filter on the day's first signal,
    then its short-side rule. A watch-only short comes back with tr["watch"] = True (not a trade)."""
    st = C.STRATEGIES[name]
    tr, status = run_day(bars, ctx, dict(C.RULES, **st["rules"]))
    if tr and not C.STRATEGY_FILTERS[st["filter"]](tr):
        why = "against the first 15-min candle" if (tr["side"] == "long") != tr["or_candle_up"] else "breakout volume too low"
        return None, f"{status}: filtered, {why}"
    if tr:
        tr["watch"] = False
        mode = st.get("shorts", "trade")
        if tr["side"] == "short" and (mode == "watch" or (mode == "below_sma20" and tr["above_sma20"])):
            tr["watch"] = True
            tr["r_sized"] = 0.0
            status += (": short recorded as watch only" if mode == "watch"
                       else ": short recorded as watch only (SPY above its 20-day average)")
    return tr, status


def mark_watch_symbol(tr: dict | None, symbol: str, status: str) -> tuple[dict | None, str]:
    """ETFs in config.WATCH_SYMBOLS are followed but never counted."""
    if tr and symbol in C.WATCH_SYMBOLS:
        tr["watch"], tr["r_sized"] = True, 0.0
        status += " (watch-only ETF)"
    return tr, status
