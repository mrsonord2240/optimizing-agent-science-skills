# Handoff to Codex: final-pass Phase 2 audits (2026-09-22)

You are the orchestrator. Sam will run you with **at most 4 sub-agents at a time**. Claude is out of weekly
budget, so this is yours end to end. Delete this file when the work is done.

## Read first

1. `F:\optimizing-agent-science-skills\CLAUDE.md`: how the orchestrator runs the work (dispatch, backlog,
   landing, promotion). Written for Claude; it applies to you as-is.
2. `process\COMMON.md`, then `process\FINAL_PASS_BRIEF.md`: every sub-agent reads these two plus
   `FIX_BRIEF.md` and `AUDIT_BRIEF.md`.

## The job

Around 107 Skills had a Phase 1 fix pass on their staging worktrees (`F:\OpenScience\wt\<short>`, branches
`fix/<short>` in `F:\OpenScience\external\mrsonord2240__bioSkills`). Each now needs a **Phase 2 audit**: a
fresh agent per Skill that reads `F:\OpenScience\audits\_final_pass\<skill-id>\CHECKPOINT.md` and the fix
log, then audits the branch tip per `FINAL_PASS_BRIEF.md`. When all have landed, staging gets retired (Sam
decided this on 2026-09-22; see "After" below).

## Step 0: the tracker is not trustworthy. Fix it before dispatching anything

`F:\OpenScience\wt\_final_pass.json` (111 entries) marks 85 as `p2-done`, but **none has a Phase 2 report**
(no `eval_report_*_result.json` with `meta.auditor_independent: false`). Checked 2026-09-22 21:36 PDT:

- **75 of 111 `CHECKPOINT.md` files do not follow the template** in `FINAL_PASS_BRIEF.md`. Some are
  audits, not fix checkpoints. Example: `bio-admet-prediction`'s is titled "Phase 1 Audit", signed
  "GPTomics", dated 2026-09-23, and points at another Skill's worktree (`wt\entrez-fetch\...`).
- There are duplicate or near-duplicate ids (`bio-entrez-fetch` twice; `pathway-wikipathways` next to
  `pathway-analysis-wikipathways`; `pathway-reactome` next to `pathway-analysis-reactome-pathways`).
- Several `audits\` folders show modification times later than the time of the check. Rule out clock
  skew before relying on mtimes.

Write a script (save it under `tools\`) that builds `F:\OpenScience\wt\_phase2_manifest.json`, one row per
**unique** frontmatter `name`:

| field | how |
| --- | --- |
| `skill_id`, `worktree`, `branch`, `folder_path` | match `SKILL.md` frontmatter `name` inside each `wt\<short>` worktree (`git worktree list` in staging) |
| `tip_commit`, `phase1_commits` | commits on the branch after 2026-09-21 that touch the Skill |
| `env` | the `F:\OpenScience\audit-envs\<env>` whose `TOOLS.md` covers the folder |
| `checkpoint` | `ok` (template, correct Skill, correct worktree) / `bad` / `missing` |
| `phase2_report` | true only if a report with `auditor_independent: false` audits `tip_commit` |
| `status` | `ready` (checkpoint ok, Phase 1 commits exist), `redo-p1`, `p2-done` |

Then rewrite `_final_pass.json` from the manifest, keeping the old file as `_final_pass.pre-20260922.json`.
**Skills in `redo-p1` get Phase 1 re-run** (fresh agent, `FINAL_PASS_BRIEF.md` Phase 1) before their Phase 2.
Report the counts to Sam before Step 1.

## Step 1: four lanes, one agent slot each

Split by env so two agents never install into the same env at once. Inside a lane, run one Skill at a time,
fresh agent per Skill per phase. Rebalance at the end if a lane runs dry.

| Lane | Skills (id without `bio-`) | Env(s) |
| --- | --- | --- |
| A: sequence and databases (~33) | `alignment-*`, `sam-bam-basics`, `bam-statistics`, `duplicate-handling`, `reference-operations`, `vcf-basics`, `variant-annotation`, `phylo-tree-visualization`, `entrez-*`, `blast-searches`, `local-blast`, `sra-data`, `geo-data`, `ncbi-datasets-cli`, `biomart-queries`, `batch-downloads`, `database-access-remote-homology` | `alignment`, `alignment-files`, `database-access`, `variant-annotation-curation-analyst`, `molecular-phylogenetics-analyst` |
| B: genetics and statistics (~25) | `causal-genomics-*`, `experimental-design-*`, `differential-expression-deseq2-basics`, `pathway-*` | `mendelian-randomization-analyst`, others per manifest |
| C: screens, cells, splicing (~31) | `crispr-screens-*`, `single-cell-*`, `differential-splicing`, `long-read-splicing`, `outlier-splicing-detection`, `sashimi-plots`, `splice-variant-prediction`, `splicing-qc`, `isoform-switching` | `crispr-screen-analyst`, `single-cell-transcriptomics-analyst`, `alternative-splicing`, `bio-single-cell-lineage-tracing` |
| D: chemistry and omics (~26) | `admet-prediction`, `conformer-generation`, `covalent-design`, `pharmacophore-modeling`, `pose-validation`, `protac-degraders`, `shape-similarity`, `virtual-screening`, `metabolomics-*`, `workflows-metabolomics-pipeline`, `proteomics-*`, `workflows-proteomics-pipeline`, `microbiome-*` | `cheminformatics-hit-triage-analyst`, `untargeted-metabolomics-analyst`, `mass-spec-proteomics-analyst`, `microbiome-metagenomics-analyst` |

**Every dispatch names:** skill id, worktree, branch, tip commit, folder path, env and its `TOOLS.md`, the
checkpoint path, the fix log path, and the brief (`FINAL_PASS_BRIEF.md`, phase 1 or 2). Include any
checkpoint "still blocked" item Sam has decided. Otherwise, blocked items stay blocked and the audit
scores the Skill as it is.

Known issues from Phase 1: PICRUSt2 CLI broken in WSL, Python module only
(`microbiome-functional-prediction`); scvelo 0.3.4 vs numpy ≥ 2 (`single-cell-trajectory-inference`);
DEqMS/proDA/msqrob2 optional (`proteomics-differential-abundance`); isoform-switching SKILL.md targets
IsoformSwitchAnalyzeR v2.6, v2.12 is installed; wikipathways GMT handling is dated.

## Step 2: land each Skill as its Phase 2 report lands

Per `CLAUDE.md`: `python tools/publish_audits.py --repo F:/optimizing-agent-science-skills --skill <id>`,
`npm run audits:index`, then commit the record, index and fix log together, staging by explicit path. A
Skill that passes (deployable, no open P0, no veto) merges `--no-ff` into staging `main`, gets pushed, and
its branch and worktree are deleted. Update `_final_pass.json` to `p2-done` only after the report exists.

Batch promotion when a lane finishes: advance `FORK_COMMIT` in `tools/promote_skills.py`, dry run, then
`--apply`, update the shelf README Status table, commit and push `F:\optimized-scientific-skills`. **Never
force-push the shelf** (the marketplace pins its SHAs).

## Rules that bite

- Never `git reset --hard`, force-push, or delete anything unique without Sam's word.
- Never write in `F:\OpenScience\external\` (except merges to staging `main`), and never delete someone
  else's `install.lock`.
- Commit messages via `git commit -F <file>`. Files are UTF-8 without a BOM; never round-trip them
  through PowerShell 5.1 `Get-Content`/`Out-File`.
- Judge every sub-agent's claim by the files it left, not its final message. Phase 1 is how the tracker
  got into this state.

## After (not this handoff)

Once every Skill has landed: retire staging. Archive `mrsonord2240/bioSkills-Improved` on GitHub, prune
`F:\OpenScience\wt`, and move editing onto the shelf (the plan is in `CLAUDE.md` → Consolidation). Ask Sam
first. About 12 GB of scratch folders in `F:\OpenScience` are also waiting on his word.

## Final report to Sam

Counts of passed, failed and blocked; what each blocked item needs; commits pushed; anything that
contradicted this file.
