# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 21 trades, 33.3% win, -0.03R ±0.28 per trade, profit factor 0.94, max drawdown -5.04R
  - watch-only shorts (not counted): 22 trades, 59.1% win, +0.45R ±0.26 per trade, profit factor 2.47, max drawdown 0.0R
- **v2 candle:** 6 trades, 16.7% win, -0.41R ±0.32 per trade, profit factor 0.29, max drawdown -2.47R
  - watch-only shorts (not counted): 16 trades, 50.0% win, +0.33R ±0.33 per trade, profit factor 1.81, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 9 trades, 33.3% win, +0.06R ±0.42 per trade, profit factor 1.11, max drawdown -2.98R
  - watch-only shorts (not counted): 13 trades, 46.2% win, +0.17R ±0.34 per trade, profit factor 1.41, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Hold to 3:55 PM | 40 | +0.72 | +28.84 |
| Stop: VWAP; Target 2R | 40 | +0.69 | +27.61 |
| Stop: middle of range; Hold to 3:55 PM | 40 | +0.65 | +26.19 |
| Stop: middle of range; Target 2R | 40 | +0.61 | +24.53 |
| Stop: VWAP; Target: range width | 40 | +0.61 | +24.46 |
| Stop: VWAP; Half at 1R, trail VWAP | 40 | +0.54 | +21.61 |
| OR 5 min | 40 | +0.53 | +21.39 |
| Stop: middle of range; Target: range width | 40 | +0.52 | +20.88 |
| OR 30 min | 26 | +0.48 | +12.61 |
| Stop: middle of range; Half at 1R, trail VWAP | 40 | +0.42 | +16.96 |
| Stop: VWAP; Target 1R | 40 | +0.40 | +15.83 |
| Enter at signal close | 40 | +0.31 | +12.25 |
| Signals until 3:00 PM | 40 | +0.30 | +12.19 |
| Stop: middle of range; Target 1R | 40 | +0.30 | +11.92 |
| Signals until 10:30 AM | 39 | +0.29 | +11.15 |
| Stop: other side of range; Hold to 3:55 PM | 40 | +0.28 | +11.02 |
| Stop: other side of range; Half at 1R, trail VWAP | 40 | +0.27 | +10.88 |
| Stop: other side of range; Target 1R | 40 | +0.25 | +10.09 |
| Stop: other side of range; Target: range width | 40 | +0.25 | +9.95 |
| Side risk caps (long 1%, short 0.5%) | 24 | +0.03 | +0.72 |

Compare these with the backtest after about 40 paper trades.
