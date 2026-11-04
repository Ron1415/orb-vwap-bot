# ETF ORB-15 + VWAP: backtest review

Generated 2026-11-04 17:23 ET. ETFs traded: SPY, QQQ, XLK, SMH; watch only: IWM, DIA. Main candidate: v2 candle. Data: Alpaca (SIP). 1210 sessions, 2022-01-10 to 2026-11-04. Results are net of 1 cent per share per side.

## Baseline (version 1)
Range 9:30-9:45; first 5-minute close outside the range on the same side of VWAP, before 11:30; entry at the next bar's open; stop at the other side of the range; target 2R; exit 3:55 PM; one trade a day.

- **All:** 3568 trades, 14.74 per week, 44.8% win, +0.07R ±0.02 per trade, profit factor 1.14, max drawdown -40.3R
- **Gross of costs:** +0.09R per trade
- **Last 6 months:** 329 trades, 13.16 per week, 40.1% win, -0.13R ±0.06 per trade, profit factor 0.75, max drawdown -37.45R
- **2022-01-10 to 2024-06-07:** 1767 trades, 44.9% win, +0.09R ±0.03 per trade, profit factor 1.18, max drawdown -24.46R
- **2024-06-07 to 2026-11-04:** 1801 trades, 44.6% win, +0.05R ±0.03 per trade, profit factor 1.1, max drawdown -40.3R
- **Size-weighted total (longs 1x, shorts 0.5x):** 189.57R
- **Days without a trade:** skipped: risk too large 1099, no breakout before cutoff 173

## The paper-traded strategies
The candle and volume factors were found on 2024-11-25 onward. Earlier sessions (723) are out of sample: the fair test of v2 and v3.

| Strategy | Out of sample | Found period | Last 6 months | All |
|---|---|---|---|---|
| v1 control | 2126 trades, +0.10R, t 3.65, PF 1.19 | 1442 trades, +0.03R, t 0.85, PF 1.05 | 329 trades, -0.13R, t -2.31, PF 0.75 | 3568 trades, +0.07R, t 3.43, PF 1.14 |
| v2 candle | 749 trades, +0.14R, t 3.07, PF 1.28 | 515 trades, +0.07R, t 1.55, PF 1.17 | 127 trades, -0.03R, t -0.31, PF 0.94 | 1264 trades, +0.11R, t 3.4, PF 1.24 |
| v2b candle, shorts in weak market | 805 trades, +0.14R, t 3.2, PF 1.28 | 549 trades, +0.06R, t 1.21, PF 1.12 | 143 trades, -0.06R, t -0.7, PF 0.87 | 1354 trades, +0.10R, t 3.3, PF 1.22 |
| v3 candle + volume | 193 trades, +0.12R, t 1.33, PF 1.24 | 132 trades, +0.04R, t 0.48, PF 1.1 | 38 trades, +0.04R, t 0.28, PF 1.11 | 325 trades, +0.09R, t 1.37, PF 1.19 |
- **v2 candle, watch-only shorts (not counted):** all 452 trades, +0.04R, t 0.76, PF 1.08; out of sample 266 trades, +0.03R, t 0.34, PF 1.05
- **v2b candle, shorts in weak market, watch-only shorts (not counted):** all 362 trades, +0.05R, t 0.75, PF 1.09; out of sample 210 trades, -0.01R, t -0.11, PF 0.98
- **v3 candle + volume, watch-only shorts (not counted):** all 145 trades, +0.11R, t 1.08, PF 1.22; out of sample 74 trades, -0.03R, t -0.24, PF 0.94
- **v1 control, watch-only ETFs IWM, DIA (not counted):** 2085 trades, +0.02R, t 0.91, PF 1.05
- **v2 candle, watch-only ETFs IWM, DIA (not counted):** 679 trades, +0.03R, t 0.68, PF 1.06
- **v2b candle, shorts in weak market, watch-only ETFs IWM, DIA (not counted):** 790 trades, +0.02R, t 0.51, PF 1.04
- **v3 candle + volume, watch-only ETFs IWM, DIA (not counted):** 119 trades, -0.12R, t -1.15, PF 0.79
- **v1 control by ETF, out of sample:** DIA (watch) +0.02R (n=683); IWM (watch) +0.05R (n=528); QQQ +0.10R (n=598); SMH +0.10R (n=269); SPY +0.09R (n=689); XLK +0.09R (n=570)
- **v1 control same-day load:** 3.02 trades a day on average, up to 4; 3+ trades on 76.3% of trading days; worst day -4.14R, worst 5% of days -3.07R or less
- **v2 candle by ETF, out of sample:** DIA (watch) +0.03R (n=225); IWM (watch) +0.03R (n=175); QQQ +0.12R (n=223); SMH +0.14R (n=89); SPY +0.13R (n=232); XLK +0.16R (n=205)
- **v2 candle same-day load:** 2.11 trades a day on average, up to 4; 3+ trades on 35.3% of trading days; worst day -4.12R, worst 5% of days -3.06R or less
- **v2b candle, shorts in weak market by ETF, out of sample:** DIA (watch) +0.01R (n=284); IWM (watch) +0.03R (n=181); QQQ +0.15R (n=236); SMH +0.14R (n=89); SPY +0.12R (n=265); XLK +0.15R (n=215)
- **v2b candle, shorts in weak market same-day load:** 2.05 trades a day on average, up to 4; 3+ trades on 32.8% of trading days; worst day -4.12R, worst 5% of days -3.06R or less
- **v3 candle + volume by ETF, out of sample:** DIA (watch) -0.02R (n=39); IWM (watch) -0.13R (n=36); QQQ +0.14R (n=55); SMH +0.08R (n=20); SPY +0.19R (n=69); XLK +0.02R (n=49)
- **v3 candle + volume same-day load:** 1.4 trades a day on average, up to 4; 3+ trades on 8.6% of trading days; worst day -4.08R, worst 5% of days -2.04R or less
- **v1 control by year:** 2022 +0.13R (n=557); 2023 +0.06R (n=845); 2024 +0.12R (n=806); 2025 +0.05R (n=784); 2026 -0.03R (n=576)
- **v2 candle by year:** 2022 +0.15R (n=190); 2023 +0.11R (n=342); 2024 +0.20R (n=246); 2025 +0.08R (n=272); 2026 +0.01R (n=214)
- **v2b candle, shorts in weak market by year:** 2022 +0.16R (n=201); 2023 +0.14R (n=364); 2024 +0.14R (n=274); 2025 +0.07R (n=281); 2026 -0.01R (n=234)
- **v3 candle + volume by year:** 2022 +0.06R (n=54); 2023 +0.03R (n=103); 2024 +0.47R (n=43); 2025 +0.09R (n=64); 2026 -0.06R (n=61)

## Best variant and filter combinations (at least 60 trades)

| Variant | Filter | Trades | Win | Avg R | ±SE | PF | Halves | Last 6 mo | Steady |
|---|---|---|---|---|---|---|---|---|---|
| Stop: VWAP; Hold to 3:55 PM | With daily trend | 2252 | 31.0% | +0.20 | 0.046 | 1.29 | +0.27 / +0.13 | -0.17 | no |
| Stop: VWAP; Hold to 3:55 PM | Trend + candle + by 10:15 | 1342 | 29.1% | +0.20 | 0.061 | 1.27 | +0.24 / +0.15 | -0.19 | no |
| Stop: middle of range; Hold to 3:55 PM | Trend + candle + by 10:15 | 1300 | 35.2% | +0.18 | 0.053 | 1.28 | +0.26 / +0.09 | -0.21 | no |
| Stop: middle of range; Hold to 3:55 PM | With daily trend | 2198 | 35.9% | +0.18 | 0.041 | 1.28 | +0.25 / +0.11 | -0.18 | no |
| Stop: VWAP; Hold to 3:55 PM | Narrow range (OR < 25% ATR) | 1753 | 26.9% | +0.17 | 0.057 | 1.22 | +0.15 / +0.18 | -0.16 | no |
| Baseline | Trend + candle + by 10:15 | 1039 | 48.9% | +0.16 | 0.037 | 1.34 | +0.22 / +0.09 | -0.10 | no |
| Stop: middle of range; Hold to 3:55 PM | Narrow range (OR < 25% ATR) | 1750 | 30.8% | +0.16 | 0.051 | 1.23 | +0.16 / +0.15 | -0.14 | no |
| Enter at signal close | Trend + candle + by 10:15 | 1034 | 49.1% | +0.16 | 0.038 | 1.34 | +0.23 / +0.09 | -0.11 | no |
| Signals until 3:00 PM | Trend + candle + by 10:15 | 1039 | 48.9% | +0.16 | 0.037 | 1.34 | +0.22 / +0.09 | -0.10 | no |
| Signals until 10:30 AM | Trend + candle + by 10:15 | 1039 | 48.9% | +0.16 | 0.037 | 1.34 | +0.22 / +0.09 | -0.10 | no |
| Stop: other side of range; Hold to 3:55 PM | Trend + candle + by 10:15 | 1039 | 47.3% | +0.15 | 0.041 | 1.32 | +0.23 / +0.07 | -0.18 | no |
| Stop: middle of range; Hold to 3:55 PM | Candle + volume (>= 0.9x) | 872 | 35.4% | +0.15 | 0.062 | 1.25 | +0.07 / +0.25 | +0.04 | yes |

## Reading the evidence

- **No combination is clearly positive** (needs +0.10R or more, t of 3 or more, both halves and the last 6 months positive). Do not automate yet.
- 210 cells were compared; about 5 would reach t = 2 by luck alone, which is why the bar is t = 3.
- Many combinations are tested, so the best one is partly luck. Treat a winner as a hypothesis to confirm on paper trades, not as proof.

## Baseline breakdowns

**ETF:** SPY +0.08R (n=1165); QQQ +0.07R (n=1042); XLK +0.05R (n=922); SMH +0.06R (n=439)

**Side:** long +0.07R (n=1852); short +0.06R (n=1716)

**Exit:** eod +0.42R (n=1359); open -0.30R (n=6); stop -1.02R (n=1566); target +1.98R (n=637)

**Signal hour:** 10:00 AM +0.09R (n=1052); 10:30 AM +0.10R (n=236); 11:00 AM +0.01R (n=76); 9:30 AM +0.05R (n=2204)

**Weekday:** Mon -0.06R (n=635); Tue +0.18R (n=747); Wed -0.06R (n=780); Thu +0.08R (n=712); Fri +0.19R (n=694)

**With daily trend (close vs 20-day):** against +0.01R (n=1803); with +0.12R (n=1765)

**With first 15-min candle:** against +0.01R (n=1212); with +0.10R (n=2356)

**Quartiles: or_width_pct:** under 0.291 +0.15R (n=892); 0.291 to 0.445 +0.04R (n=891); 0.445 to 0.61 +0.01R (n=892); 0.61 and over +0.08R (n=893)

**Quartiles: or_atr:** under 0.202 +0.10R (n=892); 0.202 to 0.259 +0.06R (n=891); 0.259 to 0.327 +0.06R (n=893); 0.327 and over +0.05R (n=892)

**Quartiles: gap_pct:** under -0.341 +0.02R (n=892); -0.341 to 0.0907 +0.02R (n=891); 0.0907 to 0.48 +0.14R (n=893); 0.48 and over +0.09R (n=892)

**Quartiles: vwap_dist_pct:** under -0.235 +0.06R (n=892); -0.235 to 0.0756 +0.07R (n=892); 0.0756 to 0.238 +0.08R (n=892); 0.238 and over +0.06R (n=892)

**Quartiles: risk_pct:** under 0.366 +0.11R (n=892); 0.366 to 0.537 +0.08R (n=892); 0.537 to 0.736 +0.01R (n=891); 0.736 and over +0.08R (n=893)

**Quartiles: breakout_vol_ratio:** under 0.54 +0.05R (n=888); 0.54 to 0.715 +0.06R (n=895); 0.715 to 0.929 +0.12R (n=893); 0.929 and over +0.04R (n=892)

**Quartiles: signal_min:** under 9:45 AM +0.00R (n=0); 9:45 AM to 9:50 AM +0.06R (n=1165); 9:50 AM to 10:05 AM +0.05R (n=1396); 10:05 AM and over +0.11R (n=1007)

