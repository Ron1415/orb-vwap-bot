# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 14 trades, 28.6% win, -0.24R ±0.30 per trade, profit factor 0.61, max drawdown -5.04R
  - watch-only shorts (not counted): 15 trades, 53.3% win, +0.36R ±0.31 per trade, profit factor 2.17, max drawdown 0.0R
- **v2 candle:** 6 trades, 16.7% win, -0.41R ±0.32 per trade, profit factor 0.29, max drawdown -2.47R
  - watch-only shorts (not counted): 12 trades, 50.0% win, +0.42R ±0.38 per trade, profit factor 2.14, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 8 trades, 25.0% win, -0.19R ±0.40 per trade, profit factor 0.67, max drawdown -2.98R
  - watch-only shorts (not counted): 10 trades, 50.0% win, +0.40R ±0.41 per trade, profit factor 2.19, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Target 2R | 26 | +0.68 | +17.79 |
| Stop: VWAP; Target: range width | 26 | +0.59 | +15.41 |
| Stop: middle of range; Target 2R | 26 | +0.56 | +14.69 |
| Stop: middle of range; Target: range width | 26 | +0.51 | +13.16 |
| OR 5 min | 26 | +0.49 | +12.84 |
| Stop: VWAP; Hold to 3:55 PM | 26 | +0.45 | +11.59 |
| Stop: VWAP; Half at 1R, trail VWAP | 26 | +0.43 | +11.29 |
| Stop: middle of range; Hold to 3:55 PM | 26 | +0.42 | +10.95 |
| Stop: middle of range; Half at 1R, trail VWAP | 26 | +0.35 | +8.99 |
| Stop: VWAP; Target 1R | 26 | +0.31 | +8.00 |
| Stop: other side of range; Half at 1R, trail VWAP | 26 | +0.26 | +6.88 |
| Stop: other side of range; Target 1R | 26 | +0.24 | +6.26 |
| Stop: middle of range; Target 1R | 26 | +0.23 | +6.07 |
| Enter at signal close | 26 | +0.20 | +5.25 |
| Stop: other side of range; Target: range width | 26 | +0.20 | +5.20 |
| Signals until 3:00 PM | 26 | +0.20 | +5.13 |
| Signals until 10:30 AM | 25 | +0.16 | +4.08 |
| Side risk caps (long 1%, short 0.5%) | 18 | +0.14 | +2.52 |
| Stop: other side of range; Hold to 3:55 PM | 26 | +0.12 | +3.23 |
| OR 30 min | 16 | +0.06 | +0.91 |

Compare these with the backtest after about 40 paper trades.
