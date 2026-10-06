# Starting a new chat (cloud or desktop) on this project

Who does what (since Oct 6 evening): the CLOUD master researches; the LAPTOP operator (Claude Desktop + Claude in
Chrome) is the only one that touches the runner. Shared branch: `claude/focused-fermat-5fdhyo`.
Details: `handoff/MEMORY.md` (LATEST) and `handoff/OPERATOR.md`.

## Laptop operator (Claude Desktop, Sonnet, opened in the repo folder)
First message (rebuilds the runner if needed):
> You are the TrexQuant Operator. First load the Claude in Chrome tools and list connected browsers; use only the Windows Chrome (if the tools are missing, tell me to type /chrome). Then run `git fetch origin && git checkout claude/focused-fermat-5fdhyo && git pull`, read CLAUDE.md and handoff/OPERATOR.md, do "First visit only", then "Every visit".

Then start the automatic loop:
> /loop 30m Operator visit: git pull, then follow handoff/OPERATOR.md "Every visit"

## Any other chat (research / questions)
> This is the TrexQuant Alpha Factory. Clone or pull github.com/abhinavteja2005/trexquant-alpha-research, branch claude/focused-fermat-5fdhyo, and read, in order: CLAUDE.md (hard rules, including NO DELETIONS), handoff/MEMORY.md (LATEST section), reports/status.md (who owns the runner), reports/RESEARCH_REPORT.md (story so far), alphas/registry.md (every alpha and its status). Do not touch Chrome unless you are the laptop operator. Then tell me in 5 lines where things stand.

Where everything lives:
- Rules: `CLAUDE.md`. State and next steps: `handoff/MEMORY.md`. Loop program: `handoff/AUTORESEARCHER.md`. Operator: `handoff/OPERATOR.md`.
- Every alpha: `alphas/registry.md` / `.csv`. Repairs: `knowledge/repairs.md`. Lessons: `knowledge/lessons.md`.
- Ideas: `ideas/backlog.md`, `ideas/cards-oct6-new-families.md`. Playbook: `knowledge/repair-playbook.md`. Research survey: `knowledge/autoresearch-survey.md`.
- Interview narrative: `reports/RESEARCH_REPORT.md`. Runner code: `runner/runner.js`; helpers: `runner/px.js`.
