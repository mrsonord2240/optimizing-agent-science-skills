> **Audit record for `bio-single-cell-markers-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@f704543](https://github.com/mrsonord2240/bioSkills/tree/f704543b45168b0df1a09670e5f584e173c06d97/single-cell/markers-annotation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0 exact-commit focused re-audit.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-markers-annotation

Re-audited 2026-09-24 against exact clean commit `f704543b45168b0df1a09670e5f584e173c06d97` in `agent/fix-bio-single-cell-markers-annotation`, based on staging `main` at `12be3fc12a733fbbb8479bc8aa6abc1248950803`.

The original canonical report and viewer are preserved in `re-audit-20260924/pre-fix/`.

## Result

| Measure | Pre-fix | Re-audit |
|---|---:|---:|
| Static score | 84.0 | 94.0 |
| Execution average | 90.0 | 93.4 |
| Assertions | 19/20 | 20/20 |
| Final score | 88/100 | **94/100** |
| Grade | Production Ready | **Production Ready** |
| Open P0 / P1 / P2 | 0 / 1 / 4 | **0 / 0 / 0** |

All structural and research vetoes pass. The source worktree was clean at the exact commit recorded above.

## Resolved pseudobulk defect

The Python pseudobulk path now requires and uses raw counts:

```python
if 'counts' not in cell_type.layers:
    raise ValueError("Pseudobulk requires raw integer counts in adata.layers['counts']; do not sum normalized .X")
pseudobulk = sc.get.aggregate(cell_type, by='sample', func='sum', layer='counts')
```

It then checks that the aggregated values are integral. The exact published block was executed on a two-sample fixture with log-normalized `.X` and an integer `counts` layer; it produced `[[5, 1], [1, 6]]`. Removing the counts layer raised the documented `ValueError`, so a normalized matrix cannot silently proceed to pseudobulk. The Common Errors table and usage guide now tell users to reacquire raw counts if the layer is absent.

## Resolved annotation and reporting gaps

- CD8 T versus NK annotation now requires a `CD3D`/`CD3E` lineage gate before interpreting cytotoxic genes (`NKG7`, `GNLY`) and CD8/NK markers.
- The unverifiable claim that Seurat defaults to 24 bins was removed. Cross-ecosystem examples set `nbin=25` and `ctrl=50` explicitly and decline to promise identical score values.
- A concise reporting block now requires the test/version/thresholds, marker effect sizes and in/out expression fractions, lineage gates, and the standing descriptive-only p-value caveat.

## Evidence

- Exact-commit executable and documentation assertions: `re-audit-20260924/run-focused/focused_validation.out`
- Preserved pre-fix audit: `re-audit-20260924/pre-fix/`

No P0, P1, or P2 findings remain.
