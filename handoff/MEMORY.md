# Handoff from the retired master chat (Oct 5, 21:20 IST)

## State at handoff
- Submitted: 0. Runner v3 is live in the user's Chrome tab, with ~20 queued and ~18 Fast-done.
- Every promising candidate so far FAILED in Slow mode:
  - c3_rnd_earn: Fast IR .094, pool corr .56, eligible -> Slow IR .082, corr .688, not eligible.
  - VWAPV_rnd_sbc_w2: Fast IR .078, pool corr .476 -> Slow IR .052 (Slow lookback 140).

## FIRST PRIORITY
Diagnose why Fast and Slow disagree before testing many more blends:
1. Run the same blend in Slow at lookback 140 and at 300.
2. Run a price-only alpha in Fast and in Slow as a control, e.g. the last-hour reversal composite.
3. Run one ts_fill fundamental alone in Fast and in Slow.

If fundamentals or ts_fill are unreliable in Slow, focus on price/intraday alphas or use a longer lookback. Lower nothing in the auto-submit rule.

## Key facts
- Pool = all participants' submissions. Plain short-term reversal is crowded (0.5-0.85 corr).
- Daily IR comes mostly from short-term reversal (intraday composite c_intra: Fast IR .090, corr .649). Fundamentals alone have IR < .045 but very low turnover.
- Fast-only recipe: reversal base + 2 slow companions (z-scored, at_nan2zero). Unproven in Slow.
- cs_factorneut against ret1/ret5 removes all signal. Heavy smoothing kills the IR. Industry-level signals are cancelled by the industry-neutral setting (use subindustry).
- Portal: >= 2 s between simulation requests; one simulation at a time (extras stay "created" forever); 100-submission cap; Slow runs take 4-45 min.
- Chrome freezes a hidden tab. The runner self-drives only while its window is at least partly visible. Otherwise explicit window.R.tick() calls push it (sync XHR works in a frozen tab).
- The cloud-session credit was NOT drawn by the earlier claude.ai chat. Verify the meter moves for claude.ai/code sessions.
- Auto-submit approved by the user (keyword HUMAN is automatic in competition mode).
- Design doc (background): https://claude.ai/code/artifact/e626cbcb-b666-4636-a3fb-55debe016e9d
