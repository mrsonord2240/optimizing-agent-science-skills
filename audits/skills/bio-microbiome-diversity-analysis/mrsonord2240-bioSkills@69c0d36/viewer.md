> **Audit record for `bio-microbiome-diversity-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@69c0d36](https://github.com/mrsonord2240/bioSkills/tree/69c0d367c211d04226456107fde34f4c1dbee672/microbiome/diversity-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-microbiome-diversity-analysis

## Canonical final summary

**Final:** 97/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23

Source: mrsonord2240/bioSkills@69c0d367c211d04226456107fde34f4c1dbee672:microbiome/diversity-analysis

## Final result

**97/100 - Production Ready - deployable: true.** Both veto gates passed. This final-pass JSON deliberately sets meta.auditor_independent to false with the required CHECKPOINT note.

Static: 98/100. Dynamic: 95.8/100. Assertions: 33/33.

| Input | Type | Basic | Specialized | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical fixture | 38 | 57 | 95 | 3/3 | PASS |
| 2 | Depth variant | 38 | 58 | 96 | 3/3 | PASS |
| 3 | No-tree edge | 38 | 56 | 94 | 3/3 | PASS |
| 4 | QIIME2 + generalized UniFrac | 39 | 58 | 97 | 3/3 | PASS |
| 5 | Longitudinal stress | 38 | 57 | 95 | 3/3 | PASS |
| 6 | Scope boundary | 39 | 57 | 96 | 3/3 | PASS |
| 7 | Adversarial | 39 | 58 | 97 | 3/3 | PASS |
| 8 | Independent strata fixture | 38 | 58 | 96 | 3/3 | PASS |
| 9 | Verbatim R blocks | 37 | 57 | 94 | 3/3 | PASS |
| 10 | Numeric depth helper | 39 | 59 | 98 | 3/3 | PASS |
| 11 | Shipped R example | 39 | 57 | 96 | 3/3 | PASS |

## Fresh execution evidence

- Inputs 1-5 and 8-9 ran through final_pass_regression_runner.ps1. The Windows R wrapper reports exit status 2816 after successful materialized output, so each result was judged by saved, run-specific content assertions.
- Input 10 ran the exact worktree pick_sampling_depth.R: depth 7771, 35/40 retained, dropped S03, S17, S20, S29, and S40.
- Input 11 ran the exact worktree diversity_analysis.R and produced both nonempty PDFs plus weighted and unweighted UniFrac PERMANOVA output.
- Input 4 ran public moving-pictures data through fresh QIIME2 import, demux, DADA2, MAFFT/FastTree, core metrics, and weighted/unweighted PERMANOVA plus PERMDISP. Both exported distance matrices have 31 samples; weighted gut versus left palm had pseudo-F 65.72, p=0.001, 999 permutations.
- Inputs 6-7 are saved direct Skill executions: correct cross-skill routing, refusal of metric shopping, no diagnostic conclusion.

## Veto review

| Gate | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | All 11 inputs produced checked output. |
| T2 Contract | PASS | Required frontmatter and shipped references/scripts exist. |
| T3 Determinism | PASS | R paths are seeded; numeric depth is analytic. |
| T4 Security | PASS | No secrets, raw-string execution, or destructive action. |
| M1 Scientific integrity | PASS | Numbers are traceable to saved fresh artifacts. |
| M2 Practice boundaries | PASS | The patient prompt was not diagnosed. |
| M3 Methodology | PASS | Depth, tree, metrics, dispersion, and strata safeguards executed. |
| M4 Code usability | PASS | R and shell parsing plus live workflows passed. |

## Remaining issue

- P2: the GlobalPatterns example still selects a tenth-percentile depth while the main Skill now offers a numeric plateau helper. This is not deployment-blocking; call the helper or label the quantile as a demonstration-only placeholder.

## Artifact map

- Fresh scripts and logs: F:/OpenScience/audits/bio-microbiome-diversity-analysis/run/
- Fresh QIIME artifacts: run/final_new5_qiime_moving_pictures_r2/
- Preserved preceding audit: F:/OpenScience/audits/_pre-fix-20260923/bio-microbiome-diversity-analysis/
- Original pre-fix audit: F:/OpenScience/audits/_pre-fix-20260919/bio-microbiome-diversity-analysis/

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@69c0d367c211d04226456107fde34f4c1dbee672:microbiome/diversity-analysis`
- `auditor_independent:false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@69c0d367c211d04226456107fde34f4c1dbee672:microbiome/diversity-analysis`
- `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`
