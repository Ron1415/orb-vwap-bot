# ETF Opening Range + VWAP bot (testing phase)

Third strategy, separate from the reversal swing bot and the FVG day-trading scanner.
Paper trades only; there is no broker connection.

## ETFs (November 4, 2026)
Traded: SPY, QQQ, XLK, SMH. Watch only (followed, never counted): IWM, DIA (`config.WATCH_SYMBOLS`).
XLF, XLE, GLD and TLT were dropped after the 5-year 10-ETF backtest (negative in every year).
Every signal is taken: one trade per ETF per day. Each ETF uses its own opening range, VWAP and 20-day average.
Main candidate: v2 candle, longs only (`config.MAIN_STRATEGY`).

## Rules (version 1, the baseline)
1. **Opening range:** high and low of 9:30-9:45 AM ET (three 5-minute bars).
2. **Long signal:** the first 5-minute bar that closes above the range high while its close is above VWAP (anchored at 9:30).
3. **Short signal:** the first 5-minute bar that closes below the range low while its close is below VWAP.
4. **Entry:** the open of the next bar. Signals only before 11:30 AM. One trade per day.
5. **Stop:** the other side of the range, plus 0.01% of price. Skip if the stop is more than 1% or less than 0.05% away.
6. **Target:** 2R. Anything open closes at 3:55 PM.
7. **Size:** longs 1x, shorts 0.5x (lower risk on shorts).
8. **Costs:** 1 cent per share per side; every headline result is net of costs.

## Paper-traded strategies (approved November 4, 2026)
| Strategy | Rule | Shorts | Risk limit |
|---|---|---|---|
| v1 control | The original rules above, unchanged | traded | 1% both sides |
| v2 candle | Trade only in the direction of the first 15-minute candle | watch only | longs 1%, shorts 0.5% |
| v2b candle, shorts in weak market | v2, but shorts are traded when SPY's prior close is below its 20-day average | below 20-day only | longs 1%, shorts 0.5% |
| v3 candle + volume | v2, and breakout-bar volume at least 0.9x the average opening-range bar | watch only | longs 1%, shorts 0.5% |

Watch-only shorts are recorded and followed with the same rules but are not counted (size 0), so they can be reviewed later.
Only the day's first signal counts; if it fails a strategy's filter, that strategy does not trade that day.
The backtest covers about 5 years (1250 sessions). Sessions before November 25, 2024 are reported separately
as out of sample, because the candle and volume factors were found in the later period.

## Side-by-side tests (every day re-run with each)
- Stops: other side of range, middle of range, VWAP.
- Exits: 1R, 2R, range width, hold to 3:55 PM, half at 1R then trail VWAP.
- Single changes: 5- or 30-minute range, entry at the signal close, signals until 10:30 AM or 3:00 PM.
- Filters (columns): longs, shorts, with the daily trend (prior close vs 20-day average), with the first 15-minute candle,
  narrow range (under 25% of daily ATR), signal by 10:15, small gap (under 0.3%), and trend + candle + by 10:15.
- A combination is only called a candidate with 60+ trades, +0.10R or more, t of 3 or more, and both halves and the
  last 6 months positive. About 180 cells are compared, so t = 2 happens by luck several times.

## Files (all in the repository root, so a flattened upload still works)
| File | What it does |
|---|---|
| `config.py` | Every setting |
| `engine.py` | Opening range, VWAP, signal, trade simulation |
| `data.py` | Alpaca (years of 5-minute bars) and Yahoo (live, and ~60 days without keys) |
| `backtest.py` / `analysis.py` / `review.py` | Backtest, statistics and `backtest/review.md` |
| `live.py` | Live paper checks and the end-of-day result for every variant |
| `report.py` | The GitHub Pages dashboard |
| `run.py` | Entry point used by the workflow |
| `test_engine.py` | Rule checks on hand-built charts (`python test_engine.py`) |
| `spy_orb_vwap_strategy.pine` | The same rules as a TradingView `strategy()` for the Strategy Tester |

## Setup
1. Create a public repository, for example `Ron1415/orb-vwap-bot`, and upload the files.
2. Create the workflow with **Add file → Create new file**, name it `.github/workflows/orb.yml`, and paste the contents of `orb.yml`.
3. **Settings → Secrets and variables → Actions:** add `ALPACA_KEY_ID` and `ALPACA_SECRET_KEY` (the same free keys as fvg-scanner).
4. **Settings → Pages:** set Source to **GitHub Actions**.
5. **Actions → SPY ORB VWAP bot → Run workflow:** mode `backtest`, 1250 days. Then the schedule runs the live paper checks.

## Outputs
- `backtest/summary.json`, `backtest/trades.csv.gz` (every variant), `backtest/review.md`
- `live/today.json`, `live/paper_trades.json`, `live/review.md`
- Dashboard on GitHub Pages.

## Known limits
- 5-minute bars: when one bar touches both the stop and the target, the stop is assumed first (conservative).
- GitHub's schedule can run several minutes late; the paper record keeps the rule-based entry and notes when it was seen.
- Without Alpaca keys the backtest covers only about 60 sessions, which is far too few for one trade a day.
