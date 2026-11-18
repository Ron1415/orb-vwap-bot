# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 17 trades, 35.3% win, +0.02R ±0.30 per trade, profit factor 1.04, max drawdown -5.04R
  - watch-only shorts (not counted): 19 trades, 57.9% win, +0.36R ±0.27 per trade, profit factor 2.21, max drawdown 0.0R
- **v2 candle:** 6 trades, 16.7% win, -0.41R ±0.32 per trade, profit factor 0.29, max drawdown -2.47R
  - watch-only shorts (not counted): 15 trades, 53.3% win, +0.41R ±0.34 per trade, profit factor 2.15, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 9 trades, 33.3% win, +0.06R ±0.42 per trade, profit factor 1.11, max drawdown -2.98R
  - watch-only shorts (not counted): 12 trades, 50.0% win, +0.27R ±0.35 per trade, profit factor 1.74, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Target 2R | 33 | +0.69 | +22.69 |
| Stop: middle of range; Target 2R | 33 | +0.59 | +19.60 |
| Stop: VWAP; Target: range width | 33 | +0.58 | +19.06 |
| Stop: VWAP; Hold to 3:55 PM | 33 | +0.55 | +18.29 |
| Stop: middle of range; Hold to 3:55 PM | 33 | +0.53 | +17.34 |
| OR 5 min | 33 | +0.50 | +16.44 |
| Stop: middle of range; Target: range width | 33 | +0.49 | +16.21 |
| Stop: VWAP; Half at 1R, trail VWAP | 33 | +0.36 | +11.87 |
| OR 30 min | 22 | +0.35 | +7.62 |
| Enter at signal close | 33 | +0.31 | +10.29 |
| Signals until 3:00 PM | 33 | +0.31 | +10.23 |
| Stop: middle of range; Half at 1R, trail VWAP | 33 | +0.29 | +9.52 |
| Signals until 10:30 AM | 32 | +0.29 | +9.19 |
| Stop: other side of range; Target 1R | 33 | +0.28 | +9.13 |
| Stop: VWAP; Target 1R | 33 | +0.27 | +8.90 |
| Stop: other side of range; Half at 1R, trail VWAP | 33 | +0.27 | +8.80 |
| Stop: other side of range; Target: range width | 33 | +0.24 | +8.01 |
| Stop: other side of range; Hold to 3:55 PM | 33 | +0.23 | +7.68 |
| Stop: middle of range; Target 1R | 33 | +0.21 | +6.98 |
| Side risk caps (long 1%, short 0.5%) | 21 | +0.18 | +3.74 |

Compare these with the backtest after about 40 paper trades.
