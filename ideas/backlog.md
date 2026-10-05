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
