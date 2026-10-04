# Handoff: bio-workflows-crispr-screen-pipeline / prepare-scientific-skill-tooling

- Updated: 2026-10-04T16:30:00-04:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: normalize worker (router recut)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/crispr-screen-pipeline
- Working tree: F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline
- Branch/worktree: recut/crispr-screen-pipeline, sparse, from optimized-scientific-skills f162b3a
- Candidate tree hash: e242270b6fc053d495f12c86df5d2d8eb96f9b42fd3971d6435796c9bae5a71d (skill_preflight --shape PASS, 19 files)
- Starting identity: f7e144acbac594965ca80994397dd00fe001b9dff32c188737b5ea1891625cc9 (old layout)
- Applicable audit: none for the recut

## Completed this phase

- Cut to a router: SKILL.md (40 lines, route table), 11 routes, 4 scripts, references (install, background, citations).
- Dropped usage-guide.md and examples/crispr_pipeline.sh (replaced by scripts/rra.py and routes/count.md); inline QC, CRISPRcleanR, tier-consensus and volcano code moved to scripts.
- Description cut to a `Use when` trigger; frontmatter keeps name, category, tool_type, primary_tool, license, author; depends_on and qc_checkpoints removed (content now in routes).
- Version drift fixed: Chronos installs from PyPI as `crispr-chronos` (import `chronos`), not a GitHub-only install; BAGEL2 seed written `--seed` (short `-s` is overloaded in `bf`); drugZ `-unpaired` documented.
- Preflight warn: no Skill-root LICENSE (original had none either).

## Routes and scripts

| Route | Entry point | Status |
|---|---|---|
| qc | scripts/qc.py | executed |
| rra | scripts/rra.py | executed |
| consensus | scripts/consensus.py | executed |
| cn-correction | scripts/cn_correction.R | UNEXECUTED (CRISPRcleanR not installed) |
| count, bagel2, mle, drugz, jacks, chronos | commands shown in route | bagel2 and drugz commands run; count, mle, jacks, chronos not run |
| branches | pointers to sibling Skills | n/a |

Environment: native Windows, `F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts` on PATH (no crispr env exists in WSL `science`). Input: HAP1 TKOv3 (70,754 guides; public-data). Evidence: F:\OpenScience\fix-evidence\recut-crispr-pipeline\.

- qc.py: HAP1 plasmid=HAP1_T0 -> exit 1, replicate Pearson 0.789 (matches the 0.789 in the original text), plasmid Gini 0.288; synthetic clean table -> PASS (Pearson 0.853). Traps tripped: non-integer counts, unknown plasmid label.
- rra.py: HAP1 T18A-C vs T0, 18,056 genes; defaults fdr 0.05 lfc 0.5 -> 848 negative, 3 positive hits (POLR2L, EIF3A, GTPBP10 top); fdr=1.1 lfc=0 -> 8,447 / 9,609. Traps tripped: missing control, unknown sample, norm=control without ctrl_genes.
- consensus.py: three methods -> Tier-1 481, Tier-2 399, Tier-3 874; two methods fdr=1.1 -> all Tier-2; one method refused.
- BAGEL2 `--seed 42` run twice: max BF difference 0.0. drugZ `-unpaired` ran (top POLR2L, POLR3H).

## Runnable-surface inventory and dependency clues

mageck count/test/mle (0.5.9.5), BAGEL.py fc/bf/pr, drugz.py, run_JACKS.py, chronos (venv chronos-venv), CRISPRcleanR (R; not installed), pandas/numpy/matplotlib. Reference sets CEGv2/NEGv1 in public-data.

## Open ambiguities for tooling and audit

- cn_correction.R is written from the original calls plus a `library=` option and a `min_reads` pass-through; CRISPRcleanR API (first sample column = control, annotation file format, `display=TRUE` under Rscript) is unverified.
- mle design-matrix format (Samples, baseline, 0/1 columns) is standard MAGeCK usage, not from the original; mle, jacks, chronos, count commands are not run here.
- consensus.py covers depletion only (as the original); no enrichment tiering.
- Original `ccr.GWclean` and counting caveats on corrected-count column layout untested.

## Worktree safety

- Run-owned changes: all files under the working tree above (deletions of usage-guide.md and examples/ unstaged); run evidence under F:\OpenScience\fix-evidence\recut-crispr-pipeline\
- Pre-existing/user-owned changes: records test/validate.bats untracked, untouched
- Records state: this handoff only
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
