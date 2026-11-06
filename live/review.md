# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 5 trades, 0.0% win, -0.86R ±0.14 per trade, max drawdown -2.75R
  - watch-only shorts (not counted): 4 trades, 75.0% win, +0.32R ±0.28 per trade, profit factor 5.65, max drawdown 0.0R
- **v2 candle:** 2 trades, 0.0% win, -0.60R ±0.29 per trade, max drawdown -1.19R
  - watch-only shorts (not counted): 4 trades, 50.0% win, +0.02R ±0.45 per trade, profit factor 1.05, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 2 trades, 0.0% win, -0.60R ±0.29 per trade, max drawdown -1.19R
  - watch-only shorts (not counted): 4 trades, 50.0% win, +0.02R ±0.45 per trade, profit factor 1.05, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Target: range width | 9 | +0.25 | +2.24 |
| Stop: VWAP; Target 2R | 9 | +0.23 | +2.04 |
| Stop: middle of range; Target: range width | 9 | +0.16 | +1.45 |
| Stop: other side of range; Target: range width | 9 | -0.02 | -0.16 |
| Stop: other side of range; Target 1R | 9 | -0.03 | -0.23 |
| OR 5 min | 9 | -0.03 | -0.26 |
| Stop: middle of range; Target 1R | 9 | -0.08 | -0.70 |
| Stop: VWAP; Target 1R | 9 | -0.08 | -0.75 |
| Stop: middle of range; Target 2R | 9 | -0.12 | -1.08 |
| Stop: other side of range; Half at 1R, trail VWAP | 9 | -0.12 | -1.11 |
| Stop: VWAP; Half at 1R, trail VWAP | 9 | -0.16 | -1.45 |
| Stop: middle of range; Half at 1R, trail VWAP | 9 | -0.17 | -1.52 |
| Stop: VWAP; Hold to 3:55 PM | 9 | -0.27 | -2.41 |
| OR 30 min | 5 | -0.29 | -1.45 |
| Side risk caps (long 1%, short 0.5%) | 7 | -0.30 | -2.13 |
| Stop: middle of range; Hold to 3:55 PM | 9 | -0.31 | -2.77 |
| Enter at signal close | 9 | -0.32 | -2.90 |
| Stop: other side of range; Hold to 3:55 PM | 9 | -0.34 | -3.02 |
| Signals until 3:00 PM | 9 | -0.34 | -3.02 |
| Signals until 10:30 AM | 8 | -0.51 | -4.06 |

Compare these with the backtest after about 40 paper trades.
