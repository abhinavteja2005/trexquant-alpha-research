# New families to explore (Oct 6, 17:30): mean reversion, momentum, market making

Why: the VWAP-gap / late-day-composite reversal family and the fundamental-change family are now saturated
(blocked by #570310, #604930 and our own #695151). Plain reversal is crowded, so each card adds a conditioning
idea (WHO is trading, informed vs uninformed flow), residualisation, or a slow anti-correlated partner.
All code is dtype-safe (no bool into ts_/cs_ operators; flags cast with `(close/close)*(...)`), within 10 variables,
with windows from {3, 5, 10, 20, 40, 60, 120, 250}. The Writer adds the per-line comments and the `# Thesis:` /
`# Source:` header before queueing. Queue as Slow with lb/wlb as noted (max 300).

## A. Market making / liquidity provision (fade uninformed flow, follow informed flow)
### MM1 Toxicity-aware late-day reversal (lb 60)
Thesis: market makers lose to informed (toxic) flow and earn from uninformed flow. A last-hour move that was smooth
and one-directional (high |information ratio| within the hour) looks informed and tends to continue; a choppy move
looks like noise or liquidity demand and reverts.
Source: Easley, Lopez de Prado & O'Hara, "Flow Toxicity and Liquidity in a High-Frequency World" (RFS 2012),
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1695596
```
r = cs_zscore(ts_mean(return_last_hour, 5))
smooth = cs_rank(ts_mean(abs(information_ratio_last_hour), 5))
alpha = -r * (1.5 - smooth)
```
(1.5 - smooth) is +0.5 for the choppiest stocks (fade) and -0.5 for the smoothest (follow). Variables: 2.

### MM2 Trade-size-aware reversal (lb 60)
Thesis: late-day moves made by small (retail-sized) trades revert; moves made by large (institutional) trades carry
information and continue.
Source: Barber, Odean & Zhu, "Do Retail Trades Move Markets?" (RFS 2009); Hvidkjaer, "Small Trades and the
Cross-Section of Stock Returns" (RFS 2008).
```
r = cs_zscore(ts_mean(return_last_hour, 5))
size = cs_rank(ts_mean(volume_last_hour/number_of_trades_last_hour, 20) / ts_mean(volume_first_hour/number_of_trades_first_hour, 20))
alpha = -r * (1.5 - size)
```
(Size: close-hour trade size relative to open-hour trade size, which is dimensionless and stock-specific.) Variables: 5.

### MM3 Closing-auction pressure (lb 80)
Thesis: when an unusually large share of the day's volume prints in the last hour (index rebalancing, fund flows),
the close is pushed away from fair value and reverts.
Source: Bogousslavsky & Muravyev, "Who Trades at the Close? Implications for Price Discovery and Liquidity" (2023).
```
share = volume_last_hour/volume
spike = cs_rank(ts_mean(share, 5) / ts_mean(share, 60)) > 1.5
alpha = at_zero2nan(-cs_rank(ts_mean(return_last_hour, 5)) * spike)
```
Variables: 3.

## B. Mean reversion (residualised, less crowded)
### MR1 Residual reversal (lb 140)
Thesis: reversal of the stock-specific (residual) part of the return is cleaner and less exposed to momentum crashes
than raw reversal.
Source: Blitz, Huij, Lansdorp & Verbeek, "Short-Term Residual Reversal" (Journal of Financial Markets 2013),
https://www.ssrn.com/abstract=1911449
```
beta = ts_corr_binary(ret1, ret1_spx, 120) * ts_std(ret1, 120) / (ts_std(ret1_spx, 120) + 0.0001)
res = ret1 - beta*ret1_spx
alpha = -cs_rank(ts_sum(res, 5) / (ts_std(res, 60) + 0.0001))
```
Warning: VP_RESREV_VIX (residual 3-day with a VIX tilt) had IR .02 / corr .83. Test the plain 5-day, vol-scaled
version once; drop the family if IR < .04.

### MR2 Morning-anchor reversion (lb 60)
Thesis: the first-hour VWAP is the day's consensus price after overnight news is absorbed; closes far from it,
without an information-like (smooth) last hour, revert.
Source: Bogousslavsky & Muravyev (2023); Gao, Han, Li & Zhou, "Market Intraday Momentum" (JFE 2018), for
first-hour information.
```
dev = ts_mean((close - vwap_first_hour)/vwap_first_hour, 5)
smooth = cs_rank(ts_mean(abs(information_ratio_last_hour), 5))
alpha = -cs_zscore(dev) * (1.5 - smooth)
```
Variables: 3.

## C. Momentum (slow, low turnover: natural PARTNERS for the reversal blends, since momentum and reversal PnL are negatively correlated)
### MO1 Residual momentum, 12-1 months (lb 300)
Thesis: momentum in the stock-specific return, scaled by its volatility, has about half the risk of plain momentum
and avoids momentum crashes.
Source: Blitz, Huij & Martens, "Residual Momentum" (Journal of Empirical Finance 2011); Huij & Lansdorp, "Residual
Momentum and Reversal Strategies Revisited" (2017), https://www.ssrn.com/abstract=2929306
```
beta = ts_corr_binary(ret1, ret1_spx, 120) * ts_std(ret1, 120) / (ts_std(ret1_spx, 120) + 0.0001)
res = ret1 - beta*ret1_spx
mom = (ts_sum(res, 250) - ts_sum(res, 20)) / (ts_std(res, 250) + 0.0001)
alpha = cs_rank(mom)
```
Expect daily IR ~.02-.04 alone, low turnover. Main use: as a partner. Check `PX.pair` against U_PRICE2_szvo and
`PX.blend` before writing the combined alpha.

### MO2 Frog-in-the-pan, dtype-fixed rerun of Q_FROG (lb 300)
Thesis and source as Q_FROG (Da, Gurun & Warachka, RFS 2014). The first run crashed because a bool went into
ts_mean. Fix:
```
one = close/close
pret = close/ts_delay(close, 250) - 1
pos = ts_mean(one*(ret1 > 0), 250)
neg = ts_mean(one*(ret1 < 0), 250)
sgn = one*(pret > 0)*2 - 1
alpha = cs_rank(pret) * (2 - cs_rank(sgn*(neg - pos)))
```

### MO3 Volume-confirmed momentum (lb 300)
Thesis: past winners with LOW turnover keep winning (under-followed), while high-turnover winners are crowded and
fade. Momentum is best where attention is low.
Source: Lee & Swaminathan, "Price Momentum and Trading Volume" (Journal of Finance 2000).
```
mom = close/ts_delay(close, 250) - close/ts_delay(close, 20)
turn = cs_rank(ts_mean(volume/shsout, 120))
alpha = cs_rank(mom) * (2.5 - turn)
```

## D. How to use them (the partner recipe that produced the 4th submission)
1. Run each card alone first (Slow). Record IR, TVR, corr, blocker.
2. For every reversal-type result with IR >= .06, look for partners with `PX.pair(base, cand) < -.05` and
   `PX.own` < .5 (accruals, residual momentum, FROG, volume-confirmed momentum).
3. `PX.blend([[base,1],[partner,w]])` for w in {.5, 1, 1.5}; queue the best one or two as a single alpha
   (equal-risk z-scored blocks: `alpha = at_zero2nan(at_nan2zero(rev) + w*at_nan2zero(part))`).
4. Do NOT build more variants of the saturated families: VWAP-gap / late-day composite + fundamental changes
   (blocked by #695151) or R&D / gross-profit blends (#605850).
