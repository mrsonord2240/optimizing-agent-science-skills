> **Audit record for `bio-data-visualization-multipanel-figures`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/multipanel-figures) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-multipanel-figures

Generated: 2026-09-20 | source: mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/multipanel-figures | Category: Data Analysis | Mode A | Moderate, N=5

Environment: R 4.4.3 (`r.sh`: ggplot2 4.0.3, patchwork 1.3.2, cowplot 1.2.0, gridExtra 2.3; `r-gg35.sh`: ggplot2 3.5.2), audit-private patchwork 1.2.0 and 1.1.3, Python 3.12 (`py.sh`: matplotlib 3.11.2), poppler in WSL `dv-cli` for PDF fonts, page size and text positions. Data are synthetic and seeded (`data/`). All scripts are in `run/`; figures in `out/`.

## Skill Veto
T1-T4 PASS (no eval/exec, no network, deterministic with seeds; frontmatter complete; all shipped files present: SKILL.md, usage-guide.md, 2 examples; all four Related Skills exist in the staging repo).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 31 | 44 | 75 | 4/5 PASS | ✅ |
| 2 | Variant A | 33 | 48 | 81 | 4/5 PASS | ✅ |
| 3 | Variant B | 27 | 38 | 65 | 3/5 PASS | ⚠️ |
| 4 | Edge | 27 | 40 | 67 | 2/5 PASS | ⚠️ |
| 5 | Stress | 26 | 36 | 62 | 2/5 PASS | ⚠️ |

**Static: 73 / 100 | Execution average: 70.0 / 100 | Final: 71.2 -> 71, Beta Only (not deployable) | Assertion pass rate: 15/25 | Research Veto: PASS | open P0: none**

Floors: static 73 (>= 70 ok), execution average 70.0 (< 75), assertions 60% (< 80%), so Limited Release is not reached; the grade follows the score (71).

## Detailed Outputs

### Input 1 - Canonical: Nature-style 2x2 patchwork figure (SKILL.md block as written), 180x140 mm cairo_pdf + 300 dpi PNG, synthetic data

**Executed:** Executed: run/i1_canonical.R (r.sh, ggplot2 4.0.3, patchwork 1.3.2), i1_tagsize.R and i1_tagsize_g35.R (ggplot2 3.5.2), i1_tag_defaulttheme.R; PDF read with poppler pdffonts/pdftotext -bbox in WSL dv-cli; PNG opened.

SKILL.md block run as written (titles SCATTER/BOX/HIST/COLOR added so panels can be identified in the PDF text layer), `ggsave(..., width=180, height=140, units="mm", device=cairo_pdf)`. Measured: PDF 510x396 pt = 179.9x139.7 mm; PNG 2125x1653 px; one legend; ArialMT TrueType embedded, 49 words of vector text. Text sizes: ticks 8.8 pt, axis titles 11 pt, tags 13.2 pt regular; tag size 6/10/20 give identical output (i1_tagsize*.R), `& theme(plot.tag=element_text(face="bold",size=6))` gives 6.7 pt bold. Same on ggplot2 3.5.2 and patchwork 1.2.0. PNG opened: four panels, tags a-d, one legend at right, not blank.

**Scores:** Basic 31/40 | Specialized 44/60 | Total 75/100

**Assertions:**
- [PASS] PDF page is 180x140 mm (510x396 pt) and the 300 dpi PNG is 2125x1653 px (180x140 mm) - pdfinfo 510x396 pt; PNG 2125x1653 vs expected 2126x1654
- [PASS] Four panels with tags a-d, each tag at the top-left of its own panel (checked with unique panel titles in the PDF text layer) - a/b/c/d sit left of SCATTER/BOX/HIST/COLOR at the correct row and column
- [PASS] guides='collect' yields exactly one legend with the right mapping (ctrl/trt from panel d) - one legend at right, group title once, ctrl/trt once
- [PASS] Text is vector and fonts are embedded (cairo_pdf) - ArialMT TrueType, emb=yes, 49 words in the text layer
- [FAIL] plot_annotation(theme = theme(plot.tag = element_text(face='bold', size=10))) styles the tags as documented - tag height identical for size 6, 10 and 20 (13.2 pt default), no Bold font in the PDF; same on ggplot2 3.5.2, patchwork 1.2.0 and 1.3.2, with or without theme_classic; only '& theme(plot.tag=...)' works

### Input 2 - Variant A: Layout operators: widths ratio, (p1|p2)/p3, design string, inset_element, cowplot plot_grid/rel_*/labels, gridExtra

**Executed:** Executed: run/i2_layout.R (all checks PASS), run/i2_cowplot_blocks.R; gridExtra arrangeGrob run separately to confirm it works (not shown by the Skill).

Panels coloured A-D, PNG bounding boxes: widths c(2,1) 398:198 px; (A|B)/C: C spans 644 px, A/B 298; design AAB/AAB/CCC: A 398x202, B 198x202, C 644x100; inset at x 476-685, y 74-148 within the parent; cowplot rel_widths c(1,2) 187:423; nested rel_heights c(1,1.2) 179:136 (1.32 panel ratio because the axis area is fixed). cowplot AUTO/auto and patchwork tag_levels A and i verified in the text layer; gridExtra arrangeGrob(layout_matrix) works but the Skill contains no gridExtra code.

**Scores:** Basic 33/40 | Specialized 48/60 | Total 81/100

**Assertions:**
- [PASS] plot_layout(widths=c(2,1)) gives panel widths 2:1 - 398 px vs 198 px (2.01)
- [PASS] Design string AAB/AAB/CCC gives A two columns and two rows, C the full width - A 398x202 px, B 198x202, C 644x100 (A/C height 2.02)
- [PASS] inset_element(p2, 0.6, 0.6, 1, 1) places the inset in the upper-right of the parent panel - inset x 476-685, y 74-148 inside parent 49-692 x 41-420
- [PASS] cowplot plot_grid labels 'AUTO'/'auto', nested rel_heights=c(1,1.2), rel_widths and patchwork tag_levels 'A'/'i' put the right letters on the right panels; ggsave cairo_pdf embeds Arial regular+bold - A-D, a-c and i-iii read at each panel's top-left in the text layer; bottom row 1.32x top (cell ratio 1.2)
- [FAIL] The description promises gridExtra composition; the Skill body shows how to use it - no gridExtra code anywhere in SKILL.md or the examples (only the install line); arrangeGrob(layout_matrix) works when tried

### Input 3 - Variant B: Python GridSpec, subfigures with colorbar, and 89 mm single-column blocks; PDF fonts and saved size

**Executed:** Executed: run/i3_python.py (py.sh, matplotlib 3.11.2): 7 PASS, 2 FAIL; PDFs read with pdffonts.

GridSpec block and subfigures block run as written (data supplied). Layout correct (ax2 spans cols 1-2, ax3 all; subfigure ratio 2.000; colorbar present). Saved: 180x120 mm block -> 182.9x122.9 mm, 89 mm block -> 91.9x62.9 mm because of `bbox_inches="tight"`; PDFs list DejaVu Type 3 fonts; with pdf.fonttype=42 CID TrueType (verified) but that is never set. Default `figure.constrained_layout.use` is False and the default layout engine is None (the "default-on in 3.6+" statement is wrong). PNGs opened: label c sits far left of the wide bar axes.

**Scores:** Basic 27/40 | Specialized 38/60 | Total 65/100

**Assertions:**
- [PASS] GridSpec(2,3): ax2 spans columns 1-2, ax3 spans all columns - ax2.x1 == ax3.x1 and ax3.x0 == ax1.x0
- [PASS] Subfigures width_ratios=[2,1]: 2 stacked left axes, image plus colorbar on the right - subfigure width ratio 2.000; right subfigure has 2 axes
- [PASS] Panel labels a/b/c are attached to their own axes (transAxes), lowercase, inside the canvas and not over tick labels - no overlap with tick labels or neighbours; but label c sits about 250 px left of its y axis versus 60 px for a (offset scales with axes width)
- [FAIL] The 180 mm and 89 mm blocks save at the stated width - 180x120 block saved as 182.9x122.9 mm; 89 mm block as 91.9x62.9 mm (bbox_inches='tight'); Nature single column is 89 mm
- [FAIL] PDFs use embedded TrueType/Type 42 fonts as the description promises - matplotlib default pdf.fonttype=3: every PDF from the blocks and both examples lists Type 3 fonts; rcParams['pdf.fonttype']=42 gives CID TrueType (verified) but appears only as a comment and a usage-guide bullet

### Input 4 - Edge: Every 'Per-Method Failure Modes' claim reproduced: tag alignment, shared legend, axes='collect', default device, units, cowplot align, old patchwork

**Executed:** Executed: run/i4_failmodes.R + i4_analyze.py, i4_collect.R + i4_collect_an.py, i4_collect_pw120.R, i4_oldpw.R (patchwork 1.2.0 and 1.1.3 installed into an audit-private lib), i4_extra.R. patchwork 1.1.3 cannot render at all with ggplot2 3.5.2 (add_guides error), so only its formals were tested.

Results (i4_analyze.log, i4_collect.log): default pdf device Helvetica unembedded (claim true); tag offsets differ 14.8 pt between panels with different y-label widths (symptom true) and 14.5 pt after the documented fix (fix ineffective; ignored inside the plot_annotation theme); different palettes give 2 legends, same palette 1, colour vs fill 2; dropping the second legend leaves a legend that is wrong for panel 2; cowplot align="v" aligns exactly (claim false); `axes="collect"` on the nested 2x2: 4 x and 4 y titles remain (patchwork 1.2.0 and 1.3.2), flat wrap_plots: 1 and 1, collect at every level: 2 and 2; patchwork 1.1.3 `plot_layout(axes=)` raises "unused argument" (not silent); ggsave default units errors "Dimensions exceed 50 inches"; patchwork 1.2.0 on ggplot2 4.0.3 errors "object is not a unit".

**Scores:** Basic 27/40 | Specialized 40/60 | Total 67/100

**Assertions:**
- [PASS] Default ggsave() pdf device gives non-embedded fonts; cairo_pdf embeds them - Helvetica Type 1 emb=no vs ArialMT TrueType emb=yes
- [PASS] Different scales with guides='collect' give duplicate legends; identical scales give one - ctrl label count 2 vs 1; a colour panel next to a fill panel with the same palette also stays at 2 legends (not mentioned)
- [FAIL] The documented fix for tag misalignment (plot.tag.position=c(0.02,0.98)) makes labels sit at the same offset from each panel - symptom reproduces (14.8 pt offset difference); after the fix 14.5 pt; inside plot_annotation(theme=) it is ignored entirely
- [FAIL] cowplot plot_grid(p_wide, p_narrow, align='v') misaligns and needs 'hv' - align='v' aligns stacked panels exactly (0 px left/right difference); only align='none' or 'h' is off
- [FAIL] plot_layout(axes='collect', axis_titles='collect') on the Skill's (p1+p2)/(p3+p4) collapses repeated axes when scales are shared - 4 x-titles and 4 y-titles remain (no-op) on patchwork 1.2.0 and 1.3.2; works on flat wrap_plots(ncol=2) (1 and 1) or when set at every nesting level (2 and 2)

### Input 5 - Stress: Both shipped examples end to end (R under ggplot2 4.0.3 and 3.5.2; Python) measured against the Skill's journal/font/legend advice

**Executed:** Executed from copies in run/scratch_r, scratch_r35, scratch_py: multi_panel_figure.R wrote Figure1.pdf/png in both ggplot2 versions; multipanel_matplotlib.py wrote 4 files. PNGs opened.

R example: Figure1.pdf/png written in both ggplot2 versions; 720x576 pt (254x203 mm), Helvetica/Helvetica-Bold/Symbol Type 1 not embedded; PNG opened: tags A-D correct, but the bottom legend row holds four legends and is clipped left ("significant") and right ("Upregulated"). Python example: multipanel_2x2 214.5x200.9 mm, multipanel_complex 254.6x181.9 mm, Type 3 fonts, correct A-D labels; the suptitle leaves a large blank band.

**Scores:** Basic 26/40 | Specialized 36/60 | Total 62/100

**Assertions:**
- [PASS] Both examples run from a clean copy and write non-blank PDF and PNG - R 3000x2400 px PNG 334 KB; Python 2534x2373 and 3007x2149 px; PNGs opened
- [PASS] Panel labels A-D sit on the intended panels in both examples - A/B/C/D at the top-left of Differential Expression/PCA/Top DE Genes/DE Summary; Python A-D likewise
- [FAIL] The R example's guides='collect' produces one shared legend and stays inside the page - four legends (significant, Group colour, Group fill, category) because legend.position='bottom' is re-applied to all and colour/fill do not merge; the row is clipped at both page edges
- [FAIL] Output size follows the Skill's journal spec (mm, <= 183 mm wide) - R example 254x203 mm (10x8 in, units='in'); Python 214x201 mm and 255x182 mm
- [FAIL] PDF fonts are embedded as the Skill's own advice requires - R: default pdf() device, Helvetica/Helvetica-Bold/Symbol Type 1 emb=no; Python: DejaVu Type 3 (its header comment mentions pdf.fonttype=42 but never sets it)

## Recommendations

- **[P1] plot_annotation(theme=plot.tag) is silently ignored** (inputs [1, 4]): The headline patchwork recipe sets bold size-10 tags through plot_annotation(theme=...); the PDF shows 13.2 pt regular tags for size 6, 10 and 20, on patchwork 1.2.0/1.3.2 and ggplot2 3.5.2/4.0.3. Fix: Show '& theme(plot.tag = element_text(face="bold", size=8))' (verified to work) and state the journal label size (8 pt) once; make every snippet match.
- **[P1] axes='collect' does nothing in the Skill's nested 2x2 form** (inputs [1, 4]): (p1+p2)/(p3+p4) + plot_layout(axes='collect', axis_titles='collect') leaves 4 x and 4 y titles even when all scales are identical (patchwork 1.2.0 and 1.3.2); the demo panels do not share scales anyway. Fix: Use wrap_plots(list, ncol=2) + plot_layout(axes='collect', axis_titles='collect') (verified: one x and one y title), or set plot_layout at every nesting level, and say collection needs identical scales.
- **[P1] Python blocks break the mm size and never set Type-42** (inputs [3, 5]): bbox_inches='tight' turns the 180 mm and 89 mm figures into 182.9 and 91.9 mm; pdf.fonttype is never set so every PDF has Type 3 fonts, although the description advertises Type-42 embedding. Fix: Add rcParams['pdf.fonttype']=42 to the block, drop bbox_inches='tight' (or keep labels inside the axes) and assert the saved size in mm.
- **[P1] Shipped examples violate the Skill's own rules** (inputs [5]): multi_panel_figure.R saves 10x8 in with the default pdf device (unembedded Helvetica) and produces four un-merged, clipped legends; multipanel_matplotlib.py is 12x8 in with Type 3 fonts and hspace/wspace instead of constrained layout. Fix: Rewrite both examples to 183 mm, units='mm', cairo_pdf / fonttype 42, a single merged legend (same aesthetic and palette across panels), and print the measured size.
- **[P1] Several failure-mode explanations are wrong or ineffective** (inputs [4]): Tag fix plot.tag.position=c(0.02,0.98) does not equalise offsets (14.5 pt vs 14.8 pt); cowplot align='v' does not fail as described; patchwork 1.1.3 raises 'unused argument' instead of silently ignoring axes=; ggsave with default units errors ('Dimensions exceed 50 inches') instead of writing a 180 in file; 'constrained_layout is default-on in 3.6+' is false (default layout engine is None). Fix: Re-test and correct each claim; for tag alignment use a tag position relative to the panel (plot.tag.location='panel') or a constant y-label width.
- **[P2] Inconsistent label/text sizes and column widths** (inputs [1, 3, 5]): Panel labels are 8 pt in the table, 9/10 pt in R snippets and 10/12/14 in Python; default text is 8.8-11 pt against the stated 5-7 pt; code uses 180 mm, not 183 (Nature) or 174 (Cell); Nature labels are called 'serif' while the code is sans. Fix: One size table (label, body, line) referenced by all snippets, use the per-journal widths from the sizing table, and drop 'serif'.
- **[P2] Promised coverage missing** (inputs [2, 3]): gridExtra, matplotlib shared legends/sharex/sharey and subplot_mosaic are named or implied but have no code; Python panel-label offsets in axes fraction differ with axes width. Fix: Add a short gridExtra/arrangeGrob block and a fig.legend/subplot_mosaic block, or narrow the description; use a fixed-point offset for labels.
- **[P2] Version notes incomplete** (inputs [4]): patchwork 1.2.0 (CRAN 2024-01-08, not 01-05) errors 'object is not a unit' under ggplot2 4.0.3, and 1.1.3 fails inside add_guides on ggplot2 3.5.2; dropping a legend with legend.position='none' is only safe when the mapping is identical. Fix: State patchwork >= 1.3 for ggplot2 4.x, correct the release date, and warn that dropping N-1 legends misleads when palettes differ.
