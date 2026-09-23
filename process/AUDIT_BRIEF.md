# Brief: audit one bioSkills Skill

Read `COMMON.md` first. You are the **auditor** for ONE Skill. A different agent will later fix it, or
it will be promoted as it stands, so grade it honestly. You never fix it and have no stake in it
passing. Your dispatch names the Skill, its source path and commit, the env and its `TOOLS.md`.

## Read first

- `COMMON.md` → Thresholds.
- `F:\OpenScience\audit-envs\<env>\TOOLS.md`, **before writing any code**: every tool the folder needs,
  where it lives, what is blocked, and notes for auditors. If something you need is genuinely missing,
  install it under COMMON's install rules.
- `F:\OpenScience\skills\skill-auditor\SKILL.md` and every file in its `references/`: the method. Follow
  it exactly: Skill Veto → 25-criteria static score → classification and execution mode → N inputs by
  the complexity rule → execution → Layer 1/2/3 scoring → Research Veto → final score, grade, floors and
  P0/P1/P2 recommendations.

Upstream audits were found templated ("Test case N", identical totals across ~100 Skills) and
backfilled, and were rejected as evidence. Yours must be the opposite: inputs written for this Skill's
real use, outputs you actually produced, scores you can defend line by line.

## Claim

`mkdir F:\OpenScience\audits\<skill-id>`. If it fails, another auditor owns the Skill: stop and say so.
Skip the claim if the folder exists and holds no report (the orchestrator may have made it). A folder
holding a finished `eval_report_*_result.json` is a complete audit.

## Audit

A first audit reads the Skill from `F:\OpenScience\external\GPTomics__bioSkills\<folder>\<skill>\`
(`SKILL.md`, usually `usage-guide.md` and `examples/`).

- **Inputs:** N by the complexity rule, each a realistic request a researcher would send with this Skill
  loaded. Where the Skill analyses data, build a small synthetic dataset for the canonical input under
  `F:\OpenScience\audits\<skill-id>\data\` and say it is synthetic.
- **Execution:** most bioSkills Skills are Mode A (the agent writes code by following the Skill). Produce
  the code as the Skill directs and **run it**. Take the time installs need; there is no deadline. Only if
  `TOOLS.md` says a tool runs nowhere, check the commands against the tool's documented flags and say
  plainly they were not executed.
- Per input record `executed: true|false` and, if false, why. An unexecuted output may still score well on
  inspection, but Research Veto M4 (code usability) needs positive evidence: syntax that parses, imports
  that exist, flags that exist in the documented tool version.
- **Shipped means present:** every file `SKILL.md` or `usage-guide.md` points at must exist. A missing
  primary file is a P0.
- **Research scope:** anything that diagnoses, prescribes or triages an individual fails Practice
  Boundaries (M2).
- Open P1s do not block deployability; open P0s and fired vetoes do. Say so rather than hedging.

## Re-auditing a fixed Skill

- Read the Skill from the staging path and commit in your dispatch. `"source"` becomes
  `"mrsonord2240/bioSkills@<commit>:<folder>/<skill>"`.
- The pre-fix report is archived under `F:\OpenScience\audits\_pre-fix-<date>\<skill-id>\` (your dispatch
  names the date). Re-run its inputs as regression tests and add at least two new inputs of your own, so
  the score does not only measure the defects the fixer was told about. The fix log
  (`F:\optimizing-agent-science-skills\fixes\<skill-id>.md`) says what changed; only your runs are
  evidence.
- Write the new report into `F:\OpenScience\audits\<skill-id>\` as for a first audit. Never file a copy of
  a final report as `_pre-fix-<date>b`: the publisher refuses it as auditing the same commit it
  supersedes.

## Write, into `F:\OpenScience\audits\<skill-id>\`

- `eval_report_<skill-id>_result.json`: exactly the schema in
  `skill-auditor/references/report_json_schema.md` (`final.score`, `final.grade`, `final.deployable`,
  `final.veto_override`, `veto_gates`, `dynamic_score.inputs[]`, `recommendations[]` with `priority`).
  Add `"source": "GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:<folder>/<skill>"`, and per
  input `"executed"` plus `"execution_note"`. `meta.evaluated_on` = the date you run the audit.
- `run\`: every script you ran. **The publisher copies everything under `run\`**, third-party packages
  included (leidenalg and scikit-misc reached the public repo this way), so install test libraries
  outside your audit folder.
- `eval_viewer_<skill-id>.md`: the Step 7 viewer, with the generated code, what ran and what it printed
  (trim long output, keep what the scores depend on).

## Final message (≤ 80 words)

Final score, grade, deployable, executed k/N, veto, top P0/P1.
