"""SPY price data.

History: Alpaca (free account, keys as repository secrets ALPACA_KEY_ID / ALPACA_SECRET_KEY)
gives years of 5-minute bars. Without keys, Yahoo gives about the last 60 days only.
Live: Yahoo 5-minute bars (Alpaca IEX feed if keys are set and Yahoo fails).
Every series is a list of engine.Bar in New York time (bar start).
"""
from __future__ import annotations

import datetime as dt
import gzip
import logging
import os
import pickle
import time
from pathlib import Path
from zoneinfo import ZoneInfo

import config as C
from engine import Bar

NY = ZoneInfo("America/New_York")
ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
log = logging.getLogger("data")
ERRORS: list[str] = []


def alpaca_enabled() -> bool:
    return bool(os.environ.get("ALPACA_KEY_ID", "").strip() and os.environ.get("ALPACA_SECRET_KEY", "").strip())


def _bar(t, o, h, l, c, v) -> Bar:
    return Bar(int(t.timestamp()), t.strftime("%Y-%m-%d"), t.hour * 60 + t.minute, float(o), float(h), float(l), float(c), float(v or 0))


def alpaca_bars(symbol: str, start: dt.date, end: dt.date, timeframe="5Min", feed=None) -> list:
    import pandas as pd
    import requests
    feed = feed or C.ALPACA_FEED
    cache = CACHE / f"alpaca_{symbol}_{timeframe}_{feed}_{start}_{end}.pkl.gz"
    if cache.exists() and end < dt.date.today():
        return pickle.loads(gzip.decompress(cache.read_bytes()))
    hdr = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY_ID"].strip(),
           "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"].strip()}
    end_dt = min(dt.datetime(end.year, end.month, end.day, 23, 59, tzinfo=dt.timezone.utc),
                 dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=20 if feed == "sip" else 0))
    params = {"timeframe": timeframe, "start": f"{start}T00:00:00Z", "end": end_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
              "limit": 10000, "adjustment": "split", "feed": feed, "sort": "asc"}
    url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars"
    rows, token = [], None
    for _ in range(500):
        if token:
            params["page_token"] = token
        for attempt in range(4):
            r = requests.get(url, headers=hdr, params=params, timeout=30)
            if r.status_code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            break
        if r.status_code != 200:
            ERRORS.append(f"Alpaca {symbol}: HTTP {r.status_code} {r.text[:150]}")
            log.warning(ERRORS[-1])
            return []
        j = r.json()
        rows += j.get("bars") or []
        token = j.get("next_page_token")
        if not token:
            break
        time.sleep(0.35)
    out = []
    for b in rows:
        t = pd.Timestamp(b["t"]).tz_convert(NY)
        m = t.hour * 60 + t.minute
        if C.RTH_OPEN <= m < C.RTH_CLOSE:
            out.append(_bar(t, b["o"], b["h"], b["l"], b["c"], b.get("v")))
    if end < dt.date.today():
        CACHE.mkdir(exist_ok=True)
        cache.write_bytes(gzip.compress(pickle.dumps(out)))
    return out


def yahoo_bars(symbol: str, period="60d", interval="5m") -> list:
    import yfinance as yf
    try:
        df = yf.download(symbol, period=period, interval=interval, prepost=False, auto_adjust=False,
                         progress=False, multi_level_index=False)
    except Exception as e:
        ERRORS.append(f"Yahoo {symbol}: {e}")
        return []
    if df is None or df.empty:
        ERRORS.append(f"Yahoo {symbol}: no data")
        return []
    df = df.dropna(subset=["Open", "High", "Low", "Close"])
    idx = df.index if df.index.tz is not None else df.index.tz_localize("UTC")
    idx = idx.tz_convert(NY)
    out = []
    for t, o, h, l, c, v in zip(idx, df["Open"], df["High"], df["Low"], df["Close"], df["Volume"]):
        m = t.hour * 60 + t.minute
        if C.RTH_OPEN <= m < C.RTH_CLOSE:
            out.append(_bar(t, o, h, l, c, v))
    return out


def yahoo_daily(symbol: str, period="6mo") -> list[dict]:
    import yfinance as yf
    try:
        df = yf.download(symbol, period=period, interval="1d", auto_adjust=False, progress=False, multi_level_index=False)
    except Exception as e:
        ERRORS.append(f"Yahoo daily {symbol}: {e}")
        return []
    df = df.dropna(subset=["Close"])
    return [{"date": d.strftime("%Y-%m-%d"), "h": float(h), "l": float(l), "c": float(c)}
            for d, h, l, c in zip(df.index, df["High"], df["Low"], df["Close"])]


def history(days: int) -> tuple[dict, str]:
    """{date: [Bar]} for about `days` sessions plus DAILY_LOOKBACK days of lead-in, and the source name."""
    today = dt.datetime.now(NY).date()
    start = today - dt.timedelta(days=int(days * 7 / 5) + 10 + C.DAILY_LOOKBACK)
    bars, src = [], ""
    if alpaca_enabled():
        bars, src = alpaca_bars(C.SYMBOL, start, today), "Alpaca (SIP)"
    if not bars:
        bars, src = yahoo_bars(C.SYMBOL, "60d"), "Yahoo (about 60 days only)"
    by_day: dict[str, list] = {}
    for b in bars:
        by_day.setdefault(b.date, []).append(b)
    return by_day, src


def today_bars() -> tuple[list, str]:
    """Today's regular-session 5-minute bars, completed bars only."""
    today = dt.datetime.now(NY).strftime("%Y-%m-%d")
    now_min = dt.datetime.now(NY).hour * 60 + dt.datetime.now(NY).minute
    bars, src = [b for b in yahoo_bars(C.SYMBOL, "1d") if b.date == today], "Yahoo"
    if not bars and alpaca_enabled():
        d = dt.date.fromisoformat(today)
        bars, src = alpaca_bars(C.SYMBOL, d, d, feed="iex"), "Alpaca (IEX)"
    # drop the bar that is still forming
    bars = [b for b in bars if b.minute + C.BAR_MINUTES <= now_min]
    return bars, src
