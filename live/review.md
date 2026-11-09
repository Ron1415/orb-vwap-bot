# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 6 trades, 16.7% win, -0.55R ±0.33 per trade, profit factor 0.24, max drawdown -2.75R
  - watch-only shorts (not counted): 6 trades, 83.3% win, +0.88R ±0.39 per trade, profit factor 19.97, max drawdown 0.0R
- **v2 candle:** 3 trades, 33.3% win, -0.06R ±0.56 per trade, profit factor 0.85, max drawdown -1.19R
  - watch-only shorts (not counted): 6 trades, 66.7% win, +0.68R ±0.50 per trade, profit factor 4.01, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 3 trades, 33.3% win, -0.06R ±0.56 per trade, profit factor 0.85, max drawdown -1.19R
  - watch-only shorts (not counted): 6 trades, 66.7% win, +0.68R ±0.50 per trade, profit factor 4.01, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Target: range width | 12 | +0.67 | +8.01 |
| Stop: VWAP; Target 2R | 12 | +0.67 | +7.99 |
| Stop: VWAP; Hold to 3:55 PM | 12 | +0.66 | +7.94 |
| Stop: middle of range; Hold to 3:55 PM | 12 | +0.56 | +6.77 |
| Stop: middle of range; Target: range width | 12 | +0.56 | +6.68 |
| OR 5 min | 12 | +0.48 | +5.70 |
| Stop: middle of range; Target 2R | 12 | +0.41 | +4.87 |
| Stop: VWAP; Half at 1R, trail VWAP | 12 | +0.38 | +4.51 |
| Stop: middle of range; Half at 1R, trail VWAP | 12 | +0.35 | +4.14 |
| Side risk caps (long 1%, short 0.5%) | 10 | +0.29 | +2.86 |
| Stop: other side of range; Half at 1R, trail VWAP | 12 | +0.24 | +2.92 |
| Stop: other side of range; Target 1R | 12 | +0.23 | +2.74 |
| Stop: other side of range; Target: range width | 12 | +0.22 | +2.62 |
| Stop: middle of range; Target 1R | 12 | +0.19 | +2.26 |
| Stop: VWAP; Target 1R | 12 | +0.18 | +2.21 |
| Enter at signal close | 12 | +0.17 | +2.09 |
| Stop: other side of range; Hold to 3:55 PM | 12 | +0.17 | +2.07 |
| Signals until 3:00 PM | 12 | +0.16 | +1.98 |
| OR 30 min | 7 | +0.11 | +0.80 |
| Signals until 10:30 AM | 11 | +0.09 | +0.94 |

Compare these with the backtest after about 40 paper trades.
