# Ordered finding ledger — bio-data-visualization-volcano-and-ma-plots

Audited identity: `b94e14b191a0a1f2c6138fe10108d39b44b52efd299c47ae5a850e4e425ccb76`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | VOL-001 | P1 | open | [1] | volcano_phd.R clips significant points and their labels with an unconditional y cap. Apply the cap only when requested (y_cap = NULL by default), or squish with pmin(neg_log10_p, y_cap) plus a marker/axis break, and state the cap in the caption. |
| 2 | VOL-002 | P1 | open | [1, 2] | Shipped volcanoes draw the FDR line on a raw-p axis, contradicting the Skill. Plot -log10(padj) on y (as for EnhancedVolcano) or draw the line at the smallest -log10(p) among padj < fdr genes and label it. |
| 3 | VOL-003 | P2 | open | [4] | EnhancedVolcano example loses direction and mislabels the axis. Use colCustom per direction or document that EnhancedVolcano colours by class; set ylab = expression(-log[10]~adjusted~italic(P)). |
| 4 | VOL-004 | P2 | open | [3] | ashr is said to return svalue; it does not. State that svalue comes from apeglm with svalue=TRUE (or from ashr::ash lfsr) and correct the decision-tree row. |
| 5 | VOL-005 | P2 | open | [5] | sanbomics.tools.volcano does not exist. Name sanbomics.plots.volcano (and note the optional dependency) or drop the mention. |
| 6 | VOL-006 | P2 | open | [4] | EnhancedVolcano selectLab-threshold gotcha does not reproduce. Remove or version-qualify the gotcha and the manual-layer workaround. |
| 7 | VOL-007 | P2 | open | [3] | Shrinkage is described as only pulling toward zero. Add a sentence that apeglm uses a different estimator and can exceed the MLE for a few genes; compare against the MLE before reporting extremes. |
| 8 | VOL-008 | P2 | open | [1, 5] | Rasterization guidance is not implemented and its size claim is overstated. Wrap the point layer in ggrastr::rasterise or drop the comment; replace '5MB+' with the measured vector/raster ratio. |

No audit-local repair was made; no Skill bytes changed.
