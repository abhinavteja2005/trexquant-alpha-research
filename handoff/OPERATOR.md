# OPERATOR: the laptop Chrome session (Claude Desktop, Sonnet)

The work is split in two (Abhinav, Oct 6):
- **Cloud master** (claude.ai/code session): all research. Scout/Writer/Critic, checks, repairs, queue files,
  registry, reports. It cannot reach Chrome.
- **Operator** (you, Claude Desktop on Abhinav's Windows ASUS laptop, Claude in Chrome): the ONLY hands on the
  Trexsim runner. You move files between the repo and the runner. You do NOT invent, edit or judge alphas.

Branch: `claude/focused-fermat-5fdhyo` (shared with the cloud master). Every visit starts with
`git fetch origin && git checkout claude/focused-fermat-5fdhyo && git pull`.

## Hard rules (also in CLAUDE.md)
- Use only Abhinav's Windows Chrome. If `list_connected_browsers` shows a Mac, it is a friend's: never select it.
- Never delete, withdraw or replace any alpha or submission; never call delete endpoints or click delete controls.
- Never edit `R.cfg`, `R.promoteOk`, `R.submitOk`. Never type credentials. If Trexsim is logged out: STOP, tell Abhinav.
- One runner only. Never reload or navigate the runner tab (titled "RUNNER - do not reload"); browse in another tab.
- JS results: return arrays of short strings (long strings are cut at ~1000 chars; URL-like text is redacted).

## First visit only: rebuild the runner (Plan B)
1. Load the Chrome tools in one ToolSearch call; `list_connected_browsers`; select the Windows browser.
2. Open https://www.trexsim.com/trexsim/pysim/alphalist in your tab group. Confirm you are logged in (else stop).
3. Paste the whole of `runner/runner.js` (from the repo, NOT `localStorage.R3_code`) via the javascript tool, then
   run `RUNNER(); document.title = 'RUNNER - do not reload'; localStorage.R3_owner = 'laptop-operator ' + new Date().toISOString();`
4. Paste the whole of `runner/px.js`. Expect `'PX ready'`.
5. Check `R.counts()` (expect about 13 squeued + 25 queued + 5 submitted) and `R.cur() && R.cur().tag` (expect
   Y_PLsz_ACC_w07, sid 698181, which kept running on the server).
After any later page reload by accident: re-paste runner.js + `RUNNER()` and px.js (jobs survive in localStorage).

## After a pause (laptop closed, slept or restarted) — for Abhinav
Nothing is lost: a simulation already running finishes on Trexsim's servers and the runner collects it on wake.
1. Open the laptop, make sure the Chrome window with the "RUNNER - do not reload" tab is visible.
2. Claude Desktop still open with the loop running: do nothing; the next 30-min visit ticks the runner.
3. Claude Desktop was closed or the laptop restarted: in a Desktop session (Sonnet, repo folder) paste
   `/loop 30m Operator visit: git pull, then follow handoff/OPERATOR.md "Every visit"`.
4. Chrome was closed too (runner tab gone): paste the first-visit message from `handoff/NEW_CHAT_START.md` first;
   it rebuilds the runner from `runner/runner.js` (jobs survive in localStorage), then start the loop (step 3).

## Automatic mode (approved by Abhinav, Oct 6): run yourself every 30 minutes
Speed matters: an alpha that waits in the repo can be taken by another participant. After the first visit, Abhinav
starts `/loop 30m Operator visit: git pull, then follow handoff/OPERATOR.md "Every visit"` so no human is needed.
Keep each visit cheap: after step 1, if `alphas/queue/next.json` and `ops.json` are unchanged since the last line of
`loaded.log` AND no Slow job finished since the last snapshot (compare `R.counts()`), stop there (no commit, one-line reply).

## Runner reload request
If `alphas/queue/ops.json` has `reload_runner`, re-paste `runner/runner.js` from the repo, call `RUNNER()`, re-paste `runner/px.js` (the submit rule needs `window.PX`), and confirm `R.ownMax` exists. Jobs survive in localStorage. Then remove nothing; just note it in loaded.log.
Held jobs: list `R.jobs.filter(j=>j.hold).map(j=>[j.tag,j.sid,j.ownMax].join(' '))` as `HELD <tag> <sid> <maxOwnCorr>` lines in the snapshot and your reply.

## Every visit (about 5 minutes)
1. **Health.** In the runner tab: `[R.counts(), R.cur() && R.cur().tag, Math.round((Date.now()-R.lastTick)/1000), R.lastErr||'']`.
   If seconds since last tick > 90, run `R.tick()`. If `window.R` is missing, do the rebuild above (steps 3-4).
2. **Hand submissions.** Abhinav may submit alphas by hand. In ANOTHER tab, open the portal's submissions view and list
   the submitted alpha IDs. For any job whose `sid` is submitted but whose state is not `submitted`:
   `j.state='submitted'; j.subAt=Date.now(); R.save()`. Write `tag sid` of each change into the snapshot (step 3).
3. **Snapshot.** Run the JS printed by `python tools/ledger_sync.py` (no arguments). Save the returned rows, one per
   line, to `alphas/snapshots/<YYYYMMDD-HHMM>.txt` (IST). If the result is cut off, run it on slices
   (`R.jobs.slice(0,60)`, `slice(60,120)`, ...) by replacing `R.jobs` in the snippet.
   Then run `python tools/ledger_sync.py alphas/snapshots/<file>.txt`.
4. **PX requests.** If `alphas/queue/ops.json` has a `px` list, run each call in the runner tab (paste px.js first if
   `window.PX` is missing) and save `call -> result` lines to `alphas/snapshots/<YYYYMMDD-HHMM>-px.txt`.
5. **Unskips.** For each tag in `ops.json` `unskip` whose state is `skipped`, set `j.state='squeued'` (they go behind the front list). Then:
   **Skips.** For each tag in `ops.json` `skip`: if its state is `queued` or `squeued`, set `j.state='skipped'`; never
   remove a job. Then `R.save()`.
6. **Load the queue.** `alphas/queue/next.json` holds new jobs (already checked by the cloud master). Add them with
   `R.add([...])` in batches of <= 10, pasting the JSON objects unchanged (they carry `state` and `lb`). `R.add`
   ignores tags it already has, so loading the same file twice is harmless. Then `R.save()` and `R.counts()`.
   **Priority:** move the jobs tagged in `ops.json` `front` (in that order) to the front of `R.jobs`, so the runner
   simulates them next: `const F=<front list>; const pick=R.jobs.filter(j=>F.includes(j.tag)).sort((a,b)=>F.indexOf(a.tag)-F.indexOf(b.tag)); R.jobs=pick.concat(R.jobs.filter(j=>!F.includes(j.tag))); R.save()`.
   Reordering only: never remove a job.
6b. **Eligible but not auto-submitted.** `R.jobs.filter(j=>j.s&&j.s.elig&&j.state!=='submitted').map(j=>[j.tag,j.sid,j.s.ir,j.s.corr].join(' '))`.
   Put each as `ELIGIBLE <tag> <sid> <ir> <corr>` at the top of the snapshot file and in your reply, so Abhinav can
   decide quickly whether to submit by hand. Never submit them yourself.
7. **Log and push.** Append one line to `alphas/queue/loaded.log`:
   `<YYYYMMDD-HHMM> | next.json <git short hash of the file> | added <n> | counts <R.counts()>`.
   Commit the snapshot files, `alphas/ledger.md`, `alphas/runner-export.json` and `loaded.log`; push.
8. **Reply in 3 lines:** runner health and counts; jobs finished since last visit (best Slow IR); anything wrong.
9. **Wake the cloud master** (if your SendMessage/ListAgents tools list the cloud session `trexquant-alpha-research-4f`):
   after pushing a snapshot with newly finished Slow jobs or an ELIGIBLE line, send it one line:
   `operator: snapshot <file> pushed; finished <n>; eligible <tags or none>`. It then triages at once instead of
   waiting for its 3-hourly cycle.

Do not do research, write alphas, change tools, or edit any other file. Problems you cannot fix in one step: stop and
say exactly what you saw.
