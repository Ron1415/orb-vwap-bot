# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 11 trades, 9.1% win, -0.69R ±0.19 per trade, profit factor 0.12, max drawdown -5.04R
  - watch-only shorts (not counted): 11 trades, 54.5% win, +0.17R ±0.35 per trade, profit factor 1.43, max drawdown 0.0R
- **v2 candle:** 6 trades, 16.7% win, -0.41R ±0.32 per trade, profit factor 0.29, max drawdown -2.47R
  - watch-only shorts (not counted): 9 trades, 44.4% win, +0.11R ±0.43 per trade, profit factor 1.23, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 7 trades, 14.3% win, -0.50R ±0.28 per trade, profit factor 0.23, max drawdown -2.98R
  - watch-only shorts (not counted): 8 trades, 50.0% win, +0.25R ±0.46 per trade, profit factor 1.6, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Target: range width | 19 | +0.21 | +3.90 |
| Stop: VWAP; Target 2R | 19 | +0.20 | +3.89 |
| Stop: VWAP; Half at 1R, trail VWAP | 19 | +0.16 | +3.12 |
| Stop: middle of range; Target: range width | 19 | +0.13 | +2.42 |
| OR 5 min | 19 | +0.10 | +1.93 |
| Stop: VWAP; Hold to 3:55 PM | 19 | +0.07 | +1.25 |
| Stop: middle of range; Half at 1R, trail VWAP | 19 | +0.06 | +1.12 |
| Stop: VWAP; Target 1R | 19 | +0.06 | +1.11 |
| Stop: middle of range; Target 2R | 19 | +0.04 | +0.79 |
| Stop: middle of range; Hold to 3:55 PM | 19 | +0.01 | +0.15 |
| Stop: other side of range; Target 1R | 19 | -0.04 | -0.68 |
| Stop: other side of range; Half at 1R, trail VWAP | 19 | -0.04 | -0.80 |
| Stop: middle of range; Target 1R | 19 | -0.04 | -0.83 |
| Stop: other side of range; Target: range width | 19 | -0.04 | -0.85 |
| Side risk caps (long 1%, short 0.5%) | 15 | -0.10 | -1.46 |
| Enter at signal close | 19 | -0.14 | -2.62 |
| Stop: other side of range; Hold to 3:55 PM | 19 | -0.14 | -2.64 |
| Signals until 3:00 PM | 19 | -0.14 | -2.72 |
| OR 30 min | 12 | -0.19 | -2.30 |
| Signals until 10:30 AM | 18 | -0.21 | -3.77 |

Compare these with the backtest after about 40 paper trades.
