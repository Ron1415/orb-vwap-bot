"""Entry point used by the GitHub Actions workflow.

  python run.py --auto            decide from New York time: live check in the session, end-of-day job after 4:15 PM
  python run.py --live            one live paper check now
  python run.py --eod             end-of-day: final paper result and every variant
  python run.py --backtest 500    backtest about 500 sessions (needs Alpaca keys for more than ~60 days)
  python run.py --report          rebuild the dashboard only
"""
from __future__ import annotations

import argparse
import datetime as dt
import logging

import config as C
import data
import report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--eod", action="store_true")
    ap.add_argument("--backtest", type=int, nargs="?", const=C.BACKTEST_DAYS)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    if a.backtest:
        import backtest
        s = backtest.run(a.backtest)
        print(f"Backtest: {s['sessions']} sessions from {s['source']}; baseline {s['baseline']['all']}")
    if a.auto or a.live or a.eod:
        import live
        now = dt.datetime.now(data.NY)
        m = now.hour * 60 + now.minute
        if now.weekday() >= 5 and not (a.live or a.eod):
            print("Weekend: nothing to do")
        elif a.eod or (a.auto and m >= C.EOD_AFTER):
            print(live.scan(final=True))
        elif a.live or (C.LIVE_WINDOW[0] <= m <= C.LIVE_WINDOW[1]):
            print(live.scan())
        else:
            print("Outside the session: nothing to do")
    report.build()


if __name__ == "__main__":
    main()
