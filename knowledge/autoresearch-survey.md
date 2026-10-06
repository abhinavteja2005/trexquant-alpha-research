# AI alpha auto-researchers: what exists and what we copy (Oct 6)

| System | Shape | Key mechanism we can copy cheaply | Source |
|---|---|---|---|
| Man Group AlphaGPT (2025, production) | 3-agent research pod: Idea person -> Implementer (writes Python on the internal research stack) -> Evaluator (significance, risk, economic sense), plus an orchestrator | Same acceptance thresholds as human research; a consistency check that the code implements the stated idea; full logging; humans review hypotheses and code | https://www.man.com/insights/what-ai-can-do-for-alpha ; https://www.ai-street.co/p/man-group-details-its-alphagpt ; https://www.bloomberg.com/news/articles/2025-07-10/man-group-says-agentic-ai-is-now-devising-quant-trading-signals |
| Alpha-GPT (2023) | Human-AI interactive: ideation -> implementation (LLM + search enhancement) -> review of backtest summaries | Human gives direction in plain words; the LLM expands it into many formula variants; results summarised back for the next round | https://arxiv.org/html/2308.00016v2 |
| AlphaAgent (KDD 2025) | Idea / Factor / Eval agents in a closed loop | Three regularisers: originality (largest common AST subtree vs existing alphas), hypothesis-factor alignment (LLM-judged), complexity penalty (expression length, parameter count). Aimed at alpha decay and crowding | https://arxiv.org/abs/2502.16789 |
| RD-Agent(Q), Microsoft (2025) | Research (hypothesis synthesis) / Development (code agent with a knowledge base of task-code-feedback triples) / Feedback | Thompson-sampling bandit chooses what to work on next; dedup of new factors by IC correlation >= .99; reports < $10 per full R&D run | https://arxiv.org/abs/2505.15155 ; https://github.com/microsoft/RD-Agent |
| Alpha Jungle (2025) | LLM inside Monte Carlo tree search over formulas | Backtest metrics guide which branch to refine; frequent-subtree avoidance stops the search collapsing onto one formula family | https://arxiv.org/abs/2505.11122 |
| QuantaAlpha (2026) | Evolutionary: mutation + crossover of whole research trajectories | Localise the weak step of a near-miss and fix only that; recombine good parts of two parents; constrain complexity and redundancy | https://arxiv.org/abs/2602.07085 |
| wq-alpha-research (GitHub skill for WorldQuant BRAIN, the closest analogue to Trexsim) | A SKILL.md playbook + batch submit script + `evolve_skill.py` that turns results into lessons | Self-correlation measured on DAILY PnL against already-submitted alphas before submitting; lessons file grows from results; fundamentals + sub-industry neutral as default baseline | https://github.com/QuantML-Research/wq-alpha-research |
| Karpathy autoresearch | One editable file, a fixed evaluation harness, keep/discard on one metric, a TSV log, never stop to ask | Our runner is the fixed harness; the ledger is the TSV; keep = eligible; simpler beats complex at equal score | https://github.com/karpathy/autoresearch/blob/master/program.md |
| Kakushadze, How to Combine a Billion Alphas | Theory of combining many weak, low-correlated alphas | Weak signals combined with low mutual correlation beat one strong crowded one | https://arxiv.org/abs/1603.05937 |

## What this means for us (cost-aware)
- Our bottleneck is the simulator (one Slow run at a time, 5-25 min, so ~60-100 per day), not ideas. LLM calls should be batched: one cycle writes 15-25 drafts, i.e. ~3-5 cycles a day. Polling is done by scripts, not by the LLM.
- Do the cheap, deterministic work in Python or in-page JS before spending LLM tokens or simulator time:
  1. Originality check (AlphaAgent / Alpha Jungle): reject drafts sharing most of their structure with tested or submitted alphas.
  2. Daily-PnL correlation pre-screen (wq skill, RD-Agent dedup): estimate a blend's IR and its correlation with OUR submissions from component PnLs before simulating it.
  3. Bandit over families (RD-Agent): give simulator slots to families with the best posterior hit rate, while still exploring.
  4. Mutation and crossover of near-misses (QuantaAlpha): `tools/mutate.py`.
- Spend LLM tokens on what only an LLM does well: new hypotheses with sources (Scout), thesis-to-code (Writer), and a skeptical alignment and look-ahead review (Critic), as in AlphaGPT and AlphaAgent.
