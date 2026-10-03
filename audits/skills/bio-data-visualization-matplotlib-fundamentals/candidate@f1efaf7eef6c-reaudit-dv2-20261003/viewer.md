> **Audit record for `bio-data-visualization-matplotlib-fundamentals`**
> - Audited working candidate `f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/data-visualization/matplotlib-fundamentals), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-matplotlib-fundamentals

Generated: 2026-10-03  
Audit type: final independent re-audit (second loop) of the fixed candidate  
Exact candidate content SHA-256: `f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 56 | 94 | 5/5 | ✅ COMPLETED |
| 2 | Variant A | 38 | 56 | 94 | 5/5 | ✅ COMPLETED |
| 3 | Edge | 33 | 48 | 81 | 2/4 | ❌ PARTIAL |
| 4 | Variant B | 37 | 55 | 92 | 4/4 | ✅ COMPLETED |
| 5 | Stress | 37 | 55 | 92 | 5/5 | ✅ COMPLETED |

**Execution average:** 90.6 / 100  
**Assertion pass rate:** 21 / 23  
**Static score:** 88 / 100  
**Final score:** 90 / 100 — ⭐ Production Ready  
**Research veto:** PASS

Readiness decision: **candidate-ready** for this exact identity (final 90, static 88, execution average 90.6, assertions 21/23 = 91.3 %, no veto, no open P0 or P1; one P2 recommendation open: MPL-010). Exact identity is in [`source-identity.json`](source-identity.json).

## Prior findings (initial audit 146857c3b9b5; failed re-audit 5a5bd8a000b2)

| Prior finding | Verdict | Evidence |
|---|---|---|
| MPL-007 (P2) seaborn.objects example ships with no colour key | corrected for the shipped example; residual P2 disclosure gap MPL-010 | `scripts/matplotlib_phd.py` section 7 now keeps the legend: inside the exact 89x70 mm page at x 0.815-0.988 / y 0.406-0.594, clear of the axes (right edge 0.750), handles #999999/#0072b2/#d55e00, text 6-7 pt, fonts CID TrueType (`logs/m1_phd.log`, `logs/pdffonts_phd.log`, volcano_so_pdf.png opened). Stress: longer labels alone, 8 and 12 classes clear; a longer legend title overflows into the axes (x0 0.604 and 0.299 against 0.750), extent 0.70 does not help; no mention of the 22 % reserve, the private `Plot.plot()._figure` or the seaborn 0.13.2-only check; a public `Plot.on(fig)` route measured clean (`logs/m2_legend_stress.log`, `logs/m2b_axes_probe.log`) |
| MPL-008 (P2) Tick frequency recipe raises ValueError | corrected | 11 of 11 chart-recipes.md fragments run verbatim without warnings, Tick frequency gives ticks 0/2/4 labelled A/B/C (`logs/staged_recipes.log`) |
| MPL-009 (P2) tight_layout entry not reproduced | corrected | clipped after a longer label and after resize, constrained at creation not clipped, set_layout_engine after a colorbar raises ZeroDivisionError and before it works, multi-axes colorbar warns, single colorbar not clipped (`logs/staged_failure_modes.log`, 22 of 22) |
| MPL-001 (P1) rcParams do not give the documented 89/180 mm | corrected, not regressed | five PDFs 89x70, 180x110, 89x90, 89x70, 89x70 mm; bbox tight gives about 92 mm (`logs/m1_phd.log`, `logs/staged_failure_modes.log`) |
| MPL-002 (P1) list palettes bind colours to data order | corrected, not regressed | 18,238 of 18,238 drawn points carry their class colour in three row orders (`logs/m3_skill_blocks.log`) |
| MPL-003 (P2) failure-modes nonexistent method/exaggeration | corrected, not regressed | `Axes.set_rasterization_zorder(1)` image object; 1.52 MB vs 23.2 KB; Figure has no such method (`logs/staged_failure_modes.log`) |
| MPL-004 (P2) SVG text as paths | corrected, not regressed | 14 `<text>` with svg.fonttype none vs 0 default (`logs/m3_skill_blocks.log`) |
| MPL-005 (P2) example styling departs from rules | corrected, not regressed | cluster colours = four Okabe-Ito, no panel titles, text only 6 and 7 pt (`logs/m6_regress.log`) |
| MPL-006 (P2) pyplot state calls in an OO Skill | corrected, not regressed | no plt.imshow/colorbar/scatter calls in shipped code (`logs/m6_regress.log`) |

## Executed versus static-only

Environment: Windows Python 3.12.13 via `py.sh` (MPLBACKEND=Agg), matplotlib 3.11.2, seaborn 0.13.2, numpy 2.5.3, pandas 3.0.6, cmcrameri (metadata 1.10), PIL 12.3.0; fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt` (re-hashed identical); poppler (`pdffonts`, `pdftoppm`) in WSL `dv-cli`. Inputs: staged airway DESeq2 results; the script's own seeded synthetic data. Tool inventory: `TOOLS-bio-data-visualization-matplotlib-fundamentals.md` sha256 a4a13bf881d7db3a8a26cc45fe8aef405ca9d60316b9187db89bdc9eba35d83c. Skill bytes were not edited; scripts ran with the output directory as working directory.

| Surface | Classification | Evidence |
|---|---|---|
| `scripts/matplotlib_phd.py` (5 PDFs, sizes, fonts, text, colours, determinism) | executed | `scripts/m1_phd.py`, `logs/m1_phd.log`, `scripts/pdf_render_m.sh`, `logs/pdffonts_phd.log`; figures opened |
| seaborn.objects legend section 7 (MPL-007), stress variants, public route | executed | `scripts/m2_legend_stress.py`, `scripts/m2b_axes_probe.py`, `logs/m2_legend_stress.log`, `logs/m2b_axes_probe.log`; renders opened |
| SKILL.md python blocks (5), Saving block, colour binding on airway data | executed | `scripts/m3_skill_blocks.py`, `logs/m3_skill_blocks.log` |
| `references/chart-recipes.md` (2 blocks, 11 fragments) incl. Tick frequency (MPL-008) | executed | `scripts/staged_recipes.py`, `logs/staged_recipes.log` |
| `references/failure-modes.md` (22 checks) incl. tight_layout entry (MPL-009) | executed | `scripts/staged_failure_modes.py`, `logs/staged_failure_modes.log` |
| API/layout/EPS/rasterization claims in SKILL.md and usage-guide | executed | `scripts/m5_claims.py`, `logs/m5_claims.log` |
| First-loop regressions MPL-005, MPL-006 | executed | `scripts/m6_regress.py`, `logs/m6_regress.log` |
| Pandas4Warning origin (seaborn internals, not the Skill) | executed | `scripts/m1b_warn_origin.py`, `logs/m1b_warn_origin.log`: raised inside seaborn `Plot.plot()` via `pd.concat(copy=)` on pandas 3.0.6, hidden by Python's default filters, no effect on output |
| `usage-guide.md` | static-only | prose, prompts and the install line (covers every import of the script) |

Reused (not rerun): none. Notes: staged_recipes.py and staged_failure_modes.py are the staged tool copies of the fixer's scripts, read and run unchanged; m3_skill_blocks.py is adapted from the dv1 re-audit script. Failure-modes numeric claim 63x vs measured 66x from unrounded sizes (1.52 MB vs 23.2 KB) is within rounding of the stated 1.5 MB and 24 KB.

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS — Every drawn point of the airway volcano (18,238 genes) carries its class colour in three row orders (0 mismatches); page sizes, font embedding and file sizes are measured; the Skill's numeric claims (89 vs about 92 mm with bbox tight, 1.5 MB vs 24 KB) reproduce.
  - practice_boundaries: PASS — Plotting skill; no clinical or prescriptive output.
  - methodological_ground: PASS — Colours are bound to category names, journal page sizes are exact, no methodological fallacy.
  - code_usability: PASS — scripts/matplotlib_phd.py, all five SKILL.md python blocks and both chart-recipes.md blocks (11 fragments) run verbatim on matplotlib 3.11.2 and seaborn 0.13.2; the legend recipe's limits (MPL-010) concern layout, not running.

## Static categories

- functional_suitability: 11/12 — Covers OO API, rcParams, grid, heatmap, seaborn and seaborn.objects with exact journal sizes; the seaborn.objects legend now ships and fits for its own labels. Its 22 % reservation and private-attribute use are not stated as limits (MPL-010).
- reliability: 11/12 — All shipped code and every recipe runs warning-free and deterministically (second run reproduces every PDF); the legend recipe overflows into the axes with a longer legend title and depends on seaborn's private Plotter._figure (verified on seaborn 0.13.2 only).
- performance_context: 7/8 — SKILL.md routes to two references and one script; compact, with some restatement across SKILL.md, usage-guide.md and failure-modes.md.
- agent_usability: 14/16 — Clear defaults and guardrails with trigger/mechanism/symptom/fix; section 7 explains why the legend is moved but not when the 22 % reserve is too small.
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

**Status:** PARTIAL — The page stays exactly 89x70 mm and the legend stays inside it in every variant, and it clears the axes for the Skill's labels, for longer labels alone, and for 8 and 12 classes; a 51-character title puts the legend at x 0.299-0.988 (axes end at 0.750) and 'Differential expression class' with longer labels at 0.604-0.988, covering 13 mm of data. Neither the 22 % reserve, the private Plot.plot()._figure use, nor the seaborn 0.13.2-only verification appears in the Skill.  
**Scores:** Basic 33/40 | Specialized 48/60 | Total 81/100

**Assertions:**

- PASS — The legend stays inside the exact 89 x 70 mm page for every title/label/class-count variant (seven variants: inside the page, MediaBox 89.0x70.0 each.)
- PASS — The legend clears the axes for the shipped labels, longer labels alone, and 8 or 12 classes (x0 0.815, 0.757, 0.820, 0.808 against axes right edge 0.750.)
- FAIL — A longer legend title keeps the legend off the axes (title 'Differential expression class (DESeq2, padj < 0.05)': legend x0 0.299; 'Differential expression class' with long labels: x0 0.604; extent 0.70 did not help (axes end 0.671); out/legend/D_long_title_long_labels.png opened: legend over the data.)
- FAIL — The limits of the recipe (fixed 22 % reserve, private Plot.plot()._figure, verified on seaborn 0.13.2 only) are disclosed in SKILL.md or the script (SKILL.md names only 'seaborn 0.13+ (0.13.2)'; the script comment explains why the legend moves but not these limits; a public route exists (Plot.on(fig) + legend move + subplots_adjust: legend 0.815-0.988, axes end 0.760, page 89.0x70.0).)

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

- **[P2] MPL-010 seaborn.objects legend recipe discloses neither its private-attribute use nor its fixed 22 % reserve** (inputs [3]): Section 7 reserves the right 22 % of the page and moves fig.legends[0] through Plot.plot()._figure, a private seaborn attribute verified on seaborn 0.13.2 only; with a longer legend title ('Differential expression class' with longer labels) the legend spans x 0.604-0.988 and covers 13 mm of the plot area (axes end at 0.750), and a 51-character title spans 0.299-0.988. Nothing in SKILL.md or the script says so. Fix: Text-only: add to the script comment and SKILL.md a line that the recipe uses a private seaborn attribute (verified on 0.13.2), that 22 % fits legend text up to about 'Downregulated', and that longer titles need a smaller extent[2] or a shorter title with the legend bbox checked; optionally name the public route Plot.on(fig) + fig.legends[0] + fig.subplots_adjust(right=0.76), which measured inside the page and clear of the axes.

## Ordered finding ledger

Audited identity: `f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | MPL-010 | P2 | open | [3] | seaborn.objects legend recipe discloses neither its private-attribute use nor its fixed 22 % reserve. Text-only: add to the script comment and SKILL.md a line that the recipe uses a private seaborn attribute (verified on 0.13.2), that 22 % fits legend text up to about 'Downregulated', and that longer titles need a smaller extent[2] or a shorter title with the legend bbox checked; optionally name the public route Plot.on(fig) + fig.legends[0] + fig.subplots_adjust(right=0.76), which measured inside the page and clear of the axes. |

MPL-001 to MPL-009 are corrected and not listed (see verdicts in the viewer). MPL-010 is a new P2 finding and a text-only fix. No audit-local repair was made; no Skill bytes changed.
