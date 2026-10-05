# Idea backlog (attach a real, opened source URL when an idea is queued)

Status: idea | queued | tested-pass | tested-fail | dropped

## Reversal bases
- INTRA: last-hour composite (return, range position, VWAP gap). Taken alone (corr .649). queued in blends
- VWAPV: VWAP gap where volume is elevated. Best Fast blend (corr .476), but failed in Slow
- RETL (last-hour return): queued. OVN, D3, RANGE: tested-fail (Fast IR .060-.067)

## Slow companions
- rnd (R&D/mktcap), sbc (stock-based pay/mktcap), fcf (FCF yield), gpa (gross profitability), iss (net issuance). Reliability in Slow is unknown; diagnose first.
- earn: dropped (possible look-ahead)

## To research
- 101 Formulaic Alphas (https://arxiv.org/pdf/1601.00991): translate the OHLCV/vwap ones (vwap -> vwap_last_hour)
- Overnight vs intraday tug of war (Lou, Polk & Skouras 2019): queued as TUGOFWAR
- Sub-industry lead-lag momentum: queued as SUBIND_MOM
- Intraday volatility, skew, trade-size and information-ratio variables: mostly untested
- Volume-spike conditioned drift (a post-earnings-drift proxy without the earnings-date variable)
- Value composites from the ratio group (earnings_yield, ev_to_t12m_ebit, price_to_book_ratio)

## Oct 5 late: price/intraday-only batch (queued at the front, tag prefix P_)
Insider-trading data does not exist on Trexsim; the closest public proxies are issuance (shsout) and stock-based pay, already used as companions.
- P_CI_s3, P_CI_volcond, P_CI_lowvol: INTRA composite smoothed / volume-conditioned / calm stocks only (Bogousslavsky & Muravyev 2023; Nagel 2012)
- P_VWAPV_s3, P_VWAPV_sub, P_VWAPV_illiq, P_VWAPT: VWAP-gap reversal variants (Campbell-Grossman-Wang 1993; Amihud 2002)
- P_RETL_small: last-hour reversal in small-trade (retail-like) stocks (Barber, Odean & Zhu 2009)
- P_RANGE_volcond: last-hour range position on heavy volume
- P_A101: Alpha #101 (Kakushadze 2016, https://arxiv.org/abs/1601.00991)
- P_FIRST_LAST: long first-hour, short last-hour return (Gao, Han, Li & Zhou 2018)
Plan: anything with Fast IR >= .078 and corr <= .55 auto-promotes to Slow (no ts_fill, so short lookback and quick Slow runs).

## Oct 5 22:05: volatility batch (tag prefix V_, queued after P_)
No single-stock implied vol on Trexsim; VIX (close_vix, ret1_vix) and realized-vol inputs exist.
- V_RSJ: signed jump variation, short good-vol (Bollerslev, Li & Zhao, JFQA 2020)
- V_RSKEW: intraday realized skewness (Amaya, Christoffersen, Jacobs & Vasquez, JFE 2015)
- V_VIXBETA: aggregate-volatility (VIX) beta (Ang, Hodrick, Xing & Zhang, JF 2006)
- V_VOLSHOCK: 5d/60d realized variance spike
- V_LATEVOL_REV: last-hour reversal where the close is more volatile than the open
Slow-ish signals (VIXBETA, RSKEW, RSJ) are candidate blend partners for the reversal base if their PnL is uncorrelated.

## Cycle 1 (local master): vol-premium and regime proxies
Format: name | thesis | source URL | variables | horizon | sign | why uncrowded. Drafts in `alphas/drafts/c1.json` (base C1). Not duplicating V_RSJ/V_RSKEW/V_VIXBETA/V_VOLSHOCK/V_LATEVOL_REV.
- VP_VOLOFVOL | uncertainty about risk (vol of rolling vol) is priced: high vol-of-vol underperforms (~8%/yr) | https://ideas.repec.org/a/cup/jfinqa/v53y2018i04p1615-1651_00.html | ret1; std_dev_return_first/last_hour | weeks-months | short high vov | second moment of vol, not a return signal; intraday variant uses untested hour-std data
- VP_COSKEW | stocks that rise when the market makes big moves (long-gamma-like, positive coskewness) are overpriced; skew premium ~3.6%/yr | https://people.duke.edu/~charvey/Research/Published_Papers/P56_Conditional_skewness_in.pdf | ret1, ret1_spx | months | long negative coskew | ts_corr_binary(ret1, ret1_spx^2) is a slow risk tilt with no reversal content
- VP_RESREV_VIX | reversal = liquidity provision, whose return rises with VIX (Nagel 2012); apply to beta-residual returns and tilt toward high idio-vol names only in high-VIX regimes | https://econpapers.repec.org/RePEc:oup:rfinst:v:25:y:2012:i:7:p:2005-2039 | ret1, ret1_spx, close_vix | 3 days | fade residual | VIX changes the cross-sectional weights (not the book scale); residual 3d is less crowded than raw 1-5d. Critic: highest risk of pool corr in this batch
- REG_VARRATIO | Lo-MacKinlay variance ratio (var(ret5)/5var(ret1)) labels each stock trending vs mean-reverting: momentum in high-VR, reversal in low-VR, NaN in between | https://www.nber.org/papers/w2168 | ret1, ret5, ret10 | 5-10 days | sign flips by regime | sign-flipping by regime decorrelates from plain reversal (half the book is momentum)
- REG_RANGECC | Parkinson range variance (log(high/low)^2/4ln2) above close-to-close variance means intraday noise that reverts; reverse only those names | https://www.nber.org/papers/w2168 | high, low, ret1, ret5 | 5 days | fade, gated | gate keeps ~half the universe; range/close-vol ratio not used elsewhere
- REG_DOWNBETA | downside beta (comovement on market down days) earns ~6%/yr; asymmetry (down minus up corr) or excess downside beta | https://www.nber.org/papers/w11824 | ret1, ret1_spx | months | long downside beta | slow risk premium, candidate blend companion, unrelated to reversal
- ID_TRADESIZE | small-trade (retail) favored stocks underperform for months; proxy with falling average trade size and small-trade-weighted first-hour returns | https://econpapers.repec.org/article/ouprfinst/v_3a21_3ay_3a2008_3ai_3a3_3ap_3a1123-1151.htm | volume_first/last_hour, number_of_trades_first/last_hour, return_first_hour | weeks | short retail-favored | trade-count data barely used by the pool
- ANOM_MAX | lottery demand: max daily return over the past month predicts low returns (>1%/month spread); vol-adjusted variant separates spikes from plain vol | https://pages.stern.nyu.edu/~rwhitela/papers/max%20jfe11.pdf | ret1 | month | short high MAX | sourced anomaly, not in backlog; 52-week-high card skipped (source page not openable)

## Oct 5 23:55: Slow-only round 2 (queued, lb 300)
- S_COMP5_slow: rnd+sbc+iss+fcf+gpa composite alone (low TVR; tests IR/sqrtTVR route)
- S_CI_sbc_iss_fcf_w2: INTRA composite base + sbc/iss/fcf at 2x (10 vars)
- S_BL1_subind: best blend (IR .090, corr .72) made sub-industry relative
- S_VWAPT_vol_iss: VWAPT + RSJ + VIX beta + issuance at 1.5x (non-fundamental partners)
- S_LATEVOL_sbc_iss_fcf_w2: volatile-close reversal base + sbc/iss/fcf at 2x
