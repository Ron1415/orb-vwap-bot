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
    "min_risk_pct": 0.05,               # skip if the stop is closer than 0.05% (noise)
    "long_size": 1.0,                   # Ron: a bit more weight on longs ...
    "short_size": 0.5,                  # ... and lower risk on shorts
    "allow_shorts": True,
}

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
    "Trend + candle + by 10:15": lambda f: ((f["side"] == "long") == f["above_sma20"]
                                            and (f["side"] == "long") == f["or_candle_up"]
                                            and f["signal_min"] < 615),
}

# Numeric features broken into quartiles in the review
BUCKET_FEATURES = ["or_width_pct", "or_atr", "gap_pct", "vwap_dist_pct", "risk_pct", "breakout_vol_ratio", "signal_min"]

# ----------------------------------------------------------------- backtest / data
BACKTEST_DAYS = 500                     # about 2 years of sessions (one trade a day needs a long sample)
RECENT_DAYS = 125                       # the last ~6 months are also reported on their own
DAILY_LOOKBACK = 80                     # extra calendar days fetched before the start for SMA/ATR
ALPACA_FEED = "sip"                     # history; the free plan blocks only the latest 15 minutes
MIN_TRADES_TO_JUDGE = 60
