"""Builds eval_report_*_result.json and eval_viewer_*.md from the scored audit data below (2026-09-20)."""
import json, os
D = r'F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals'
NAME = 'bio-data-visualization-ggplot2-fundamentals'
SRC = 'mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/ggplot2-fundamentals'

A = lambda t, r, n: {"text": t, "result": r, "note": n}
inputs = [
 dict(index=1, type="Canonical", label="Publication volcano of real airway DESeq2 results, 89 mm cairo_pdf + 300 dpi PNG",
  status="COMPLETED", status_flag="\u26a0\ufe0f",
  note="Data and colours correct; SKILL.md's own ggtext y-label prints a literal backslash-u2212; top-10 Ensembl labels overlap at 89 mm",
  basic=32, specialized=48,
  assertions=[
   A("Colour mapping matches the input: 541 Up / 497 Down / 17,200 NS, all Up points have log2FC > 1", "PASS", "layer_data colours counted against an independent dplyr classification of the CSV"),
   A("cairo_pdf output is 89 x 70 mm with embedded TrueType fonts and no Type 3", "PASS", "pdfinfo.py: MediaBox 252 x 198 pt (88.9 x 69.8 mm), 3 FontFile2, 0 Type3; default ggsave gives unembedded Helvetica, as the Skill says"),
   A("PNG is 89 mm at 300 dpi (1051 x 827 px), non-blank", "PASS", "1051 x 826 px, nonwhite 0.099, opened"),
   A("The ggtext y-axis title from SKILL.md renders a minus sign", "FAIL", "'\\u2212' inside single quotes in R source is a literal backslash-u2212; the opened PNG shows '\\u2212log10(p)'"),
   A("Top-10 gene labels are legible and not overplotted", "FAIL", "max.overlaps = Inf forces all 10 labels but ENSG ids overlap each other in the opened 89 mm PNG; Skill gives no label-size or force guidance"),
  ]),
 dict(index=2, type="Variant A", label="Faceted box + jitter per tissue, free y, log10 axis (synthetic, seed 42)",
  status="COMPLETED", status_flag="\u26a0\ufe0f",
  note="Verbatim 'Grammar in Layers' block runs but scale_color_manual is inert, outliers are drawn twice and label_log() gives 10^3.48 style labels; corrected version verified",
  basic=30, specialized=44,
  assertions=[
   A("facet_wrap(~tissue, ncol = 3, scales = 'free_y') yields 1 x 3 panels with independent y ranges", "PASS", "3 panels ROW 1 COL 1-3; Liver/Brain upper y limits differ 223x"),
   A("Box statistics equal quantile(type 7) of log10 of the raw data for all 9 boxes; whiskers follow 1.5 IQR", "PASS", "asserted on layer_data to 1e-9; stats are computed on the log scale"),
   A("Corrected plot maps colour to condition correctly (Treatment orange sits highest in Liver, 36 points per colour)", "PASS", "layer_data colour vs y"),
   A("The Skill's verbatim block honours its own rule 'always suppress outliers when overlaying jitter'", "FAIL", "block has no outlier.shape = NA: 2 outlier points drawn beneath the jitter (opened i2_verbatim.png)"),
   A("The verbatim block's scale_color_manual takes effect", "FAIL", "no colour aesthetic is mapped, the scale is inert; points stay black (opened)"),
  ]),
 dict(index=3, type="Variant B", label="Programmatic plotting with tidy eval on a real PCA of airway counts",
  status="COMPLETED", status_flag="\u2705",
  note=".data[[var]], {{ }}, !!sym() all give identical layer data; missing column error names the column; {{ }} with strings silently draws a constant",
  basic=36, specialized=52,
  assertions=[
   A("plot_var(df,'PC1','PC2') plots exactly the prcomp scores and titles the axes PC1/PC2", "PASS", "layer_data x,y equal df$PC1,df$PC2; get_labs gives PC1/PC2 on 4.0.3 (p$labels is empty until build) and 3.5.2"),
   A("plot_var2 with bare names and the !!sym() variant give identical data; a column with a space works", "PASS", "all.equal on layer data"),
   A("aes_string() still draws but warns, as the Skill states", "PASS", "warning '`aes_string()` was deprecated in ggplot2 3.0.0.' on both ggplot2 versions"),
   A("Shipped create_pca_plot colours by dex, shapes by cell, axis labels carry the variance explained", "PASS", "4 trt / 4 untrt colours, 4 shapes, 'PC1 (42.2%)' matches prcomp; opened"),
   A("plot_var2 called with strings (the plot_var calling style) fails loudly", "FAIL", "silently maps the constant string: one point column, only a 'aesthetics have length 1' warning; Skill does not warn"),
  ]),
 dict(index=4, type="Edge", label="50,000-point scatter: rasterisation and PDF/PNG/TIFF export (synthetic, seed 7)",
  status="COMPLETED", status_flag="\u26a0\ufe0f",
  note="geom_point(rasterize = TRUE) is not a ggplot2 3.5+ feature: unknown parameter, points stay vector (1.85 MB); ggrastr recipe works (85 KB)",
  basic=32, specialized=46,
  assertions=[
   A("geom_point(..., rasterize = TRUE) rasterises the layer ('ggplot2 3.5+ inline')", "FAIL", "warning 'Ignoring unknown parameters: rasterize' on 3.5.2 and 4.0.3; PDF has 0 images and 1,850,716 bytes"),
   A("ggrastr::rasterise(geom_point(), dpi = 300) with cairo_pdf keeps axes/text vector and shrinks the file", "PASS", "85,303 bytes, 2 image objects, fonts still TrueType, layer keeps 50,000 rows"),
   A("ggsave TIFF with compression = 'lzw' is LZW at 300 dpi", "PASS", "PIL: tiff_lzw, tag 259 = 5, dpi (300, 300), 1051 x 826"),
   A("PNG at 89 mm / 300 dpi is 1051 px wide and non-blank", "PASS", "1051 x 826, nonwhite 0.287"),
   A("The recommended large-N figure is readable", "FAIL", "with alpha 0.5 and default size 50,000 points saturate to a solid black blob (opened); the Skill advises rasterising but says nothing about overplotting"),
  ]),
 dict(index=5, type="Stress", label="Shipped examples/publication_figures.R end to end: volcano, boxplot, PCA, 3- and 4-panel figure",
  status="COMPLETED", status_flag="\u26a0\ufe0f",
  note="Runs and the numbers are right, but the dashed threshold line is p = 0.05 while colours use padj < 0.05 (1,617 grey genes above it) and save_publication_figure breaks the Skill's own cairo_pdf/mm rule",
  basic=30, specialized=44,
  assertions=[
   A("Volcano colour counts equal an independent classification of all 19,772 genes (NA padj kept as NS)", "PASS", "541 / 497 / 18,734"),
   A("The 10 labels are the 10 smallest padj genes; boxplot medians equal the raw per-group medians", "PASS", "setequal on gene ids; medians all.equal"),
   A("3- and 4-panel patchwork figures build with tags A-C / A-D and saved PNGs are 3000 x 2100 and non-blank", "PASS", "opened i5_multi3.png and i5_multi4.png"),
   A("The volcano's dashed horizontal line marks the boundary that colours the points", "FAIL", "line at -log10(0.05) = 1.301 (raw p) but colours use padj < 0.05: 1,617 genes above the line are grey, and coloured points start at 1.956"),
   A("save_publication_figure follows the Skill's doctrine (cairo_pdf, mm)", "FAIL", "uses default pdf() in inches: PDF has unembedded Helvetica/Symbol (2 Type1, 0 FontFile); the example also draws '\u2212 Log10 P \u2212 value' with a spaced stray minus"),
  ]),
]
for i in inputs:
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_total"] = len(i["assertions"])
    i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
ap = sum(i["assertions_passed"] for i in inputs); at = sum(i["assertions_total"] for i in inputs)

cats = {
 "functional_suitability": (8, 12, "Covers grammar, geoms, scales, facets, theme, tidy eval, ggtext, export. Correctness 2/4: five verified factual errors (ggtext \\u2212 string, geom_point(rasterize=TRUE), aes(color='red') 'blue', ggrepel N>10 claim, label_log on free-y panels) plus a nonsense axis-line tip"),
 "reliability": (7, 12, "Version-drift note says to introspect, but there is no error handling or verification step; silent failures (unknown parameter rasterize, inert scale_color_manual, {{ }} with strings) are not called out"),
 "performance_context": (6, 8, "283-line SKILL.md plus a short usage guide, one example; a little repetition between SKILL.md and usage-guide.md"),
 "agent_usability": (10, 16, "Clear layered structure and a good Common Failure Modes section; inconsistent doctrine (cairo_pdf/mm/Okabe-Ito in SKILL.md, default pdf/inches/Set1/Set2/NPG colours in the shipped example), no instruction to open or verify the output"),
 "human_usability": (6, 8, "Natural trigger wording and example prompts; strict-example forgiveness is fine for R, but the usage guide's 'panel.grid.off' and 'remove top/right axis lines with element_line()' would mislead"),
 "security": (11, 12, "No credentials or network; tidy eval used correctly (.data pronoun, no eval(parse())); writes only to paths the caller supplies"),
 "maintainability": (8, 12, "One SKILL.md, one usage guide, one example file, clean separation; no tests or version-pinned expectations, example not exercised by anything"),
 "agent_specific": (14, 20, "Description precise; related skills are named and exist; jitter and ggrepel are unseeded so figures are not reproducible; no escape hatch for when a figure is better made elsewhere or how to check it"),
}
sub = sum(v[0] for v in cats.values())
sw = round(sub * 0.4, 1); dw = round(avg * 0.6, 1); score = round(sw + dw)

recs = [
 dict(priority="P1", title="ggtext '\\u2212' label prints a literal backslash sequence", observed_in=[1],
  problem="The Labels-with-ggtext snippet writes y = '\\u2212log<sub>10</sub>(*p*)'; in R source that is backslash-u2212, so the opened PNG shows '\\u2212log10(p)' instead of a minus sign.",
  root_cause="A JSON/Python-style escape was pasted into an R single-quoted string.",
  fix="Use '\\u2212' with a single backslash ('\u2212log<sub>10</sub>(*p*)') or the literal character, and add a note to open the rendered label."),
 dict(priority="P1", title="geom_point(rasterize = TRUE) is not a ggplot2 3.5+ feature", observed_in=[4],
  problem="The Common Geoms block claims inline rasterisation in ggplot2 3.5+. On 3.5.2 and 4.0.3 it is ignored ('Ignoring unknown parameters: rasterize'), the PDF stays all-vector (1.85 MB, 0 images) and the failure is only a warning.",
  root_cause="Confusion between ggplot2 and ggrastr::geom_point_rast/rasterise.",
  fix="Delete the inline claim and keep only ggrastr::rasterise(geom_point(), dpi = 300); add that overplotting at large N also needs smaller points, alpha, hexbin or density."),
 dict(priority="P1", title="'Grammar in Layers' block contradicts the Skill's own rules", observed_in=[2],
  problem="The block calls scale_color_manual without mapping colour (inert), keeps default boxplot outliers under geom_jitter (drawn twice, against the 'always suppress' rule) and label_log() on default free-y breaks yields labels such as 10^3.48 and 10^2.7.",
  root_cause="Block written as a syntax tour, never rendered.",
  fix="Map colour = condition, add outlier.shape = NA, and use scale_y_log10() with breaks_log() or plain labels; note the y-axis title 'Expression (log10)' clashes with 10^n tick labels."),
 dict(priority="P1", title="Shipped example: threshold line, save function and axis label", observed_in=[5],
  problem="create_volcano draws the dashed line at -log10(fdr_threshold) on raw p while colouring by padj (1,617 genes above the line are grey); save_publication_figure uses default pdf() in inches (unembedded Helvetica) against the Skill's own cairo_pdf + mm rule; expression(-Log[10]~P-value) draws a spaced '\u2212 Log10 P \u2212 value'.",
  root_cause="Example was not checked against the doctrine or against the numbers behind the plot.",
  fix="Drop the horizontal line or compute it as the smallest -log10(p) with padj < fdr; pass device = cairo_pdf and units = 'mm'; label with expression(-log[10](italic(p)))."),
 dict(priority="P2", title="Failure-mode claims that do not reproduce", observed_in=[],
  problem="aes(color='red') points render #F8766D salmon (not 'blue'); ggrepel drops labels because of overlaps, not N > 10 (60 spread labels all drawn; 400 dense labels: 74 text grobs vs 405 with Inf) and no warning was observed at draw time in a non-interactive run.",
  root_cause="Claims written from memory.",
  fix="Correct the colour statement, state the real trigger for label loss and tell the agent to count drawn labels."),
 dict(priority="P2", title="Minor doctrine and reproducibility gaps", observed_in=[1, 3],
  problem="usage-guide tip 'remove top/right axis lines with theme(axis.line = element_line())' does nothing (theme_classic has no top/right axes); panel.grid = element_blank() is redundant on 4.0.3; jitter and ggrepel are unseeded; {{ x_var }} with a string silently draws a constant; Set1 in create_pca_plot fails above 9 groups; ggplot2 4.0 builds labels at print time so p$labels is empty.",
  root_cause="Tips not tested against a rendered figure or the current ggplot2.",
  fix="Remove the axis-line tip, add position_jitter(seed=) and geom_text_repel(seed=), warn about {{ }} with strings, and note get_labs() for ggplot2 4."),
]

rep = {
 "meta": {
  "skill_name": NAME,
  "description": "Build publication-quality figures in R with ggplot2 using the grammar of graphics (data + aesthetics + geometries + scales + facets + themes) with CVD-safe palettes, cairo_pdf TrueType embedding, programmatic aes via tidy evaluation, and the theme_classic publication baseline. Use when producing static figures in R for papers, presentations, or reports.",
  "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "A",
  "complexity": "Moderate", "n_inputs": 5, "source": SRC,
  "audit_type": "first audit (unmodified upstream GPTomics/bioSkills)", "executed": True,
  "execution_note": "Executed 5/5 inputs plus a block-by-block run of every SKILL.md snippet. R 4.4.3 via r.sh (ggplot2 4.0.3, ggtext 0.2.0, ggrepel 0.9.8, ggrastr 1.0.2, patchwork 1.3.2) and every script re-run under r-gg35.sh (ggplot2 3.5.2); only differences: p$labels is empty until build on 4.0 and theme_classic's panel.grid element. Each figure was asserted on ggplot_build() layer data against the input (real Bioconductor airway DESeq2 results and counts; synthetic sets labelled per input), PDFs inspected with run/pdfinfo.py (fonts, MediaBox, images), TIFF with PIL, and the key PNGs opened. Shipped example run from run/skill (copy), clone untouched."
 },
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {
   "applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "References (Wickham 2010 JCGS 19(1):3-28, Wickham 2016 ggplot2 2nd ed, Wilkinson 2005) are real; no fabricated statistic or DOI. Factual errors found (ggtext string, rasterize, 'blue') are recorded as P1/P2, not integrity failures."},
   "practice_boundaries": {"result": "PASS", "detail": "Plotting Skill for research data; no diagnostic, prescriptive or patient-level content."},
   "methodological_ground": {"result": "PASS", "detail": "No principled fallacy. The example volcano's dashed line at raw p = 0.05 beside padj-based colouring is a mislabelled threshold, recorded P1, not a fallacy that inverts a conclusion."},
   "code_usability": {"result": "PASS", "detail": "Every R block and the shipped example parse and run on ggplot2 4.0.3 and 3.5.2. Faulty behaviour (literal \\u2212 label, ignored rasterize parameter, inert scale) produces a figure or warning rather than a crash and each has a working alternative documented in the recommendations."}
  }
 },
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
 "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": ap, "total": at},
  "inputs": [dict(i) for i in inputs]},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": "Beta Only", "grade_symbol": "\u26a0\ufe0f",
  "deployable": False, "veto_override": False,
  "grade_note": "Numeric score %d is in the Limited Release band, but the assertion pass rate %d/%d (%.0f%%) is below the 80%% Limited Release floor in scoring_rubric.md section 5, so the grade drops one tier to Beta Only. No veto fired and no P0 is open." % (score, ap, at, 100 * ap / at)},
 "key_strengths": [
  "Core grammar, tidy evaluation (.data[[var]], {{ }}, !!sym()), facet, scale and theme guidance is correct: all 30+ snippets build on ggplot2 4.0.3 and 3.5.2 and the numbers behind the plots match the input",
  "cairo_pdf and mm-based export advice is verified: 89 x 70 mm PDF, 3 embedded TrueType fonts, 0 Type 3; default ggsave leaves unembedded Helvetica exactly as claimed",
  "ggrastr::rasterise recipe cuts a 50,000-point PDF from 1.85 MB to 85 KB with vector text intact; TIFF LZW verified",
  "Common Failure Modes section targets real pitfalls (units, aes vs constant, aes_string, linewidth) and the aes_string and linewidth warnings reproduce as described",
 ],
 "recommendations": recs,
}
json.dump(rep, open(os.path.join(D, 'eval_report_%s_result.json' % NAME), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

# ---------- viewer ----------
L = []
w = L.append
w("# Eval Viewer \u2014 %s\n" % NAME)
w("Generated: 2026-09-20  |  source: `%s`  |  Category: Data Analysis  |  Mode: A  |  Complexity: Moderate (N=5)\n" % SRC)
w("Runtime: R 4.4.3 via `r.sh` (ggplot2 4.0.3 default) and `r-gg35.sh` (ggplot2 3.5.2); every script in `run/`, logs `run/*.4.0.3.log` / `*.3.5.2.log`, figures in `run/out_<version>/`.\n")
w("## Skill veto\nT1 stability PASS, T2 contract PASS (name + description present), T3 determinism PASS (plots deterministic; jitter/ggrepel unseeded, P2), T4 security PASS.\n")
w("Shipped means present: `SKILL.md`, `usage-guide.md`, `examples/publication_figures.R` all exist; nothing points at a missing file. Related skills named (color-palettes, multipanel-figures, distribution-plots, volcano-and-ma-plots, heatmaps-clustering) exist in the folder.\n")
w("## Static score: %d / 100\n" % sub)
w("| category | score | note |\n|---|---|---|")
for k, v in cats.items():
    w("| %s | %d/%d | %s |" % (k, v[0], v[1], v[2]))
w("\n## Summary table\n")
w("| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|")
for i in inputs:
    w("| %d | %s | %d | %d | %d | %d/%d PASS | %s |" % (i["index"], i["type"], i["basic"], i["specialized"], i["total"], i["assertions_passed"], i["assertions_total"], i["status_flag"]))
w("\n**Execution Average: %s / 100**  |  **Assertion Pass Rate: %d/%d (%.0f%%)**\n" % (avg, ap, at, 100 * ap / at))
w("Layer 1 average %.1f/40 (floor 28), Layer 2 average %.1f/60 (floor 42), static %d (floor 70), execution avg %s (floor 75), assertion rate %.0f%% (floor 80%%: **missed**).\n" % (
  sum(i["basic"] for i in inputs) / 5, sum(i["specialized"] for i in inputs) / 5, sub, avg, 100 * ap / at))
w("## Final\nStatic %d x 0.4 = %s; dynamic %s x 0.6 = %s; **FINAL %d / 100**. %s\n" % (sub, sw, avg, dw, score, rep["final"]["grade_note"]))
w("**Grade: Beta Only, not deployable. No veto. No open P0.** Research Veto: M1 PASS, M2 PASS, M3 PASS, M4 PASS.\n")

w("## Execution detail\n")
w("""### Input 1 \u2014 Canonical: publication volcano of real airway results
**Prompt:** "Make a publication figure of the airway dexamethasone DESeq2 results: log2 fold change vs -log10 p, Okabe-Ito colours for up/down/NS, label the top 10 genes, rich-text axis titles, save as an 89 mm wide PDF and a 300 dpi PNG."
**Code:** `run/i1_canonical.R` (theme_pub, ggrepel with max.overlaps = Inf, ggtext element_markdown, `ggsave(..., device = cairo_pdf)` exactly as in SKILL.md).
**What ran / printed (ggplot2 4.0.3; 3.5.2 identical):**
```
Down 497  NS 17200  Up 541   (19,772 genes, 1,534 NA padj dropped)
SKILL.md y-label string as R sees it:  \\u2212log<sub>10</sub>(*p*)   -> literal backslash-u2212: TRUE
[PASS] colour counts Up/Down/NS match input: 541/497/17200 vs 541/497/17200
[PASS] all Up-colour points have log2FC > 1, all Down < -1
[PASS] 10 labels drawn ... are the 10 smallest padj
PDF i1_fix.pdf: MediaBox 252 x 198 pt (88.9 x 69.8 mm); FontFile2_truetype 3; Type3 0; basefonts Arial-ItalicMT, ArialMT
PDF i1_default.pdf (ggsave without device): Type1_unembedded 2 (Helvetica, Helvetica-Oblique), FontFile 0
PNG i1_fix.png: 1051 x 826 px, nonwhite 0.099
ggsave(width=89, height=70) with no units -> error "Dimensions exceed 50 inches"
```
**Opened** `run/out_4.0.3/i1_asis.png`: y title reads `\\u2212log10(p)`; `i1_fix.png`: `-log10(p)` with italic p; the ten Ensembl labels overlap each other at 89 mm.
**Scores:** Basic 32/40 | Specialized 48/60 | Total 80.
""")
for a in inputs[0]["assertions"]:
    w("- [%s] %s \u2014 %s" % (a["result"], a["text"], a["note"]))
w("""
### Input 2 \u2014 Variant A: faceted box + jitter, free y, log10 (synthetic, seed 42; `data/synthetic_expression_by_tissue.csv`)
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
""")
for a in inputs[1]["assertions"]:
    w("- [%s] %s \u2014 %s" % (a["result"], a["text"], a["note"]))
w("""
### Input 3 \u2014 Variant B: programmatic plots on a real PCA of airway counts
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
""")
for a in inputs[2]["assertions"]:
    w("- [%s] %s \u2014 %s" % (a["result"], a["text"], a["note"]))
w("""
### Input 4 \u2014 Edge: 50,000-point scatter (synthetic, seed 7), rasterise and export
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
""")
for a in inputs[3]["assertions"]:
    w("- [%s] %s \u2014 %s" % (a["result"], a["text"], a["note"]))
w("""
### Input 5 \u2014 Stress: shipped `examples/publication_figures.R` end to end
**Prompt:** "Using the example helpers, make the volcano of all airway genes, a boxplot of the top gene's counts by treatment, the PCA, and combine them into a labelled 3-panel and 4-panel figure; save PDF and PNG."
**Code:** `run/i5_example.R` (sources the example, real airway results incl. NA padj, real counts of ENSG00000152583).
```
[PASS] volcano draws 19,772 genes; colours 541 / 497 / 18,734 = independent count
[PASS] 10 labels = 10 smallest padj; [PASS] boxplot medians equal raw medians; jitter 8 points
dashed hline y = 1.30103 (p = 0.05); smallest -log10(p) among coloured points 1.956
genes above the dashed line yet grey (padj >= 0.05): 1617 of 5730 with p < 0.05   -> [FAIL] line != colour boundary
PNG 3000 x 2100 (3-panel A-C, 4-panel A-D), non-blank; save_publication_figure PDF: Helvetica, Symbol unembedded (Type1 x2), 0 images
```
**Opened** `i5_multi3.png`, `i5_multi4.png`, `i5_volcano.png`: layouts and tags correct; y label reads "\u2212 Log10 P \u2212 value" (spaced minus from `expression(-Log[10]~P-value)`); some ENSG labels overlap.
**Scores:** Basic 30/40 | Specialized 44/60 | Total 74.
""")
for a in inputs[4]["assertions"]:
    w("- [%s] %s \u2014 %s" % (a["result"], a["text"], a["note"]))
w("""
## Block-by-block run of SKILL.md (`run/blocks.R`, both ggplot2 versions)
All Common Geoms, Scales (incl. scico batlow, viridis, gradient2, date), Facets (facet_grid 2 x 2 asserted), theme_pub and element_markdown blocks build without error. Only warning: `geom_line(size=)` -> "Using `size` aesthetic for lines was deprecated in ggplot2 3.4.0" (matches the Skill). Claims that failed: `aes(color='red')` renders `#F8766D` (salmon), the Skill says blue; default `geom_text_repel` on 400 dense labels drew 74 text grobs versus 405 with `max.overlaps = Inf` with no warning captured (`run/repel_count.R`), while 60 spread labels were all drawn with the default (`run/repel_test.R`), so N > 10 is not the trigger.

## ggplot2 4.0.3 vs 3.5.2
Everything above reproduced on both. Differences: `p$labels` is empty until build on 4.0 (use `get_labs()`); `theme_classic` on 4.0.3 already carries `panel.grid = element_blank()` (the Skill's line is redundant there, harmless on 3.5.2); `scale_y_continuous(trans=)` gave no deprecation warning on either.

## Recommendations
""")
for r in recs:
    w("**[%s] %s**  \nObserved in: %s  \nProblem: %s  \nRoot cause: %s  \nFix: %s\n" % (r["priority"], r["title"], r["observed_in"], r["problem"], r["root_cause"], r["fix"]))
open(os.path.join(D, 'eval_viewer_%s.md' % NAME), 'w', encoding='utf-8').write('\n'.join(L))
print(sub, avg, sw, dw, score, ap, at)
