# ETF ORB-15 + VWAP: backtest review

Generated 2026-11-04 16:20 ET. ETFs: SPY, QQQ, IWM, DIA, XLF, XLK, XLE, SMH, GLD, TLT. Data: Alpaca (SIP). 1210 sessions, 2022-01-10 to 2026-11-04. Results are net of 1 cent per share per side.

## Baseline (version 1)
Range 9:30-9:45; first 5-minute close outside the range on the same side of VWAP, before 11:30; entry at the next bar's open; stop at the other side of the range; target 2R; exit 3:55 PM; one trade a day.

- **All:** 9464 trades, 39.11 per week, 43.3% win, +0.01R ±0.01 per trade, profit factor 1.02, max drawdown -111.12R
- **Gross of costs:** +0.04R per trade
- **Last 6 months:** 930 trades, 37.2 per week, 40.3% win, -0.10R ±0.03 per trade, profit factor 0.8, max drawdown -91.1R
- **2022-01-10 to 2024-06-07:** 4646 trades, 43.6% win, +0.02R ±0.02 per trade, profit factor 1.05, max drawdown -63.94R
- **2024-06-07 to 2026-11-04:** 4818 trades, 43.0% win, -0.00R ±0.02 per trade, profit factor 0.99, max drawdown -111.12R
- **Size-weighted total (longs 1x, shorts 0.5x):** 31.6R
- **Days without a trade:** skipped: risk too large 2013, no breakout before cutoff 623

## The paper-traded strategies
The candle and volume factors were found on 2024-11-25 onward. Earlier sessions (723) are out of sample: the fair test of v2 and v3.

| Strategy | Out of sample | Found period | Last 6 months | All |
|---|---|---|---|---|
| v1 control | 5629 trades, +0.02R, t 1.32, PF 1.04 | 3835 trades, -0.01R, t -0.42, PF 0.98 | 930 trades, -0.10R, t -3.0, PF 0.8 | 9464 trades, +0.01R, t 0.78, PF 1.02 |
| v2 candle | 1957 trades, +0.02R, t 0.82, PF 1.04 | 1330 trades, +0.01R, t 0.23, PF 1.01 | 319 trades, -0.08R, t -1.47, PF 0.83 | 3287 trades, +0.01R, t 0.79, PF 1.03 |
| v2b candle, shorts in weak market | 2279 trades, +0.02R, t 0.78, PF 1.04 | 1542 trades, -0.00R, t -0.02, PF 1.0 | 404 trades, -0.07R, t -1.38, PF 0.85 | 3821 trades, +0.01R, t 0.6, PF 1.02 |
| v3 candle + volume | 523 trades, +0.01R, t 0.2, PF 1.02 | 340 trades, -0.01R, t -0.14, PF 0.98 | 91 trades, -0.15R, t -1.33, PF 0.73 | 863 trades, +0.00R, t 0.07, PF 1.01 |
- **v2 candle, watch-only shorts (not counted):** all 1390 trades, -0.01R, t -0.3, PF 0.98; out of sample 804 trades, -0.03R, t -0.73, PF 0.94
- **v2b candle, shorts in weak market, watch-only shorts (not counted):** all 856 trades, -0.01R, t -0.16, PF 0.99; out of sample 482 trades, -0.06R, t -1.02, PF 0.9
- **v3 candle + volume, watch-only shorts (not counted):** all 433 trades, +0.00R, t 0.04, PF 1.0; out of sample 239 trades, +0.01R, t 0.08, PF 1.01
- **v1 control by ETF, out of sample:** SPY +0.09R (n=689); QQQ +0.10R (n=598); IWM +0.05R (n=528); DIA +0.02R (n=683); XLF -0.07R (n=572); XLK +0.09R (n=570); XLE -0.06R (n=323); SMH +0.10R (n=269); GLD -0.05R (n=699); TLT -0.05R (n=698)
- **v1 control same-day load:** 7.82 trades a day on average, up to 10; 3+ trades on 99.1% of trading days; worst day -8.77R, worst 5% of days -5.57R or less
- **v2 candle by ETF, out of sample:** SPY +0.13R (n=232); QQQ +0.12R (n=223); IWM +0.03R (n=175); DIA +0.03R (n=225); XLF -0.12R (n=230); XLK +0.16R (n=205); XLE -0.20R (n=114); SMH +0.14R (n=89); GLD +0.03R (n=222); TLT -0.13R (n=242)
- **v2 candle same-day load:** 3.2 trades a day on average, up to 10; 3+ trades on 56.1% of trading days; worst day -8.77R, worst 5% of days -4.27R or less
- **v2b candle, shorts in weak market by ETF, out of sample:** SPY +0.12R (n=265); QQQ +0.15R (n=236); IWM +0.03R (n=181); DIA +0.01R (n=284); XLF -0.13R (n=244); XLK +0.15R (n=215); XLE -0.20R (n=114); SMH +0.14R (n=89); GLD +0.04R (n=300); TLT -0.10R (n=351)
- **v2b candle, shorts in weak market same-day load:** 3.41 trades a day on average, up to 10; 3+ trades on 61.7% of trading days; worst day -8.77R, worst 5% of days -4.22R or less
- **v3 candle + volume by ETF, out of sample:** SPY +0.19R (n=69); QQQ +0.14R (n=55); IWM -0.13R (n=36); DIA -0.02R (n=39); XLF +0.06R (n=62); XLK +0.02R (n=49); XLE -0.23R (n=11); SMH +0.08R (n=20); GLD -0.02R (n=92); TLT -0.14R (n=90)
- **v3 candle + volume same-day load:** 1.58 trades a day on average, up to 6; 3+ trades on 14.3% of trading days; worst day -5.15R, worst 5% of days -2.1R or less
- **v1 control by year:** 2022 +0.05R (n=1588); 2023 +0.01R (n=2119); 2024 +0.01R (n=2136); 2025 +0.01R (n=2058); 2026 -0.05R (n=1563)
- **v2 candle by year:** 2022 +0.06R (n=542); 2023 -0.01R (n=797); 2024 +0.05R (n=678); 2025 +0.00R (n=738); 2026 -0.02R (n=532)
- **v2b candle, shorts in weak market by year:** 2022 +0.05R (n=633); 2023 +0.01R (n=931); 2024 +0.02R (n=798); 2025 -0.00R (n=816); 2026 -0.03R (n=643)
- **v3 candle + volume by year:** 2022 +0.02R (n=152); 2023 -0.01R (n=224); 2024 +0.05R (n=160); 2025 +0.05R (n=187); 2026 -0.12R (n=140)

## Best variant and filter combinations (at least 60 trades)

| Variant | Filter | Trades | Win | Avg R | ±SE | PF | Halves | Last 6 mo | Steady |
|---|---|---|---|---|---|---|---|---|---|
| Stop: middle of range; Hold to 3:55 PM | Narrow range (OR < 25% ATR) | 4220 | 29.4% | +0.07 | 0.032 | 1.09 | +0.07 / +0.06 | -0.06 | no |
| Stop: VWAP; Hold to 3:55 PM | Narrow range (OR < 25% ATR) | 4213 | 25.6% | +0.07 | 0.037 | 1.09 | +0.08 / +0.06 | -0.11 | no |
| Stop: other side of range; Hold to 3:55 PM | Narrow range (OR < 25% ATR) | 4101 | 39.3% | +0.06 | 0.024 | 1.1 | +0.08 / +0.04 | -0.13 | no |
| Stop: VWAP; Hold to 3:55 PM | With daily trend | 5715 | 29.0% | +0.06 | 0.028 | 1.07 | +0.07 / +0.04 | -0.14 | no |
| Stop: middle of range; Hold to 3:55 PM | With daily trend | 5628 | 33.6% | +0.05 | 0.025 | 1.08 | +0.07 / +0.03 | -0.15 | no |
| Stop: other side of range; Hold to 3:55 PM | Trend + candle + by 10:15 | 2718 | 43.1% | +0.05 | 0.026 | 1.1 | +0.09 / +0.01 | -0.14 | no |
| Stop: middle of range; Hold to 3:55 PM | Trend + candle + by 10:15 | 3254 | 32.9% | +0.05 | 0.033 | 1.07 | +0.06 / +0.04 | -0.12 | no |
| Stop: other side of range; Hold to 3:55 PM | With daily trend | 4784 | 43.0% | +0.04 | 0.019 | 1.09 | +0.07 / +0.02 | -0.14 | no |
| Stop: VWAP; Hold to 3:55 PM | Trend + candle + by 10:15 | 3321 | 27.3% | +0.04 | 0.039 | 1.06 | +0.03 / +0.06 | -0.06 | no |
| Stop: VWAP; Hold to 3:55 PM | Shorts | 5535 | 28.4% | +0.04 | 0.028 | 1.06 | +0.04 / +0.04 | -0.17 | no |
| Stop: middle of range; Hold to 3:55 PM | Candle + volume (>= 0.9x) | 2040 | 34.1% | +0.04 | 0.039 | 1.06 | -0.00 / +0.09 | -0.11 | no |
| Stop: other side of range; Hold to 3:55 PM | Shorts | 4582 | 40.9% | +0.04 | 0.02 | 1.08 | +0.05 / +0.02 | -0.08 | no |

## Reading the evidence

- **No combination is clearly positive** (needs +0.10R or more, t of 3 or more, both halves and the last 6 months positive). Do not automate yet.
- 210 cells were compared; about 5 would reach t = 2 by luck alone, which is why the bar is t = 3.
- Many combinations are tested, so the best one is partly luck. Treat a winner as a hypothesis to confirm on paper trades, not as proof.

## Baseline breakdowns

**ETF:** SPY +0.08R (n=1165); QQQ +0.07R (n=1042); IWM +0.02R (n=946); DIA +0.02R (n=1139); XLF -0.08R (n=935); XLK +0.05R (n=922); XLE -0.06R (n=554); SMH +0.06R (n=439); GLD -0.02R (n=1150); TLT -0.06R (n=1172)

**Side:** long -0.01R (n=4882); short +0.02R (n=4582)

**Exit:** eod +0.33R (n=3990); open +0.19R (n=19); stop -1.04R (n=3987); target +1.96R (n=1468)

**Signal hour:** 10:00 AM +0.03R (n=2877); 10:30 AM +0.04R (n=658); 11:00 AM -0.05R (n=287); 9:30 AM -0.00R (n=5642)

**Weekday:** Mon -0.04R (n=1723); Tue +0.07R (n=1963); Wed -0.10R (n=2008); Thu +0.05R (n=1898); Fri +0.06R (n=1872)

**With daily trend (close vs 20-day):** against -0.01R (n=4680); with +0.03R (n=4784)

**With first 15-min candle:** against +0.00R (n=3244); with +0.01R (n=6220)

**Quartiles: or_width_pct:** under 0.268 +0.03R (n=2366); 0.268 to 0.406 +0.01R (n=2366); 0.406 to 0.578 -0.00R (n=2365); 0.578 and over +0.00R (n=2367)

**Quartiles: or_atr:** under 0.203 +0.01R (n=2363); 0.203 to 0.268 +0.02R (n=2369); 0.268 to 0.348 +0.03R (n=2365); 0.348 and over -0.03R (n=2367)

**Quartiles: gap_pct:** under -0.34 -0.01R (n=2366); -0.34 to 0.0648 -0.01R (n=2366); 0.0648 to 0.44 +0.03R (n=2365); 0.44 and over +0.03R (n=2367)

**Quartiles: vwap_dist_pct:** under -0.221 +0.02R (n=2365); -0.221 to 0.0723 +0.02R (n=2367); 0.0723 to 0.219 +0.01R (n=2366); 0.219 and over -0.02R (n=2366)

**Quartiles: risk_pct:** under 0.337 +0.02R (n=2366); 0.337 to 0.494 +0.01R (n=2365); 0.494 to 0.69 +0.00R (n=2367); 0.69 and over +0.00R (n=2366)

**Quartiles: breakout_vol_ratio:** under 0.491 +0.00R (n=2361); 0.491 to 0.68 -0.00R (n=2362); 0.68 to 0.927 +0.02R (n=2370); 0.927 and over +0.01R (n=2371)

**Quartiles: signal_min:** under 9:45 AM +0.00R (n=0); 9:45 AM to 9:55 AM +0.01R (n=4714); 9:55 AM to 10:05 AM -0.01R (n=1956); 10:05 AM and over +0.02R (n=2794)

