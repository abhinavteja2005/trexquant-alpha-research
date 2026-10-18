# Deck content draft: top single-thesis alphas (no combinations)

All numbers are Trexsim Slow mode, delay 0, industry-neutral, 2008-02..2021-12, taken from `alphas/registry.csv`.
- IR is daily (x15.9 = annualised).
- TVR is daily turnover.
- OOS1 is the IR on the 2017-21 hold-out.
- Corr is the highest daily-PnL correlation to any alpha already in the competition pool.

## Important caveat
All 10 of our submissions are combinations:
- 8 blend a fast price pattern with a slow accounting signal;
- 2 are multi-factor accounting composites (T_COMP7, SWC_BS5_acc).

So every alpha below was simulated as a standalone single-signal alpha. None of them was submitted on its own, because each one failed the pool-correlation gate or the IR bar. The deck should say this openly.

## Candidates (ranked)

### 1. Gap-down rebound: close near the day's low after a drop (Alpha #54, `A101_054_S`)
- **Thesis:** a stock that gaps down at the open and closes near its low has been hit by forced or liquidity selling. Delay-0 contrarians who supply liquidity at the close are paid as the price reverts the next day.
- **Code:**
  ```
  loc = (low - close)/(low - high - 0.001*close)
  alpha = -loc*(open/close)**5
  ```
- **Source:** Kakushadze, "101 Formulaic Alphas" (2016), arXiv:1601.00991. Liquidity-provision link: Campbell, Grossman & Wang (QJE 1993).
- **Slow results:**
  - IR .112 (annualised about 1.78), TVR 1.38, best year .34.
  - OOS1 only .015: the signal decayed after 2016.
  - Corr .995 to pool #629528, so another participant already holds it.
- **Research path:**
  - Fast screen first, then a Slow re-run.
  - Our version blended with low accruals at 1.5x was SUBMITTED (#715966, IR .137).

### 2. Closing-pressure reversal: fade the close-vs-last-hour-VWAP gap (`P_VWAPT`)
- **Thesis:** heavy, price-insensitive flow in the last hour (index rebalancing, end-of-day hedging) pushes the close away from the hour's VWAP, and the push reverts. It is a pure liquidity effect rather than news, so it should hold out of sample.
- **Code** (core leg, as used in `alphas/drafts/r-ria-repair.json`):
  ```
  g = ts_mean((close - vwap_last_hour)/vwap_last_hour, 5)
  alpha = -cs_rank(g)
  ```
  The exact P_VWAPT expression was queued straight into the runner, so it is not in the repo. Copy it from the portal (or from an R_RIA alpha's code) before the deck goes out.
- **Sources:**
  - Campbell, Grossman & Wang (QJE 1993);
  - Bogousslavsky & Muravyev (2023), closing-auction price pressure;
  - Amihud (2002), illiquidity.
- **Slow results:**
  - IR .083 (Fast .098), TVR 1.05, irtvr .081.
  - OOS1 .085, the most stable of the price signals.
  - Corr .782 to #570310.
- **Research findings:**
  - Fast and Slow PnL correlate only .34, so Fast is a noisy filter.
  - Size and volatility neutralisation cut its IR to .051.
  - A 60-day regime gate cut it to .071.
  - This leg later became the base of submissions #705948 and #703370 (weekly-held blends).

### 3. Intraday range-location drift (Alpha #53, `A101_053_S`)
- **Thesis:** a sharp 10-day change in where the close sits inside the daily high-low range reflects temporary order imbalance, and it mean-reverts.
- **Code:**
  ```
  pos = ((close-low)-(high-close))/(close-low+0.001*close)
  alpha = -delta(pos, 10)
  ```
- **Source:** Kakushadze (2016), Alpha #53.
- **Slow results:** IR .074, TVR 1.52, corr .654 to #631586, OOS1 .014, best year .42.

### 4. Flow-toxicity reversal (`MM1_TOXREV`): our own new family; the strongest thesis, the weakest numbers
- **Thesis:** market makers lose money to informed (toxic) flow and earn from uninformed flow.
  - A smooth, one-directional last-hour move looks informed and tends to continue.
  - A choppy move looks like liquidity demand and reverts.
  - So the signal fades choppy moves and follows smooth ones, with smoothness measured net of move size.
- **Code:**
  ```
  r = cs_zscore(ts_mean(return_last_hour, 5))
  sz = cs_rank(ts_mean(abs(return_last_hour), 5))
  smooth = cs_rank(cs_rank(ts_mean(abs(information_ratio_last_hour), 5)) - sz)
  alpha = -r * (1.5 - smooth)
  ```
- **Source:** Easley, Lopez de Prado & O'Hara, "Flow Toxicity and Liquidity in a High-Frequency World" (RFS 2012).
- **Slow results:** IR .059 (below the .07 bar), TVR .97, OOS1 .068, corr .628.
- **Research path:** an Opus critic review led to netting move size out of the smoothness measure (see `alphas/drafts/c2-newfam.critic.md`).

**Reserve option:** low accruals with low asset growth (`Q_ACCR_AG`, Sloan 1996 plus Cooper, Gulen & Schill 2008) has IR .067, TVR .05, irtvr .298 and OOS1 .095. It has two legs, so it counts as a combination; use it only if a fundamental example is needed.

## Research-process slides (shared across ideas)
- **Pipeline:** literature or Kakushadze-101 idea, then a written thesis, then a critic review (look-ahead, dimensionless, at most 10 variables), then a Fast screen, then a Slow simulation, then pool-correlation triage.
- **Main lesson:** daily IR in this universe comes mostly from short-term reversal, but the pool is crowded with it (corr .78 to .99).
- **Data:** 403 alphas simulated in total; full log in `alphas/registry.csv`.

## Plots: not in the repo
The runner stored only summary metrics, not daily PnL series, so the plots have to be captured from Trexsim. For each alpha:
1. Open its sim (search by name in the portal).
2. Screenshot the cumulative PnL chart and the yearly IR table.

Portal sim IDs on record: P_VWAPT #673000. A101_054_S, A101_053_S and MM1_TOXREV have no ID in our records; re-run them in Slow mode if they can't be found.
