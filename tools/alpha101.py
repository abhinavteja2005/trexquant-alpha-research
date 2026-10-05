"""Hand-checked Trexsim translations of Kakushadze's "101 Formulaic Alphas".

Usage: python tools/alpha101.py [out.json]   (default alphas/drafts/a101.json), then run check_alpha.

Mapping (paper -> Trexsim): rank->cs_rank, delay->ts_delay, correlation/covariance->ts_corr_binary,
stddev->ts_std, sum->ts_sum, Ts_Rank->ts_rank, delta/decay_linear/ts_argmax/ts_argmin -> custom ops,
returns->ret1, vwap->vwap_last_hour (approximation: the portal has no full-day VWAP), adv20->ts_mean(volume,20),
cap->mktcap, x?y:z -> cond*y + (1-cond)*z, sign(x) -> ((x>0)-(x<0)).
Edits for this portal: price differences are divided by close (dimensionless, avoids split
adjustments), windows are snapped to {3,5,10,20,40,60,120,250}, and IndNeutralize/parameter-fitted
alphas (#48, #56-#100) are skipped (industry neutralization is already applied by the simulator).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = "Kakushadze, \"101 Formulaic Alphas\" (2016), https://arxiv.org/abs/1601.00991"

# (number, family, thesis, [(code, comment), ...]); the last line must assign alpha.
ALPHAS = [
    (2, "A101_VOLPX", "Days when volume growth and the open-to-close return move together tend to reverse.", [
        ("dv = delta(at_signlog(volume), 2)", "2-day change in log volume"),
        ("oc = (close - open)/open", "open-to-close return"),
        ("alpha = -ts_corr_binary(cs_rank(dv), cs_rank(oc), 5)", "short names whose volume and return ranks co-move"),
    ]),
    (3, "A101_VOLPX", "A rising open price on rising volume over two weeks is crowded buying that fades.", [
        ("alpha = -ts_corr_binary(cs_rank(open), cs_rank(volume), 10)", "negative 10-day corr of open-price rank and volume rank"),
    ]),
    (4, "A101_REV", "Stocks whose lows are at the top of their own recent range tend to mean-revert.", [
        ("alpha = -ts_rank(cs_rank(low), 10)", "short stocks whose low-price rank is high versus its last 10 days"),
    ]),
    (6, "A101_VOLPX", "Price-volume co-movement signals liquidity-driven moves that reverse.", [
        ("alpha = -ts_corr_binary(open, volume, 10)", "negative 10-day correlation of open price and volume"),
    ]),
    (9, "A101_TREND", "Follow a move only when the last week was one-directional; otherwise fade it.", [
        ("up = ts_min(ret1, 5) > 0", "every day of the last 5 was up"),
        ("dn = ts_max(ret1, 5) < 0", "every day of the last 5 was down"),
        ("trend = up + dn", "1 if the week was one-directional"),
        ("alpha = trend*ret1 - (1 - trend)*ret1", "momentum in clean trends, reversal otherwise"),
    ]),
    (12, "A101_VOLPX", "A price move made on rising volume reverses next day (liquidity shock).", [
        ("dv = delta(volume, 1)/ts_mean(volume, 20)", "change in volume, scaled by average volume"),
        ("alpha = -((dv > 0) - (dv < 0))*ret1", "fade today's return in the direction of the volume change"),
    ]),
    (14, "A101_VOLPX", "Accelerating returns combined with price-volume correlation tend to reverse.", [
        ("acc = delta(ret1, 3)", "3-day change in daily return"),
        ("alpha = -cs_rank(acc)*ts_corr_binary(open, volume, 10)", "short acceleration, scaled by open-volume corr"),
    ]),
    (15, "A101_VOLPX", "Persistent high-price/volume co-movement marks crowded moves that fade.", [
        ("c = ts_corr_binary(cs_rank(high), cs_rank(volume), 3)", "3-day corr of high-price rank and volume rank"),
        ("alpha = -ts_sum(cs_rank(c), 3)", "short names where that corr stays high"),
    ]),
    (18, "A101_REV", "Large, volatile intraday bodies that track the open reverse.", [
        ("body = (close - open)/close", "open-to-close move as a fraction of price"),
        ("vol = ts_std(abs(close - open)/close, 5)", "5-day volatility of the intraday move"),
        ("alpha = -cs_rank(vol + body + ts_corr_binary(close, open, 10))", "fade big, volatile, open-anchored moves"),
    ]),
    (20, "A101_GAP", "Opening above yesterday's high, close and low is an overreaction that fades.", [
        ("g_hi = open/ts_delay(high, 1) - 1", "gap versus yesterday's high"),
        ("g_cl = open/ts_delay(close, 1) - 1", "gap versus yesterday's close"),
        ("g_lo = open/ts_delay(low, 1) - 1", "gap versus yesterday's low"),
        ("alpha = -cs_rank(g_hi)*cs_rank(g_cl)*cs_rank(g_lo)", "short the stocks that gap up the most"),
    ]),
    (22, "A101_VOLPX", "Rising high-price/volume correlation in volatile names precedes reversal.", [
        ("dc = delta(ts_corr_binary(high, volume, 5), 5)", "5-day change in the 5-day high-volume corr"),
        ("alpha = -dc*cs_rank(ts_std(close, 20)/close)", "weight by 20-day price volatility"),
    ]),
    (26, "A101_VOLPX", "When volume and high-price both sit at local peaks together, the move is exhausted.", [
        ("c = ts_corr_binary(ts_rank(volume, 5), ts_rank(high, 5), 5)", "corr of 5-day volume and high ranks"),
        ("alpha = -ts_max(c, 3)", "short names with the highest recent co-peaking"),
    ]),
    (30, "A101_TREND", "Three straight up-closes on fading volume is a weak rally to sell.", [
        ("s1 = (ret1 > 0) - (ret1 < 0)", "sign of today's return"),
        ("s2 = ts_delay(s1, 1) + ts_delay(s1, 2)", "signs of the previous two days"),
        ("alpha = (1 - cs_rank(s1 + s2))*ts_sum(volume, 5)/ts_sum(volume, 20)", "fewer up days and higher recent volume is better"),
    ]),
    (33, "A101_REV", "Close above open (intraday gain) reverts the next day.", [
        ("alpha = cs_rank(open/close - 1)", "long stocks that fell from open to close"),
    ]),
    (34, "A101_REV", "Calm stocks that fell today rebound; short-term vol spikes and gains fade.", [
        ("vr = ts_std(ret1, 3)/ts_std(ret1, 5)", "short- over medium-horizon volatility"),
        ("alpha = cs_rank((1 - cs_rank(vr)) + (1 - cs_rank(ret1)))", "low vol ratio and low return rank are long"),
    ]),
    (35, "A101_VOLPX", "High-volume days with a weak range position and weak returns lead to rebounds.", [
        ("v = ts_rank(volume, 40)", "volume versus its last 40 days"),
        ("r = 1 - ts_rank((close + high - low)/close, 20)", "low intraday range position versus history"),
        ("alpha = v*r*(1 - ts_rank(ret1, 40))", "heavy volume, weak range position, weak return"),
    ]),
    (38, "A101_REV", "Stocks at a local price high that also rose intraday fade.", [
        ("alpha = -cs_rank(ts_rank(close, 10))*cs_rank(close/open)", "short high 10-day rank times intraday gain"),
    ]),
    (40, "A101_VOLPX", "Volatile highs that move with volume mark crowded, reversing moves.", [
        ("hv = ts_std(high, 10)/close", "10-day volatility of the high, as a fraction of price"),
        ("alpha = -cs_rank(hv)*ts_corr_binary(high, volume, 10)", "short volatile, volume-driven highs"),
    ]),
    (41, "A101_VWAP", "A close-hour VWAP above the geometric mid of the day's range signals buying that fades.", [
        ("mid = (high*low)**0.5/close", "geometric mid of the day's range, relative to the close"),
        ("alpha = mid - vwap_last_hour/close", "long when the last-hour VWAP sits below the mid"),
    ]),
    (43, "A101_VOLPX", "Price drops on unusually high volume rebound.", [
        ("rv = ts_rank(volume/ts_mean(volume, 20), 20)", "relative volume versus its recent history"),
        ("alpha = rv*ts_rank(-delta(close, 5)/close, 10)", "long recent losers that traded heavily"),
    ]),
    (44, "A101_VOLPX", "High prices that coincide with high volume rank are exhausted.", [
        ("alpha = -ts_corr_binary(high, cs_rank(volume), 5)", "negative 5-day corr of high and volume rank"),
    ]),
    (50, "A101_VWAP", "Persistent co-movement of volume and VWAP ranks marks crowded trades.", [
        ("c = ts_corr_binary(cs_rank(volume), cs_rank(vwap_last_hour), 5)", "5-day corr of volume rank and VWAP rank"),
        ("alpha = -ts_max(cs_rank(c), 5)", "short the most persistent co-movers"),
    ]),
    (53, "A101_RANGE", "A change in where the close sits within the day's range reverts.", [
        ("pos = ((close - low) - (high - close))/(close - low + 0.001*close)", "close location within the day's range"),
        ("alpha = -delta(pos, 10)", "fade the 10-day change in close location"),
    ]),
    (54, "A101_RANGE", "A close near the low on a gap-down open rebounds (delay-0 contrarian).", [
        ("loc = (low - close)/(low - high - 0.001*close)", "how far the close sits above the low, 0..1"),
        ("alpha = -loc*(open/close)**5", "long closes near the low, scaled by the open-to-close drop"),
    ]),
    (55, "A101_RANGE", "Stochastic-oscillator level moving with volume marks crowded moves.", [
        ("stoch = (close - ts_min(low, 10))/(ts_max(high, 10) - ts_min(low, 10) + 0.001*close)", "10-day stochastic"),
        ("alpha = -ts_corr_binary(cs_rank(stoch), cs_rank(volume), 5)", "short where stochastic and volume co-move"),
    ]),
]


def build(n, family, thesis, body):
    lines = [f"# Thesis: {thesis} (Alpha #{n}, adapted)", f"# Source: {SOURCE}"]
    lines += [f"{code}  # {comment}" for code, comment in body]
    return {"tag": f"A101_{n:03d}", "base": "A101", "family": family, "expr": "\n".join(lines),
            "source_url": "https://arxiv.org/abs/1601.00991"}


def main(out):
    drafts = [build(*a) for a in ALPHAS]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(drafts, indent=1), encoding="utf-8")
    print(f"wrote {len(drafts)} drafts to {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "alphas" / "drafts" / "a101.json"))
