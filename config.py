"""SPY 15-minute Opening Range Breakout + VWAP bot: every setting in one place.

Times are minutes after midnight, New York time, and refer to the START of a 5-minute bar
(the bar that starts at 9:45 closes at 9:50).
"""

SYMBOL = "SPY"
BAR_MINUTES = 5

# ----------------------------------------------------------------- session
RTH_OPEN, RTH_CLOSE = 570, 960          # 9:30 AM - 4:00 PM
LIVE_WINDOW = (565, 965)                # live paper checks 9:25 AM - 4:05 PM
EOD_AFTER = 975                         # end-of-day job after 4:15 PM

# ----------------------------------------------------------------- baseline rules (version 1)
# Opening range = 9:30-9:45. Long: first 5-minute close above the range high while the close is
# above VWAP. Short: first 5-minute close below the range low while the close is below VWAP.
# One trade per day. Entry at the open of the next bar (what a bot can actually do).
RULES = {
    "or_minutes": 15,
    "entry": "next_open",               # next_open | signal_close
    "entry_cutoff": 690,                # no new signals from bars starting at/after 11:30
    "stop": "or_opposite",              # or_opposite | or_mid | vwap | signal_bar
    "stop_buffer_pct": 0.01,            # stop placed 0.01% of price beyond the level (about 7 cents)
    "target": "r2",                     # r1 | r2 | r3 | or_width | eod | half_r1_trail_vwap | trail_vwap
    "eod_exit": 955,                    # anything open exits at 3:55 PM
    "max_risk_pct": 1.0,                # skip if the stop is more than 1% of price away
                                        # (per side, "max_risk_pct_long" / "max_risk_pct_short" override it)
    "min_risk_pct": 0.05,               # skip if the stop is closer than 0.05% (noise)
    "long_size": 1.0,                   # Ron: a bit more weight on longs ...
    "short_size": 0.5,                  # ... and lower risk on shorts
    "allow_shorts": True,
}

# ----------------------------------------------------------------- strategies paper traded side by side
# Approved by Ron on November 4, 2026:
#   v1 control  = the original rules, unchanged, as the yardstick
#   v2 candle   = trade only in the direction of the first 15-minute candle
#   v3 candle + volume = v2, and the breakout bar's volume is at least VOL_MIN x the average opening-range bar
# v2 and v3 use a higher risk limit for longs than for shorts (Ron: more room on longs, tighter shorts).
# Each day only the FIRST signal counts; if it fails a filter, that strategy does not trade that day.
SIDE_RISK = {"max_risk_pct_long": 1.0, "max_risk_pct_short": 0.5}
VOL_MIN = 0.9                           # set before any out-of-sample check (the in-sample quartile cut was 0.94)
STRATEGIES = {
    "v1 control": {"rules": {}, "filter": None},
    "v2 candle": {"rules": SIDE_RISK, "filter": "candle"},
    "v3 candle + volume": {"rules": SIDE_RISK, "filter": "candle_vol"},
}
STRATEGY_FILTERS = {
    None: lambda f: True,
    "candle": lambda f: (f["side"] == "long") == f["or_candle_up"],
    "candle_vol": lambda f: (f["side"] == "long") == f["or_candle_up"] and (f.get("breakout_vol_ratio") or 0) >= VOL_MIN,
}
# The candle and volume factors were found on Nov 25, 2024 - Nov 3, 2026. Sessions before this date
# are out of sample for them, and are reported separately.
FACTORS_FOUND_FROM = "2024-11-25"

# ----------------------------------------------------------------- costs
# SPY: one cent of slippage per share per side, no commission. Results are reported net of costs.
COST_PER_SHARE_PER_SIDE = 0.01

# ----------------------------------------------------------------- side-by-side tests
# Every trading day is re-run with each variant. The live rules do not change until Ron approves.
TEST_STOPS = ["or_opposite", "or_mid", "vwap"]
TEST_TARGETS = ["r1", "r2", "or_width", "eod", "half_r1_trail_vwap"]
EXTRA_VARIANTS = {                     # single changes from the baseline
    "OR 5 min": {"or_minutes": 5},
    "OR 30 min": {"or_minutes": 30},
    "Enter at signal close": {"entry": "signal_close"},
    "Signals until 3:00 PM": {"entry_cutoff": 900},
    "Signals until 10:30 AM": {"entry_cutoff": 630},
    "Side risk caps (long 1%, short 0.5%)": {"max_risk_pct_long": 1.0, "max_risk_pct_short": 0.5},
}

# Filters (columns of the test grid). Each is a predicate on the trade's recorded features.
FILTERS = {
    "All": lambda f: True,
    "Longs": lambda f: f["side"] == "long",
    "Shorts": lambda f: f["side"] == "short",
    "With daily trend": lambda f: (f["side"] == "long") == f["above_sma20"],
    "With first 15-min candle": lambda f: (f["side"] == "long") == f["or_candle_up"],
    "Narrow range (OR < 25% ATR)": lambda f: f["or_atr"] < 0.25,
    "Signal by 10:15": lambda f: f["signal_min"] < 615,
    "Small gap (< 0.3%)": lambda f: abs(f["gap_pct"]) < 0.3,
    "Candle + volume (>= 0.9x)": lambda f: ((f["side"] == "long") == f["or_candle_up"]
                                             and (f.get("breakout_vol_ratio") or 0) >= VOL_MIN),
    "Trend + candle + by 10:15": lambda f: ((f["side"] == "long") == f["above_sma20"]
                                            and (f["side"] == "long") == f["or_candle_up"]
                                            and f["signal_min"] < 615),
}

# Numeric features broken into quartiles in the review
BUCKET_FEATURES = ["or_width_pct", "or_atr", "gap_pct", "vwap_dist_pct", "risk_pct", "breakout_vol_ratio", "signal_min"]

# ----------------------------------------------------------------- backtest / data
BACKTEST_DAYS = 1250                    # about 5 years of sessions (Alpaca SIP history starts in 2016)
RECENT_DAYS = 125                       # the last ~6 months are also reported on their own
DAILY_LOOKBACK = 80                     # extra calendar days fetched before the start for SMA/ATR
ALPACA_FEED = "sip"                     # history; the free plan blocks only the latest 15 minutes
MIN_TRADES_TO_JUDGE = 60
