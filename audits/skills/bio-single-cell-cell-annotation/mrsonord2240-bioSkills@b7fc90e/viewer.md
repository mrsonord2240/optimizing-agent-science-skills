> **Audit record for `bio-single-cell-cell-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@b7fc90e](https://github.com/mrsonord2240/bioSkills/tree/b7fc90e69bdf4839b958a13b37581945ba694413/single-cell/cell-annotation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-cell-annotation

## Exact-commit re-audit

| Source commit | Re-audited | Scope | Result |
|---|---|---|---|
| `b7fc90e69bdf4839b958a13b37581945ba694413` | 2026-09-24 | All prior P1/P2 findings | 15/15 focused assertions PASS |

The previous five-input audit’s fixture evidence is retained. This re-audit executes the changed CellTypist and QC-first triage paths directly from the exact committed `SKILL.md`; it also source-checks the Seurat normalization precondition. The local re-audit host has no `Rscript`, so an Azimuth end-to-end rerun was not claimed.

## Scores

| Dimension | Score |
|---|---:|
| Static quality | 94 / 100 |
| Dynamic execution | 94.0 / 100 |
| Assertions | 20 / 20 PASS |
| Final | **94 / 100 — Production Ready** |

## Re-audit evidence

`run/exact-commit-b7fc90e/reaudit_focused.py` verified the checked-out SHA before reading the source, parsed the Python fences, and passed all 15 assertions:

- CellTypist uses an explicit `over_clustering='leiden'` and repeatable majority labels on the existing fixture.
- Raw counts raise the documented invalid-expression-matrix error; Ensembl IDs raise the documented no-feature-overlap error.
- The QC-first triage fence retains every cluster and surfaces a high-confidence doublet/low-quality artifact instead of filtering it out on confidence.
- The source now states SingleR pruning’s ambiguity-only scope and normalizes Seurat data before `DotPlot`.

The log is at `run/exact-commit-b7fc90e/reaudit_focused.log`.

## Finding disposition

| Prior finding | Priority | Disposition |
|---|---|---|
| Confidence-first artifact triage | P1 | Fixed and executed |
| Stale CellTypist normalization and gene-ID symptoms | P2 | Fixed and executed |
| SingleR pruning presented as a general safety net | P2 | Fixed and source-checked against retained SingleR evidence |
| Marker plot assumed normalized Seurat object | P2 | Fixed; source-checked (no R runtime available) |
| Implicit/unseeded CellTypist over-clustering | P2 | Fixed and executed |

**Remaining P0/P1/P2 findings: none.**
