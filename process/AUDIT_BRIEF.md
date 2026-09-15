# Brief: select and audit the Skills for one round-2 Specialist candidate

You are the **auditor** for ONE candidate Specialist. A different agent will later write the
Specialist from your results, so your job is to pick the Skills and grade them honestly. You never
write the Specialist, and you have no stake in any Skill passing.

## Read first

- `F:\OpenScience\specialist-src\round2\CANDIDATES.md` — your candidate's scope, source folders and
  boundaries, and why every candidate uses `GPTomics/bioSkills` only.
- `F:\OpenScience\specialist-src\THRESHOLD.md` — the viability gates. You own the evidence for gates
  2, 3, 4, 7 and 8.
- `F:\OpenScience\skills\skill-auditor\SKILL.md` and every file in its `references/` — the audit
  method. Follow it exactly: Skill Veto → 25-criteria static score → classification and execution
  mode → N inputs by the complexity rule → execution → Layer 1/2/3 scoring → Research Veto → final
  score, grade, floors and P0/P1/P2 recommendations.
- The previous round found upstream audits that were templated ("Test case N", identical totals
  across ~100 Skills) and backfilled summaries that quoted the Skill's own description. Those were
  rejected as evidence. Yours must be the opposite: inputs written for this Skill's real use,
  outputs you actually produced, scores you can defend line by line.

## Working limits (2026-09-15)

- **Do not spawn sub-agents.** Audit your Skills one after another yourself; at most two auditors run on
  the machine at once, and a fan-out of eight made every run crawl.
- **Audit the core Skills first** — the ones the Specialist's central step cannot exist without. If
  no core Skill reaches 85, stop, write the not-viable verdict in `AUDIT.md`, and skip the rest.

## Re-auditing a fixed Skill (2026-09-15)

Failing Skills are being fixed in Sam's fork (`round2\FIX_BRIEF.md`). When your dispatch names a
fixed Skill:

- Read the Skill from the fork path and commit in your dispatch, not from `GPTomics__bioSkills`.
  `"source"` becomes `"mrsonord2240/bioSkills@<commit>:<folder>/<skill>"`.
- The pre-fix report is archived at `F:\OpenScience\audits\_pre-fix-20260915\<skill-id>\`. Re-run its
  inputs as regression tests, and add at least two new inputs of your own so the score does not
  only measure the defects the fixer was told about. The fix log
  (`round2\fixes\<skill-id>.md`) says what changed; it is not evidence — only your runs are.
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
- `eval_viewer_<skill-id>.md` — the Step 7 viewer, including the generated code, what ran, and
  what it printed (trim long output, keep what the scores depend on).

**Never write anything inside `F:\OpenScience\external\`** — the clones must stay byte-identical to
their upstream commits; the builder checks this.

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

## Final message (≤ 200 words)

Candidate verdict (viable / not viable and the failing gate); Skills audited with final scores;
how many inputs actually executed; the three most important findings about Skill quality; anything
pending or blocked.
