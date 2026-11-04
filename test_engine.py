"""Rule checks on hand-built charts. Run: python test_engine.py"""
import random

import config as C
import engine as E

D = "2026-11-02"


def mk(spec):
    """spec: list of (o,h,l,c) starting at 9:30, 5 minutes apart, volume 1000."""
    return [E.Bar(i, D, 570 + 5 * i, o, h, l, c, 1000) for i, (o, h, l, c) in enumerate(spec)]


OR = [(100, 100.5, 99.6, 100.2), (100.2, 100.6, 99.8, 100.4), (100.4, 100.7, 99.9, 100.5)]   # ORH 100.7 ORL 99.6
FLAT = (100.5, 100.6, 100.4, 100.5)


def rules(**kw):
    kw.setdefault("max_risk_pct", 5.0)      # test charts use wide ranges; the risk cap has its own test
    return dict(C.RULES, **kw)


def test_long_target():
    bars = mk(OR + [(100.5, 100.9, 100.4, 100.85),   # 9:45 closes above ORH and VWAP -> signal
                    (100.9, 101.0, 100.8, 100.95),    # 9:50 entry at open 100.9
                    (100.95, 103.6, 100.9, 103.4)] + [FLAT] * 75)
    tr, st = E.run_day(bars, {}, rules())
    assert tr and tr["side"] == "long" and tr["signal_min"] == 585 and tr["entry_min"] == 590, (tr, st)
    assert abs(tr["entry"] - 100.9) < 1e-9
    stop = 99.6 - 100.9 * 0.0001
    assert abs(tr["stop"] - stop) < 1e-4
    assert tr["exit_reason"] == "target" and abs(tr["exit"] - (100.9 + 2 * (100.9 - stop))) < 1e-4
    assert abs(tr["r_gross"] - 2) < 1e-6 and tr["r_net"] < 2
    print("long target ok", tr["r_net"])


def test_short_needs_vwap():
    # close below ORL but price is far above VWAP? Build a session where VWAP sits low: no short.
    bars = mk(OR + [(99.7, 99.8, 99.5, 99.55)] + [FLAT] * 70)
    vw = E.session_vwap(E.rth(bars))
    sig, st = E.find_signal(bars, rules(), vw)
    assert sig and sig["side"] == "short" and vw[3] > 99.55, (sig, st)
    # same close but VWAP forced below the close -> no signal at that bar
    vw2 = list(vw)
    vw2[3] = 99.5
    sig2, _ = E.find_signal(bars[:4], rules(), vw2)
    assert sig2 is None
    print("short/VWAP ok")


def test_stop_first_and_size():
    bars = mk(OR + [(99.7, 99.8, 99.5, 99.55), (99.55, 101.0, 97.0, 99.0)] + [FLAT] * 70)
    tr, _ = E.run_day(bars, {}, rules())
    assert tr["side"] == "short" and tr["exit_reason"] == "stop" and tr["r_gross"] < -0.99, tr
    assert tr["size"] == 0.5 and abs(tr["r_sized"] - tr["r_net"] * 0.5) < 1e-6
    print("stop first ok", tr["r_net"])


def test_cutoff_and_eod():
    late = mk(OR + [FLAT] * 30 + [(100.6, 101, 100.5, 100.95)] + [FLAT] * 44)   # breakout at 12:15
    tr, st = E.run_day(late, {}, rules())
    assert tr is None and "No breakout" in st, st
    tr, _ = E.run_day(late, {}, rules(entry_cutoff=900, target="eod"))
    assert tr and tr["exit_reason"] == "eod" and tr["exit_min"] == 955, tr
    print("cutoff/eod ok")


def test_half_trail():
    bars = mk(OR + [(100.5, 100.9, 100.4, 100.85), (100.9, 102.2, 100.8, 102.1),   # hits 1R (~102.2) in entry bar? 1R=~1.31 -> 102.21
                    (102.1, 102.4, 102.0, 102.3), (102.3, 102.3, 99.0, 99.2)] + [FLAT] * 70)
    tr, _ = E.run_day(bars, {}, rules(target="half_r1_trail_vwap"))
    assert tr["half_taken"] and tr["exit_reason"] in ("breakeven", "vwap trail"), tr
    assert abs(tr["r_gross"] - 0.5) < 1e-6, tr
    print("half + breakeven ok", tr["exit_reason"], tr["r_gross"])


def test_next_bar_risk_skip():
    # wide range: risk > 1% is skipped
    wide = [(100, 101, 98.5, 100.5), (100.5, 101, 99, 100.8), (100.8, 101.2, 99.5, 101)]
    bars = mk(wide + [(101, 101.5, 100.9, 101.4)] + [FLAT] * 70)
    tr, st = E.run_day(bars, {}, rules(max_risk_pct=1.0))
    assert tr is None and "risk too large" in st, st
    print("risk filter ok")


def test_random_sanity():
    """On a driftless random walk (30 steps inside each bar, so highs and lows are real) every
    stop/target choice should average about 0R. A clear positive result here would mean a bug."""
    random.seed(1)
    worst = 0
    for stop in ("or_opposite", "or_mid", "vwap"):
        for target in ("r2", "eod", "half_r1_trail_vwap"):
            tot = n = 0
            random.seed(1)
            for _ in range(800):
                p, spec = 100.0, []
                for _ in range(78):
                    path = [p]
                    for _ in range(30):
                        path.append(path[-1] * (1 + random.gauss(0, 0.0011 / 30 ** 0.5)))
                    spec.append((path[0], max(path), min(path), path[-1]))
                    p = path[-1]
                tr, _ = E.run_day(mk(spec), {}, rules(stop=stop, target=target))
                if tr:
                    tot += tr["r_gross"]
                    n += 1
            worst = max(worst, abs(tot / n))
            print(f"random walk {stop}/{target}: {n} trades, avg gross {tot / n:+.3f}R")
    assert worst < 0.15, worst


def test_strategies_and_side_risk():
    # first candle up (OR open 100, close 100.5); breakout long, risk about 1.3% -> v1 at 5% cap trades,
    # side caps: long 1% cap skips it; a narrower day passes
    narrow = [(100, 100.3, 99.95, 100.1), (100.1, 100.35, 100.0, 100.2), (100.2, 100.4, 100.05, 100.3)]
    up = mk(narrow + [(100.3, 100.6, 100.25, 100.55), (100.55, 100.7, 100.5, 100.6)] + [FLAT] * 75)
    v1, _ = E.run_strategy(up, {}, "v1 control")
    v2, _ = E.run_strategy(up, {}, "v2 candle")
    assert v1 and v2 and v2["side"] == "long", (v1, v2)
    # same chart mirrored into a short after an UP first candle -> v2 filters it out, v1 trades it
    dn = mk([(100, 100.05, 99.7, 99.9), (99.9, 100.0, 99.65, 99.8), (99.8, 100.1, 99.6, 100.05)]
            + [(100.0, 100.0, 99.4, 99.45), (99.45, 99.5, 99.3, 99.35)] + [(99.4, 99.45, 99.3, 99.4)] * 75)
    v1, _ = E.run_strategy(dn, {}, "v1 control")
    v2, st = E.run_strategy(dn, {}, "v2 candle")
    assert v1 and v1["side"] == "short" and v2 is None, (v1, st)
    assert C.STRATEGY_FILTERS["candle"](v1) is False and C.STRATEGY_FILTERS[None](v1)
    # side risk: a short risking 0.6% is skipped with the 0.5% short cap, a long risking 0.6% is not
    r = dict(C.RULES, max_risk_pct_long=1.0, max_risk_pct_short=0.5)
    tr, st = E.run_day(dn, {}, r)
    assert tr is None and "risk too large" in st and v1["risk_pct"] > 0.5, (tr, st)
    tl, _ = E.run_day(up, {}, dict(r, max_risk_pct_long=0.3))
    assert tl is None and E.run_day(up, {}, r)[0]["risk_pct"] > 0.3
    print("strategies + side risk ok")


if __name__ == "__main__":
    for f in [test_long_target, test_short_needs_vwap, test_stop_first_and_size, test_cutoff_and_eod,
              test_half_trail, test_next_bar_risk_skip, test_strategies_and_side_risk, test_random_sanity]:
        f()
    print("ALL TESTS PASSED")
