> **Audit record for `bio-data-visualization-multipanel-figures`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3749f31](https://github.com/mrsonord2240/bioSkills/tree/3749f31f1c2d406f5e948bb389eaea7379c6e71a/data-visualization/multipanel-figures) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-multipanel-figures

Generated: 2026-09-24 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@3749f31f1c2d406f5e948bb389eaea7379c6e71a:data-visualization/multipanel-figures`
Audit type: final-pass exact-commit re-audit
Category: Data Analysis · Execution mode: A · Complexity: Moderate · N = 5 · Executed: None

## What the Skill claims to do

Compose exact-size publication multi-panel figures with patchwork, cowplot, gridExtra, matplotlib GridSpec, subfigures, and subplot mosaics, with qualified shared axes and legends.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 57 | **95** | 5/5 | yes | ✅ |
| 2 | Variant A | 38 | 56 | **94** | 5/5 | yes | ✅ |
| 3 | Variant B | 39 | 57 | **96** | 5/5 | yes | ✅ |
| 4 | Edge | 37 | 55 | **92** | 5/5 | yes | ✅ |
| 5 | Regression | 38 | 56 | **94** | 5/5 | yes | ✅ |

**Execution Average: 94.2 / 100** · **Assertion Pass Rate: 25/25**

**Static: 94/100** · Static weighted 37.6 + dynamic weighted 56.5 = **94.1/100** → ⭐ Production Ready, deployable.

---

## Veto gates

### Skill veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| stability | PASS |  |
| contract | PASS |  |
| determinism | PASS |  |
| security | PASS |  |

### Research veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | Dimensions, font types, legend qualifications, and layout behavior are supported by executed or directly inspected evidence. |
| practice boundaries | PASS | Figure composition only; no diagnostic or prescriptive content. |
| methodological ground | PASS | The skill now prevents misleading shared guides and axes when mappings or units differ. |
| code usability | PASS | Both shipped examples and all promised layout families have runnable checked paths. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 12/12 | Every promised R and Python arrangement has correct, runnable guidance and the primary examples meet the stated export contract. |
| reliability | 11/12 | Collection preconditions, version boundaries, fixed page sizes, font types, and layout-engine behavior are explicit and tested. |
| performance context | 7/8 | The 219-line operational skill keeps full workflows in examples and avoids redundant usage-guide material. |
| agent usability | 15/16 | A compact decision table, exact constants, qualified sharing rules, and runnable alternatives make route selection predictable. |
| human usability | 8/8 | Sizing, labels, legends, and verification steps are consistent across prose and examples. |
| security | 12/12 | No credentials, network access, destructive operations, or sensitive-data handling are introduced. |
| maintainability | 11/12 | Two standalone deterministic examples and focused cross-language checks cover the load-bearing contracts. |
| agent specific | 18/20 | The trigger, fallbacks, version notes, output paths, and escape hatches are explicit without exceeding scope. |

## Input 1 — Canonical: Exact shipped R patchwork figure

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Execution: verify_r.R through data-visualization/r.sh, verify_source.py, and prior exact-output pdfinfo/pdffonts verification.
- Finding: The committed example built the flat 2x2 figure at the journal canvas with one semantically valid shared guide.

| Assertion | Result | Evidence |
|---|---|---|
| The exact R example reaches its completed output path | PASS | It printed both page and PNG measurements and verify_r.R printed R verification PASS; the known shared Windows R cleanup issue occurred only after outputs completed. |
| The R canvas is 183 x 140 mm | PASS | PNG measured 182.96 x 139.95 mm at 300 dpi; the exact PDF verification log reports 518.74 x 396.85 points. |
| R PDF fonts are embedded and non-Type3 | PASS | pdffonts reports embedded subset ArialMT and Arial-BoldMT TrueType fonts. |
| Tags use the working patchwork styling route | PASS | The exact source applies `& theme(plot.tag=element_text(size=8, face='bold'))` with panel-relative placement. |
| Axis and guide collection is semantically qualified | PASS | The example uses a flat wrap_plots grid with identical coordinate limits and an identical Condition scale before collection. |

## Input 2 — Variant A: cowplot and gridExtra alternative R arrangements

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: verify_r.R and verify_pdf.sh evidence under run/multipanel_fix_20260923.
- Finding: Both promised alternative R paths rendered on the same exact-size Cairo canvas.

| Assertion | Result | Evidence |
|---|---|---|
| cowplot route renders | PASS | cowplot.pdf is nonempty and uses the documented `align='hv'` plus 8 pt bold labels. |
| gridExtra layout-matrix route renders | PASS | gridextra.pdf is nonempty from the explicit 2-row layout matrix. |
| Alternative PDFs retain the target page size | PASS | Exact-output verification reports 518.74 x 396.85 points. |
| Alternative PDFs use embedded non-Type3 fonts | PASS | pdffonts reports embedded TrueType Arial fonts for both routes. |
| Guide limitations are explicit | PASS | The source states that gridExtra does not collect guides and that one shared legend is valid only for identical mappings. |

## Input 3 — Variant B: Exact shipped matplotlib grid, mosaic, and subfigures

- Status: ✅ COMPLETED · Basic 39/40 · Specialized 57/60 · **Total 96/100**
- Execution: verify_python.py through the data-visualization Python wrapper plus exact-output PDF verification.
- Finding: The exact Python example and a fresh subfigure route completed with exact-size raster and vector products.

| Assertion | Result | Evidence |
|---|---|---|
| The exact Python example executes | PASS | verify_python.py exited 0 and printed Python verification PASS. |
| Both PNG canvases match 183 x 140 mm | PASS | Each is 2161 x 1653 pixels, or 182.96 x 139.95 mm at 300 dpi. |
| Python PDFs use Type-42-compatible embedded fonts | PASS | pdf.fonttype=42 is set before pyplot import; pdffonts reports embedded CID TrueType fonts and no Type 3. |
| One representative shared legend and fixed-point tags are implemented | PASS | The example calls fig.legend from one axes and uses offset_copy(..., units='points') for 8 pt tags. |
| Mosaic and subfigure routes execute | PASS | The named spanning mosaic writes PNG/PDF output; the subfigure check creates two left axes and a heatmap plus local colorbar on the right. |

## Input 4 — Edge: Compatibility, bounding-box, and misleading-legend guards

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 55/60 · **Total 92/100**
- Execution: verify_source.py plus exact source review at 3749f31.
- Finding: The formerly incorrect failure-mode claims are replaced by executable or narrowly qualified guidance.

| Assertion | Result | Evidence |
|---|---|---|
| patchwork compatibility is explicit | PASS | The source requires patchwork >= 1.3 with ggplot2 4.x and no longer gives the incorrect archived release date. |
| Contractual page size rejects tight bounding boxes | PASS | The source explicitly forbids bbox_inches='tight' for fixed page dimensions and the Python example omits it. |
| Constrained layout is opt-in | PASS | The source says it is not a global default and both Python layouts opt in. |
| Shared axes and legends require comparable mappings | PASS | The source does not promise collection across different quantities, limits, scale types, aesthetics, labels, or palettes. |
| Stale cowplot, ggsave, and tag-position claims are removed | PASS | verify_source.py passes against the 219-line exact SKILL.md and current examples. |

## Input 5 — Regression: Cross-language publication export contract

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Execution: Combined exact R, Python, source-contract, page-size, and font evidence.
- Finding: R and Python now agree on page dimensions, label sizing, layout intent, and font requirements.

| Assertion | Result | Evidence |
|---|---|---|
| Both shipped examples create named nonempty vector and raster outputs | PASS | R Figure1.pdf/png and Python grid/mosaic PDF/PNG products are all present and nonempty. |
| The same 183 x 140 mm constants drive R and Python | PASS | Source checks and measured output checks agree within backend precision. |
| The output font contract is checkable | PASS | R uses CairoPDF and Python sets pdf.fonttype=42; exact verification logs contain no Type 3 fonts. |
| Promised layout coverage is present | PASS | patchwork, cowplot, gridExtra, GridSpec, subfigures, and subplot_mosaic all have runnable guidance. |
| Progressive disclosure is within the project boundary | PASS | SKILL.md is 219 lines and the lean usage guide is under 80 lines; full workflows live in the two examples. |

## Key strengths

- Exact R and Python examples agree on a 183 x 140 mm publication canvas and non-Type3 embedded vector fonts.
- Shared axes and legends are limited to genuinely equivalent scales and mappings instead of being treated as cosmetic collection.
- patchwork, cowplot, gridExtra, GridSpec, subfigures, and subplot_mosaic have runnable, scoped patterns.
- Fixed-point panel tags and explicit layout engines avoid width-dependent offsets and implicit defaults.
