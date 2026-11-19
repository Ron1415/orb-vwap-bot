# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 19 trades, 36.8% win, +0.07R ±0.30 per trade, profit factor 1.14, max drawdown -5.04R
  - watch-only shorts (not counted): 21 trades, 61.9% win, +0.52R ±0.26 per trade, profit factor 2.91, max drawdown 0.0R
- **v2 candle:** 6 trades, 16.7% win, -0.41R ±0.32 per trade, profit factor 0.29, max drawdown -2.47R
  - watch-only shorts (not counted): 15 trades, 53.3% win, +0.41R ±0.34 per trade, profit factor 2.15, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 9 trades, 33.3% win, +0.06R ±0.42 per trade, profit factor 1.11, max drawdown -2.98R
  - watch-only shorts (not counted): 12 trades, 50.0% win, +0.27R ±0.35 per trade, profit factor 1.74, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Hold to 3:55 PM | 37 | +0.86 | +31.86 |
| Stop: VWAP; Target 2R | 37 | +0.83 | +30.64 |
| Stop: middle of range; Hold to 3:55 PM | 37 | +0.79 | +29.22 |
| Stop: middle of range; Target 2R | 37 | +0.74 | +27.56 |
| Stop: VWAP; Target: range width | 37 | +0.69 | +25.50 |
| OR 5 min | 37 | +0.66 | +24.41 |
| Stop: middle of range; Target: range width | 37 | +0.59 | +21.93 |
| Stop: VWAP; Half at 1R, trail VWAP | 37 | +0.54 | +20.14 |
| Stop: middle of range; Half at 1R, trail VWAP | 37 | +0.46 | +16.99 |
| OR 30 min | 25 | +0.42 | +10.61 |
| Enter at signal close | 37 | +0.41 | +15.27 |
| Signals until 3:00 PM | 37 | +0.41 | +15.21 |
| Signals until 10:30 AM | 36 | +0.39 | +14.17 |
| Stop: other side of range; Hold to 3:55 PM | 37 | +0.38 | +14.03 |
| Stop: other side of range; Half at 1R, trail VWAP | 37 | +0.38 | +13.89 |
| Stop: other side of range; Target 1R | 37 | +0.35 | +13.11 |
| Stop: VWAP; Target 1R | 37 | +0.35 | +12.86 |
| Stop: other side of range; Target: range width | 37 | +0.31 | +11.31 |
| Stop: middle of range; Target 1R | 37 | +0.30 | +10.94 |
| Side risk caps (long 1%, short 0.5%) | 21 | +0.18 | +3.74 |

Compare these with the backtest after about 40 paper trades.
