> **Audit record for `bio-data-visualization-volcano-and-ma-plots`**
> - Audited working candidate `b94e14b191a0a1f2c6138fe10108d39b44b52efd299c47ae5a850e4e425ccb76`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/data-visualization/volcano-and-ma-plots), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-volcano-and-ma-plots

Generated: 2026-10-03  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256: `b94e14b191a0a1f2c6138fe10108d39b44b52efd299c47ae5a850e4e425ccb76`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 28 | 38 | 66 | 2/4 | ⚠️ COMPLETED |
| 2 | Variant A | 32 | 44 | 76 | 3/4 | ✅ COMPLETED |
| 3 | Edge | 28 | 38 | 66 | 2/4 | ⚠️ COMPLETED |
| 4 | Variant B | 27 | 36 | 63 | 1/4 | ⚠️ COMPLETED |
| 5 | Stress | 29 | 40 | 69 | 2/4 | ❌ PARTIAL |

**Execution average:** 68.0 / 100  
**Assertion pass rate:** 10 / 20  
**Static score:** 72 / 100  
**Final score:** 70 / 100 — ⚠️ Beta Only  
**Research veto:** PASS

This score is diagnostic. It does not make the candidate ready. Findings are ordered in the ledger below; exact identity is in [`source-identity.json`](source-identity.json).

## Executed versus static-only

Environment: Windows R 4.4.3 via `r.sh` (DESeq2 1.46.0, apeglm 1.28.0, ashr 2.2.63, EnhancedVolcano 1.24.0, ggplot2 4.0.3, ggrepel 0.9.8) and Python 3.12.13 via `py.sh` (matplotlib 3.11.2, adjustText 1.4.0, sanbomics 0.1.0 isolated under `py-extra/sanbomics`); fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt`; pdffonts 26.07.0 in WSL `dv-cli`. Input: public airway dataset, `public-data/derived/airway_dds_condition.rds` (29,391 genes).

| Surface | Classification | Evidence |
|---|---|---|
| `scripts/volcano_phd.R` (lfcShrink, volcano, MA, cairo_pdf, EnhancedVolcano) | executed | `scripts/v1_phd.R`, `logs/v1_phd.log`, `logs/pdffonts_phd.log`; figures `out/phd/` opened |
| `scripts/volcano_plot.R` `volcano_plot()` | executed | same run; `out/phd/volcano_plot_fn.png` opened |
| lfcShrink apeglm / ashr / svalue / contrast claims, shrunken vs MLE | executed | `logs/v1_phd.log` |
| EnhancedVolcano colours and selectLab gotcha | executed | `logs/v1_phd.log`; `out/phd/enhancedvolcano_skill.png` opened |
| `scripts/ma_plot.py`, adjustText volcano | executed | `scripts/v2_python.py`, `logs/v2_python.log`; `out/py/` opened |
| `sanbomics.tools.volcano` (SKILL.md) | executed, failed (does not exist; import fails) | `logs/v2_python.log`; source grep of `tools.py` |
| edgeR `glmTreat`, ggbreak, plotMA (SKILL.md/failure-modes mentions) | static-only (exercised by the tooling smoke, not re-run here; plotMA PNG written) | n/a |

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS — No fabricated values: counts (451 Up / 366 Down at padj<0.05 and |LFC|>1; 3,994 padj<0.05) equal independent recomputation on the airway dds.
  - practice_boundaries: PASS — Visualization skill; no clinical or prescriptive output.
  - methodological_ground: PASS — Shrinkage and FDR guidance is sound; the shipped plots draw an FDR line on a raw-p axis and clip significant points (VOL-001, VOL-002), filed as defects with fixes, not inverted conclusions.
  - code_usability: PASS — All three scripts ran on airway with exit 0 and correct counts; defects are plot-content bugs (VOL-001..VOL-003, VOL-008).

## Static categories

- functional_suitability: 9/12 — Strong method content (shrinkage, s-value, label rank); the headline volcano_phd.R clips 49 significant genes and mis-draws the threshold (VOL-001, VOL-002).
- reliability: 8/12 — Runs cleanly but requires a pre-built dds and fails silently on clipped data and on EnhancedVolcano colouring (VOL-001, VOL-003).
- performance_context: 5/8 — SKILL.md is long (11.6 KB) with repeated points across SKILL, usage-guide, failure-modes and reconciliation; references are routed.
- agent_usability: 11/16 — Operational read-order rule is helpful, but its own rule 3 (threshold matches axis) fails for the shipped script (VOL-002).
- human_usability: 6/8 — Readable tips; several factual statements are wrong or stale (VOL-004..VOL-007).
- security: 11/12 — Local reads and writes only; no credentials or network.
- maintainability: 8/12 — Scripts duplicate the volcano logic with drifting behaviour (cap, colours); no tests.
- agent_specific: 14/20 — Precise trigger, decision tables and failure modes; several claims did not reproduce on current DESeq2 and EnhancedVolcano.

## Detailed outputs

### Input 1 — Canonical: scripts/volcano_phd.R end-to-end on the real airway dds (29,391 genes, apeglm shrinkage, volcano, MA, cairo_pdf, EnhancedVolcano)

**Status:** COMPLETED — Counts correct; the volcano clips 49 significant points and 9 of 13 labels pile at the top edge, and the dashed line sits 0.7 log10 units below the colour boundary (VOL-001, VOL-002).  
**Scores:** Basic 28/40 | Specialized 38/60 | Total 66/100

**Assertions:**

- PASS — Up/Down counts equal an independent recount (451 / 366) (Exact match on apeglm results.)
- FAIL — No significant point is hidden by the y cap (y_cap = 50 hides 49 significant points (max -log10 p 135.7); opened volcano_phd_view.png.)
- FAIL — The horizontal dashed line coincides with the colour boundary (Line at 1.301 on raw p; smallest coloured point 2.015.)
- PASS — volcano.pdf and ma_plot.pdf written with cairo_pdf (1.04 MB and 1.07 MB; fonts embedded.)

### Input 2 — Variant A: volcano_plot() function on shrunken airway results with default top-10 and a gene list

**Status:** COMPLETED — Opened volcano_plot_fn.png: legible Okabe-Ito Up/Down/NS with non-overlapping labels; only the threshold line mismatch remains.  
**Scores:** Basic 32/40 | Specialized 44/60 | Total 76/100

**Assertions:**

- PASS — Top-10 labels are chosen by combined rank among significant genes (10 labels, all significant.)
- PASS — Labels do not overlap and use max.overlaps = Inf (Opened figure; no collisions.)
- PASS — Gene-list labelling works for TP53, MYC, BRCA1 (3 labelled points.)
- FAIL — Threshold line matches the colour boundary (1.301 versus 2.015.)

### Input 3 — Edge: Shrinkage method claims on airway: apeglm vs MLE, ashr contrast, svalue, apeglm contrast error

**Status:** COMPLETED — apeglm pulls low-count genes to zero (median |LFC| 0.76 to 0.01) but 108 genes grow and the maximum rises 9.51 to 10.99; ashr returns no svalue column (VOL-004, VOL-007).  
**Scores:** Basic 28/40 | Specialized 38/60 | Total 66/100

**Assertions:**

- PASS — Shrinkage pulls low-count genes toward zero (baseMean<5: median |MLE| 0.76, |shrunken| 0.01.)
- FAIL — Shrinkage never inflates an LFC (108 genes with |shrunken| > |MLE|; ALOX15B 9.51 to 10.99.)
- FAIL — lfcShrink(type='ashr') returns an svalue column (Columns baseMean, log2FoldChange, lfcSE, pvalue, padj; svalue only from apeglm with svalue=TRUE.)
- PASS — s < 0.005 approximates padj < 0.05 and apeglm rejects contrast= (4,684 versus 3,994 genes, 3,842 shared; apeglm contrast error reproduced.)

### Input 4 — Variant B: EnhancedVolcano route: SKILL.md call, colours, selectLab gotcha

**Status:** COMPLETED — Plot renders and labels correctly, but Up and Down share one colour and the selectLab-threshold gotcha does not reproduce (VOL-003, VOL-006).  
**Scores:** Basic 27/40 | Specialized 36/60 | Total 63/100

**Assertions:**

- PASS — EnhancedVolcano with y='padj' and the Skill's col vector draws and labels the selected genes (Opened enhancedvolcano_skill.png: 13 labels.)
- FAIL — Up and Down genes are coloured differently (colour by direction) (451 Up and 366 Down all class FC_P, #D55E00.)
- FAIL — A selectLab gene failing the thresholds is silently unlabeled (TSPAN6 (NS) was labelled on EnhancedVolcano 1.24.0.)
- FAIL — Y axis label matches the plotted quantity (Axis reads '-Log10 P' while y = padj.)

### Input 5 — Stress: Python route: ma_plot.py on 29,391 real rows, adjustText volcano, sanbomics claim

**Status:** PARTIAL — ma_plot and adjustText are correct; the named sanbomics.tools.volcano does not exist and sanbomics.tools fails to import (VOL-005); the 5 MB+ vector claim is not reproduced (VOL-008).  
**Scores:** Basic 29/40 | Specialized 40/60 | Total 69/100

**Assertions:**

- PASS — ma_plot colours exactly the padj < 0.05 genes orange (3,994 orange, 25,397 grey (padj NA included).)
- PASS — adjustText labels 12 top genes without overlap (0 overlapping pairs; opened adjusttext_volcano.png.)
- FAIL — sanbomics.tools.volcano exists and imports (tools.py has no volcano and fails with ModuleNotFoundError: pkg_resources; the function is sanbomics.plots.volcano.)
- FAIL — Vector scatter of 29,391 points gives a 5 MB+ PDF (445,526 B vector versus 34,780 B rasterised.)

## Key strengths

- Counts, labels and shrinkage behaviour reproduced exactly on the real airway dataset.
- volcano_plot() produces a clean, legible Okabe-Ito volcano with combined-rank labels.
- The decision content (apeglm vs ashr, s-value approximation, apeglm needs coef=) is largely verified against current DESeq2 1.46.

## Recommendations

- **[P1] VOL-001 volcano_phd.R clips significant points and their labels with an unconditional y cap** (inputs [1]): coord_cartesian(ylim = c(0, 50)) is applied regardless of the data: 49 significant genes (max -log10 p 135.7) vanish and 9 of 13 labels, including the top-ranked genes, pile at the top edge; the usage-guide says capped points remain visible at the edge. Fix: Apply the cap only when requested (y_cap = NULL by default), or squish with pmin(neg_log10_p, y_cap) plus a marker/axis break, and state the cap in the caption.
- **[P1] VOL-002 Shipped volcanoes draw the FDR line on a raw-p axis, contradicting the Skill** (inputs [1, 2]): Both R scripts plot -log10(pvalue) and draw the hline at -log10(fdr): line at 1.301, smallest coloured point at 2.015; SKILL.md says drawing the FDR line on raw p 'creates a meaningless line' and operational rule 3 asks that the line match the axis. Fix: Plot -log10(padj) on y (as for EnhancedVolcano) or draw the line at the smallest -log10(p) among padj < fdr genes and label it.
- **[P2] VOL-003 EnhancedVolcano example loses direction and mislabels the axis** (inputs [4]): col = c('grey60','#0072B2','#56B4E9','#D55E00') colours all 451 Up and 366 Down genes the same orange (class FC_P), against 'color by direction' and the ggplot volcano; y = 'padj' is labelled '-Log10 P'. Fix: Use colCustom per direction or document that EnhancedVolcano colours by class; set ylab = expression(-log[10]~adjusted~italic(P)).
- **[P2] VOL-004 ashr is said to return svalue; it does not** (inputs [3]): SKILL.md says lfcShrink(type='ashr') returns an svalue column and the usage-guide says to use ashr for s-values; DESeq2 1.46 ashr returns baseMean, log2FoldChange, lfcSE, pvalue, padj only. s-values come from lfcShrink(type='apeglm', svalue = TRUE). Fix: State that svalue comes from apeglm with svalue=TRUE (or from ashr::ash lfsr) and correct the decision-tree row.
- **[P2] VOL-005 sanbomics.tools.volcano does not exist** (inputs [5]): SKILL.md names sanbomics.tools.volcano; the function is sanbomics.plots.volcano and sanbomics.tools fails to import without pkg_resources. Fix: Name sanbomics.plots.volcano (and note the optional dependency) or drop the mention.
- **[P2] VOL-006 EnhancedVolcano selectLab-threshold gotcha does not reproduce** (inputs [4]): Gotcha 1 (repeated in SKILL.md, failure-modes.md, usage-guide, the script comment and the error table) says selectLab genes failing pCutoff/FCcutoff are silently unlabeled; on 1.24.0 the failing gene TSPAN6 was labelled. Fix: Remove or version-qualify the gotcha and the manual-layer workaround.
- **[P2] VOL-007 Shrinkage is described as only pulling toward zero** (inputs [3]): apeglm raised |LFC| for 108 of 29,391 genes and the maximum from 9.51 (MLE) to 10.99 (ALOX15B), while the text says well-estimated genes are 'essentially untouched' and the unshrunken estimate is always the inflated one. Fix: Add a sentence that apeglm uses a different estimator and can exceed the MLE for a few genes; compare against the MLE before reporting extremes.
- **[P2] VOL-008 Rasterization guidance is not implemented and its size claim is overstated** (inputs [1, 5]): volcano_phd.R comments say to rasterize above 5000 features and that ggsave raster needs ggplot2 3.5+, but no layer is rasterized (volcano.pdf 1.04 MB); '5MB+ PDFs crash Illustrator' is not reproduced (29,391 vector points = 0.45 MB). Fix: Wrap the point layer in ggrastr::rasterise or drop the comment; replace '5MB+' with the measured vector/raster ratio.

## Ordered finding ledger

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
