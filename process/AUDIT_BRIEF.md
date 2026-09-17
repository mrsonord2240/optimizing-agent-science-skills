# Brief: select and audit the Skills for one round-2 Specialist candidate

You are the **auditor** for ONE candidate Specialist. A different agent will later write the
Specialist from your results, so your job is to pick the Skills and grade them honestly. You never
write the Specialist, and you have no stake in any Skill passing.

## Read first

- `F:\optimizing-agent-science-skills\process\CANDIDATES.md` — your candidate's scope, source
  folders and boundaries, and why every candidate uses `GPTomics/bioSkills` only.
- `F:\optimizing-agent-science-skills\process\THRESHOLD.md` — the viability gates. You own the
  evidence for gates 2, 3, 4, 7 and 8.
- `F:\OpenScience\skills\skill-auditor\SKILL.md` and every file in its `references/` — the audit
  method. Follow it exactly: Skill Veto → 25-criteria static score → classification and execution
  mode → N inputs by the complexity rule → execution → Layer 1/2/3 scoring → Research Veto → final
  score, grade, floors and P0/P1/P2 recommendations.
- The previous round found upstream audits that were templated ("Test case N", identical totals
  across ~100 Skills) and backfilled summaries that quoted the Skill's own description. Those were
  rejected as evidence. Yours must be the opposite: inputs written for this Skill's real use,
  outputs you actually produced, scores you can defend line by line.

## Working limits (2026-09-15, revised 2026-09-16)

- **Do not spawn sub-agents.** At most two auditors run on the machine at once, and a fan-out of
  eight made every run crawl.
- **The audit is split across fresh agents (2026-09-16)** so no one context carries ten Skills of run
  output. Your dispatch names your stage; do only that stage, then stop:
  - **select** — Step 1 only. Write `F:\OpenScience\specialist-src\<candidate-id>\SELECTION.md`: the
    chosen Skills in audit order (core first) with role and source folder, the Skills already audited
    that you reuse, and one line for each Skill read but not chosen.
  - **audit `<skill-id>`** — Step 2 for that one Skill. Read `SELECTION.md` for its role. Skip the Step 1 claim `mkdir` if the folder exists and holds no report — the orchestrator may have made it.
  - **verdict** — Step 3 only, from the reports on disk and `SELECTION.md`.
- **Audit the core Skills first** — the ones the Specialist's central step cannot exist without. If
  no core Skill reaches 85, the orchestrator skips the rest and dispatches the verdict stage, which
  writes the not-viable verdict in `AUDIT.md`.
- **Open P1 findings do not block viability.** Open P0s and fired vetoes do. Say so in `AUDIT.md`
  rather than hedging the verdict.

## Your environment is built before you start (2026-09-16)

A **tooling agent** runs first, one per candidate, and leaves
`F:\OpenScience\audit-envs\<candidate-id>\TOOLS.md`: every package and CLI the candidate's Skills
reference, the venv or library each one lives in, its smoke test, what is blocked and why, cached
model weights and reference data, and a "Notes for auditors" section. **Read it before writing any
code.** The two candidates audited this way on 2026-09-16 executed 66/67 and 51/53 inputs; the
candidate audited before the practice existed spent five passes discovering its tools mid-audit.

If something you need is genuinely missing, take the candidate's install lock
(`mkdir ...\install.lock`), install without changing any existing package's version, verify with an
import or `packageVersion()` that prints, and `rmdir` the lock — then add it to `TOOLS.md`.

## Judge a run by its output, never by its exit code (2026-09-16)

Five tools on this machine have now exited 0 while producing nothing or producing garbage:
Philosopher `peptideprophet` and `filter`, both powsimR installs, openbabel `--gen3D` (all-zero
coordinates from an empty data dir), and a Skill's own Scrublet loop that scored a view and silently
discarded the result. **A snippet that "ran" without printing a checked result has not been shown to
work.** Assert on the content of the output — a count, a value against ground truth, a file that
exists and parses — and record that assertion in the report.

## Re-auditing a fixed Skill (2026-09-15)

Failing Skills are being fixed in Sam's fork
(`F:\optimizing-agent-science-skills\process\FIX_BRIEF.md`). When your dispatch names a fixed
Skill:

- Read the Skill from the fork path and commit in your dispatch, not from `GPTomics__bioSkills`.
  `"source"` becomes `"mrsonord2240/bioSkills@<commit>:<folder>/<skill>"`.
- The pre-fix report is archived under `F:\OpenScience\audits\_pre-fix-<date>\<skill-id>\`, and your
  dispatch names the date (2026-09-15 for the first fix round, 2026-09-16 for the second). Re-run its
  inputs as regression tests, and add at least two new inputs of your own so the score does not
  only measure the defects the fixer was told about. The fix log
  (`F:\optimizing-agent-science-skills\fixes\<skill-id>.md`) says what changed; it is not evidence
  — only your runs are.
- Write the new report into `F:\OpenScience\audits\<skill-id>\` as for a first audit.

## Step 1 — choose the Skills (8–14)

A first attempt at this round was cancelled mid-way. Folders under `F:\OpenScience\audits\` that
hold a finished `eval_report_*_result.json` are complete audits: reuse them rather than redo them.

Skills live under `F:\OpenScience\external\GPTomics__bioSkills\<folder>\<skill>\` (`SKILL.md`,
usually `usage-guide.md` and `examples/`). Read the `SKILL.md` of every Skill in your candidate's
folders. Choose the set that gives end-to-end coverage (gate 4): framing/design, the domain's
central operation, and validation or reporting. Prefer fewer, stronger Skills over breadth. Mark
the ones the Specialist cannot exist without as `core`. Write down, for every Skill you read and
did not choose, one line saying why.

Before auditing a Skill, claim it: `mkdir F:\OpenScience\audits\<skill-id>` (the Skill ID is the
frontmatter `name`). `mkdir` is atomic. If it fails, another auditor owns that Skill: do not audit
it; reuse its report when it appears (check back later; if it has not appeared by the time you
finish everything else, note it as pending).

## Step 2 — audit each chosen Skill

- Inputs: N by the skill-auditor complexity rule, each a realistic request a researcher would send
  with this Skill loaded. Where the Skill analyses data, create a small synthetic dataset for the
  canonical input under `F:\OpenScience\audits\<skill-id>\data\` and say it is synthetic.
- Execution: most bioSkills Skills are Mode A (the agent writes code by following the Skill's
  patterns). Produce the code and output as the Skill directs. **Run the generated code when you
  can.** Python: one venv per candidate at `F:\OpenScience\audit-envs\<candidate-id>\` created
  from `F:\OpenScience\runtime\envs\.p\python.exe` (Python 3.12, the Open Science runtime's own
  interpreter); `pip install` what the code needs. R: `F:\OpenScience\runtime\envs\.r\Scripts\Rscript.exe`
  **but never invoke it bare — it exits 0 and prints nothing when R's DLLs are not on `PATH`.**
  Verified 2026-09-17: both `Scripts\Rscript.exe` and `lib\R\bin\Rscript.exe` work with
  `.r/Library/bin` and `.r/Library/mingw-w64/bin` prepended, and both silently produce no output
  without them. Write a wrapper once and use it for every R call — see
  `F:\OpenScience\audit-envs\mendelian-randomization-analyst\r.sh`, which also pins Rtools 4.4 so
  source packages can compile. This is the exit-code trap below, in the one tool you will use most.
  with a private library at `F:\OpenScience\audit-envs\<candidate-id>\R-lib`. Take the time
  installs need; there is no deadline. Only one or two agents run at a time now, so the machine is
  yours. Command-line tools that have no Windows build (MAFFT, IQ-TREE,
  MAGeCK, QIIME 2, Kraken 2, GATK…) will usually not run here: then check the commands against the
  tool's documented flags in the Skill and say plainly that they were not executed.
- For every input record `executed: true|false` and, if false, why. Never describe code as having
  run when it did not. An output whose code was not executed may still score well if inspection
  finds it correct, but the Research Veto M4 (code usability) needs positive evidence: syntax that
  parses, imports that exist, flags that exist in the documented tool version.
- Check shipped-means-present (gate 8): every file the `SKILL.md` or `usage-guide.md` points at
  must exist. A missing primary file is a P0.
- Check research scope (gate 7): anything that diagnoses, prescribes, or triages an individual is a
  Practice Boundaries (M2) failure.

Write per Skill, into `F:\OpenScience\audits\<skill-id>\`:

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
their upstream commits; the builder checks this. This includes what your interpreter writes for you:
importing a Skill's `examples/` module leaves a `__pycache__` beside it, and `.pyc` files are
gitignored, so **`git status` in the clone reads clean while byte-identity is broken**. Check the
filesystem (`find <clone> -name __pycache__`), not git status, and run every script from your own
`F:\OpenScience\audits\<skill-id>\run\` with the Skill's folder copied, not imported in place.

## Step 3 — skeleton spec

Write `F:\OpenScience\specialist-src\<candidate-id>\spec.json`:

```json
{
  "id": "<candidate-id>",
  "version": "1.0.0",
  "upstream": {
    "repository": "https://github.com/GPTomics/bioSkills",
    "commit": "d91ed3d563019e649dc854c56ccd62551359488a",
    "license": "MIT",
    "path": "F:/OpenScience/external/GPTomics__bioSkills"
  },
  "display_name": "",
  "summary": "",
  "skills": [
    {"id": "<frontmatter name>", "source": "<folder>/<skill>", "core": true,
     "display_name": "", "description": "", "_audit": 0, "_upstream_description": "<first 250 chars>"}
  ],
  "connectors": [{"id": "pubmed", "required": false, "default_selected": true}]
}
```

Include only Skills that passed (core ≥ 85, supporting ≥ 75, no veto, deployable, no open P0).
Suggest connectors only from this vocabulary: pubmed literature clinical-trials biorxiv genes
genomes expression protein-annotation structures rna regulation biomart clinical-genomics
human-genetics drug-regulatory cancer-models research-resources chembl chemistry molecule zinc
omics-archives variants cellguide.

Then write `F:\OpenScience\specialist-src\<candidate-id>\AUDIT.md` (dated heading):

- a table of every audited Skill: ID, role, category, mode, N, executed k/N, static, execution
  average, final, grade, veto, top P1;
- the Skills read but not chosen, one line each;
- your verdict against gates 2, 3, 4, 7 and 8. If the candidate fails (no core-grade executor for
  the central step, or coverage gaps), say so and what would fix it. Do not soften the verdict.

## Rules

- Windows: edit files with the Write/Edit tools or Python with `encoding='utf-8'`; never
  round-trip text through PowerShell `Get-Content`/`Out-File`. Prefix Python with
  `PYTHONIOENCODING=utf-8` in Bash. Keep paths short: Windows fails past 260 characters.
- Do not touch `F:\OpenScience\skills`, `F:\OpenScience\external`, `F:\OpenScience\specialists`,
  the builder, or other candidates' folders.
- No network calls to paid or authenticated services. Public downloads for pip/CRAN/Bioconductor
  are fine.

## Final message

- **select** (≤ 100 words): the audit order with core marked, and which reports are reused.
- **audit** (≤ 80 words): final score, grade, deployable, executed k/N, veto, top P0/P1.
- **verdict** (≤ 200 words): candidate verdict (viable / not viable and the failing gate); Skills audited with final scores;
how many inputs actually executed; the three most important findings about Skill quality; anything
pending or blocked.
