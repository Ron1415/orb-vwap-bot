# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 8 trades, 12.5% win, -0.66R ±0.26 per trade, profit factor 0.16, max drawdown -3.74R
  - watch-only shorts (not counted): 8 trades, 62.5% win, +0.41R ±0.42 per trade, profit factor 2.41, max drawdown 0.0R
- **v2 candle:** 5 trades, 20.0% win, -0.44R ±0.39 per trade, profit factor 0.32, max drawdown -2.18R
  - watch-only shorts (not counted): 7 trades, 57.1% win, +0.43R ±0.49 per trade, profit factor 2.29, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 5 trades, 20.0% win, -0.44R ±0.39 per trade, profit factor 0.32, max drawdown -2.18R
  - watch-only shorts (not counted): 7 trades, 57.1% win, +0.43R ±0.49 per trade, profit factor 2.29, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Target: range width | 16 | +0.25 | +3.95 |
| Stop: VWAP; Target 2R | 16 | +0.25 | +3.94 |
| Stop: VWAP; Hold to 3:55 PM | 16 | +0.24 | +3.90 |
| Stop: VWAP; Half at 1R, trail VWAP | 16 | +0.17 | +2.74 |
| Stop: middle of range; Hold to 3:55 PM | 16 | +0.17 | +2.73 |
| Stop: middle of range; Target: range width | 16 | +0.16 | +2.64 |
| Stop: middle of range; Half at 1R, trail VWAP | 16 | +0.14 | +2.26 |
| OR 5 min | 16 | +0.10 | +1.67 |
| Stop: middle of range; Target 2R | 16 | +0.05 | +0.83 |
| Stop: middle of range; Target 1R | 16 | +0.01 | +0.21 |
| Stop: VWAP; Target 1R | 16 | +0.01 | +0.16 |
| Side risk caps (long 1%, short 0.5%) | 13 | -0.01 | -0.16 |
| Stop: other side of range; Half at 1R, trail VWAP | 16 | -0.07 | -1.11 |
| Stop: other side of range; Target 1R | 16 | -0.08 | -1.29 |
| Stop: other side of range; Target: range width | 16 | -0.09 | -1.41 |
| Enter at signal close | 16 | -0.12 | -1.94 |
| Stop: other side of range; Hold to 3:55 PM | 16 | -0.12 | -1.96 |
| Signals until 3:00 PM | 16 | -0.13 | -2.05 |
| OR 30 min | 9 | -0.13 | -1.21 |
| Signals until 10:30 AM | 15 | -0.21 | -3.09 |

Compare these with the backtest after about 40 paper trades.
