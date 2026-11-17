# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 16 trades, 37.5% win, +0.04R ±0.32 per trade, profit factor 1.07, max drawdown -5.04R
  - watch-only shorts (not counted): 17 trades, 52.9% win, +0.38R ±0.30 per trade, profit factor 2.14, max drawdown 0.0R
- **v2 candle:** 6 trades, 16.7% win, -0.41R ±0.32 per trade, profit factor 0.29, max drawdown -2.47R
  - watch-only shorts (not counted): 14 trades, 50.0% win, +0.43R ±0.36 per trade, profit factor 2.11, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 9 trades, 33.3% win, +0.06R ±0.42 per trade, profit factor 1.11, max drawdown -2.98R
  - watch-only shorts (not counted): 11 trades, 45.5% win, +0.27R ±0.39 per trade, profit factor 1.69, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Target 2R | 30 | +0.76 | +22.73 |
| Stop: VWAP; Hold to 3:55 PM | 30 | +0.66 | +19.74 |
| Stop: middle of range; Target 2R | 30 | +0.65 | +19.63 |
| Stop: middle of range; Hold to 3:55 PM | 30 | +0.63 | +18.90 |
| Stop: VWAP; Target: range width | 30 | +0.62 | +18.63 |
| Stop: middle of range; Target: range width | 30 | +0.54 | +16.26 |
| OR 5 min | 30 | +0.49 | +14.80 |
| Stop: VWAP; Half at 1R, trail VWAP | 30 | +0.45 | +13.41 |
| OR 30 min | 20 | +0.40 | +8.09 |
| Stop: middle of range; Half at 1R, trail VWAP | 30 | +0.37 | +11.06 |
| Enter at signal close | 30 | +0.34 | +10.22 |
| Signals until 3:00 PM | 30 | +0.34 | +10.09 |
| Stop: VWAP; Target 1R | 30 | +0.33 | +9.94 |
| Signals until 10:30 AM | 29 | +0.31 | +9.05 |
| Stop: other side of range; Half at 1R, trail VWAP | 30 | +0.28 | +8.32 |
| Stop: other side of range; Target 1R | 30 | +0.27 | +8.23 |
| Stop: middle of range; Target 1R | 30 | +0.27 | +8.02 |
| Stop: other side of range; Hold to 3:55 PM | 30 | +0.25 | +7.55 |
| Stop: other side of range; Target: range width | 30 | +0.22 | +6.61 |
| Side risk caps (long 1%, short 0.5%) | 20 | +0.18 | +3.51 |

Compare these with the backtest after about 40 paper trades.
