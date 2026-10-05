# Trexsim portal facts (Oct 5, 2026)

Username: dasariveeravenkataabhinavteja

## Competition and scoring
- Group pysim-competition-India-2026_Campus-QR_03, 248 people, 198 with 0 qualified (Oct 5). Top-10 qualified counts: 86, 80, 47, 41, 30, 26, 22, 22, 16, 16.
- Qualify: daily IR > 0.07 AND correlation <= 0.5 to the pool, or IR/sqrt(TVR) >= 1.2x EVERY pool alpha it exceeds 0.5 with.
- POOL = every alpha submitted in this competition BY ANY PARTICIPANT (pool_is_competition: true). The Submit Alpha button is disabled when not eligible.
- Organizer email: quantity (minimum one alpha/day), quality and diversity of logic, documentation "in the comment section". In competition mode the submit dialog auto-fills: name alpha<user>Competition<id>, keywords HUMAN,COMPETITION, description "Competition alpha." So documentation must be # comments inside the alpha code.
- Submission cap: total_os_allowed = 100.
- Portal countdown: Oct 27 14:14 UTC. The user believes submissions may close at the end of this week.
- Auto-submit approved by the user: Slow IR >= 0.072, portal eligible, recency-weighted IR >= 0.04, best-year share <= 0.5.

## API (logged-in tab; token window.CSRF_TOKEN sent as csrfmiddlewaretoken)
- POST /trexsim/pysim/alpha/ (form):
  - post_type=simulate, action=submit (= RUN a sim), alpha_id='', alpha_expression, region_universe=US:TOP1000, neut=industry, delay=0, mode=os_fast|os, lookback, slippage=no, slippage_value=0.1, liq_uni_sim=no -> {status, alpha_id}
  - post_type=get_result, alpha_id -> status created|running|success|failed, simulation_progress
  - post_type=check_submission_validity, alpha_id -> eligible, submission_corr, correlated_alpha_id, corr_ir_tvr, verdict_type (read-only)
  - post_type=get_last_sub_info -> alpha_name, alpha_kw, ..., total_os_allowed
- POST /trexsim/pysim/alphalist/ (form): alpha_submit_production=true, alphaid, alphaname, alphakw, alphades, authorname, username, authoremail (the UI sends values from get_last_sub_info) = competition submission.
- GET /trexsim/pysim/alpha/<id>/?format=json -> metrics + simresdata daily PnL.
- GET /trexsim/pysim/api/data_description_browser/ -> 255 variables.
- LIMITS: >= 2 s between simulate requests. ONE sim per user at a time (extras stay "created" forever).
- Pairwise correlation tool = Pearson correlation of daily PnL over the last 500 days (2020-01-08..2021-12-30).

## Data
- 255 vars: price/volume/returns 16; intraday first/last hour 30 (OHLC, vwap, volume, trades, return, std, skew, IR); 8-K fundamentals 84; ratios 91; calendar/events 18; market/macro 16. Max 10 per alpha.
- In-sample: Fast ~2006-04..2021-12-30; Slow 2007-03-15..2021-12-30. Hidden out-of-sample 2022+.
- Settings fixed: US TOP1000, delay 0, industry neutralization, no slippage.
- Custom operators saved in the portal: delta, decay_linear, ts_argmax, ts_argmin.
