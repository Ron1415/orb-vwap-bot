# ETF ORB-15 + VWAP: live paper review

- **v1 control:** 13 trades, 23.1% win, -0.41R ±0.27 per trade, profit factor 0.38, max drawdown -5.04R
  - watch-only shorts (not counted): 13 trades, 46.2% win, +0.12R ±0.30 per trade, profit factor 1.32, max drawdown 0.0R
- **v2 candle:** 6 trades, 16.7% win, -0.41R ±0.32 per trade, profit factor 0.29, max drawdown -2.47R
  - watch-only shorts (not counted): 10 trades, 40.0% win, +0.10R ±0.39 per trade, profit factor 1.23, max drawdown 0.0R
- **v2b candle, shorts in weak market:** 7 trades, 14.3% win, -0.50R ±0.28 per trade, profit factor 0.23, max drawdown -2.98R
  - watch-only shorts (not counted): 9 trades, 44.4% win, +0.23R ±0.41 per trade, profit factor 1.6, max drawdown 0.0R
- **v3 candle + volume:** no trades
  - watch-only shorts (not counted): 1 trades, 0.0% win, -1.07R per trade, max drawdown 0.0R

| Variant | Trades | Avg R | Total R |
|---|---|---|---|
| Stop: VWAP; Target 2R | 23 | +0.51 | +11.83 |
| Stop: VWAP; Target: range width | 23 | +0.47 | +10.72 |
| OR 5 min | 23 | +0.43 | +9.89 |
| Stop: middle of range; Target 2R | 23 | +0.38 | +8.74 |
| Stop: middle of range; Target: range width | 23 | +0.36 | +8.25 |
| Stop: VWAP; Half at 1R, trail VWAP | 23 | +0.34 | +7.78 |
| Stop: middle of range; Half at 1R, trail VWAP | 23 | +0.23 | +5.34 |
| Stop: VWAP; Target 1R | 23 | +0.22 | +5.05 |
| Stop: other side of range; Target 1R | 23 | +0.14 | +3.29 |
| Stop: middle of range; Target 1R | 23 | +0.14 | +3.12 |
| Stop: other side of range; Target: range width | 23 | +0.11 | +2.51 |
| Stop: other side of range; Half at 1R, trail VWAP | 23 | +0.11 | +2.48 |
| Stop: VWAP; Hold to 3:55 PM | 23 | +0.06 | +1.39 |
| Stop: middle of range; Hold to 3:55 PM | 23 | +0.01 | +0.25 |
| Enter at signal close | 23 | -0.03 | -0.72 |
| Signals until 3:00 PM | 23 | -0.04 | -0.85 |
| Signals until 10:30 AM | 22 | -0.09 | -1.89 |
| Side risk caps (long 1%, short 0.5%) | 16 | -0.09 | -1.46 |
| Stop: other side of range; Hold to 3:55 PM | 23 | -0.11 | -2.59 |
| OR 30 min | 13 | -0.20 | -2.56 |

Compare these with the backtest after about 40 paper trades.
