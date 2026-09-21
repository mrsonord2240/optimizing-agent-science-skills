> **Audit record for `bio-data-visualization-volcano-and-ma-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@019953e](https://github.com/mrsonord2240/bioSkills/tree/019953e9ca90f6f6f69e3f5a9cd19a5c1b9dc6be/data-visualization/volcano-and-ma-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-volcano-and-ma-plots (FIRST AUDIT)

Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@019953e9ca90f6f6f69e3f5a9cd19a5c1b9dc6be:data-visualization/volcano-and-ma-plots` (unmodified upstream; extracted with `git archive` to `run\skill\`, `diff -r --strip-trailing-cr` identical to the clone; no file written in the clone, no `__pycache__`).
Env: `F:\OpenScience\audit-envs\data-visualization` (R 4.4.3 via `r.sh`: DESeq2 1.46.0, EnhancedVolcano 1.24.0, ggplot2 4.0.3, ggrepel 0.9.8, apeglm 1.28.0, ashr 2.2.63, limma, ALL; Python 3.12 via `py.sh`: pandas 3.0.6, matplotlib 3.11.2, adjustText 1.4.0).
Category: Data Analysis (3) | Mode A (agent writes code from the Skill's patterns; one shipped example) | Complexity: Moderate (4 task types, 3 files) -> 5 inputs
Data: real Bioconductor `airway` (dex vs untreated, DESeq2 fit here, `data\airway_objs.rds`) and real `ALL` (limma); ONE table is SYNTHETIC and labelled so (`data\synthetic_extreme_p.csv`, seed 20260920, extreme p-values).

## Result

| | |
|---|---|
| Static | **74** / 100 |
| Execution average | **77.8** / 100 (L1 avg 31.2/40, L2 avg 46.6/60) |
| Final | **76** (29.6 + 46.7 = 76.3) |
| Grade | **Beta Only** (numeric Limited Release, one tier down) |
| Deployable | **false** |
| Vetoes | none (Skill veto PASS, Research veto PASS) |
| Open P0 / P1 / P2 | 0 / 3 / 6 |
| Assertions | 17/24 (70.8%) |

Grade note: 76.3 is Limited Release numerically, but the assertion pass rate (70.8%) is under the 80% Limited Release floor (scoring_rubric section 5), so the grade drops exactly one tier. Static, execution, L1 and L2 floors are met. The failing assertions are almost all the same handful of tool-behaviour claims and two design defects, each easy to fix; nothing fabricated, no crash on real data, no P0.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: SKILL ggplot volcano on airway apeglm | 33 | 48 | 81 | 4/5 | pass |
| 2 | Variant A: EnhancedVolcano block + shrinkage/selectLab claims | 31 | 47 | 78 | 3/5 | pass |
| 3 | Variant B: plotMA (R) + ma_plot (Python), fan diagnostic | 35 | 53 | 88 | 4/5 | pass |
| 4 | Stress: shipped `volcano_phd.R` + synthetic extreme p | 29 | 43 | 72 | 3/4 | warn (<75) |
| 5 | Scope boundary: limma table + missing Python volcano | 28 | 42 | 70 | 3/5 | warn (<75) |

**Execution Average: 77.8 / 100** | **Assertion Pass Rate: 17/24** | Executed 5/5.

Static breakdown: functional 8/12, reliability 8/12, performance/context 5/8, agent usability 12/16, human usability 6/8, security 11/12, maintainability 8/12, agent-specific 16/20 (notes in the JSON).

## Skill veto and shipped-means-present

- T1-T4 PASS: no eval/exec/shell/network, no credentials, deterministic (no RNG in the Skill; airway fit is deterministic). frontmatter has `name`, `description`, `license`.
- Gate 8: the folder ships `SKILL.md`, `usage-guide.md`, `examples/volcano_phd.R` (no `references/`, `scripts/`, `assets/` pointed at). All seven Related Skills exist in staging. One dangling wiki link: `[[api_gotchas]]` (SKILL.md line 121) points at nothing (P2). `sanbomics.tools.volcano` (line 24) is named but not installed and no code uses it.
- Gate 7: visualization Skill, no diagnostic/prescriptive content.
- Every code block parses: 4 R blocks (`i6_parse_R.out`), the Python block (`ast.parse`) and `volcano_phd.R`. Blocks were extracted from SKILL.md by `run\extract_blocks.py` into `run\blocks\` and run verbatim (`source()` / `exec`), not retyped. Block 01 (`lfcShrink` apeglm coef / ashr contrast) was run as the same two calls inside `i0_prep_airway.R`.

## Detailed Outputs

### Input 1 - Canonical: ggplot2 + ggrepel volcano (block 02, verbatim) on real airway
**Prompt:** "Plot a volcano for my DESeq2 results with shrunken LFC and FDR < 0.05; label the top 10 hits by combined rank." Then: "Label DUSP1, KLF15, PER1, TSC22D3, FKBP5 and TP53."
**Run:** `run\i0_prep_airway.R` (DESeq2 fit, `lfcShrink` apeglm/ashr/normal, symbols), `run\i1_ggplot_volcano.R`. Figures: `figs\i1_volcanoA_default.png`, `figs\i1_volcanoB_symbols.png` (both opened).
**Printed (trimmed):**
```
points drawn: 33469 (non-NA pvalue rows in res: 33469)
class counts among plotted: Down 365  NS 32654  Up 450
[PASS] Up/Down count on plot == independent recompute; x range == shrunken LFC range; y max == -log10(min pvalue)
hline y = 1.30103 ; vline x = -1 1
labelled (symbols): SAMHD1,ZBTB16,DUSP1,SPARCL1,VCAM1,KLF15,CACNB2,PER1,MAOA,GPX3
Run B labelled: FKBP5,DUSP1,TP53,TSC22D3,KLF15,PER1   (TP53: LFC -0.40, padj 3e-4)
```
`run\i1b_line_recount.R`: 5,677 genes lie above the drawn line; 1,596 of them have padj >= 0.05 and 88 have NA padj (1,684 not FDR-significant); 3,178 padj<0.05 genes are grey by design (|LFC| <= 1). The largest -log10 p among padj >= 0.05 genes is 1.95, which is the real padj boundary; the drawn line is at 1.30 (raw p 0.05).
**Reading of the figure:** non-blank, thresholds and colours as coded, labels are the right genes (dex-responsive ZBTB16, DUSP1, KLF15, PER1), no housekeeping. Two Ensembl labels partly touch. With Ensembl rownames the labels are unreadable IDs and the Skill has no ID-to-symbol step (the auditor mapped with org.Hs.eg.db).
**Scores:** Basic 33/40 | Specialized 48/60 | Total 81/100
**Assertions:** 4/5 (FAIL: the hline does not separate FDR-significant from other points, the Skill's own "raw p threshold line on adjusted axis" failure mode).

### Input 2 - Variant A: EnhancedVolcano block (block 03) and the Skill's stated gotchas
**Prompt:** "Use EnhancedVolcano on my apeglm results, y = padj, label TP53, MYC, BRCA1. Why might a listed gene not be labelled?"
**Run:** `run\i2_enhancedvolcano.R`, `i2b_ev_followup.R`, `i2c_selectlab_matrix.R`, `i2d_ashr_svalue.R`. Figures `figs\i2_enhancedvolcano_block03.png`, `figs\i2c_selectlab_nonpassing.png` (opened).
**Printed (trimmed):**
```
layer1 rows: 22392  non-NA y: 14905  res non-NA padj: 14905  NA padj: 7487   -> NA padj dropped exactly as the Skill says
hline y: 1.30103  (on the padj axis)   colored min y: 1.30 (p-value class), 1.39 (both)
labels drawn (block 03): BRCA1,MYC,TP53
selectLab test: DUSP1 (both) TRUE, TP53 (p only) TRUE, GAPDH (padj 0.43, LFC -0.14) TRUE, ACTB TRUE
   FGR/MYH16 (padj NA) are in the label data but have no y, so nothing is drawn
ashr as written: baseMean,log2FoldChange,lfcSE,pvalue,padj      ashr svalue=TRUE: baseMean,log2FoldChange,lfcSE,svalue
apeglm padj identical to results() padj: TRUE ;  s<0.005: 3921 (ashr) / 4681 (apeglm) vs padj<0.05: 3993
formals(lfcShrink)$type = c("apeglm","ashr","normal")      -> 'apeglm is the default' holds in 1.46
```
**Verdicts:** confirmed: NA-padj drop, y = padj line placement, apeglm default and coef requirement, ashr accepting contrast, s<0.005 tracking padj<0.05. **Not reproduced (checked by layer data, rendered PNG and source):** "Gotcha 1 / selectLab filters through pCutoff AND FCcutoff" (stated five times in SKILL.md, the usage-guide and the example comment). EnhancedVolcano 1.24.0 matches `lab %in% selectLab` only. Also wrong: "ashr also returns svalue column" (needs `svalue = TRUE`, which replaces pvalue/padj). Minor: the y axis reads "-Log10 P" though it plots padj (no `ylab` set); default `xlim` asymmetric as the Skill says.
**Scores:** Basic 31/40 | Specialized 47/60 | Total 78/100
**Assertions:** 3/5 (FAIL: selectLab filter claim; ashr svalue comment).

### Input 3 - Variant B: MA plots (R plotMA block 04, Python ma_plot block 05)
**Prompt:** "Make an MA plot to check whether low-count genes have inflated fold changes; do it in R and in Python."
**Run:** `run\i3a_ma_R.R`, `run\i3b_ma_python.py`. Figures `figs\i3a_plotMA_block04.png`, `figs\i3b_ma_python_raw_vs_apeglm.png` (opened).
**Printed (trimmed):**
```
plotMA: padj<0.05: 3993 of 33469 ; genes with |shrunken LFC|>5: 5  -> 5 open triangles at the ylim edge in the PNG
baseMean<10: |LFC|>2 fraction raw MLE 0.0473, apeglm 0.0018 ; baseMean>=1000 median |LFC| raw 0.1815, apeglm 0.1655
Python: drawn ns 29476 sig 3993 total 33469
[PASS] sig count == padj<0.05 (3993); x == log10(baseMean); y == log2FoldChange; layers rasterized; y=0 line present
baseMean<5: max|LFC| raw 5.19, apeglm 2.91   [PASS] fan diagnostic
PDF rasterized=True 33,492 B ; rasterized=False 498,466 B   [FAIL] Skill claim '5MB+ PDFs'
```
The side-by-side PNG shows the fan (raw) collapsing to a funnel (apeglm) as the Skill describes. `ma_plot()` hard-codes the y label "(shrunken)" (mislabels a raw table). The "stripe = batch confound" and "asymmetry = normalisation failure" MA heuristics are asserted without support.
**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100
**Assertions:** 4/5 (FAIL: the 5 MB PDF claim, measured 0.50 MB).

### Input 4 - Stress: shipped `examples/volcano_phd.R` and extreme p-values
**Prompt:** "Run the PhD-level volcano + MA example on my dds; cap the y-axis because a few genes have p ~ 1e-200."
**Run:** `run\i4_shipped_example.R` (`sys.source` of the shipped file with `dds` in the environment; once with Ensembl rownames, once with symbols), `i4b_pdf_check.py`, `i4c_extreme_synth.R` (SYNTHETIC), `i4d_repel_default.R`. The PDFs are in `run\scratch4\{ensembl,symbols}\` (opened); `figs\i4c_*.png` opened.
**Printed (trimmed):**
```
[ensembl] labels requested (13): TP53,MYC,BRCA1,ENSG00000152583,...   genes_of_interest present in data: (none)   <- silent
[symbols] genes_of_interest present: TP53,MYC,BRCA1
points with -log10 p > y_cap(50): 49 of 22392 (all Up/Down); labelled ones above the cap: 9 of 13 ; max -log10 p 135.7
[FAIL] no significant gene hidden by the y cap   coord ylim: -2.5 52.5
[FAIL] drawn hline coincides with padj<0.05 boundary  (line 1.30 vs 1.91)
volcano.pdf 773,238 B, ma_plot.pdf 784,245 B (symbols); /TrueType 3 and 2, /Type3 0 in every PDF
SYNTHETIC extreme table: p==0: 1, min p 1e-200 ; volcano_plot() ok; Inf point drawn at the top edge and labelled
coord_cartesian(0,50): points inside panel 19992 of 20000 ; significant beyond cap: 9  -> [FAIL] 'stay visible at the edge'
sqrt transform runs (max y 14.14); ggbreak::scale_y_break runs on this stack
ggrepel default max.overlaps, 60 labels: no warning on real or synthetic data (claim not reproduced, not scored)
```
`volcano.pdf` opened: with the shipped cap the 49 strongest genes are gone and 9 of 13 labels are stacked into an illegible overprint on the top edge with leader lines to nothing (DUSP1, KLF15, PER1, SPARCL1 ...). The example applies the cap unconditionally although its comment calls it optional. The example also plots raw p against an FDR line, and admits it in a comment ("approximate").
**Scores:** Basic 29/40 | Specialized 43/60 | Total 72/100
**Assertions:** 3/4 (FAIL: top hits and labels stay visible/readable under the cap).

### Input 5 - Scope boundary: limma microarray table and a Python volcano
**Prompt:** "This is a limma topTable from the ALL microarray data (BCR/ABL vs NEG); volcano it. Also give me the matplotlib/adjustText version."
**Run:** `run\i5_limma_scope.R` (real `ALL`, 79 B-cell arrays, 12,625 probes, 183 adj.P.Val<0.05), `run\i5b_prep_symbols.R` + `i5b_python_volcano.py`. Figures `figs\i5_limma_volcano_renamed.png`, `figs\i5b_python_volcano.png`, `figs\i5_limma_enhancedvolcano.png` (opened).
**Printed (trimmed):**
```
(a) volcano_plot(topTable) as delivered -> Failed to evaluate ... in case_when(): object 'padj' not found      [FAIL]
(b) after renaming logFC/P.Value/adj.P.Val/AveExpr -> Up 31 / Down 2, equals the table                       [PASS]
    labelled probes: 1635_at,1636_g_at,1674_at (ABL1) ,...  ; x label 'log2 fold change (shrunken)'
    max|limma logFC - plain difference of group means| = 2.22e-15                                            [FAIL: 'limma shrinks the LFC']
(c) EnhancedVolcano(x='logFC', y='adj.P.Val') draws 12625 points                                             [PASS]
Python volcano (Skill ships none): Up=450 Down=365, labels SPARCL1,SAMHD1,CACNB2,GPX3,MAOA,DUSP1,KLF15,ZBTB16,VCAM1,PER1  [PASS]
```
The Skill's decision-tree rows "Proteomics (limma/MSstats): Already moderated; plot logFC vs adj.P.Val directly" and "limma is the original shrunken-LFC method" are wrong about LFC (eBayes moderates the variance), and the Skill's function cannot take those columns. `sanbomics.tools.volcano` is not installed (`ModuleNotFoundError`) and was not run.
**Scores:** Basic 28/40 | Specialized 42/60 | Total 70/100
**Assertions:** 3/5.

## Research Veto

M1 PASS (no fabricated DOI/statistic; sampled citations real), M2 PASS (n/a), M3 PASS (classification by padj and |LFC| is computed correctly; the raw-p axis and limma claims are recorded as P1 defects, not conclusion-inverting), M4 PASS (all code parses and ran).

## Recommendations (also in the JSON)

- **P1** Threshold line on the wrong axis quantity: `volcano_plot()` and the example plot raw p, colour by padj, draw the FDR line at 1.30 (real boundary 1.95; 1,684 non-significant genes above it).
- **P1** Shipped y cap hides the 49 top genes and overprints 9 of 13 labels; `coord_cartesian` does not "render at the edge".
- **P1** Not usable on the non-DESeq2 tables it claims (case_when error on limma columns, hard-coded "shrunken" label) and limma LFC described as shrunken (it is not).
- P2 EnhancedVolcano `selectLab` filter claim does not reproduce (five places); real cause of a missing label is NA padj.
- P2 `ashr also returns svalue` false without `svalue=TRUE`, which then drops pvalue/padj.
- P2 Python volcano advertised but not shipped; `sanbomics` unverified.
- P2 Ensembl IDs vs symbol labels, example needs an undefined `dds`, dangling `[[api_gotchas]]`.
- P2 Smaller items: 5 MB PDF claim (0.50 MB), EnhancedVolcano `-Log10 P` label for padj, hard-coded "(shrunken)" in `ma_plot`, Dudoit "JASA" vs Stat Sin, unsupported MA heuristics, inconsistent MA colouring rule.
- P2 SKILL.md and usage-guide.md duplicate the same tips (no references/ layer).

## Reproduce

Run order (each `.out` beside its script holds the raw output): `extract_blocks.py`, `i0_prep_airway.R` (about 2 min), `i1_ggplot_volcano.R`, `i1b_line_recount.R`, `i2_enhancedvolcano.R`, `i2b_ev_followup.R`, `i2c_selectlab_matrix.R`, `i2d_ashr_svalue.R`, `i3a_ma_R.R`, `i3b_ma_python.py`, `i4_shipped_example.R`, `i4b_pdf_check.py`, `i4c_extreme_synth.R`, `i4d_repel_default.R`, `i5_limma_scope.R`, `i5b_prep_symbols.R`, `i5b_python_volcano.py`, `i6_parse_R.R`, `finalize_report.py`. R through `r.sh`, Python through `py.sh`.
