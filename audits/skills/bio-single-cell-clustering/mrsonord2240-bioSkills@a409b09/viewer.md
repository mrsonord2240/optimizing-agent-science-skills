> **Audit record for `bio-single-cell-clustering`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@a409b09](https://github.com/mrsonord2240/bioSkills/tree/a409b098b3602b13d7c40610f1c6bc09057258ac/single-cell/clustering) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-clustering

Generated: 2026-09-24
Exact source: `mrsonord2240/bioSkills@a409b098b3602b13d7c40610f1c6bc09057258ac:single-cell/clustering`
Category: Data Analysis · Mode: A · Complexity: Moderate
Environment: Scanpy 1.12.4 / anndata 0.13.3 / scikit-learn 1.9.1; Seurat 5.5.0.

## Summary

| Input | Scenario | Total | Assertions | Status |
|---|---|---:|---:|---|
| 1 | Defensible Scanpy sweep | 96 | 4/4 | ✅ |
| 2 | Seurat 5 Leiden route | 96 | 4/4 | ✅ |
| 3 | Batch-driven split | 97 | 4/4 | ✅ |
| 4 | Homogeneous-subset subclustering | 96 | 4/4 | ✅ |
| 5 | High-resolution marker-p claim | 96 | 4/4 | ✅ |
| 6 | New: helper guards and stability | 97 | 4/4 | ✅ |
| 7 | New: formal-test boundary | 94 | 4/4 | ✅ |

**Execution average: 96.0 / 100**
**Assertion pass rate: 28 / 28**
**Final: 95 / 100 — Production Ready — deployable**

## Executed evidence

`run/re_audit_20260924.py` ran against the exact source commit:

```text
source_commit=a409b098b3602b13d7c40610f1c6bc09057258ac
input1_reproducible_leiden_and_pc_rule=PASS
input2_seurat5_leiden_dependency=PASS
input3_batch_split_stop_rule=PASS
input4_subclustering_stop_rule=PASS
input5_double_dipping_and_reporting=PASS
ARI(candidate, batch) = 1.000
mean bootstrap Jaccard by cluster:
cluster
0    1.0
1    1.0
input6_helper_clusters=2 min_jaccard=1.000 missing_key=PASS
input7_python_blocks_compiled=4 scSHC_guard=PASS
```

Focused Seurat inspection executed with the audit R environment:

```text
seurat=5.5.0 leiden_method=TRUE leidenbase_installed=FALSE
```

The source now gives the correct Seurat 5 `leidenbase` install path and an explicit `igraph` backend alternative, so an absent optional package is an actionable boundary rather than a misleading reticulate error.

## Re-audit findings

All prior P1/P2 findings are fixed. Candidate partitions no longer pass solely because their selected marker sets differ: the skill supplies covariate-alignment and bootstrap-Jaccard checks, requires formal split testing and independent replication for a population claim, and labels unvalidated splits as hypotheses. It also resolves the early-elbow versus 30-50-PC conflict, specifies the required sweep report, and bundles the validation helper.

The optional `scSHC` package is not installed in this audit environment. This is not an open source finding: the skill explicitly fails with installation guidance instead of presenting post-clustering marker p-values as an alternative formal test.

No P0, P1, or P2 findings remain from this re-audit.
