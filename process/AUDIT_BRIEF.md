# Brief: audit one bioSkills Skill

You are the **auditor** for ONE Skill. A different agent will later fix it, or it will be promoted as
it stands, so your job is to grade it honestly. You never fix it, and you have no stake in it passing.
Your dispatch names the Skill, its source path and commit, the env and its `TOOLS.md`.

## Two facts

- **Skill ID is the SKILL.md frontmatter `name`, not the folder name.** Every report, audit folder
  and `--skill` argument depends on it.
- **Upstream provenance.** `GPTomics/bioSkills` at `d91ed3d` (MIT) is the base, and the read-only
  clone is `F:\OpenScience\external\GPTomics__bioSkills`. Diff against it to see what the original
  said.

## Read first

- `F:\optimizing-agent-science-skills\process\THRESHOLD.md` — the two gates every audit is held to.
- `F:\OpenScience\skills\skill-auditor\SKILL.md` and every file in its `references/` — the audit
  method. Follow it exactly: Skill Veto → 25-criteria static score → classification and execution
  mode → N inputs by the complexity rule → execution → Layer 1/2/3 scoring → Research Veto → final
  score, grade, floors and P0/P1/P2 recommendations.
- The previous round found upstream audits that were templated ("Test case N", identical totals
  across ~100 Skills) and backfilled summaries that quoted the Skill's own description. Those were
  rejected as evidence. Yours must be the opposite: inputs written for this Skill's real use,
  outputs you actually produced, scores you can defend line by line.

## Working limits

- **Do not spawn sub-agents.** One auditor, one Skill, one context.
- **Open P1 findings do not block deployability.** Open P0s and fired vetoes do. Say so in the
  report rather than hedging.

## Your environment is built before you start (2026-09-16)

A **tooling agent** runs first, one per folder, and leaves `F:\OpenScience\audit-envs\<env>\TOOLS.md`:
every package and CLI the folder's Skills reference, the venv or library each one lives in, its smoke
test, what is blocked and why, cached model weights and reference data, and a "Notes for auditors"
section. **Read it before writing any code.** Audits run after a tooling pass executed 66/67 and 51/53
inputs; one run before the practice existed spent five passes discovering its tools mid-audit.

If something you need is genuinely missing, take the env's install lock (`mkdir ...\install.lock`),
install without changing any existing package's version, verify with an import or `packageVersion()`
that prints, and `rmdir` the lock — then add it to `TOOLS.md`.

## Judge a run by its output, never by its exit code (2026-09-16)

Five tools on this machine have now exited 0 while producing nothing or producing garbage: Philosopher
`peptideprophet` and `filter`, both powsimR installs, openbabel `--gen3D` (all-zero coordinates from an
empty data dir), and a Skill's own Scrublet loop that scored a view and silently discarded the result.
**A snippet that "ran" without printing a checked result has not been shown to work.** Assert on the
content of the output — a count, a value against ground truth, a file that exists and parses — and
record that assertion in the report.

## Re-auditing a fixed Skill (2026-09-15)

Failing Skills are fixed in Sam's fork (`F:\optimizing-agent-science-skills\process\FIX_BRIEF.md`).
When your dispatch names a fixed Skill:

- Read the Skill from the fork path and commit in your dispatch, not from `GPTomics__bioSkills`.
  `"source"` becomes `"mrsonord2240/bioSkills@<commit>:<folder>/<skill>"`.
- The pre-fix report is archived under `F:\OpenScience\audits\_pre-fix-<date>\<skill-id>\`, and your
  dispatch names the date. Re-run its inputs as regression tests, and add at least two new inputs of
  your own so the score does not only measure the defects the fixer was told about. The fix log
  (`F:\optimizing-agent-science-skills\fixes\<skill-id>.md`) says what changed; it is not evidence
  — only your runs are.
- Write the new report into `F:\OpenScience\audits\<skill-id>\` as for a first audit. Never file a
  copy of a final report as `_pre-fix-<date>b`: the publisher then refuses, saying it audits the
  same commit as the audit it supersedes.

## Audit the Skill

Skills live under `F:\OpenScience\external\GPTomics__bioSkills\<folder>\<skill>\` (`SKILL.md`, usually
`usage-guide.md` and `examples/`). A folder under `F:\OpenScience\audits\` that holds a finished
`eval_report_*_result.json` is a complete audit.

Before you start, claim the Skill: `mkdir F:\OpenScience\audits\<skill-id>`. `mkdir` is atomic. If it
fails, another auditor owns the Skill: stop and say so. Skip the claim if the folder exists and holds
no report — the orchestrator may have made it.

- Inputs: N by the skill-auditor complexity rule, each a realistic request a researcher would send
  with this Skill loaded. Where the Skill analyses data, create a small synthetic dataset for the
  canonical input under `F:\OpenScience\audits\<skill-id>\data\` and say it is synthetic.
- Execution: most bioSkills Skills are Mode A (the agent writes code by following the Skill's
  patterns). Produce the code and output as the Skill directs. **Run the generated code when you
  can.** Python: the env's venv at `F:\OpenScience\audit-envs\<env>\`, created from
  `F:\OpenScience\runtime\envs\.p\python.exe` (Python 3.12, the Open Science runtime's own
  interpreter); `pip install` what the code needs. R: `F:\OpenScience\runtime\envs\.r\Scripts\Rscript.exe`
  with the private library at `F:\OpenScience\audit-envs\<env>\R-lib`, **but never invoke it bare — it
  exits 0 and prints nothing when R's DLLs are not on `PATH`.** Verified 2026-09-17: both
  `Scripts\Rscript.exe` and `lib\R\bin\Rscript.exe` work with `.r/Library/bin` and
  `.r/Library/mingw-w64/bin` prepended, and both silently produce no output without them. Use the
  env's `r.sh` wrapper for every R call; see
  `F:\OpenScience\audit-envs\mendelian-randomization-analyst\r.sh`, which also pins Rtools 4.4 so
  source packages can compile. This is the exit-code trap below, in the one tool you will use most.
  Take the time installs need; there is no deadline. Linux-only tools (MAFFT, IQ-TREE, MAGeCK,
  QIIME 2, Kraken 2, GATK…) run in the WSL `science` seat, documented in
  `process/TOOLING_BRIEF.md`; only if `TOOLS.md` says a tool cannot run anywhere, check the commands
  against the tool's documented flags in the Skill and say plainly that they were not executed.
- For every input record `executed: true|false` and, if false, why. Never describe code as having
  run when it did not. An output whose code was not executed may still score well if inspection
  finds it correct, but the Research Veto M4 (code usability) needs positive evidence: syntax that
  parses, imports that exist, flags that exist in the documented tool version.
- Check shipped-means-present: every file the `SKILL.md` or `usage-guide.md` points at must exist. A
  missing primary file is a P0.
- Check research scope: anything that diagnoses, prescribes, or triages an individual is a Practice
  Boundaries (M2) failure.

Write, into `F:\OpenScience\audits\<skill-id>\`:

- `eval_report_<skill-id>_result.json` — exactly the schema in
  `skill-auditor/references/report_json_schema.md` (`final.score`, `final.grade`,
  `final.deployable`, `final.veto_override`, `veto_gates`, `dynamic_score.inputs[]`,
  `recommendations[]` with `priority`). Add `"source": "GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:<folder>/<skill>"`
  and per input `"executed": true|false` plus `"execution_note"` inside `meta`/each input.
  `meta.evaluated_on` = the date you run the audit.
- `run\` — every script you ran, saved as a file (`.py`, `.R`, `.sh`), including the ones that are
  one CLI or `docker run` invocation. The publisher copies this folder into the record; commands that
  only ever existed in a tool call publish as nothing, and two audits on 2026-09-16 published zero
  scripts that way.
- `eval_viewer_<skill-id>.md` — the Step 7 viewer, including the generated code, what ran, and
  what it printed (trim long output, keep what the scores depend on).

**Never write anything inside `F:\OpenScience\external\`** — the clones must stay byte-identical to
their upstream commits. This includes what your interpreter writes for you: importing a Skill's
`examples/` module leaves a `__pycache__` beside it, and `.pyc` files are gitignored, so **`git status`
in the clone reads clean while byte-identity is broken**. Check the filesystem
(`find <clone> -name __pycache__`), not git status, and run every script from your own
`F:\OpenScience\audits\<skill-id>\run\` with the Skill's folder copied, not imported in place.

## Rules

- Windows: edit files with the Write/Edit tools or Python with `encoding='utf-8'`; never
  round-trip text through PowerShell `Get-Content`/`Out-File`. Prefix Python with
  `PYTHONIOENCODING=utf-8` in Bash. Keep paths short: Windows fails past 260 characters.
- Do not touch `F:\OpenScience\skills`, `F:\OpenScience\external`, or another agent's audit folder.
- No network calls to paid or authenticated services. Public downloads for pip/CRAN/Bioconductor
  are fine.
- **The publisher copies everything under `run\`**, third-party packages included (leidenalg and
  scikit-misc reached the public repo this way). Install test libraries outside your audit folder.
- **Never kill a process by image name** (`taskkill /IM Rscript.exe` killed three unrelated runs). Kill
  by the PID you started.
- Python on Windows cannot read MSYS `/f/...` paths: use `F:\...`. Read reports with `python -X utf8`.

## Final message (≤ 80 words)

Final score, grade, deployable, executed k/N, veto, top P0/P1.
