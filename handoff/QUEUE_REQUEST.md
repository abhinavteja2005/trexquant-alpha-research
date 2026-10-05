# Queue request from the local master (Oct 5, ~23:55 IST)

The local master (Claude Code on the laptop) cannot reach the shared runner tab: Claude in Chrome only
controls tabs in its own group, and window.R keeps jobs in memory, so writing localStorage from
another tab would be overwritten. Whoever drives the runner: please add these jobs to the SAME window.R.

    // paste the JSON array from alphas/queue/next.json as LIST
    window.R.add(LIST)

- alphas/queue/next.json: 39 jobs, all pass tools/check_alpha.py.
  - 14 cycle-1 non-reversal alphas (vol-of-vol, coskewness, VIX-gated residual reversal, variance-ratio
    regime, range-vs-close vol, downside beta, trade size, MAX): state 'squeued', explicit lb (60-520).
  - 25 A101 translations: state 'queued' (Fast IR screen only; runner promotes if it qualifies).
- Expressions live in alphas/drafts/c1.json and a101.json; tools/ledger_sync.py joins runner metrics by tag.
- Do not change R.cfg, promoteOk or submitOk. Delete this file once the jobs are added.
