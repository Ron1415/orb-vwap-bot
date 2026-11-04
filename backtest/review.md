# SPY ORB-15 + VWAP: backtest review

Generated 2026-11-04 15:42 ET. Data: Alpaca (SIP). 1210 sessions, 2022-01-10 to 2026-11-04. Results are net of 1 cent per share per side.

## Baseline (version 1)
Range 9:30-9:45; first 5-minute close outside the range on the same side of VWAP, before 11:30; entry at the next bar's open; stop at the other side of the range; target 2R; exit 3:55 PM; one trade a day.

- **All:** 1165 trades, 4.81 per week, 44.3% win, +0.08R ±0.04 per trade, profit factor 1.16, max drawdown -12.0R
- **Gross of costs:** +0.09R per trade
- **Last 6 months:** 122 trades, 4.88 per week, 44.3% win, -0.01R ±0.10 per trade, profit factor 0.98, max drawdown -7.67R
- **2022-01-10 to 2024-06-07:** 573 trades, 44.2% win, +0.09R ±0.05 per trade, profit factor 1.17, max drawdown -12.0R
- **2024-06-07 to 2026-11-04:** 592 trades, 44.4% win, +0.07R ±0.05 per trade, profit factor 1.14, max drawdown -11.44R
- **Size-weighted total (longs 1x, shorts 0.5x):** 72.67R
- **Days without a trade:** skipped: risk too large 30, no breakout before cutoff 15

## The paper-traded strategies
The candle and volume factors were found on 2024-11-25 onward. Earlier sessions (723) are out of sample: the fair test of v2 and v3.

| Strategy | Out of sample | Found period | Last 6 months | All |
|---|---|---|---|---|
| v1 control | 689 trades, +0.09R, t 1.94, PF 1.18 | 476 trades, +0.06R, t 1.12, PF 1.12 | 122 trades, -0.01R, t -0.1, PF 0.98 | 1165 trades, +0.08R, t 2.22, PF 1.16 |
| v2 candle | 232 trades, +0.13R, t 1.49, PF 1.24 | 163 trades, +0.15R, t 1.64, PF 1.34 | 44 trades, +0.07R, t 0.36, PF 1.14 | 395 trades, +0.14R, t 2.19, PF 1.27 |
| v2b candle, shorts in weak market | 265 trades, +0.12R, t 1.54, PF 1.23 | 189 trades, +0.14R, t 1.58, PF 1.29 | 56 trades, +0.03R, t 0.2, PF 1.06 | 454 trades, +0.13R, t 2.19, PF 1.25 |
| v3 candle + volume | 69 trades, +0.19R, t 1.17, PF 1.36 | 36 trades, +0.26R, t 1.3, PF 1.63 | 12 trades, +0.40R, t 1.15, PF 2.19 | 105 trades, +0.21R, t 1.7, PF 1.44 |
- **v2 candle, watch-only shorts (not counted):** all 261 trades, +0.05R, t 0.58, PF 1.08; out of sample 141 trades, -0.01R, t -0.06, PF 0.99
- **v2b candle, shorts in weak market, watch-only shorts (not counted):** all 202 trades, +0.04R, t 0.4, PF 1.07; out of sample 108 trades, -0.04R, t -0.32, PF 0.93
- **v3 candle + volume, watch-only shorts (not counted):** all 91 trades, +0.15R, t 1.14, PF 1.31; out of sample 42 trades, +0.01R, t 0.05, PF 1.02
- **v1 control by year:** 2022 +0.11R (n=225); 2023 +0.14R (n=243); 2024 +0.04R (n=246); 2025 +0.06R (n=242); 2026 +0.06R (n=209)
- **v2 candle by year:** 2022 +0.10R (n=72); 2023 +0.12R (n=95); 2024 +0.22R (n=72); 2025 +0.12R (n=84); 2026 +0.13R (n=72)
- **v2b candle, shorts in weak market by year:** 2022 +0.11R (n=79); 2023 +0.18R (n=109); 2024 +0.10R (n=88); 2025 +0.14R (n=90); 2026 +0.10R (n=88)
- **v3 candle + volume by year:** 2022 +0.02R (n=21); 2023 +0.12R (n=36); 2024 +0.78R (n=13); 2025 +0.40R (n=14); 2026 +0.09R (n=21)

## Best variant and filter combinations (at least 60 trades)

| Variant | Filter | Trades | Win | Avg R | ±SE | PF | Halves | Last 6 mo | Steady |
|---|---|---|---|---|---|---|---|---|---|
| Stop: VWAP; Hold to 3:55 PM | Candle + volume (>= 0.9x) | 232 | 29.3% | +0.28 | 0.159 | 1.39 | +0.13 / +0.48 | +0.73 | yes |
| Stop: middle of range; Hold to 3:55 PM | Candle + volume (>= 0.9x) | 233 | 35.2% | +0.26 | 0.138 | 1.41 | +0.16 / +0.40 | +0.41 | yes |
| Stop: VWAP; Hold to 3:55 PM | Narrow range (OR < 25% ATR) | 694 | 26.9% | +0.22 | 0.093 | 1.29 | +0.29 / +0.15 | +0.33 | yes |
| Stop: other side of range; Hold to 3:55 PM | Candle + volume (>= 0.9x) | 227 | 46.7% | +0.20 | 0.096 | 1.41 | +0.13 / +0.29 | +0.33 | yes |
| Side risk caps (long 1%, short 0.5%) | Candle + volume (>= 0.9x) | 196 | 48.0% | +0.19 | 0.092 | 1.38 | +0.10 / +0.28 | +0.33 | yes |
| Stop: VWAP; Target 2R | Candle + volume (>= 0.9x) | 232 | 40.5% | +0.18 | 0.096 | 1.3 | +0.14 / +0.24 | +0.30 | yes |
| Stop: middle of range; Hold to 3:55 PM | Narrow range (OR < 25% ATR) | 696 | 29.6% | +0.18 | 0.083 | 1.25 | +0.27 / +0.09 | +0.20 | yes |
| Enter at signal close | Candle + volume (>= 0.9x) | 227 | 47.6% | +0.17 | 0.084 | 1.36 | +0.09 / +0.28 | +0.32 | yes |
| Baseline | Candle + volume (>= 0.9x) | 227 | 47.6% | +0.17 | 0.084 | 1.35 | +0.09 / +0.28 | +0.32 | yes |
| Signals until 3:00 PM | Candle + volume (>= 0.9x) | 229 | 47.6% | +0.17 | 0.083 | 1.35 | +0.08 / +0.28 | +0.33 | yes |
| Signals until 10:30 AM | Candle + volume (>= 0.9x) | 220 | 46.8% | +0.16 | 0.085 | 1.33 | +0.05 / +0.29 | +0.33 | yes |
| Stop: VWAP; Half at 1R, trail VWAP | Candle + volume (>= 0.9x) | 232 | 54.7% | +0.16 | 0.086 | 1.34 | +0.08 / +0.25 | +0.29 | yes |

## Reading the evidence

- **No combination is clearly positive** (needs +0.10R or more, t of 3 or more, both halves and the last 6 months positive). Do not automate yet.
- 210 cells were compared; about 5 would reach t = 2 by luck alone, which is why the bar is t = 3.
- Many combinations are tested, so the best one is partly luck. Treat a winner as a hypothesis to confirm on paper trades, not as proof.

## Baseline breakdowns

**Side:** long +0.09R (n=600); short +0.07R (n=565)

**Exit:** eod +0.53R (n=346); open -0.04R (n=1); stop -1.01R (n=571); target +1.99R (n=247)

**Signal hour:** 10:00 AM +0.15R (n=361); 10:30 AM +0.19R (n=67); 11:00 AM +0.21R (n=23); 9:30 AM +0.03R (n=714)

**Weekday:** Mon +0.05R (n=214); Tue +0.19R (n=246); Wed -0.05R (n=241); Thu +0.05R (n=232); Fri +0.15R (n=232)

**With daily trend (close vs 20-day):** against +0.04R (n=585); with +0.12R (n=580)

**With first 15-min candle:** against +0.05R (n=407); with +0.10R (n=758)

**Quartiles: or_width_pct:** under 0.189 +0.09R (n=291); 0.189 to 0.27 +0.16R (n=291); 0.27 to 0.4 +0.09R (n=291); 0.4 and over -0.02R (n=292)

**Quartiles: or_atr:** under 0.173 +0.19R (n=291); 0.173 to 0.223 +0.00R (n=291); 0.223 to 0.3 +0.10R (n=291); 0.3 and over +0.03R (n=292)

**Quartiles: gap_pct:** under -0.266 -0.01R (n=291); -0.266 to 0.0546 +0.11R (n=291); 0.0546 to 0.352 +0.14R (n=291); 0.352 and over +0.08R (n=292)

**Quartiles: vwap_dist_pct:** under -0.165 +0.12R (n=291); -0.165 to 0.0536 +0.05R (n=291); 0.0536 to 0.151 +0.16R (n=291); 0.151 and over -0.01R (n=292)

**Quartiles: risk_pct:** under 0.24 +0.09R (n=291); 0.24 to 0.344 +0.13R (n=291); 0.344 to 0.486 +0.07R (n=291); 0.486 and over +0.03R (n=292)

**Quartiles: breakout_vol_ratio:** under 0.6 +0.03R (n=291); 0.6 to 0.755 +0.11R (n=289); 0.755 to 0.953 +0.09R (n=291); 0.953 and over +0.10R (n=294)

**Quartiles: signal_min:** under 9:45 AM +0.00R (n=0); 9:45 AM to 9:55 AM +0.03R (n=581); 9:55 AM to 10:05 AM +0.06R (n=260); 10:05 AM and over +0.19R (n=324)

