> **Audit record for `bio-data-visualization-ggplot2-fundamentals`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/ggplot2-fundamentals) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-ggplot2-fundamentals

Generated: 2026-09-20  |  source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/ggplot2-fundamentals`  |  Category: Data Analysis  |  Mode: A  |  Complexity: Moderate (N=5)

Runtime: R 4.4.3 via `r.sh` (ggplot2 4.0.3 default) and `r-gg35.sh` (ggplot2 3.5.2); every script in `run/`, logs `run/*.4.0.3.log` / `*.3.5.2.log`, figures in `run/out_<version>/`.

## Skill veto
T1 stability PASS, T2 contract PASS (name + description present), T3 determinism PASS (plots deterministic; jitter/ggrepel unseeded, P2), T4 security PASS.

Shipped means present: `SKILL.md`, `usage-guide.md`, `examples/publication_figures.R` all exist; nothing points at a missing file. Related skills named (color-palettes, multipanel-figures, distribution-plots, volcano-and-ma-plots, heatmaps-clustering) exist in the folder.

## Static score: 70 / 100

| category | score | note |
|---|---|---|
| functional_suitability | 8/12 | Covers grammar, geoms, scales, facets, theme, tidy eval, ggtext, export. Correctness 2/4: five verified factual errors (ggtext \u2212 string, geom_point(rasterize=TRUE), aes(color='red') 'blue', ggrepel N>10 claim, label_log on free-y panels) plus a nonsense axis-line tip |
| reliability | 7/12 | Version-drift note says to introspect, but there is no error handling or verification step; silent failures (unknown parameter rasterize, inert scale_color_manual, {{ }} with strings) are not called out |
| performance_context | 6/8 | 283-line SKILL.md plus a short usage guide, one example; a little repetition between SKILL.md and usage-guide.md |
| agent_usability | 10/16 | Clear layered structure and a good Common Failure Modes section; inconsistent doctrine (cairo_pdf/mm/Okabe-Ito in SKILL.md, default pdf/inches/Set1/Set2/NPG colours in the shipped example), no instruction to open or verify the output |
| human_usability | 6/8 | Natural trigger wording and example prompts; strict-example forgiveness is fine for R, but the usage guide's 'panel.grid.off' and 'remove top/right axis lines with element_line()' would mislead |
| security | 11/12 | No credentials or network; tidy eval used correctly (.data pronoun, no eval(parse())); writes only to paths the caller supplies |
| maintainability | 8/12 | One SKILL.md, one usage guide, one example file, clean separation; no tests or version-pinned expectations, example not exercised by anything |
| agent_specific | 14/20 | Description precise; related skills are named and exist; jitter and ggrepel are unseeded so figures are not reproducible; no escape hatch for when a figure is better made elsewhere or how to check it |

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 32 | 48 | 80 | 3/5 PASS | ⚠️ |
| 2 | Variant A | 30 | 44 | 74 | 3/5 PASS | ⚠️ |
| 3 | Variant B | 36 | 52 | 88 | 4/5 PASS | ✅ |
| 4 | Edge | 32 | 46 | 78 | 3/5 PASS | ⚠️ |
| 5 | Stress | 30 | 44 | 74 | 3/5 PASS | ⚠️ |

**Execution Average: 78.8 / 100**  |  **Assertion Pass Rate: 16/25 (64%)**

Layer 1 average 32.0/40 (floor 28), Layer 2 average 46.8/60 (floor 42), static 70 (floor 70), execution avg 78.8 (floor 75), assertion rate 64% (floor 80%: **missed**).

## Final
Static 70 x 0.4 = 28.0; dynamic 78.8 x 0.6 = 47.3; **FINAL 75 / 100**. Numeric score 75 is in the Limited Release band, but the assertion pass rate 16/25 (64%) is below the 80% Limited Release floor in scoring_rubric.md section 5, so the grade drops one tier to Beta Only. No veto fired and no P0 is open.

**Grade: Beta Only, not deployable. No veto. No open P0.** Research Veto: M1 PASS, M2 PASS, M3 PASS, M4 PASS.

## Execution detail

### Input 1 — Canonical: publication volcano of real airway results
**Prompt:** "Make a publication figure of the airway dexamethasone DESeq2 results: log2 fold change vs -log10 p, Okabe-Ito colours for up/down/NS, label the top 10 genes, rich-text axis titles, save as an 89 mm wide PDF and a 300 dpi PNG."
**Code:** `run/i1_canonical.R` (theme_pub, ggrepel with max.overlaps = Inf, ggtext element_markdown, `ggsave(..., device = cairo_pdf)` exactly as in SKILL.md).
**What ran / printed (ggplot2 4.0.3; 3.5.2 identical):**
```
Down 497  NS 17200  Up 541   (19,772 genes, 1,534 NA padj dropped)
SKILL.md y-label string as R sees it:  \u2212log<sub>10</sub>(*p*)   -> literal backslash-u2212: TRUE
[PASS] colour counts Up/Down/NS match input: 541/497/17200 vs 541/497/17200
[PASS] all Up-colour points have log2FC > 1, all Down < -1
[PASS] 10 labels drawn ... are the 10 smallest padj
PDF i1_fix.pdf: MediaBox 252 x 198 pt (88.9 x 69.8 mm); FontFile2_truetype 3; Type3 0; basefonts Arial-ItalicMT, ArialMT
PDF i1_default.pdf (ggsave without device): Type1_unembedded 2 (Helvetica, Helvetica-Oblique), FontFile 0
PNG i1_fix.png: 1051 x 826 px, nonwhite 0.099
ggsave(width=89, height=70) with no units -> error "Dimensions exceed 50 inches"
```
**Opened** `run/out_4.0.3/i1_asis.png`: y title reads `\u2212log10(p)`; `i1_fix.png`: `-log10(p)` with italic p; the ten Ensembl labels overlap each other at 89 mm.
**Scores:** Basic 32/40 | Specialized 48/60 | Total 80.

- [PASS] Colour mapping matches the input: 541 Up / 497 Down / 17,200 NS, all Up points have log2FC > 1 — layer_data colours counted against an independent dplyr classification of the CSV
- [PASS] cairo_pdf output is 89 x 70 mm with embedded TrueType fonts and no Type 3 — pdfinfo.py: MediaBox 252 x 198 pt (88.9 x 69.8 mm), 3 FontFile2, 0 Type3; default ggsave gives unembedded Helvetica, as the Skill says
- [PASS] PNG is 89 mm at 300 dpi (1051 x 827 px), non-blank — 1051 x 826 px, nonwhite 0.099, opened
- [FAIL] The ggtext y-axis title from SKILL.md renders a minus sign — '\u2212' inside single quotes in R source is a literal backslash-u2212; the opened PNG shows '\u2212log10(p)'
- [FAIL] Top-10 gene labels are legible and not overplotted — max.overlaps = Inf forces all 10 labels but ENSG ids overlap each other in the opened 89 mm PNG; Skill gives no label-size or force guidance

### Input 2 — Variant A: faceted box + jitter, free y, log10 (synthetic, seed 42; `data/synthetic_expression_by_tissue.csv`)
**Prompt:** "Faceted boxplot of expression per tissue (3 tissues x 3 conditions, n = 12) with overlaid jitter, log10 y axis, each panel with its own y range, colour-blind-safe colours."
**Code:** `run/i2_facets.R`: the SKILL.md 'Grammar in Layers' block verbatim, then a corrected version using the Skill's own rules.
```
verbatim block: aes names x,y only -> scale_color_manual inert; boxplot outlier points drawn = 2 (doubled under jitter)
Liver y labels via label_log(): NA | 10^3 | 10^3.48 | 10^4 | 10^4.48 | NA
corrected: [PASS] 3 panels 1x3; free_y ranges [724, 36290] / [43.8, 1316] / [4.9, 163]
[PASS] boxplot middle/lower/upper equal quantile(type 7) of log10(raw) for 9 boxes; [PASS] whiskers = 1.5 IQR
[PASS] 108 jitter points, 36 per colour; Treatment (orange) higher than Control in Liver; planted 16,000 outlier inside y range
scale_y_continuous(trans='log10'): no deprecation warning on 4.0.3 or 3.5.2
PDF 182.7 x 69.8 mm, 2 TrueType fonts, 0 Type3
```
**Opened** `i2_verbatim.png` (black points, outliers doubled, ticks 10^3.48 / 10^3.7 / 10^2.7) and `i2_corrected.png` (violin + box + jitter coloured by condition, ticks 10^1.48 in Brain).
**Scores:** Basic 30/40 | Specialized 44/60 | Total 74.

- [PASS] facet_wrap(~tissue, ncol = 3, scales = 'free_y') yields 1 x 3 panels with independent y ranges — 3 panels ROW 1 COL 1-3; Liver/Brain upper y limits differ 223x
- [PASS] Box statistics equal quantile(type 7) of log10 of the raw data for all 9 boxes; whiskers follow 1.5 IQR — asserted on layer_data to 1e-9; stats are computed on the log scale
- [PASS] Corrected plot maps colour to condition correctly (Treatment orange sits highest in Liver, 36 points per colour) — layer_data colour vs y
- [FAIL] The Skill's verbatim block honours its own rule 'always suppress outliers when overlaying jitter' — block has no outlier.shape = NA: 2 outlier points drawn beneath the jitter (opened i2_verbatim.png)
- [FAIL] The verbatim block's scale_color_manual takes effect — no colour aesthetic is mapped, the scale is inert; points stay black (opened)

### Input 3 — Variant B: programmatic plots on a real PCA of airway counts
**Prompt:** "Write a function that takes the x and y variable names as strings and plots them, avoid the deprecated aes_string, then colour the airway PCA by treatment and shape by cell line with variance-explained labels."
**Code:** `run/i3_programmatic.R` (prcomp of log2 counts, 16,139 genes x 8 samples; PC1 42.2 %, PC2 22.4 %; SKILL.md functions verbatim, then the shipped `create_pca_plot`).
```
[PASS] plot_var(df,'PC1','PC2'): x,y equal prcomp scores; axis titles PC1/PC2
[PASS] plot_var2(df, PC1, PC2) identical; [PASS] !!sym() identical; [PASS] column "my var" works
aes_string warning: `aes_string()` was deprecated in ggplot2 3.0.0.
plot_var2(df, "PC1", "PC2") (strings): unique x = 1, unique y = 1 -> "All aesthetics have length 1, but the data has 8 rows" warning only
missing column PCX -> Column `PCX` not found in `.data`.
create_pca_plot: 4 trt/4 untrt colours, 4 shapes, "PC1 (42.2%)"; 10-level colour var -> "n too large, allowed maximum for palette Set1 is 9"
ggplot2 4.0.3: p$labels$x is NULL until build (use get_labs()); 3.5.2: "PC1"
```
**Opened** `i3_pca.png` and `i3_plotvar.png`: correct axes, legends, no overplotting.
**Scores:** Basic 36/40 | Specialized 52/60 | Total 88.

- [PASS] plot_var(df,'PC1','PC2') plots exactly the prcomp scores and titles the axes PC1/PC2 — layer_data x,y equal df$PC1,df$PC2; get_labs gives PC1/PC2 on 4.0.3 (p$labels is empty until build) and 3.5.2
- [PASS] plot_var2 with bare names and the !!sym() variant give identical data; a column with a space works — all.equal on layer data
- [PASS] aes_string() still draws but warns, as the Skill states — warning '`aes_string()` was deprecated in ggplot2 3.0.0.' on both ggplot2 versions
- [PASS] Shipped create_pca_plot colours by dex, shapes by cell, axis labels carry the variance explained — 4 trt / 4 untrt colours, 4 shapes, 'PC1 (42.2%)' matches prcomp; opened
- [FAIL] plot_var2 called with strings (the plot_var calling style) fails loudly — silently maps the constant string: one point column, only a 'aesthetics have length 1' warning; Skill does not warn

### Input 4 — Edge: 50,000-point scatter (synthetic, seed 7), rasterise and export
**Prompt:** "50,000 points scatter for a journal: keep axes and text as vector but rasterise the points; give me PDF, PNG and TIFF at single-column width."
**Code:** `run/i4_raster_export.R`, `run/tiffcheck.py`.
```
geom_point(rasterize = TRUE) warnings: Ignoring unknown parameters: `rasterize`      (3.5.2 and 4.0.3)
i4_inline.pdf   : 1,850,716 bytes, images 0
i4_rasterise.pdf:    85,303 bytes, images 2, FontFile2 1, Type3 0   (ggrastr::rasterise + cairo_pdf)
[PASS] rasterised layer carries 50,000 rows
ggsave tiff compression='lzw': ok; PIL: tiff_lzw, tag259=5, dpi (300,300), 1051x826
PNG 1051 x 826, nonwhite 0.287
```
**Opened** `i4_fig.png`: axes and ticks fine, but points saturate to a solid black cloud. PDF rendering could not be viewed (no poppler); its structure was checked from the PDF objects and the PNG twin was opened.
**Scores:** Basic 32/40 | Specialized 46/60 | Total 78.

- [FAIL] geom_point(..., rasterize = TRUE) rasterises the layer ('ggplot2 3.5+ inline') — warning 'Ignoring unknown parameters: rasterize' on 3.5.2 and 4.0.3; PDF has 0 images and 1,850,716 bytes
- [PASS] ggrastr::rasterise(geom_point(), dpi = 300) with cairo_pdf keeps axes/text vector and shrinks the file — 85,303 bytes, 2 image objects, fonts still TrueType, layer keeps 50,000 rows
- [PASS] ggsave TIFF with compression = 'lzw' is LZW at 300 dpi — PIL: tiff_lzw, tag 259 = 5, dpi (300, 300), 1051 x 826
- [PASS] PNG at 89 mm / 300 dpi is 1051 px wide and non-blank — 1051 x 826, nonwhite 0.287
- [FAIL] The recommended large-N figure is readable — with alpha 0.5 and default size 50,000 points saturate to a solid black blob (opened); the Skill advises rasterising but says nothing about overplotting

### Input 5 — Stress: shipped `examples/publication_figures.R` end to end
**Prompt:** "Using the example helpers, make the volcano of all airway genes, a boxplot of the top gene's counts by treatment, the PCA, and combine them into a labelled 3-panel and 4-panel figure; save PDF and PNG."
**Code:** `run/i5_example.R` (sources the example, real airway results incl. NA padj, real counts of ENSG00000152583).
```
[PASS] volcano draws 19,772 genes; colours 541 / 497 / 18,734 = independent count
[PASS] 10 labels = 10 smallest padj; [PASS] boxplot medians equal raw medians; jitter 8 points
dashed hline y = 1.30103 (p = 0.05); smallest -log10(p) among coloured points 1.956
genes above the dashed line yet grey (padj >= 0.05): 1617 of 5730 with p < 0.05   -> [FAIL] line != colour boundary
PNG 3000 x 2100 (3-panel A-C, 4-panel A-D), non-blank; save_publication_figure PDF: Helvetica, Symbol unembedded (Type1 x2), 0 images
```
**Opened** `i5_multi3.png`, `i5_multi4.png`, `i5_volcano.png`: layouts and tags correct; y label reads "− Log10 P − value" (spaced minus from `expression(-Log[10]~P-value)`); some ENSG labels overlap.
**Scores:** Basic 30/40 | Specialized 44/60 | Total 74.

- [PASS] Volcano colour counts equal an independent classification of all 19,772 genes (NA padj kept as NS) — 541 / 497 / 18,734
- [PASS] The 10 labels are the 10 smallest padj genes; boxplot medians equal the raw per-group medians — setequal on gene ids; medians all.equal
- [PASS] 3- and 4-panel patchwork figures build with tags A-C / A-D and saved PNGs are 3000 x 2100 and non-blank — opened i5_multi3.png and i5_multi4.png
- [FAIL] The volcano's dashed horizontal line marks the boundary that colours the points — line at -log10(0.05) = 1.301 (raw p) but colours use padj < 0.05: 1,617 genes above the line are grey, and coloured points start at 1.956
- [FAIL] save_publication_figure follows the Skill's doctrine (cairo_pdf, mm) — uses default pdf() in inches: PDF has unembedded Helvetica/Symbol (2 Type1, 0 FontFile); the example also draws '− Log10 P − value' with a spaced stray minus

## Block-by-block run of SKILL.md (`run/blocks.R`, both ggplot2 versions)
All Common Geoms, Scales (incl. scico batlow, viridis, gradient2, date), Facets (facet_grid 2 x 2 asserted), theme_pub and element_markdown blocks build without error. Only warning: `geom_line(size=)` -> "Using `size` aesthetic for lines was deprecated in ggplot2 3.4.0" (matches the Skill). Claims that failed: `aes(color='red')` renders `#F8766D` (salmon), the Skill says blue; default `geom_text_repel` on 400 dense labels drew 74 text grobs versus 405 with `max.overlaps = Inf` with no warning captured (`run/repel_count.R`), while 60 spread labels were all drawn with the default (`run/repel_test.R`), so N > 10 is not the trigger.

## ggplot2 4.0.3 vs 3.5.2
Everything above reproduced on both. Differences: `p$labels` is empty until build on 4.0 (use `get_labs()`); `theme_classic` on 4.0.3 already carries `panel.grid = element_blank()` (the Skill's line is redundant there, harmless on 3.5.2); `scale_y_continuous(trans=)` gave no deprecation warning on either.

## Recommendations

**[P1] ggtext '\u2212' label prints a literal backslash sequence**  
Observed in: [1]  
Problem: The Labels-with-ggtext snippet writes y = '\u2212log<sub>10</sub>(*p*)'; in R source that is backslash-u2212, so the opened PNG shows '\u2212log10(p)' instead of a minus sign.  
Root cause: A JSON/Python-style escape was pasted into an R single-quoted string.  
Fix: Use '\u2212' with a single backslash ('−log<sub>10</sub>(*p*)') or the literal character, and add a note to open the rendered label.

**[P1] geom_point(rasterize = TRUE) is not a ggplot2 3.5+ feature**  
Observed in: [4]  
Problem: The Common Geoms block claims inline rasterisation in ggplot2 3.5+. On 3.5.2 and 4.0.3 it is ignored ('Ignoring unknown parameters: rasterize'), the PDF stays all-vector (1.85 MB, 0 images) and the failure is only a warning.  
Root cause: Confusion between ggplot2 and ggrastr::geom_point_rast/rasterise.  
Fix: Delete the inline claim and keep only ggrastr::rasterise(geom_point(), dpi = 300); add that overplotting at large N also needs smaller points, alpha, hexbin or density.

**[P1] 'Grammar in Layers' block contradicts the Skill's own rules**  
Observed in: [2]  
Problem: The block calls scale_color_manual without mapping colour (inert), keeps default boxplot outliers under geom_jitter (drawn twice, against the 'always suppress' rule) and label_log() on default free-y breaks yields labels such as 10^3.48 and 10^2.7.  
Root cause: Block written as a syntax tour, never rendered.  
Fix: Map colour = condition, add outlier.shape = NA, and use scale_y_log10() with breaks_log() or plain labels; note the y-axis title 'Expression (log10)' clashes with 10^n tick labels.

**[P1] Shipped example: threshold line, save function and axis label**  
Observed in: [5]  
Problem: create_volcano draws the dashed line at -log10(fdr_threshold) on raw p while colouring by padj (1,617 genes above the line are grey); save_publication_figure uses default pdf() in inches (unembedded Helvetica) against the Skill's own cairo_pdf + mm rule; expression(-Log[10]~P-value) draws a spaced '− Log10 P − value'.  
Root cause: Example was not checked against the doctrine or against the numbers behind the plot.  
Fix: Drop the horizontal line or compute it as the smallest -log10(p) with padj < fdr; pass device = cairo_pdf and units = 'mm'; label with expression(-log[10](italic(p))).

**[P2] Failure-mode claims that do not reproduce**  
Observed in: []  
Problem: aes(color='red') points render #F8766D salmon (not 'blue'); ggrepel drops labels because of overlaps, not N > 10 (60 spread labels all drawn; 400 dense labels: 74 text grobs vs 405 with Inf) and no warning was observed at draw time in a non-interactive run.  
Root cause: Claims written from memory.  
Fix: Correct the colour statement, state the real trigger for label loss and tell the agent to count drawn labels.

**[P2] Minor doctrine and reproducibility gaps**  
Observed in: [1, 3]  
Problem: usage-guide tip 'remove top/right axis lines with theme(axis.line = element_line())' does nothing (theme_classic has no top/right axes); panel.grid = element_blank() is redundant on 4.0.3; jitter and ggrepel are unseeded; {{ x_var }} with a string silently draws a constant; Set1 in create_pca_plot fails above 9 groups; ggplot2 4.0 builds labels at print time so p$labels is empty.  
Root cause: Tips not tested against a rendered figure or the current ggplot2.  
Fix: Remove the axis-line tip, add position_jitter(seed=) and geom_text_repel(seed=), warn about {{ }} with strings, and note get_labs() for ggplot2 4.
