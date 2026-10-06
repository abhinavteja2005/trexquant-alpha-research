# Repair playbook: turning a rejected alpha into a submittable one

Start with `PX.triage(.065)` in the runner tab (from `runner/px.js`). Each row gives IR, TVR, IR/sqrt(TVR), the blocking
pool alpha, the bar (1.2 x that alpha's IR/sqrt(TVR)), and the turnover at which the current IR would clear the bar.

Arithmetic: new irtvr / old irtvr = (1 - IR loss) / sqrt(1 - TVR cut). Example: cut TVR 50% and lose 20% of IR, and
IR/sqrt(TVR) rises 13%. A repair pays when the % IR loss is well under half the % TVR cut.

## Route A: cut turnover (for "corr_ir_tvr_not_ok" with needTVR >= ~0.35 x current TVR)
| Rank | Technique | Trexsim template (last lines) | Evidence |
|---|---|---|---|
| 1 | Blend with a slow, uncrowded signal at 2-3x weight | `alpha = at_zero2nan(at_nan2zero(r) + 3*(at_nan2zero(k1)+...))` | All 3 submissions. Double weight on VWAPT_rnd_sbc_gpa: TVR .655 -> .463, irtvr .111 -> .125 |
| 2 | Banding / buy-hold spread: enter at the extremes, exit late | `q = cs_rank(s)`; `hl = (ts_max(q, 5) > 1.8)*(q > 1.6)`; `hs = (ts_min(q, 5) < 1.2)*(q < 1.4)`; `alpha = at_zero2nan(hl - hs)` | Most effective cost-mitigation technique in Novy-Marx & Velikov (RFS 2016) and the CFA comparison. Test: R_PRICE2_band |
| 3 | Partial trading toward the target (exponential smoothing) | `alpha = ts_mean_exp(s, 10, 0.7)` (exp_factor meaning not yet verified; R_PRICE2_ewm tests it) | Garleanu & Pedersen (JF 2013): "aim in front of the target, trade partially" |
| 4 | Trade one day a week (weekly rebalance) | `f0 = day_of_the_week < ts_delay(day_of_the_week, 1)`; `f1..f3 = ts_delay(f0, 1..3)`; `alpha = at_zero2nan(f0*s + (1-f0)*(f1*ts_delay(s,1) + (1-f1)*(f2*ts_delay(s,2) + (1-f2)*(f3*ts_delay(s,3) + (1-f3)*ts_delay(s,4)))))` with `s` NaN-to-0 first | Cuts TVR up to ~5x but uses a stale signal: best on slow or blended signals. Test: R_RIG_weekly |
| 5 | Longer windows (5 -> 10 days) | change the ts_mean windows | U_PRICE2_w10: TVR .998 -> .848, IR .093 -> .080, corr .704 -> .610 |
| 6 | Plain smoothing ts_mean(x, 3) | `ts_mean(s, 3)` | T_LATE_s3_w2: IR .075 -> .061 (costly) |

## Route B: lower the correlation to the blocking alpha (needed when the TVR route is hopeless)
| Technique | Evidence |
|---|---|
| Change horizon (5 -> 10/20-day inputs) | w10: corr -.09 |
| Size + volatility neutral: `cs_factorneut(x, [cs_rank(at_signlog(mktcap)), cs_rank(ts_std(ret1, 20))])` | 2-signal price blend: corr .753 -> .704, IR flat. P_VWAPT alone: corr .78 -> .61 but IR .083 -> .051 |
| Gate to a subset (volume shock, volatility, trade size, liquidity) | VWAPV gates gave different blockers (.70 vs .78) |
| Blend with a partner unrelated to the blocker: corr ~ c / sqrt(1 + w^2) | 0.78 -> .47 needs w ~ 1.3 with an independent partner |
| Sub-industry neutral | ineffective on BL1 (.72 -> .715); `subindustry` counts as a variable |

## Route C: raise IR (for "ir_below_threshold" at .060-.072)
1. Multi-horizon ensemble: average of the 5-, 10- and 20-day versions (diversifies horizon noise).
2. Winsorize or rank the inputs: `cs_winsor(x, 0.05, False)`.
3. Condition on the regime where the effect is stronger: volume shock, high VIX (Nagel 2012), high volatility.
4. Combine two near-misses whose daily PnL correlate < .4 (check with `PX.pair`, predict with `PX.blend`).
5. Trade only the conviction tails: `cs_remove_middle(x, 0.6)`.

## Route D: regime gate learned from the alpha's OWN past returns (no hard-coded dates)
Idea (Abhinav): compute the alpha every day, but stand aside after it has been losing, and re-enter once its record
recovers; the alpha recognises a crash from its own returns instead of being told when crashes happened.
Theory: a stop rule only helps if strategy returns run in streaks (Kaminski & Lo, Journal of Financial Markets
2014; factor momentum in Gupta & Kelly 2019). Our reversal alphas have 10-day block autocorrelation of only .03-.08,
so most rules HURT them; test before queueing.
1. Pre-screen with `PX.gate(tag, rule)` (rules mom20, mom60, mom120, stop10re5) on the parent's real PnL. Keep a rule
   only if IR improves in BOTH halves of the sample. Oct 6 replay results:
   - P_VWAPT mom60 .083 -> .093 (both halves up); S_VWAPT_rnd_iss_gpa mom60 .096 -> .101 (both up);
     Q_ACCR_AG stop10re5 .067 -> .074 and mom20 .067 -> .076 (both up).
   - Hurt: stop10re5 on every reversal alpha (e.g. U_PRICE2_szvo .093 -> .072); mom20 on most reversal alphas.
2. In-code implementation (adds only `ret1` and `close` as variables):
   `s = <parent alpha>`; `z = at_nan2zero(cs_zscore(s))`; `one = close/close`;
   `x = at_nan2zero(ts_delay(z, 1)*ret1)`; `p = x - cs_indneut(x, one)` (cross-sectional mean = shadow return);
   `on = ts_sum(p, 60) > 0` (or `1 - (ts_sum(p, 10) < 0)*(ts_sum(p, 5) < 0)`); `alpha = at_zero2nan(at_nan2zero(s)*on)`.
   Queued Oct 6: G_VWAPT_mom60, G_RIG_mom60, G_ACCR_mom20, G_ACCR_stop10. The `cs_indneut(x, one)` trick is unproven
   on the portal; check these runs first.
3. Per-day scaling has no effect on the portal (each day is re-scaled to $1M), so a gate can only be on/off
   (NaN = no positions), not a size dial.
4. Never gate on calendar dates or known crisis periods: that is look-ahead and will fail out of sample (2022+).

## Portal facts that break repairs
- Slow lookback maximum is 300 days ("Lookback cannot exceed 300").
- `bool - bool` crashes the simulation at the loading stage: cast flags with `1.0*(...)` before subtracting.

## Guardrails (multiple-testing discipline)
- Each repair keeps the parent's `# Thesis:` and `# Source:` lines and adds `# Repair: <technique> (<source>). Parent <tag> IR .., TVR .., corr .. to #...`.
- At most 2 techniques stacked per variant, and at most 4 variants per parent per cycle. A parent that fails 8 repairs is retired.
- Prefer repairs that also keep OOS1 (2017-21) >= half of the IS IR, and recency IR >= .04.
- Check self-correlation with our submissions (`PX.own(tag)` after the run; `PX.blend` before queueing a blend).
- Log every outcome in `knowledge/repairs.md`, so the next cycle picks techniques by measured success.
- Slow lookback must cover the longest window + delay (+ ~70 days for ts_fill). Set `lb` and `wlb` (<= 300).
