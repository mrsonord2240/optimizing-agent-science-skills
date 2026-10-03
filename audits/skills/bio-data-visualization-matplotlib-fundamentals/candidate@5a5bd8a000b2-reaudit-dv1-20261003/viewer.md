> **Audit record for `bio-data-visualization-matplotlib-fundamentals`**
> - Audited working candidate `5a5bd8a000b20722cdcf14b12a5adb381bbecad2d16d952870cbbdf8dddb4cc8`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/data-visualization/matplotlib-fundamentals), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-matplotlib-fundamentals

Generated: 2026-10-03  
Audit type: independent final re-audit (certification), fresh auditor  
Exact candidate content SHA-256: `5a5bd8a000b20722cdcf14b12a5adb381bbecad2d16d952870cbbdf8dddb4cc8`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 35 | 54 | 89 | 4/5 | ✅ COMPLETED |
| 2 | Variant A | 36 | 56 | 92 | 5/5 | ✅ COMPLETED |
| 3 | Edge | 36 | 56 | 92 | 4/4 | ✅ COMPLETED |
| 4 | Variant B | 30 | 47 | 77 | 3/4 | ✅ COMPLETED |
| 5 | Stress | 29 | 48 | 77 | 4/5 | ✅ COMPLETED |

**Execution average:** 85.4 / 100 (Layer 1 avg 33.2 / 40, Layer 2 avg 52.2 / 60)  
**Assertion pass rate:** 20 / 23 (87.0 percent)  
**Static score:** 84 / 100  
**Final score:** 85 / 100 - ⭐ Production Ready  
**Research veto:** PASS

## Readiness decision

**Not candidate-ready** for the exact identity above. The numeric thresholds are met (final 85, static 84, execution average 85.4, Layer 1 average 33.2, Layer 2 average 52.2, no veto, no P0) but the assertion pass rate is 20/23 = 87 percent, below the 90 percent floor. Three new P2 findings (MPL-007, MPL-008, MPL-009), all text-only fixes, cause the three failed assertions. Route to `fix-scientific-skill` (text-only edits to chart-recipes.md, failure-modes.md and scripts/matplotlib_phd.py), then a fresh re-audit.

## Prior findings (initial audit 146857c3b9b5, Beta Only 74), each retested here

| ID | Sev | Verdict | Independent evidence (scripts/logs) |
|---|---|---|---|
| MPL-001 | P1 | resolved | all five PDFs exact mm; Saving block 89.0 x 70.0 mm; bbox tight reproduces ~92 mm only when set (r1, r3, r4) |
| MPL-002 | P1 | resolved | dict palette: 0 colour mismatches on 18,238 airway points in three row orders; legend maps equal (r3) |
| MPL-003 | P2 | resolved | ax.set_rasterization_zorder works, fig method absent; large-N 1.5 MB vs 24 KB reproduces at default savefig dpi (r4, r5) |
| MPL-004 | P2 | resolved | svg.fonttype none: 14 <text>; control 0 (r3) |
| MPL-005 | P2 | resolved | rendered text 6 and 7 pt only; pdffonts TrueType only; no tab10 (r1) |
| MPL-006 | P2 | resolved | all five SKILL.md python blocks run verbatim in three orders; Color block uses fig.colorbar (r3) |

Fixer-added inline changes retested: the 180 mm grid (180.0 mm), the `data.items()` grid snippet and missing numpy import (blocks run verbatim), and the `.theme({**sns.axes_style('ticks'), **mpl.rcParams})` line (r7: without it so.Plot draws 12/11 pt, with it 7/6 pt). The `legend=False` tradeoff is real (the legend leaves the 89 mm page for every engine) but leaves the figure uninterpretable, so it is recorded as MPL-007.

## Executed versus static-only

| Surface | Class | Evidence |
|---|---|---|
| scripts/matplotlib_phd.py (five PDFs) | executed | r1, pdffonts, figures opened |
| SKILL.md python blocks on real airway table, three row orders | executed | r3 |
| SKILL.md Saving block (pdf, png, tiff, svg, eps) | executed | r3 |
| references/chart-recipes.md (11 snippets) | executed, one failed | r4 (MPL-008) |
| references/failure-modes.md claims | executed, one failed | r4, r5, r6 (MPL-009) |
| seaborn.objects legend placement alternatives | executed | r2, figure opened |
| usage-guide.md prompts and prerequisites | static-only | prose, no runnable code |

Environment: fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 (Python 3.12.13, matplotlib 3.11.2, seaborn 0.13.2, numpy 2.5.3, pandas 3.0.6); pdffonts through the recorded WSL dv-cli route; Arial resolves on Windows. Input: staged real airway DESeq2 results (19,772 rows, 18,238 after dropping NA padj or pvalue).

## Veto review

- Skill veto: PASS.
- Research veto: PASS
  - scientific_integrity: PASS - No fabricated identifiers or results; the volcano example uses clearly labelled synthetic stand-ins, and the real airway DESeq2 table gave 541 Up, 497 Down, 17,200 NS.
  - practice_boundaries: PASS - Plotting guidance only; no clinical or prescriptive content.
  - methodological_ground: PASS - Colour-to-category binding verified per drawn point on 18,238 airway genes in three row orders (0 mismatches); no methodological fallacy found.
  - code_usability: PASS - scripts/matplotlib_phd.py and all five SKILL.md python blocks run verbatim on 3.11.2; one chart-recipes.md fragment (set_xticks vs three labels) raises ValueError, a localized literal defect recorded as MPL-008, not an unrunnable-code failure.

## Static categories

- functional_suitability: 10/12 - Covers rcParams, OO API, layout, fonts, saving and seaborn; page sizes and colour binding now correct, but the Tick frequency recipe and the tight_layout/set_layout_engine failure-mode entry are wrong (MPL-008, MPL-009).
- reliability: 10/12 - Shipped script and SKILL.md blocks run clean; the recommended set_layout_engine fix raises ZeroDivisionError once a colorbar exists (MPL-009).
- performance_context: 7/8 - Compact SKILL.md routed to two references; guardrails still repeat across SKILL.md, usage-guide and failure-modes.
- agent_usability: 13/16 - Dict-palette and no-bbox guardrails are explicit and verified; the seaborn.objects example ships without a colour key (MPL-007).
- human_usability: 7/8 - Readable prompts and tips; the pyplot mixing in the Color block is gone.
- security: 11/12 - Local file writes only; no credentials, network or shell strings.
- maintainability: 10/12 - One example script mirrors SKILL.md; no automated check ties documented claims to behaviour, which is how MPL-008 and MPL-009 survived.
- agent_specific: 16/20 - Precise trigger, routed references, version note; escape-hatch guidance for non-matplotlib or interactive output is thin.

## Detailed outputs

### Input 1 - Canonical: scripts/matplotlib_phd.py unchanged: rcParams, 89 mm scatter, 2x3 grid, Crameri heatmap, seaborn scatter, seaborn.objects

**Status:** COMPLETED - All five PDFs exact mm and TrueType; seaborn.objects figure opened and has no colour key.  
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100

**Assertions:**

- PASS - The five PDFs have page sizes equal to the stated mm (89x70, 180x110, 89x90, 89x70, 89x70). (MediaBox measured 89.0x70.0, 180.0x110.0, 89.0x90.0, 89.0x70.0, 89.0x70.0 mm.)
- PASS - pdffonts reports embedded TrueType only and no Type 3 rows for every PDF. (Every row CID TrueType, emb yes; ArialMT and Arial-BoldMT (Arial resolved on Windows).)
- PASS - All rendered text is within the stated 5-7 pt range. (Text artists across open figures are 6.0 and 7.0 pt only.)
- PASS - The multipanel, heatmap and seaborn scatter figures are legible and unclipped with correct tags, symmetric colorbar and class legend. (Rendered at 150 dpi and opened: tags a-f bold, vik colorbar symmetric, legend NS/Down/Up in grey/blue/orange.)
- FAIL - volcano_so.pdf is interpretable without outside information. (legend=False leaves three unlabelled colours; reader cannot tell Up from Down from NS (MPL-007).)

### Input 2 - Variant A: Every SKILL.md python block verbatim on the real airway DESeq2 table (18,238 genes) with rows reordered three ways

**Status:** COMPLETED - All five blocks ran verbatim in Up-first, NS-first and shuffled order; colours bound by name every time.  
**Scores:** Basic 36/40 | Specialized 56/60 | Total 92/100

**Assertions:**

- PASS - All five SKILL.md python blocks execute verbatim without error or warning in each row order. (3 orders x 5 blocks clean; stand-ins x, y, data, panel_data supplied only for undefined names.)
- PASS - Every drawn seaborn point carries the colour of its own class. (18,238 facecolors compared to the dict palette per row: 0 mismatches in all three orders.)
- PASS - Legend text-to-colour mapping equals the dict palette in each order, for seaborn and seaborn.objects. (NS grey, Down #0072B2, Up #D55E00 in all orders.)
- PASS - scatter.pdf is 89 x 70 mm. (Measured 89.0 x 70.0 mm.)
- PASS - The Color block (batlow and symmetric RdBu_r with quantile vmax) renders without error. (Ran as block 4; cmcrameri imported.)

### Input 3 - Edge: SKILL.md Saving block at 89 x 70 mm: PDF, PNG, TIFF, SVG, EPS

**Status:** COMPLETED - Page and pixel sizes exact; SVG keeps text; EPS saves silently.  
**Scores:** Basic 36/40 | Specialized 56/60 | Total 92/100

**Assertions:**

- PASS - figure.pdf is 89 x 70 mm. (89.0 x 70.0 mm.)
- PASS - PNG and TIFF are 1051 px wide (89 mm at 300 dpi) and the TIFF uses tiff_lzw. (1051x826 both; compression tiff_lzw.)
- PASS - SVG saved with svg.fonttype none contains <text> elements while the default SVG contains none. (14 <text> vs 0 in the control.)
- PASS - EPS saves without warning and keeps the stated page size. (No warnings; BoundingBox 253 x 199 pt (89 x 70 mm).)

### Input 4 - Variant B: references/chart-recipes.md: all eleven snippets run verbatim onto a 180 x 110 mm figure

**Status:** COMPLETED - Ten of eleven snippets run clean; the Tick frequency snippet raises ValueError.  
**Scores:** Basic 30/40 | Specialized 47/60 | Total 77/100

**Assertions:**

- PASS - Scatter, line, bar, boxplot, histogram, heatmap, log, ScalarFormatter, date and grid snippets run without error or warning on 3.11.2. (10 of 10 clean.)
- FAIL - The Tick frequency snippet runs verbatim. (set_xticks(np.arange(0, 10, 2)) sets 5 ticks then set_xticklabels gets 3 labels: ValueError (MPL-008).)
- PASS - The stated boxplot labels= to tick_labels= rename is accurate on 3.11.2. (labels= raises TypeError; tick_labels= works.)
- PASS - The assembled recipe figure is exactly 180 x 110 mm with TrueType fonts. (180.0 x 110.0 mm; CID TrueType.)

### Input 5 - Stress: references/failure-modes.md claims re-measured: rasterization, Type 3, bbox, large-N size, FacetGrid, layout engines

**Status:** COMPLETED - Most claims reproduce; the layout-engine entry does not.  
**Scores:** Basic 29/40 | Specialized 48/60 | Total 77/100

**Assertions:**

- PASS - ax.set_rasterization_zorder(1) rasterizes zorder<1 artists and fig.set_rasterization_zorder does not exist. (1 image object, 36 KB PDF; control without it has none; hasattr(fig) False.)
- PASS - Default pdf.fonttype=3 gives Type 3 and 42 gives TrueType by pdffonts. (type3.pdf Type 3; type42.pdf CID TrueType.)
- PASS - bbox_inches='tight' yields about 92 mm, and without it the page is exactly 89 mm. (91.96 x 72.96 mm vs 89.0 x 70.0 mm.)
- PASS - The large-N and FacetGrid claims reproduce (1.5 MB vs 24 KB; set_xlabel AttributeError). (1517 KB vs 24 KB at default savefig dpi without alpha (166.9 KB at dpi 300 with alpha 0.6, so the ratio is condition-dependent); AttributeError confirmed.)
- FAIL - The tight_layout entry reproduces its symptom and its fix (fig.set_layout_engine('constrained') after creation) works with a colorbar. (tight_layout with ax= colorbar shows no clipping or overlap; set_layout_engine after the colorbar raises ZeroDivisionError (MPL-009).)

## Key strengths

- Page sizes, font types, text sizes and colour-to-category binding verified on rendered output: exact mm, TrueType only, 0 colour mismatches in 18,238 airway points across three row orders.
- Guardrails (no bbox_inches=tight, dict palettes with hue_order, set_rasterization_zorder on Axes, svg.fonttype none) are now correct and each reproduced by execution.
- Single runnable script writes five figures at stated mm and runs clean on matplotlib 3.11.2, seaborn 0.13.2 with real-data blocks also verbatim-runnable.
- Progressive disclosure is clean: short SKILL.md, failure modes and chart recipes in references, version-rename notes tested.

## Recommendations

- **[P2] MPL-007 seaborn.objects example ships with no colour key** (inputs [1]): scripts/matplotlib_phd.py volcano_so.pdf sets legend=False, leaving Up, Down and NS as three unlabelled colours; the default legend does fall outside the 89 mm page (bbox 348-408 px on a 350 px page) for every layout engine tried. Fix: Keep the legend and move it on-page, e.g. .layout(size=..., extent=[0, 0, 0.78, 1]).plot(), then reposition fig.legends[0] (verified inside the page in scripts/r2_so_legend.py), or state that a caption must name the colours.
- **[P2] MPL-008 Tick frequency recipe raises ValueError** (inputs [4]): references/chart-recipes.md sets five ticks with np.arange(0, 10, 2) and then three labels, which raises ValueError on matplotlib 3.11.2; the snippet also uses np without an import. Fix: Use equal counts, e.g. ax.set_xticks(np.arange(0, 6, 2)) with three labels, and add import numpy as np to the block.
- **[P2] MPL-009 tight_layout failure mode not reproduced; fix crashes** (inputs [5]): failure-modes.md says tight_layout clips labels and overlaps a colorbar added with ax=; in 3.11.2 it does neither. Its alternative fig.set_layout_engine('constrained') after creation raises ZeroDivisionError when a colorbar already exists. Fix: Reword the trigger to axes added with fig.add_axes, and change the alternative to set the engine before adding colorbars or pass layout='constrained' to plt.subplots only.
