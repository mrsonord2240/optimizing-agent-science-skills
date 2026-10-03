> **Audit record for `bio-data-visualization-matplotlib-fundamentals`**
> - Audited working candidate `146857c3b9b509e7fb41764055239b497b5793cf0b386f83542fdfd5c5302d78`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/data-visualization/matplotlib-fundamentals), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-matplotlib-fundamentals

Generated: 2026-10-03  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256: `146857c3b9b509e7fb41764055239b497b5793cf0b386f83542fdfd5c5302d78`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 30 | 43 | 73 | 3/4 | ⚠️ COMPLETED |
| 2 | Variant A | 28 | 38 | 66 | 3/4 | ⚠️ COMPLETED |
| 3 | Edge | 30 | 40 | 70 | 3/4 | ⚠️ COMPLETED |
| 4 | Variant B | 34 | 47 | 81 | 4/4 | ✅ COMPLETED |
| 5 | Stress | 31 | 42 | 73 | 2/4 | ⚠️ COMPLETED |

**Execution average:** 72.6 / 100  
**Assertion pass rate:** 15 / 20  
**Static score:** 77 / 100  
**Final score:** 74 / 100 — ⚠️ Beta Only  
**Research veto:** PASS

This score is diagnostic. It does not make the candidate ready. Findings are ordered in the ledger below; exact identity is in [`source-identity.json`](source-identity.json).

## Executed versus static-only

Environment: Windows Python 3.12.13 via `py.sh` (matplotlib 3.11.2, seaborn 0.13.2, numpy 2.5.3, pandas 3.0.6, cmcrameri); fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt`; pdffonts/pdftoppm 26.07.0 in WSL `dv-cli`. Input: public airway DESeq2 results; synthetic data in the shipped script.

| Surface | Classification | Evidence |
|---|---|---|
| `scripts/matplotlib_phd.py` (all seven sections) | executed | `scripts/m1_phd_check.py`, `logs/m1_phd_check.log`, `logs/pdffonts_phd.log`; PDFs rendered and opened (`out/phd/*_pdf.png`) |
| SKILL.md seaborn recipe on real data, seaborn.objects | executed | `scripts/m2_real_volcano.py`, `logs/m2_real_volcano.log`; `out/vol/` opened |
| SKILL.md Standard Setup + Saving block, chart-recipes.md blocks, failure-modes.md claims | executed | `scripts/m3_recipes.py`, `m3b_type3_probe.py`, `m3c_type3_bisect.py`, logs; `out/rec/` opened |
| EPS transparency warning (tooling lead) | executed, did not reproduce on the Skill's own recipes | `logs/m3_recipes.log` last lines |
| usage-guide.md tips | static-only (restate SKILL.md) | n/a |

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS).
- Research veto: PASS
  - scientific_integrity: PASS — No fabricated values; the shipped example uses labelled synthetic data. On real airway results (541 Up / 497 Down / 17,200 NS) the Skill's list-palette recipe drew correct points but with data-order-dependent colours (MPL-002), filed as a defect.
  - practice_boundaries: PASS — Plotting skill; no clinical or prescriptive output.
  - methodological_ground: PASS — No principled fallacy; colour-to-class binding by list order is a presentation hazard (MPL-002), not an inverted statistical conclusion.
  - code_usability: PASS — matplotlib_phd.py and every recipe ran unchanged on matplotlib 3.11.2 with exit 0; defects are page size, palette binding and doc claims (MPL-001..MPL-006).

## Static categories

- functional_suitability: 9/12 — Covers rcParams, OO API, layout, fonts, saving and seaborn; the shipped rcParams break the 89 mm promise (MPL-001) and the list-palette recipe mis-binds colours (MPL-002).
- reliability: 9/12 — All shipped code runs cleanly on 3.11.2 with no warnings; behaviour hazards are silent (page size, palette order).
- performance_context: 6/8 — Compact SKILL.md routing to two references; recipes and guardrails repeat across SKILL.md, usage-guide and failure-modes.
- agent_usability: 12/16 — Clear defaults and guardrails; an agent following the Standard Setup gets 89.4 mm output while the script gives 92.0 mm (MPL-001).
- human_usability: 6/8 — Readable; usage-guide mixes pyplot calls into an OO-API Skill (MPL-006).
- security: 11/12 — Local file writes only; no credentials or network.
- maintainability: 9/12 — Single example script mirrors SKILL.md; no tests or palette-binding checks.
- agent_specific: 15/20 — Precise trigger and routed references; failure-modes.md contains a nonexistent method and an exaggerated size claim (MPL-003).

## Detailed outputs

### Input 1 — Canonical: Run scripts/matplotlib_phd.py unchanged: rcParams, 89 mm scatter, 2x3 grid, Crameri heatmap, seaborn scatter, seaborn.objects

**Status:** COMPLETED — Exit 0, five PDFs, all fonts CID TrueType embedded; pages are 92.0 / 182.7 / 91.8 mm wide against documented 89 / 180 / 89 mm (MPL-001); cluster colours are tab10 (MPL-005).  
**Scores:** Basic 30/40 | Specialized 43/60 | Total 73/100

**Assertions:**

- PASS — Script exits 0 and writes five PDFs with no warnings (Exit 0, stderr empty.)
- PASS — Every PDF embeds TrueType fonts and has no Type 3 rows (pdffonts: ArialMT/Arial-BoldMT CID TrueType, emb yes, in all five.)
- FAIL — 89 mm and 180 mm figures are saved at the documented journal widths (MediaBox 92.0 x 73.0, 91.8 x 93.0, 182.7 x 113.0 mm (savefig.bbox 'tight' with default pad).)
- PASS — Scatter and heatmap rasterise the data layer and keep text vector (image XObjects present (2 / 12); text embedded as fonts.)

### Input 2 — Variant A: SKILL.md seaborn volcano recipe on real airway DESeq2 results (18,238 genes)

**Status:** COMPLETED — Points correct but the list palette binds by order of appearance: Up drawn blue and Down orange; the shipped example colours 'ns' orange (MPL-002).  
**Scores:** Basic 28/40 | Specialized 38/60 | Total 66/100

**Assertions:**

- PASS — NS points are drawn in the documented grey #999999 (Legend NS = #999999 on the airway data, by luck of data order.)
- FAIL — Up is orange and Down is blue as the usage-guide's Up/Down/NS colours imply (Legend Up = #0072b2, Down = #d55e00 on real data; on the shipped random data ns = orange.)
- PASS — A dict palette with hue_order fixes class colours (Control: NS grey, Down blue, Up orange.)
- PASS — rasterized=True shrinks the 18,238-point PDF (38,984 B versus 272,530 B vector.)

### Input 3 — Edge: SKILL.md Standard Setup rcParams and Saving block: PDF, PNG, TIFF, SVG, EPS at 89 mm

**Status:** COMPLETED — PNG/TIFF 1056 x 831 px (89.4 x 70.4 mm) with the Skill's pad 0.05; TIFF LZW works; SVG text is converted to paths so the 'editable vector' claim fails (MPL-004).  
**Scores:** Basic 30/40 | Specialized 40/60 | Total 70/100

**Assertions:**

- PASS — Standard Setup figure saves within 1 mm of 89 mm (89.4 mm wide with pad_inches 0.05.)
- PASS — TIFF save uses LZW compression (PIL reports tiff_lzw, 1056 x 831.)
- FAIL — SVG keeps text as editable <text> (0 <text> elements, 55 glyph <use> (svg.fonttype 'path').)
- PASS — Default Type 3 versus pdf.fonttype=42 claim (pdffonts: stock rcParams give Type 3 DejaVuSans; 42 gives TrueType.)

### Input 4 — Variant B: references/chart-recipes.md blocks as a 6-panel figure (scatter, line, bar, boxplot, hist, imshow, axis formatting)

**Status:** COMPLETED — All recipes build and render correctly; tick_labels= confirmed, labels= rejected.  
**Scores:** Basic 34/40 | Specialized 47/60 | Total 81/100

**Assertions:**

- PASS — All chart recipes execute without warnings on 3.11.2 (Opened recipes_pdf.png: six legible panels.)
- PASS — boxplot(labels=) is rejected on 3.11 while tick_labels= works (TypeError for labels=.)
- PASS — Symmetric RdBu_r imshow with 99th-percentile vmax is centred on zero (Colorbar -2..2 centred, white at 0.)
- PASS — Log y histogram and date axis recipes render (Opened figure; dates.png written.)

### Input 5 — Stress: failure-modes.md claims: tight_layout vs constrained, FacetGrid, rasterization, large-N PDF size

**Status:** COMPLETED — tight_layout/FacetGrid/Type 3/rasterize claims verified; fig.set_rasterization_zorder does not exist and the 50 MB claim is exaggerated (MPL-003).  
**Scores:** Basic 31/40 | Specialized 42/60 | Total 73/100

**Assertions:**

- PASS — tight_layout with colorbar and shared axes overlaps while constrained does not (Axes/colorbar overlaps 2 versus 0.)
- PASS — FacetGrid.set_xlabel raises AttributeError and set_axis_labels works (AttributeError reproduced.)
- FAIL — fig.set_rasterization_zorder(0) exists (Figure has no such method; it is an Axes method.)
- FAIL — A vector scatter of N=100,000 yields a ~50 MB PDF (18,238 real points: 272,530 B vector versus 38,984 B rasterised; extrapolates to ~1.5 MB.)

## Key strengths

- Every shipped and documented recipe executed cleanly on matplotlib 3.11.2 with TrueType embedding verified by pdffonts.
- Version drift (boxplot tick_labels, constrained layout) is already handled and checked.
- tight_layout, FacetGrid, Type 3 and rasterization failure modes are real and reproduced.

## Recommendations

- **[P1] MPL-001 Shipped rcParams do not yield the documented 89/180 mm journal widths** (inputs [1, 3]): savefig.bbox='tight' re-crops the canvas: matplotlib_phd.py writes 92.0, 91.8 and 182.7 mm pages for 89, 89 and 180 mm figures (default pad 0.1 in is not set); the SKILL.md Standard Setup gives 89.4 mm. Fix: Drop savefig.bbox='tight' (constrained layout already prevents clipping) from both the Standard Setup and script, or document the size change and assert page width.
- **[P1] MPL-002 List palettes bind colours to data order, not to Up/Down/NS** (inputs [2]): palette=['#999999','#0072B2','#D55E00'] with hue='significance' draws Up blue and Down orange on real airway data and 'ns' orange in the shipped example; the colour-to-class mapping depends on row order and the same list in seaborn.objects. Fix: Use palette={'NS':..., 'Down':..., 'Up':...} with hue_order in SKILL.md, matplotlib_phd.py and seaborn.objects scale.
- **[P2] MPL-003 failure-modes.md contains a nonexistent method and an exaggerated claim** (inputs [5]): `fig.set_rasterization_zorder(0)` raises AttributeError (it is `ax.set_rasterization_zorder`); '100000 points = 50 MB PDF, 30 s open' is not reproduced (19k points = 0.27 MB); 'default rasterization can include axes' is not demonstrated. Fix: Use ax.set_rasterization_zorder(0), restate the size effect with a measured ratio, drop the vague mechanism.
- **[P2] MPL-004 'SVG for editable vector' leaves text as paths** (inputs [3]): svg.fonttype defaults to 'path': the saved SVG has 0 <text> elements and 55 glyph uses, so text is not editable. Fix: Set svg.fonttype='none' (with a note that fonts must be installed) or reword the claim.
- **[P2] MPL-005 Example styling departs from the Skill's own rules** (inputs [1]): The cluster scatter uses cmap='tab10' (not CVD-safe) against the Okabe-Ito requirement; axes.titlesize=8 exceeds the stated 5-7 pt body-text limit; the grid titles repeat the panel tags a-f. Fix: Colour clusters with the Okabe-Ito list, use titlesize 7, and drop the redundant panel titles.
- **[P2] MPL-006 OO-API Skill mixes pyplot state calls** (inputs [4]): SKILL.md Color section uses plt.imshow/plt.colorbar and the recipes use plt.colorbar(..., ax=ax) while the guardrail forbids pyplot state calls after plt.subplots(n, m). Fix: Use ax.imshow and fig.colorbar(im, ax=ax) in SKILL.md, usage-guide and chart-recipes.

## Ordered finding ledger

Audited identity: `146857c3b9b509e7fb41764055239b497b5793cf0b386f83542fdfd5c5302d78`

| Order | ID | Priority | State | Evidence inputs | Required disposition |
|---:|---|---|---|---|---|
| 1 | MPL-001 | P1 | open | [1, 3] | Shipped rcParams do not yield the documented 89/180 mm journal widths. Drop savefig.bbox='tight' (constrained layout already prevents clipping) from both the Standard Setup and script, or document the size change and assert page width. |
| 2 | MPL-002 | P1 | open | [2] | List palettes bind colours to data order, not to Up/Down/NS. Use palette={'NS':..., 'Down':..., 'Up':...} with hue_order in SKILL.md, matplotlib_phd.py and seaborn.objects scale. |
| 3 | MPL-003 | P2 | open | [5] | failure-modes.md contains a nonexistent method and an exaggerated claim. Use ax.set_rasterization_zorder(0), restate the size effect with a measured ratio, drop the vague mechanism. |
| 4 | MPL-004 | P2 | open | [3] | 'SVG for editable vector' leaves text as paths. Set svg.fonttype='none' (with a note that fonts must be installed) or reword the claim. |
| 5 | MPL-005 | P2 | open | [1] | Example styling departs from the Skill's own rules. Colour clusters with the Okabe-Ito list, use titlesize 7, and drop the redundant panel titles. |
| 6 | MPL-006 | P2 | open | [4] | OO-API Skill mixes pyplot state calls. Use ax.imshow and fig.colorbar(im, ax=ax) in SKILL.md, usage-guide and chart-recipes. |

No audit-local repair was made; no Skill bytes changed.
