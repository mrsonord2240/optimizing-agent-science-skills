> **Audit record for `bio-data-visualization-matplotlib-fundamentals`**
> - Audited working candidate `79a08cbdf5339dbf6f824d9532cc4720ef00102a9985831c5c56c051c8150611`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/data-visualization/matplotlib-fundamentals), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-matplotlib-fundamentals

Generated: 2026-10-03  
Audit type: delta re-audit (text-only changes to certified bytes)  
Exact candidate content SHA-256: `79a08cbdf5339dbf6f824d9532cc4720ef00102a9985831c5c56c051c8150611` (files=5, bytes=24925)  
Certified baseline (carried forward): `f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a` (files=5, bytes=24264), record `candidate@f1efaf7eef6c-reaudit-dv2-20261003`

## Delta qualification

- `skill_preflight --offline` on the candidate: PASS, identity 79a08cbdf5339dbf6f824d9532cc4720ef00102a9985831c5c56c051c8150611, files=5, bytes=24925.
- Reverting the edit pairs listed in the fix log on a scratch copy (`scripts/d1_revert.py`, `scratch/`) reproduces the certified identity exactly.
- Changed files differ only in prose, comments or string literals (per-file diffs in `scripts/diff_*.txt`).
- `scripts/matplotlib_phd.py`: `ast.dump` identical to the certified bytes; script re-run once, exit 0 (`scripts/logs/d1_standalone.log`).
- Environment fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt`, re-hashed identical at start and end.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 56 | 94 | 5/5 | ✅ COMPLETED |
| 2 | Variant A | 38 | 56 | 94 | 5/5 | ✅ COMPLETED |
| 3 | Edge | 34 | 50 | 84 | 3/5 | ❌ PARTIAL |
| 4 | Variant B | 37 | 55 | 92 | 4/4 | ✅ COMPLETED |
| 5 | Stress | 37 | 55 | 92 | 5/5 | ✅ COMPLETED |

**Execution average:** 91.2 / 100  
**Assertion pass rate:** 22 / 24 (91.7 %)  
**Static score:** 89 / 100  
**Final score:** 90 / 100 — ⭐ Production Ready  
**Research veto:** PASS

Readiness decision: **candidate-ready** for this exact identity (90 final, static 89, execution average 91.2, assertions 22/24, no veto, no open P0 or P1; open P2: MPL-011). Scores are the certifying report's, re-scored only where the change touches (see below).

## Finding verdicts

| Finding | Verdict | Evidence |
|---|---|---|
| MPL-010 (P2) legend recipe discloses neither private attribute nor 22 % reserve | corrected (closed); residual P2 MPL-011 | SKILL.md and `scripts/matplotlib_phd.py` comment now state: p._figure private, seaborn 0.13.2 only, fixed 22 %, 29-character title covered 13 mm. Re-measured: 29-character title with the shipped labels x0 0.604 vs axes end 0.750 = 13.0 mm; with longer labels the same; shipped title clear (`scripts/logs/d1_legend_probe.log`); script re-run: exit 0, five PDFs 89x70, 180x110, 89x90, 89x70, 89x70 mm, legend 0.815-0.988, rerun reproduces every PDF (`scripts/logs/d1_m1_phd.log`, `scripts/logs/d1_standalone.log`) |
| MPL-011 (P2, new) public route as worded clips the x label | open (raised by this delta) | `scripts/logs/d1_legend_probe.log`, `scripts/logs/d1_ink_probe.log`: with only right=0.76 the label is cut at the page edge; with left 0.13 / bottom 0.17 / right 0.76 / top 0.97 it is clean (44 px margin at 300 dpi). The edit followed the certifying record's own suggestion verbatim. |
| Other certified findings and passes | carried forward unchanged | script AST identical to the certified bytes (comments only); other blocks and references untouched |

## Executed versus carried

| Surface | Classification | Evidence |
|---|---|---|
| `scripts/matplotlib_phd.py` (comment-only edit) | executed | standalone `py.sh matplotlib_phd.py`: exit 0 (`scripts/logs/d1_standalone.log`); `scripts/m1_phd.py` on the candidate: 5 PDFs at exact mm sizes, legend inside the page and clear of the axes, determinism across two runs; the lone known FAIL is the seaborn-internal Pandas4Warning, identical to the certifying log |
| Section 7 limits and public route (changed claims) | executed | `scripts/d1_legend_probe.py`, `scripts/d1_ink_probe.py`; `scripts/logs/d1_legend_probe.log`, `scripts/logs/d1_ink_probe.log`; figures opened |
| SKILL.md blocks, chart-recipes, failure-modes, usage-guide, other claims | carried (hash-identical) | certifying run `reaudit-dv2-20261003` |

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS); carried, no executable byte changed.
- Research veto: PASS
  - scientific_integrity: PASS — Every drawn point of the airway volcano (18,238 genes) carries its class colour in three row orders (0 mismatches); page sizes, font embedding and file sizes are measured; the Skill's numeric claims (89 vs about 92 mm with bbox tight, 1.5 MB vs 24 KB) reproduce.
  - practice_boundaries: PASS — Plotting skill; no clinical or prescriptive output.
  - methodological_ground: PASS — Colours are bound to category names, journal page sizes are exact, no methodological fallacy.
  - code_usability: PASS — scripts/matplotlib_phd.py, all five SKILL.md python blocks and both chart-recipes.md blocks (11 fragments) run verbatim on matplotlib 3.11.2 and seaborn 0.13.2; the legend recipe's limits (MPL-010) concern layout, not running.

## Static categories

- functional_suitability: 11/12 — Covers OO API, rcParams, grid, heatmap, seaborn and seaborn.objects with exact journal sizes; the seaborn.objects legend now ships and fits for its own labels. Its 22 % reservation and private-attribute use are not stated as limits (MPL-010).
- reliability: 11/12 — All shipped code and every recipe runs warning-free and deterministically (second run reproduces every PDF); the legend recipe overflows into the axes with a longer legend title and depends on seaborn's private Plotter._figure (verified on seaborn 0.13.2 only).
- performance_context: 7/8 — SKILL.md routes to two references and one script; compact, with some restatement across SKILL.md, usage-guide.md and failure-modes.md.
- agent_usability: 15/16 — Clear defaults and guardrails with trigger/mechanism/symptom/fix; section 7 now names the private-attribute dependency, the fixed 22 % reserve and the 29-character-title overflow (13 mm), but its public alternative is incomplete (MPL-011).
- human_usability: 7/8 — Readable; the rewritten tight_layout entry and the Tick frequency recipe now state only reproducible behaviour.
- security: 11/12 — No credentials, network or destructive operations; local savefig writes only.
- maintainability: 10/12 — Single runnable example, no tests; section 7 relies on a private seaborn attribute and a fixed fraction.
- agent_specific: 17/20 — Precise trigger description, progressive disclosure to two references and a script, guardrails aligned with measured behaviour; first-loop corrections all hold.

## Detailed outputs

### Input 1 — Canonical: scripts/matplotlib_phd.py run verbatim: five PDFs, page sizes, fonts, text sizes, seaborn.objects legend (MPL-007), determinism

**Status:** COMPLETED — Five PDFs are exactly 89x70, 180x110, 89x90, 89x70 and 89x70 mm; every font is embedded CID TrueType (no Type 3); visible text is 6 and 7 pt; the seaborn.objects legend sits at x 0.815-0.988 of the page, clear of the axes (right edge 0.750), grey/blue/orange; a second run reproduces every PDF.  
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

**Assertions:**

- PASS — Each of the five PDFs has the stated page size in mm (MPL-001) (MediaBox 89.0x70.0, 180.0x110.0, 89.0x90.0, 89.0x70.0, 89.0x70.0.)
- PASS — All fonts are embedded TrueType and no Type 3 appears (pdffonts) (ArialMT / Arial-BoldMT CID TrueType emb yes in all five PDFs.)
- PASS — The seaborn.objects legend is inside the exact page, clear of the axes, with the three significance classes in the palette colours (MPL-007) (legend bbox x 0.815-0.988, y 0.406-0.594; axes tight x1 0.750; handle colours #999999/#0072b2/#d55e00; volcano_so_pdf.png opened.)
- PASS — Visible text is only 6 or 7 pt in every figure (MPL-005) (text sizes {6.0, 7.0}; no panel titles, tags a-f present.)
- PASS — Two runs of the script reproduce every PDF byte for byte apart from creation date and ID (five identical digests.)

### Input 2 — Variant A: Every SKILL.md python block verbatim on the real airway DESeq2 table (18,238 genes) in three row orders, plus the Saving block at 89 x 70 mm

**Status:** COMPLETED — All five blocks run verbatim in each ordering; each of the 18,238 drawn points has its class colour and legends map NS/Down/Up to the palette; figure.pdf 89.0x70.0 mm, PNG and TIFF 1051 px (300 dpi), TIFF tiff_lzw, SVG keeps 14 <text> elements versus 0 by default, EPS saves without warning.  
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

**Assertions:**

- PASS — All five SKILL.md python blocks run verbatim in three row orderings ('all 5 blocks ran verbatim' for Up-first, NS-first and shuffled.)
- PASS — Every drawn point carries its category colour and the legend maps each class to the palette colour (MPL-002) (18,238 of 18,238 points, 0 mismatches in all orderings; legend and so legend maps equal the palette.)
- PASS — Saved PDF page is 89 x 70 mm and PNG/TIFF are 1051 px wide at 300 dpi with lzw TIFF (scatter.pdf and figure.pdf 89.0x70.0; 1051x826 px; compression tiff_lzw.)
- PASS — svg.fonttype='none' keeps text editable and the default does not (MPL-004) (14 <text> elements versus 0 in the control.)
- PASS — EPS saves with ps.fonttype 42 without warnings (no warnings; EPS BoundingBox 0 0 253 199; Type42 resource present, differs from fonttype 3.)

### Input 3 — Edge: Section 7 legend recipe stress: longer legend title and labels, 8 and 12 classes, a public Plot.on(fig) route (MPL-007 fragility)

**Status:** PARTIAL — Page stays exactly 89x70 mm and the legend stays inside it in every variant; it clears the axes for the shipped labels, longer labels alone and 8 and 12 classes; a 29-character title overflows into the axes by 13.0 mm with the shipped labels (51 characters: x0 0.299). The Skill now discloses the private Plot.plot()._figure use, the seaborn 0.13.2-only check, the fixed 22 % reserve and that overflow, and names a public route; that route as worded (right=0.76 only) clips the x label (MPL-011).  
**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100

**Assertions:**

- PASS — The legend stays inside the exact 89 x 70 mm page for every title/label/class-count variant (seven variants: inside the page, MediaBox 89.0x70.0 each.)
- PASS — The legend clears the axes for the shipped labels, longer labels alone, and 8 or 12 classes (x0 0.815, 0.757, 0.820, 0.808 against axes right edge 0.750.)
- FAIL — A longer legend title keeps the legend off the axes (title 'Differential expression class (DESeq2, padj < 0.05)': legend x0 0.299; 'Differential expression class' with long labels: x0 0.604; extent 0.70 did not help (axes end 0.671); out/legend/D_long_title_long_labels.png opened: legend over the data.)
- PASS — The limits of the recipe (fixed 22 % reserve, private Plot.plot()._figure, verified on seaborn 0.13.2 only) are disclosed in SKILL.md or the script (SKILL.md and the script comment now state the private Plot.plot()._figure use, seaborn 0.13.2 only, the fixed 22 % reserve and that a 29-character title covers 13 mm; re-measured: 'Differential expression class' with the shipped labels x0 0.604 vs axes end 0.750 = 13.0 mm (`scripts/logs/d1_legend_probe.log`).)
- FAIL — The public route as worded (Plot.on(fig), move fig.legends[0], fig.subplots_adjust(right=0.76)) gives a clean 89 x 70 mm figure (legend x 0.815-0.988 inside the page and clear of the axes (0.760), but the axes tight box reaches y -0.007 and the x label is clipped at the page edge; the measured route also set left 0.13, bottom 0.17, top 0.97 (`scripts/logs/d1_legend_probe.log`, `scripts/logs/d1_ink_probe.log`, right076_only.png opened).)

### Input 4 — Variant B: references/chart-recipes.md: both python blocks run verbatim as 11 fragments incl. the rewritten Tick frequency recipe (MPL-008); API and layout claims

**Status:** COMPLETED — All 11 fragments run verbatim without warnings, including Tick frequency (three ticks 0/2/4 labelled A/B/C, rotated); boxplot(labels=) raises TypeError and tick_labels= works; constrained layout is opt-in and constrained_layout=True still works.  
**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**

- PASS — All 11 chart-recipes.md fragments run verbatim without warnings (scatter, line, bar, box, histogram, heatmap, log scale, scientific notation, date axis, tick frequency, grid.)
- PASS — The Tick frequency recipe sets as many ticks as labels and runs on its own (MPL-008) (import numpy as np; set_xticks(np.arange(0, 6, 2)) then three labels; frag__Tick_frequency.png opened.)
- PASS — Axes.boxplot(labels=) is rejected on 3.11 and tick_labels= works, as SKILL.md and the recipe state (TypeError: unexpected keyword argument 'labels'; tick_labels gives A, B.)
- PASS — The default layout engine is none and constrained_layout=True still works (SKILL.md Defaults claim) (get_layout_engine() is None; legacy keyword gives ConstrainedLayoutEngine with no warning.)

### Input 5 — Stress: references/failure-modes.md claims re-measured incl. the rewritten tight_layout entry (MPL-009), rasterization through seaborn, bbox_inches, first-loop regressions

**Status:** COMPLETED — All 22 staged failure-mode checks pass: tight_layout clips after a longer label or resize while constrained does not; set_layout_engine after a colorbar raises ZeroDivisionError and before it works; multi-axes colorbar warns; 100000 points 1.52 MB vs 23.2 KB (the entry says 63x, measured 66x from unrounded sizes); bbox tight gives about 92 mm; seaborn passes rasterized=True through (0 to 2 image objects, 341 KB to 93 KB).  
**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**

- PASS — The tight_layout entry states only reproducible behaviour and its fix (MPL-009) (clipped after label change and resize; constrained at creation not clipped; set_layout_engine after colorbar ZeroDivisionError, before works; multi-axes colorbar warning; single colorbar not clipped.)
- PASS — Large-N rasterization numbers and the Axes.set_rasterization_zorder claim reproduce (MPL-003) (1.52 MB vs 23.2 KB; zorder PDF has an image object and is small; Figure has no set_rasterization_zorder.)
- PASS — bbox_inches='tight' changes the page from 89 to about 92 mm and the Type 3 / Type 42 entries hold (MPL-001) (page 91-93.5 mm vs 89.0; type3.pdf vs type42.pdf; pdffonts TrueType on all shipped PDFs.)
- PASS — The remaining entries reproduce (pyplot state machine, FacetGrid vs Axes, figsize inches, colorbar shrink, svg.fonttype, spines) (staged_failure_modes.py 22 of 22 PASS.)
- PASS — First-loop corrections hold: Okabe-Ito cluster colours, no panel titles, no pyplot state calls in shipped code (MPL-005, MPL-006) (PCA colours = four named Okabe-Ito colours; grid panels untitled; no plt.imshow/colorbar/scatter calls in code.)

## Key strengths

- Every shipped figure has the exact journal page size, embedded TrueType fonts and 6-7 pt text, and the whole example is deterministic.
- The seaborn.objects example now keeps its colour key inside an exact 89 x 70 mm page for its own labels.
- Colours are bound to category names; every drawn point of a real 18,238-gene volcano carries its class colour in three row orders.
- All SKILL.md blocks, all recipe fragments and all 22 failure-mode claims run verbatim and state only reproducible behaviour, including the rewritten tight_layout entry and Tick frequency recipe.

## Recommendations

- **[P2] MPL-011 the named public legend route omits margins and clips the x label** (inputs [3]): SKILL.md and the script comment name the public route as Plot.on(fig), move fig.legends[0], fig.subplots_adjust(right=0.76). Run exactly so on an 89 x 70 mm figure the legend sits inside the page and clear of the axes (x 0.815-0.988, axes end 0.760), but the axes tight box reaches y = -0.007 and the x-axis label is cut at the page edge (ink on the last pixel row, scripts/figures/right076_only.png). The measured route in the certifying run also set left = 0.13, bottom = 0.17 and top = 0.97 and is clean (44 px bottom margin). Fix: Text-only: write the route as fig.subplots_adjust(left=0.13, bottom=0.17, right=0.76, top=0.97) in SKILL.md and in the script comment, or name only the legend move and say the margins must be set so the x label stays inside the page.
