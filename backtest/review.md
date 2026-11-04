# SPY ORB-15 + VWAP: backtest review

Generated 2026-11-04 13:28 ET. Data: Alpaca (SIP). 1209 sessions, 2022-01-10 to 2026-11-03. Results are net of 1 cent per share per side.

## Baseline (version 1)
Range 9:30-9:45; first 5-minute close outside the range on the same side of VWAP, before 11:30; entry at the next bar's open; stop at the other side of the range; target 2R; exit 3:55 PM; one trade a day.

- **All:** 1164 trades, 4.81 per week, 44.3% win, +0.08R ±0.04 per trade, profit factor 1.16, max drawdown -12.0R
- **Gross of costs:** +0.09R per trade
- **Last 6 months:** 122 trades, 4.88 per week, 44.3% win, -0.02R ±0.10 per trade, profit factor 0.96, max drawdown -7.67R
- **2022-01-10 to 2024-06-06:** 572 trades, 44.2% win, +0.09R ±0.05 per trade, profit factor 1.17, max drawdown -12.0R
- **2024-06-06 to 2026-11-03:** 592 trades, 44.4% win, +0.07R ±0.05 per trade, profit factor 1.14, max drawdown -11.44R
- **Size-weighted total (longs 1x, shorts 0.5x):** 72.71R
- **Days without a trade:** skipped: risk too large 30, no breakout before cutoff 15

## The three paper-traded strategies
The candle and volume factors were found on 2024-11-25 onward. Earlier sessions (723) are out of sample: the fair test of v2 and v3.

| Strategy | Out of sample | Found period | Last 6 months | All |
|---|---|---|---|---|
| v1 control | 689 trades, +0.09R, t 1.94, PF 1.18 | 475 trades, +0.06R, t 1.12, PF 1.12 | 122 trades, -0.02R, t -0.18, PF 0.96 | 1164 trades, +0.08R, t 2.22, PF 1.16 |
| v2 candle | 373 trades, +0.08R, t 1.13, PF 1.14 | 282 trades, +0.13R, t 1.85, PF 1.28 | 76 trades, +0.04R, t 0.33, PF 1.09 | 655 trades, +0.10R, t 2.04, PF 1.19 |
| v3 candle + volume | 111 trades, +0.12R, t 0.96, PF 1.22 | 85 trades, +0.27R, t 2.01, PF 1.65 | 25 trades, +0.28R, t 1.13, PF 1.69 | 196 trades, +0.19R, t 2.03, PF 1.38 |
- **v1 control by year:** 2022 +0.11R (n=225); 2023 +0.14R (n=243); 2024 +0.04R (n=246); 2025 +0.06R (n=242); 2026 +0.06R (n=208)
- **v2 candle by year:** 2022 +0.14R (n=95); 2023 +0.10R (n=145); 2024 +0.02R (n=149); 2025 +0.14R (n=145); 2026 +0.13R (n=121)
- **v3 candle + volume by year:** 2022 +0.10R (n=27); 2023 +0.13R (n=53); 2024 +0.19R (n=35); 2025 +0.28R (n=40); 2026 +0.22R (n=41)

## Best variant and filter combinations (at least 60 trades)

| Variant | Filter | Trades | Win | Avg R | ±SE | PF | Halves | Last 6 mo | Steady |
|---|---|---|---|---|---|---|---|---|---|
| Stop: VWAP; Hold to 3:55 PM | Candle + volume (>= 0.9x) | 232 | 29.3% | +0.28 | 0.159 | 1.39 | +0.13 / +0.48 | +0.66 | yes |
| Stop: middle of range; Hold to 3:55 PM | Candle + volume (>= 0.9x) | 233 | 35.2% | +0.26 | 0.138 | 1.41 | +0.16 / +0.40 | +0.35 | yes |
| Stop: VWAP; Hold to 3:55 PM | Narrow range (OR < 25% ATR) | 694 | 26.9% | +0.22 | 0.093 | 1.29 | +0.29 / +0.14 | +0.30 | yes |
| Stop: other side of range; Hold to 3:55 PM | Candle + volume (>= 0.9x) | 227 | 46.7% | +0.20 | 0.096 | 1.41 | +0.13 / +0.29 | +0.28 | yes |
| Side risk caps (long 1%, short 0.5%) | Candle + volume (>= 0.9x) | 196 | 48.0% | +0.19 | 0.092 | 1.38 | +0.10 / +0.28 | +0.28 | yes |
| Stop: VWAP; Target 2R | Candle + volume (>= 0.9x) | 232 | 40.5% | +0.18 | 0.096 | 1.3 | +0.14 / +0.24 | +0.25 | yes |
| Stop: middle of range; Hold to 3:55 PM | Narrow range (OR < 25% ATR) | 696 | 29.6% | +0.18 | 0.083 | 1.25 | +0.27 / +0.09 | +0.18 | yes |
| Enter at signal close | Candle + volume (>= 0.9x) | 227 | 47.6% | +0.17 | 0.084 | 1.36 | +0.09 / +0.28 | +0.27 | yes |
| Baseline | Candle + volume (>= 0.9x) | 227 | 47.6% | +0.17 | 0.084 | 1.35 | +0.09 / +0.28 | +0.27 | yes |
| Signals until 3:00 PM | Candle + volume (>= 0.9x) | 229 | 47.6% | +0.17 | 0.083 | 1.35 | +0.08 / +0.28 | +0.28 | yes |
| Signals until 10:30 AM | Candle + volume (>= 0.9x) | 220 | 46.8% | +0.16 | 0.085 | 1.33 | +0.05 / +0.29 | +0.28 | yes |
| Stop: VWAP; Half at 1R, trail VWAP | Candle + volume (>= 0.9x) | 232 | 54.7% | +0.16 | 0.086 | 1.34 | +0.08 / +0.25 | +0.24 | yes |

## Reading the evidence

- **No combination is clearly positive** (needs +0.10R or more, t of 3 or more, both halves and the last 6 months positive). Do not automate yet.
- 210 cells were compared; about 5 would reach t = 2 by luck alone, which is why the bar is t = 3.
- Many combinations are tested, so the best one is partly luck. Treat a winner as a hypothesis to confirm on paper trades, not as proof.

## Baseline breakdowns

**Side:** long +0.09R (n=599); short +0.07R (n=565)

**Exit:** eod +0.53R (n=346); stop -1.01R (n=571); target +1.99R (n=247)

**Signal hour:** 10:00 AM +0.15R (n=360); 10:30 AM +0.19R (n=67); 11:00 AM +0.21R (n=23); 9:30 AM +0.03R (n=714)

**Weekday:** Mon +0.05R (n=214); Tue +0.19R (n=246); Wed -0.05R (n=240); Thu +0.05R (n=232); Fri +0.15R (n=232)

**With daily trend (close vs 20-day):** against +0.04R (n=584); with +0.12R (n=580)

**With first 15-min candle:** against +0.05R (n=407); with +0.10R (n=757)

**Quartiles: or_width_pct:** under 0.189 +0.09R (n=291); 0.189 to 0.27 +0.16R (n=291); 0.27 to 0.4 +0.09R (n=291); 0.4 and over -0.02R (n=291)

**Quartiles: or_atr:** under 0.173 +0.19R (n=291); 0.173 to 0.223 +0.00R (n=291); 0.223 to 0.3 +0.10R (n=291); 0.3 and over +0.03R (n=291)

**Quartiles: gap_pct:** under -0.266 -0.01R (n=291); -0.266 to 0.0546 +0.11R (n=291); 0.0546 to 0.352 +0.14R (n=291); 0.352 and over +0.08R (n=291)

**Quartiles: vwap_dist_pct:** under -0.165 +0.12R (n=291); -0.165 to 0.0536 +0.05R (n=291); 0.0536 to 0.151 +0.16R (n=291); 0.151 and over -0.01R (n=291)

**Quartiles: risk_pct:** under 0.24 +0.09R (n=291); 0.24 to 0.344 +0.13R (n=291); 0.344 to 0.486 +0.07R (n=291); 0.486 and over +0.03R (n=291)

**Quartiles: breakout_vol_ratio:** under 0.6 +0.03R (n=291); 0.6 to 0.755 +0.11R (n=289); 0.755 to 0.954 +0.08R (n=293); 0.954 and over +0.10R (n=291)

**Quartiles: signal_min:** under 9:45 AM +0.00R (n=0); 9:45 AM to 9:55 AM +0.03R (n=581); 9:55 AM to 10:05 AM +0.06R (n=259); 10:05 AM and over +0.19R (n=324)

