> **Audit record for `bio-pathway-gsea`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d6ecbe3](https://github.com/mrsonord2240/bioSkills/tree/d6ecbe33cfc1aa0e9635f83ae2f0b98832557dbe/pathway-analysis/gsea) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-gsea

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@d6ecbe33cfc1aa0e9635f83ae2f0b98832557dbe:pathway-analysis/gsea`

## Result

**Reject; deployable: false.** The static material is strong and every route materialized checked output, but five fresh top-level R computations returned Windows exit code `2816` after completion. That includes both shipped examples and a repeat of the MSigDB example. This fails Skill Veto T1 and Research Veto M4 in the manifest-selected runtime.

| Input | Type | Basic | Specialized | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Shipped GO | 29/40 | 43/60 | 72 | 3/4 | Partial: exit 2816 |
| 2 | Shipped MSigDB, repeated | 29/40 | 43/60 | 72 | 3/4 | Partial: both exit 2816 |
| 3 | nPerm/ranking edge | 32/40 | 48/60 | 80 | 4/5 | Partial: exit 2816 |
| 4 | GSVA/ssGSEA | 31/40 | 48/60 | 79 | 3/4 | Partial: exit 2816 |
| 5 | CAMERA/fry stress | 38/40 | 59/60 | 97 | 5/5 | Complete, exit 0 |
| 6 | ID-type mismatch | 32/40 | 48/60 | 80 | 2/3 | Partial: exit 2816 |
| 7 | Scope boundary | 38/40 | 59/60 | 97 | 4/4 | Complete, exit 0 |
| 8 | KEGG + Reactome | 31/40 | 47/60 | 78 | 2/3 | Partial: exit 2816 |

Execution average: **81.9/100**. Assertions: **26/32 (81.3%)**. Static: **96/100**. Nominal weighted score: **87.5/100**, overridden to Reject by the two veto failures.

## Fresh execution evidence

- Input 1: the unmodified GO example returned 31 terms; `GO:0006260` had NES `3.048360`, BH `1.51e-14`. See `run/input1_gsego_example.R.out`.
- Input 2: each run returned the planted OXPHOS Hallmark at NES `3.053965`, BH `3.14e-22`; both returned `2816`. See `run/input2_msigdb_example.R.out` and `run/input2_msigdb_repeat.out`.
- Input 3: `nPerm=1000` generated two fallback warnings, the documented guard fired, and unsorted/duplicate inputs were rejected. See `run/input3_rank_nperm.R.out`.
- Input 4: GSVA UP delta was `+0.7376`; DOWN delta `-0.8415`; both score matrices are under `data/`. See `run/input4_gsva_scores.R.out`.
- Input 5: CAMERA found both planted sets at FDR `3.60e-06` and `1.35e-07`; the reported directions are correctly interpreted against the test's `Control - Case` coefficient. See `run/input5_camera_rerun.out`.
- Input 6: symbol-matched GSEA returned 50 rows; a deliberate Entrez mismatch emitted `No gene can be mapped`. See `run/input6_id_match.R.out`.
- Input 7: the exact source warns against raw p-value ranking, gives the CAMERA route, and names ORA as the unranked-list escape hatch. It recorded the live package stack in `run/input7_scope_and_versions.R.out`.
- Input 8: live KEGG returned 311 rows and local Reactome 886, both with `NES` and `p.adjust`, then the process returned `2816`. See `run/input8_kegg_reactome.R.out`.

All execution scripts and parse logs are retained in `run/`. The pre-existing audit was archived before this run at `F:\OpenScience\audits\_pre-fix-20260923\bio-pathway-gsea`.

## Cleanliness

`pathway-analysis/gsea` has no diff from the pinned commit. The worktree itself is not clean because `alternative-splicing/isoform-switching/SKILL.md` was already modified; it was not touched.
