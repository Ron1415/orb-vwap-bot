# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 4 trades, 0.0% win, -0.86R ±0.18 per trade, max drawdown -1.87R
  - watch-only shorts (not counted): 2 trades, 100.0% win, +0.60R ±0.44 per trade, max drawdown 0.0R
- **v2 candle:** 1 trades, 0.0% win, -0.31R per trade, max drawdown -0.31R
  - watch-only shorts (not counted): 2 trades, 50.0% win, -0.01R ±1.05 per trade, profit factor 0.98, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 1 trades, 0.0% win, -0.31R per trade, max drawdown -0.31R
  - watch-only shorts (not counted): 2 trades, 50.0% win, -0.01R ±1.05 per trade, profit factor 0.98, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Target 2R | 6 | +0.45 | +2.73 |
| Stop: VWAP; Target: range width | 6 | +0.35 | +2.12 |
| Stop: middle of range; Target: range width | 6 | +0.28 | +1.66 |
| Stop: other side of range; Target 1R | 6 | +0.09 | +0.56 |
| Stop: other side of range; Target: range width | 6 | +0.04 | +0.24 |
| Stop: middle of range; Target 2R | 6 | -0.04 | -0.24 |
| Stop: middle of range; Target 1R | 6 | -0.04 | -0.24 |
| Stop: VWAP; Target 1R | 6 | -0.05 | -0.27 |
| Stop: other side of range; Half at 1R, trail VWAP | 6 | -0.05 | -0.32 |
| Stop: VWAP; Half at 1R, trail VWAP | 6 | -0.08 | -0.47 |
| Stop: middle of range; Half at 1R, trail VWAP | 6 | -0.09 | -0.56 |
| OR 5 min | 6 | -0.14 | -0.86 |
| Stop: VWAP; Hold to 3:55 PM | 6 | -0.29 | -1.72 |
| OR 30 min | 5 | -0.29 | -1.45 |
| Stop: middle of range; Hold to 3:55 PM | 6 | -0.32 | -1.92 |
| Side risk caps (long 1%, short 0.5%) | 4 | -0.34 | -1.34 |
| Stop: other side of range; Hold to 3:55 PM | 6 | -0.37 | -2.23 |
| Signals until 3:00 PM | 6 | -0.37 | -2.23 |
| Enter at signal close | 6 | -0.37 | -2.24 |
| Signals until 10:30 AM | 5 | -0.65 | -3.27 |

Compare these with the backtest after about 40 paper trades.
