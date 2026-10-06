# Critic review: c2-newfam.json (Oct 6)

| tag | verdict | reason | exact fix |
|---|---|---|---|
| MM1_TOXREV | FIX | \|IR_lh\| is roughly \|r\|/sigma, so `smooth` mostly ranks move size: the code FOLLOWS the biggest last-hour moves, where reversal is strongest, so expect negative IR | `sz = cs_rank(ts_mean(abs(return_last_hour), 5))`; `smooth = cs_rank(cs_rank(ts_mean(abs(information_ratio_last_hour), 5)) - sz)` |
| MM2_SIZEREV | FIX | the 20-day trade-size ratio is a fixed stock trait (closing-auction/index intensity), not who made this week's move | `q = (volume_last_hour/number_of_trades_last_hour)/(volume_first_hour/number_of_trades_first_hour)`; `size = cs_rank(ts_mean(q, 5)/ts_mean(q, 60))`; lb 80 |
| MM3_CLOSEPRESS | KEEP | sign, dtype and lb are correct; same gated last-hour fade as T_LATE_w3, so watch the correlation | - |
| MR1_RESREV | DROP | after industry neutralisation it is mostly raw reversal, i.e. VP_RESREV_VIX (IR .02, corr .83); code and lb 200 (needs 180) are fine if run as the card's one test | - |
| MR2_MORNANCH | DROP | same `smooth` flaw as MM1, and its base contains the last-hour return, so it is a near-duplicate of MM1 | - |
| MO1_RESMOM | KEEP | correct; flat 250-day windows fit lb 300; expect IR .02-.04, so use it as a partner | - |
| MO2_FROG2 | FIX | the uncentred product mostly holds a plain low-ID tilt and buys continuous losers (wrong per Da et al.); PRET should skip the last month | `pret = ts_delay(close, 20)/ts_delay(close, 250) - 1`; `alpha = (cs_rank(pret) - 1.5) * (2 - cs_rank(sgn*(neg - pos)))` |
| MO3_VOLMOM | FIX | the uncentred product mostly holds a low-turnover tilt (BAB-like, dead in-sample) | `alpha = (cs_rank(mom) - 1.5) * (2.5 - turn)` |

## Notes (detail behind the rows)
- Static checker: all 8 pass (dtype, variables at most 5, windows in the allowed set). No look-ahead found: every input is known at the delay-0 close.
- MM1: `information_ratio_last_hour` = mean/std of the intra-hour returns, which is proportional to |R|/sigma. So `r*(smooth - 1.5)` is roughly r*|r|. The fix ranks |IR| net of the |r| rank, so for a given move size it picks the low-noise path. The fade leg of the current code overlaps T_LATE_w3's "volatile close" gate.
- MM2: the fix keeps the close/open ratio, so it is split-immune, and measures it over the same 5 days as the move against its own 60-day norm. Caveat: close-hour trade-size spikes are large closing auctions, which MM3 fades and MM2 follows. If both sims run, one sign will be wrong.
- MM3: the 0/1 gate adds turnover (cf. banding, TVR 1.93). Check its correlation to T_LATE_w3 and #570604 (LATEVOL .527).
- MR1: the 5-day residual t-stat moves weight toward low-vol names, where daily reversal is weakest. Its only real difference from VP_RESREV_VIX is the vol scaling.
- MR2: revisit only if the fixed MM1 shows that the interaction pays, and then use MM1's decoupled `smooth`. The plain `-dev` version is the crowded VWAP-gap family.
- MO1: the residual-vol formula sigma*sqrt(1 - rho^2) is exact for that beta. Momentum was weak in 2008-21 (Q_52WH -.02).
- MO2/MO3 math: with m = rank - 1.5 and d = ID rank - 1.5, `(m + 1.5)(0.5 - d)` = 0.5m - md - 1.5d + const. The low-ID tilt (sd .43) is 3x the momentum term (sd .14), and continuous losers score 1 against 0 for discrete losers. MO3: `(m + 1.5)(1 - u)` puts sd .43 on low turnover against .29 on momentum. Centring fixes both. MO3's `mom` (R12 - R1 = R(12-1)*(1 + R1)) is acceptable.
- Lookbacks: MM1/MR2 need 5 (lb 60); MM2 needs 20, or 60 after the fix (lb 80); MM3 60 (lb 80); MR1 180 (lb 200); MO1 250, MO2 251, MO3 251 (lb 300). All fit.
