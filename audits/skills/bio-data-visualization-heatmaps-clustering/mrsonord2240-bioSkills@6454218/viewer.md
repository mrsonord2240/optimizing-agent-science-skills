> **Audit record for `bio-data-visualization-heatmaps-clustering`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6454218](https://github.com/mrsonord2240/bioSkills/tree/6454218cec8127aa7880df1b346afd108bc8e3a0/data-visualization/heatmaps-clustering) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-heatmaps-clustering

Generated: 2026-09-24 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@6454218cec8127aa7880df1b346afd108bc8e3a0:data-visualization/heatmaps-clustering`
Audit type: focused final-pass re-audit at the exact follow-up commit
Category: Data Analysis · Execution mode: A · Complexity: Complex · N = 8 · Executed: None

## What the Skill claims to do

Build clustered heatmaps for expression matrices and other features-by-samples data with rigorous distance/linkage/scaling choices, robust color mapping, optimal leaf ordering, and ComplexHeatmap/pheatmap/seaborn rendering. Covers the ward.D vs ward.D2 trap, the row-vs-column scaling decision, multi-track annotations, oncoPrint, and raster rendering for large matrices.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 57 | **94** | 5/5 | yes | ✅ |
| 2 | Variant A | 37 | 58 | **95** | 5/5 | yes | ✅ |
| 3 | Edge | 33 | 51 | **84** | 5/5 | yes | ✅ |
| 4 | Variant B | 37 | 57 | **94** | 5/5 | yes | ✅ |
| 5 | Stress | 33 | 52 | **85** | 4/5 | yes | ❌ |
| 6 | Scope Boundary | 35 | 56 | **91** | 4/4 | yes | ✅ |
| 7 | Adversarial | 37 | 57 | **94** | 4/4 | yes | ✅ |
| 8 | Adversarial | 30 | 48 | **78** | 4/4 | yes | ✅ |

**Execution Average: 89.4 / 100** · **Assertion Pass Rate: 36/37**

**Static: 90/100** · Static weighted 36.0 + dynamic weighted 53.6 = **90/100** → ⭐ Production Ready, deployable.

---

## Veto gates

### Skill veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| stability | PASS |  |
| contract | PASS |  |
| determinism | PASS |  |
| security | PASS |  |

### Research veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | Generated values support the stated methods: ward.D2 matches scipy ward within 1.42e-14, OLO equals the drawn order, real-data annotations/counts map correctly, and the final two documentation inaccuracies are corrected. |
| practice boundaries | PASS | Visualization guidance only; no diagnostic, treatment, or individual-level clinical content. |
| methodological ground | PASS | The corrected non-circular-selection guidance was checked against the pure-noise adversarial input. |
| code usability | PASS | Both shipped examples, three added executable patterns, OLO regression, and seaborn bounds regression execute in the stated environment. The stress-vector interruption is reported as partial runtime evidence, not treated as a source failure. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 11/12 | Correlation-QC, shared-order and pseudobulk workflows are executable, and the inline annotation block covers every observed pathway level. |
| reliability | 10/12 | OLO compatibility, bounds, filtering and ordering rules are strong; draw() guidance now distinguishes top-level auto-print from assignments, nested expressions, and report hosts. |
| performance context | 7/8 | Decision-oriented and reasonably scoped, with runnable details in examples; still a substantial single document. |
| agent usability | 14/16 | Decision table, failure modes, tests, and the three-level inline rowAnnotation snippet are actionable. |
| human usability | 7/8 | Examples and failure-mode explanations are clear and internally consistent. |
| security | 11/12 | No credentials, network calls, destructive operations or unnecessary sensitive-data retention. |
| maintainability | 11/12 | Self-contained examples and dedicated tests include a three-level pathway regression and explicit draw-behavior check. |
| agent specific | 19/20 | Precise trigger, related skills, version notes and predictable output paths. |

## Input 1 — Canonical: Annotated OLO ComplexHeatmap on real ALL data and both shipped R examples

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 57/60 · **Total 94/100**
- Execution: heatmap_phd.R, expression_heatmap.R, test_olo_row_annotation.R and i1_all_real.R.
- Finding: Exact examples completed; real ALL OLO order equalled the drawn order and lineage slices were pure.

| Assertion | Result | Evidence |
|---|---|---|
| heatmap_phd.R completes with explicit OLO and Pathway annotation | PASS | Exited 0; heatmap.pdf is 111,003 bytes. |
| expression_heatmap.R renders scaled ward.D2 data and all pathway levels | PASS | Exited 0; expression_heatmap.pdf is 26,078 bytes. |
| OLO drawn order equals the supplied OLO order | PASS | Dedicated test and real ALL regression both assert equality. |
| Real ALL annotations map to displayed samples | PASS | Slices were 32 T-cell and 94 B-cell with no mixed slice. |
| Exact examples produce no stray Rplots.pdf | PASS | Fresh directory contains only their named outputs. |

## Input 2 — Variant A: Seaborn clustermap with explicit row-z scores and robust bounds

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 58/60 · **Total 95/100**
- Execution: test_seaborn_zscore_bounds.py via py.sh.
- Finding: Current dedicated regression passed; bounds and plotted data both derive from df_z.

| Assertion | Result | Evidence |
|---|---|---|
| Current seaborn regression executes | PASS | test_seaborn_zscore_bounds.py exited 0. |
| Plotted values equal explicit row-z scores | PASS | Regression asserts allclose after reindexing g.data2d. |
| Limits are robust bounds of plotted data | PASS | Mesh limits equal plus/minus df_z 99th percentile. |
| Zero-variance rows are excluded | PASS | Source replaces zero SD with NaN and drops those rows. |
| Ward linkage remains explicit | PASS | The block passes method='ward' and metric='euclidean'. |

## Input 3 — Edge: Ward, color, sparse-row, draw, ordered-column, gap and raster claims

- Status: ✅ COMPLETED · Basic 33/40 · Specialized 51/60 · **Total 84/100**
- Execution: i3_edge_claims.R, i3_scipy_check.py, i3_cmp.R, i3b_timecourse.R, new_ordered_conditions.R, and delta-6454218/verify_delta_6454218.R.
- Finding: Ward, color, sparse-row, gap, ordered-column, and draw-behavior checks pass.

| Assertion | Result | Evidence |
|---|---|---|
| R ward.D2 matches scipy ward while ward.D does not | PASS | Maximum height difference was 1.42e-14 for ward.D2 and 209 for ward.D. |
| Robust color mapping clips outliers | PASS | Value 60 mapped to the extreme color. |
| Sparse z-score and pheatmap gaps guidance are accurate | PASS | One-nonzero maximum was 2.85; gaps changed positions only with clustering disabled. |
| cluster_columns=FALSE preserves ordered conditions with column_split | PASS | Both time-course and new ordered-condition tests retained input order. |
| Top-level and nested Rscript draw guidance is accurate | PASS | The exact delta produced a 6,432-byte bare top-level auto-print PDF; the revised source still requires explicit draw() as the portable contract for assignments, nested expressions, and report hosts. |

## Input 4 — Variant B: Correlation QC and linked heatmaps on real airway plus current patterns

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 57/60 · **Total 94/100**
- Execution: advanced_heatmap_patterns.R and i4_airway_qc_concat.R.
- Finding: Real airway and the new three-pattern example passed: symmetric correlation, shared order and pseudobulk groups.

| Assertion | Result | Evidence |
|---|---|---|
| Correlation matrix is symmetric with unit diagonal | PASS | Real airway regression printed TRUE. |
| Correlation row and column clustering share order | PASS | Drawn row order equalled column and hclust order. |
| Linked heatmaps use expression-derived shared order | PASS | Current pattern asserts both heatmaps retain shared_row_order. |
| Pseudobulk retains planned group levels | PASS | Current pattern asserts pseudobulk columns equal factor levels. |
| Real airway log2FC direction matches z-score panel | PASS | All 40 selected genes matched. |

## Input 5 — Stress: 5,000 by 60 raster/OLO heatmap with planted modules

- Status: ❌ PARTIAL · Basic 33/40 · Specialized 52/60 · **Total 85/100**
- Execution: i5_stress.R via r.sh; partial.
- Finding: Fresh run computed OLO in 76.4 seconds and produced i5_raster.pdf (761,672 bytes); later vector comparison was interrupted by the shared Windows R process issue.

| Assertion | Result | Evidence |
|---|---|---|
| 5,000-row OLO executes | PASS | Fresh run printed OLO 76.4 seconds. |
| Raster PDF is nonempty | PASS | i5_raster.pdf is 761,672 bytes. |
| Robust bound and outlier are computed | PASS | Fresh run printed bound 2.272 and outlier z 7.09. |
| Prior stress evidence supports order and module recovery | PASS | Archived prior run recorded OLO equality and ARI 0.992; it is not substituted for fresh vector evidence. |
| Fresh vector-versus-raster comparison completes | FAIL | Fresh vector PDF remained zero bytes after process interruption. |

## Input 6 — Scope Boundary: OncoPrint pointer and scanpy marker heatmap

- Status: ✅ COMPLETED · Basic 35/40 · Specialized 56/60 · **Total 91/100**
- Execution: i6_oncoprint_scanpy.R and i6b_scanpy.py.
- Finding: Real TCGA-LAML oncoPrint and synthetic scanpy marker heatmap completed; specialized mutation details remain delegated.

| Assertion | Result | Evidence |
|---|---|---|
| OncoPrint counts match MAF | PASS | All matrix counts matched unique-sample counts. |
| Explicit oncoPrint column_order is honoured | PASS | Regression printed TRUE. |
| scanpy marker heatmap retains planted blocks | PASS | Block argmax assignments were correct. |
| Scope remains a pointer to dedicated oncoPrint skill | PASS | No unsupported mutation-analysis recipe is claimed. |

## Input 7 — Adversarial: Circular DE selection on pure noise

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 57/60 · **Total 94/100**
- Execution: i7_adversarial.R.
- Finding: Pure-noise selection still separates perfectly; exact skill now warns against circular selection.

| Assertion | Result | Evidence |
|---|---|---|
| Pure-noise DE selection can mislead | PASS | Slices were pure 10/10 Control and Treatment. |
| Skill warns against circular selection | PASS | It requires pre-specified, held-out, or label-independent selection. |
| Skill gives independent selection mechanisms | PASS | It names pre-registration, discovery split and objective variance. |
| No biological conclusion is forced | PASS | Run is labelled pure noise. |

## Input 8 — Adversarial: Two new checks: three-level inline annotation and exact OLO regression

- Status: ✅ COMPLETED · Basic 30/40 · Specialized 48/60 · **Total 78/100**
- Execution: delta-6454218/test_olo_row_annotation.R and delta-6454218/verify_delta_6454218.R via r.sh.
- Finding: The byte-identical exact OLO regression and focused delta check pass with all three pathway levels and corrected draw semantics.

| Assertion | Result | Evidence |
|---|---|---|
| Compatible OLO row annotation renders | PASS | Exact OLO test passed and wrote a 6,363-byte PDF. |
| Incompatible OLO plus categorical row_split is explicit | PASS | Exact regression expects and matches the error. |
| Inline annotation supports all documented levels | PASS | Dynamic colors cover Metabolism, Signaling, and Immune; the focused PDF is 6,617 bytes. |
| Current draw prose precisely describes top-level Rscript | PASS | Bare unassigned top-level auto-print produced a 6,432-byte PDF, matching the exact source qualification. |

## Key strengths

- The P0 OLO/row_split crash is repaired with a self-contained example, compatible annotation and an order-checking regression.
- Seaborn now derives robust limits from the explicit row-z-scored matrix and verifies data plus limits.
- Correlation QC, shared-order and pseudobulk workflows are executable patterns.
- Real ALL, airway and TCGA-LAML regressions retain checkable mappings and nonempty outputs.
