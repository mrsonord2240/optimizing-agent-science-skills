# 2026-09-27

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Turbo offered as perceptually uniform | P1 | Made viridis/cividis/batlow the default jet replacements; retained Turbo only as a jet-like last resort and explicitly documented its non-monotonic luminance. | **ran**: Python regression on the audit spatial array with matplotlib 3.11.2 and colorspacious 1.1.2 asserted viridis L* monotonic and Turbo L* non-monotonic. | Fixed. |
| Mandatory CVD pre-flight used `cvd_emulator` incorrectly | P1 | Replaced the palette call with `deutan()` / `protan()` / `tritan()` in R and a complete `cspace_convert(..., sRGB1+CVD, ...)` loop in Python; both report minimum pairwise distance. | **ran**: R colorspace 2.1.2 returned finite CIELAB minima (deutan 14.93, protan 20.71, tritan 16.17); Python returned finite CAM02-UCS minima (14.17, 13.96, 10.97). | `cvd_emulator()` is now described accurately as an image-file emulator, not a palette transformer. |
| Pure-white midpoint contradicted built-in diverging palettes | P1 | Added measured scico/RColorBrewer centres; restricted exact white to deliberately custom ramps; anchored built-in palettes with midpoint zero and symmetric limits. | **ran**: scico 1.5.0 centres asserted as vik `#EBE5E0`, roma `#C0E9C2`, bam `#F5F0F0`; RColorBrewer 1.1.3 RdBu centre is `#F7F7F7`; odd 101-color custom ramp asserted `#FFFFFF` at its centre. | Fixed. |
| Unnamed Okabe-Ito vector recoloured subsets and omitted reserve grey | P1 | Named seven chromatic colors by category, added `Unassigned = '#BBBBBB'`, kept `drop = FALSE`, and documented the deutan grey-collision caveat plus redundant encodings. | **ran**: mapping was identical after dropping one audit-data cell type; R and Python CVD minima were finite and positive. | Fixed in `SKILL.md` and both examples. |
| Grayscale test substituted a generic grey ramp and was conflated with CVD | P1 | Changed the check to `desaturate(pal)` plus a CIELAB L* monotonicity assertion; separated grayscale and CVD sections. | **ran**: batlow monotonicity assertion passed with scico 1.5.0/colorspace 2.1.2. | Fixed. |
| Shipped examples contradicted guidance and `palettes_phd.R` lacked data | P1 | Rewrote `palette_examples.R` around batlow, symmetric vik, named Okabe-Ito, visible outlined midpoint points, and stable subsetting; made `palettes_phd.R` self-contained with simulated `df`/`de_df`. | **ran**: both examples parsed and executed via `r.sh`; PDFs were non-empty, the palette example PNG was rendered and visually inspected, and all assertions passed. | Removed Python-only palette names from R output. |
| 9-20 group palettes recommended without CVD caveat | P2 | Replaced palette recommendations with the explicit rule that no listed single palette is CVD-safe beyond eight groups; require shape, labels, or facets. | **ran**: regression used the audit's 1,270-row UMAP fixture and the audit's measured many-group failures remain the basis for the correction. | Fixed. |
| Smaller factual palette errors | P2 | Corrected matplotlib default to 2.0; corrected `bam`/`roma` descriptions; removed the nonexistent `colorblind` style claim; stopped calling RdBu uniformly perceptual; used data-derived 99th-percentile symmetric Python bounds; used odd N for exact custom white. | **ran**: Python rendered the audit 120x160 spatial array with symmetric q99 bounds (6.80893); R asserted exact built-in/custom centres. | Fixed. |
| `usage-guide.md` duplicated `SKILL.md`; khroma/colorcet were listed without code | P2 | Reduced the guide to overview, prerequisites, prompts, routing, and related Skills; removed unused khroma/colorcet install/version/tool claims instead of advertising unexercised tools. | **ran**: repository search found no remaining khroma/colorcet claims; all retained package snippets executed in the regressions/examples. | Fixed. |

## Deduplication and packaging disposition

- Deleted the guide's seven-step workflow and ten-item Tips section; their agent-facing content now lives once in `SKILL.md` under **Palette Type by Data Type**, **CVD Simulation**, **Grayscale Monotonicity Test**, **Diverging Palette Setup**, and **Common Failure Modes**.
- Deleted the duplicate `SKILL.md` **Quantitative Thresholds** and **Common Errors** tables; unique content is retained in **The Three Modern Standards**, the palette decision table, and **Common Failure Modes**.
- Deleted the unused khroma/colorcet version, tool, and install-list passages; no agent-needed behavior depended on them.
- Deleted the unsupported Tol/Polychrome/tab20/Paired/Set3 recommendation passages; the supported rule now states that hue alone is unsafe beyond eight groups and routes to redundant encodings.
- Replaced the examples' Set1/NPG-style and unmatched custom-diverging passages with the corrected batlow/vik/named-Okabe-Ito examples.
- `SKILL.md` is 252 lines after deduplication, below the 300-line split threshold; no `references/` split is required.
- No complete 15+ line workflow remains inline. The two complete runnable examples remain under `examples/`, which the fixer brief exempts from deduplication/migration. Focused R and Python regressions were added under `tests/`.

## Validation details

- R: `F:\OpenScience\audit-envs\data-visualization\r.sh` ran `tests/validate_palette_contracts.R` against the preserved audit data; the test calls `parse()` on itself and both changed example files. Result: PASS, 1,270 UMAP rows, q99 LFC 4.814764, both examples executed, outputs non-empty.
- Python: `F:\OpenScience\audit-envs\data-visualization\py.sh` ran `tests/validate_palette_contracts.py` against `synthetic_spatial_expr.npy`; the test calls `py_compile` on itself. Result: PASS, shape 120x160, q99 6.808929.
- Visual: opened the 1440x1200 rendered PNG from `palette_examples.R`; all four panels were non-blank, the vik midpoint remained visible on the grey panel with outlined points, and named category colors matched across the full/subset panels.
- Skill-creator `quick_validate.py` was attempted but is not compatible with this shelf's established frontmatter schema: it rejects the pre-existing `tool_type`, `primary_tool`, and `goal_approach_exempt` keys. Those repository-specific keys were preserved unchanged.
- Unfixed findings: none (9/9 fixed).

## 2026-09-27 round-2 follow-up

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Add a compact palette-audit response contract | P2 | Added one concise response checklist covering palette type, normalization/bounds/reference, missingness, CVD distances, luminance, redundant encoding, and visual inspection. | **ran**: the Python contract test reads `SKILL.md` and asserts every required reporting field is present. | Fixed. |
| Show arbitrary reference points and missing values | P2 | Added a `TwoSlopeNorm` example with a nonzero scientific reference, `masked_invalid`, a separate neutral bad color, validation guidance, and masked-count reporting. | **ran**: the Python contract test asserted reference `0.5` maps to the palette centre, three non-finite cells stay masked, and `#BBBBBB` is the bad color. | Fixed. |

Round-2 validation:

- Python: `validate_palette_contracts.py` passed with 120x160 audit data, q99 6.808929, and finite CVD distances under all three simulations.
- R: `validate_palette_contracts.R` reached `R palette contracts PASS`, produced both example artifacts, and reported the expected 1,270-row/q99/CVD values. The shared R launcher then returned its known package-teardown exit after successful execution; the independent round-one audit reproduced that exit with ggplot2 alone.
- Packaging: `SKILL.md` is 283 lines, below the 300-line split threshold; `git diff --check` passed.
- Unfixed round-2 findings: none (2/2 fixed).
