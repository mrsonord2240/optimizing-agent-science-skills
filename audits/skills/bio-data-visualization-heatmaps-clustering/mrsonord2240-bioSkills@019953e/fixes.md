# Fix log: bio-data-visualization-heatmaps-clustering

## 2026-09-23 — backlog correction

Skill `data-visualization/heatmaps-clustering`, branch
`fix/data-visualization-heatmaps-clustering`, commit
`6454218cec8127aa7880df1b346afd108bc8e3a0` from staging `8c75e1f4`
(initial correction `2c2fc969`, re-audit follow-up `6454218c`).
Validated with R 4.4.3, ComplexHeatmap 2.22.0, seriation 1.5.8, and the
data-visualization Python environment.

| finding | priority | change | verification |
| --- | --- | --- | --- |
| Explicit OLO dendrogram plus categorical `row_split` crashes | P0 | Removed the incompatible row split, retained Pathway as a row annotation, documented the constraint, made the flagship example self-contained, and reused one drawn heatmap for row/column orders. | Flagship and focused OLO test exit 0; drawn order matches `order.dendrogram`, all annotation levels remain, PDF is nonempty, and no `Rplots.pdf` is created. The rejected combination reproduces the documented error. |
| Seaborn limits came from raw values while `z_score=0` plotted another scale | P1 | Row-standardize explicitly and derive the robust symmetric bound from the exact matrix passed to `clustermap`. | Python regression matches an independent z-score and confirms the plotted dynamic range. |
| Circular row selection and three advertised workflows lacked executable guidance | P1 | Added the anti-circular selection boundary plus runnable sample-correlation QC (`1-r` and observed sequential range), shared expression-derived row ordering across two panels, and pseudobulk-before-heatmap patterns. | All advanced R patterns execute and their orders, dimensions, labels, and correlation invariants pass. |
| Rendering, dendrogram, sparse-row, split-order, colour, and scaling claims were inaccurate | P2 | State that a bare unassigned top-level `Heatmap()` can auto-print in Rscript while explicit `draw()` remains the portable export contract; corrected default dendrogram equivalence; reframed sparse failures as zero-variance/low-information rows; require `cluster_columns=FALSE` for ordered splits; derive Pathway colours from observed levels and use legend breaks `c(-bounds,0,bounds)`. | Runtime truth-table and focused three-level Metabolism/Signaling/Immune example pass with a nonempty PDF and no `Rplots.pdf`. |
| `expression_heatmap.R` did not implement its stated analysis | P2 | Added true row scaling, robust limits, `ward.D2`, and pathway labels aligned to planted modules. | Row means are approximately zero, row SDs approximately one, bounds are finite, and planted modules retain their labels. |
| Guide repeated or overstated operational claims | P2 | Reconciled the guide with the executable examples and removed unsupported metadata-decision language. | Source review and `git show --check` pass. |

## Findings left unfixed

None of the audit recommendations.
