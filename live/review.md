# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 21 trades, 33.3% win, -0.03R ±0.28 per trade, profit factor 0.94, max drawdown -5.04R
  - watch-only shorts (not counted): 23 trades, 60.9% win, +0.43R ±0.25 per trade, profit factor 2.5, max drawdown 0.0R
- **v2 candle:** 6 trades, 16.7% win, -0.41R ±0.32 per trade, profit factor 0.29, max drawdown -2.47R
  - watch-only shorts (not counted): 16 trades, 50.0% win, +0.33R ±0.33 per trade, profit factor 1.81, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 9 trades, 33.3% win, +0.06R ±0.42 per trade, profit factor 1.11, max drawdown -2.98R
  - watch-only shorts (not counted): 13 trades, 46.2% win, +0.17R ±0.34 per trade, profit factor 1.41, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Hold to 3:55 PM | 41 | +0.71 | +29.22 |
| Stop: VWAP; Target 2R | 41 | +0.68 | +28.00 |
| Stop: middle of range; Hold to 3:55 PM | 41 | +0.65 | +26.52 |
| Stop: middle of range; Target 2R | 41 | +0.61 | +24.86 |
| Stop: VWAP; Target: range width | 41 | +0.61 | +24.85 |
| Stop: VWAP; Half at 1R, trail VWAP | 41 | +0.54 | +22.10 |
| Stop: middle of range; Target: range width | 41 | +0.52 | +21.21 |
| OR 5 min | 41 | +0.50 | +20.39 |
| OR 30 min | 27 | +0.47 | +12.78 |
| Stop: middle of range; Half at 1R, trail VWAP | 41 | +0.43 | +17.45 |
| Stop: VWAP; Target 1R | 41 | +0.41 | +16.82 |
| Stop: middle of range; Target 1R | 41 | +0.31 | +12.91 |
| Enter at signal close | 41 | +0.30 | +12.44 |
| Signals until 3:00 PM | 41 | +0.30 | +12.37 |
| Signals until 10:30 AM | 40 | +0.28 | +11.32 |
| Stop: other side of range; Hold to 3:55 PM | 41 | +0.27 | +11.19 |
| Stop: other side of range; Half at 1R, trail VWAP | 41 | +0.27 | +11.05 |
| Stop: other side of range; Target 1R | 41 | +0.25 | +10.27 |
| Stop: other side of range; Target: range width | 41 | +0.25 | +10.12 |
| Side risk caps (long 1%, short 0.5%) | 25 | +0.04 | +0.89 |

Compare these with the backtest after about 40 paper trades.
