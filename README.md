# Trexquant Alpha Research

My research for the Trexquant Alpha Generation Competition (2026). Alphas were built and tested on the Trexsim portal: US equities, delay 0, industry-neutral, Slow simulations 2006-2021.

**The presentation:** [`reports/deck/deck.pdf`](reports/deck/deck.pdf) has 12 slides covering four thesis-driven alpha families, how each one was built up, and the best alpha in each family.

## Results

| Family | Thesis | Best alpha | IR | Turnover | IR/sqrt(TVR) |
|---|---|---|---|---|---|
| A. Closing-pressure reversal | Late-day, price-insensitive flow pushes the close away from VWAP, and the gap reverts | #708808 | .118 | .62 | .149 |
| B. Gap-down rebound | A close pinned at the low after a gap-down is forced selling, so liquidity providers get paid | #724045 | .129 | .95 | .132 |
| C. Volatile-close reversal | A close noisier than the open signals flow rather than news, so the last-hour move fades | #685104 | .092 | .33 | .161 |
| D. Slow accounting composite | Many weak, slow, low-correlated accounting premia combine into a steady signal | #716550 | .077 | .036 | .407 |

- **IR** is the daily IR (x15.9 gives the annual figure).
- **Correlations:** the four best alphas have pairwise daily-PnL correlations of .06 to .48.
- **Totals:** 403 alphas simulated, 10 submitted.

## Layout

- `alphas/drafts/`: every alpha's code, with its thesis, source and a comment on each line.
- `alphas/registry.csv`: every alpha simulated, with Slow/Fast stats, its status and what blocked it.
- `reports/deck/`: the presentation, its LaTeX source, the chart script, and the portal screenshots and stats behind it.
- `reports/RESEARCH_REPORT.md`: a dated research log.
- `knowledge/`: portal facts, operators, the variable list and lessons learned.
- `tools/check_alpha.py`: a pre-flight checker for look-ahead, variable count, window sizes and dtype rules. Test it with `python tools/test_checker.py`.
- `tools/alpha101.py`, `tools/grid.py`, `tools/sweep.py`: generators for Kakushadze-101 translations, the partner grid search and the field sweep.
- `runner/`: the in-browser job runner used to queue simulations on the portal.
- `tools/export_pnl.js`: a read-only console script that exports alpha PnL and stats from the portal.
