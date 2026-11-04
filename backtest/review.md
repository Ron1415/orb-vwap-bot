# SPY ORB-15 + VWAP: backtest review

Generated 2026-11-04 12:59 ET. Data: Alpaca (SIP). 486 sessions, 2024-11-25 to 2026-11-03. Results are net of 1 cent per share per side.

## Baseline (version 1)
Range 9:30-9:45; first 5-minute close outside the range on the same side of VWAP, before 11:30; entry at the next bar's open; stop at the other side of the range; target 2R; exit 3:55 PM; one trade a day.

- **All:** 475 trades, 4.89 per week, 44.2% win, +0.06R ±0.06 per trade, profit factor 1.12, max drawdown -10.59R
- **Gross of costs:** +0.07R per trade
- **Last 6 months:** 122 trades, 4.88 per week, 44.3% win, -0.02R ±0.10 per trade, profit factor 0.96, max drawdown -7.67R
- **2024-11-25 to 2025-11-14:** 235 trades, 43.8% win, +0.09R ±0.08 per trade, profit factor 1.17, max drawdown -6.68R
- **2025-11-14 to 2026-11-03:** 240 trades, 44.6% win, +0.04R ±0.07 per trade, profit factor 1.07, max drawdown -8.48R
- **Size-weighted total (longs 1x, shorts 0.5x):** 20.8R
- **Days without a trade:** skipped: risk too large 8, no breakout before cutoff 3

## Best variant and filter combinations (at least 60 trades)

| Variant | Filter | Trades | Win | Avg R | ±SE | PF | Halves | Last 6 mo | Steady |
|---|---|---|---|---|---|---|---|---|---|
| Stop: VWAP; Hold to 3:55 PM | Narrow range (OR < 25% ATR) | 276 | 28.3% | +0.24 | 0.148 | 1.34 | +0.24 / +0.26 | +0.30 | yes |
| Stop: VWAP; Target: range width | Trend + candle + by 10:15 | 129 | 46.5% | +0.20 | 0.121 | 1.38 | +0.32 / +0.10 | +0.17 | yes |
| Stop: VWAP; Hold to 3:55 PM | Small gap (< 0.3%) | 244 | 28.3% | +0.20 | 0.145 | 1.28 | +0.41 / -0.02 | -0.20 | no |
| Stop: VWAP; Target 2R | Trend + candle + by 10:15 | 129 | 41.1% | +0.19 | 0.129 | 1.32 | +0.32 / +0.07 | +0.31 | yes |
| Stop: middle of range; Hold to 3:55 PM | Small gap (< 0.3%) | 244 | 32.8% | +0.16 | 0.125 | 1.24 | +0.28 / +0.02 | -0.13 | no |
| Baseline | Trend + candle + by 10:15 | 127 | 51.2% | +0.16 | 0.107 | 1.34 | +0.24 / +0.09 | -0.02 | no |
| Signals until 3:00 PM | Trend + candle + by 10:15 | 127 | 51.2% | +0.16 | 0.107 | 1.34 | +0.24 / +0.09 | -0.02 | no |
| Signals until 10:30 AM | Trend + candle + by 10:15 | 127 | 51.2% | +0.16 | 0.107 | 1.34 | +0.24 / +0.09 | -0.02 | no |
| Enter at signal close | Trend + candle + by 10:15 | 127 | 51.2% | +0.16 | 0.107 | 1.34 | +0.24 / +0.09 | -0.02 | no |
| Stop: middle of range; Target 2R | Trend + candle + by 10:15 | 129 | 42.6% | +0.15 | 0.125 | 1.26 | +0.26 / +0.05 | +0.17 | yes |
| Stop: middle of range; Hold to 3:55 PM | Narrow range (OR < 25% ATR) | 276 | 30.8% | +0.15 | 0.125 | 1.21 | +0.12 / +0.18 | +0.18 | yes |
| Stop: VWAP; Hold to 3:55 PM | With first 15-min candle | 315 | 26.7% | +0.15 | 0.135 | 1.2 | +0.20 / +0.09 | +0.01 | yes |

## Reading the evidence

- **No combination is clearly positive** (needs +0.10R or more, t of 3 or more, both halves and the last 6 months positive). Do not automate yet.
- 180 cells were compared; about 4 would reach t = 2 by luck alone, which is why the bar is t = 3.
- Many combinations are tested, so the best one is partly luck. Treat a winner as a hypothesis to confirm on paper trades, not as proof.

## Baseline breakdowns

**Side:** long +0.05R (n=244); short +0.07R (n=231)

**Exit:** eod +0.45R (n=168); stop -1.01R (n=219); target +1.99R (n=88)

**Signal hour:** 10:00 AM +0.22R (n=136); 10:30 AM +0.06R (n=23); 11:00 AM -0.34R (n=9); 9:30 AM +0.00R (n=307)

**Weekday:** Mon +0.11R (n=90); Tue +0.03R (n=102); Wed +0.10R (n=96); Thu -0.04R (n=93); Fri +0.10R (n=94)

**With daily trend (close vs 20-day):** against +0.07R (n=252); with +0.05R (n=223)

**With first 15-min candle:** against -0.07R (n=165); with +0.13R (n=310)

**Quartiles: or_width_pct:** under 0.172 +0.08R (n=118); 0.172 to 0.25 +0.03R (n=119); 0.25 to 0.359 +0.21R (n=119); 0.359 and over -0.08R (n=119)

**Quartiles: or_atr:** under 0.172 +0.17R (n=118); 0.172 to 0.223 +0.03R (n=119); 0.223 to 0.305 +0.05R (n=119); 0.305 and over -0.01R (n=119)

**Quartiles: gap_pct:** under -0.222 -0.03R (n=118); -0.222 to 0.0923 +0.10R (n=119); 0.0923 to 0.338 +0.10R (n=119); 0.338 and over +0.08R (n=119)

**Quartiles: vwap_dist_pct:** under -0.14 -0.00R (n=118); -0.14 to 0.052 +0.17R (n=119); 0.052 to 0.138 +0.04R (n=119); 0.138 and over +0.05R (n=119)

**Quartiles: risk_pct:** under 0.224 +0.12R (n=117); 0.224 to 0.313 +0.07R (n=120); 0.313 to 0.445 +0.02R (n=119); 0.445 and over +0.04R (n=119)

**Quartiles: breakout_vol_ratio:** under 0.572 +0.01R (n=117); 0.572 to 0.735 +0.02R (n=120); 0.735 to 0.936 +0.00R (n=119); 0.936 and over +0.22R (n=119)

**Quartiles: signal_min:** under 9:45 AM +0.00R (n=0); 9:45 AM to 9:50 AM +0.03R (n=161); 9:50 AM to 10:05 AM +0.03R (n=187); 10:05 AM and over +0.14R (n=127)

