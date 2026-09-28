> **Audit record for `bio-data-visualization-color-palettes`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@cd2cfef](https://github.com/mrsonord2240/optimized-scientific-skills/tree/cd2cfef126db14008baf614af792317daf6ff1e1/skills/bio-data-visualization-color-palettes) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-27 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-color-palettes (INDEPENDENT RE-AUDIT)

Generated: 2026-09-27
Source: `mrsonord2240/optimized-scientific-skills@cd2cfef126db14008baf614af792317daf6ff1e1:skills/bio-data-visualization-color-palettes`
Auditor independent: `true`
Category: Data Analysis | Mode A | Complexity: Complex -> 7 inputs
Data: saved synthetic fixtures only; provider Skill snapshot copied byte-for-byte under `run/skill/` (6/6 hashes matched).

## Result

| Metric | Result |
|---|---|
| Static | **93/100** |
| Execution average | **94.9/100** (Layer 1 38.3/40; Layer 2 56.6/60) |
| Final | **94/100** |
| Grade | **Production Ready** |
| Deployable | **true** |
| Executed | **7/7** |
| Assertions | **35/35 (100%)** |
| Vetoes | none |
| Open P0/P1/P2 | **0/0/2** |

All Production Ready floors pass. The five archived prompts were rerun as regressions; Inputs 6 and 7 are genuinely new.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 57 | 95 | 5/5 | ✅ |
| 2 | Variant A | 39 | 58 | 97 | 5/5 | ✅ |
| 3 | Edge | 39 | 58 | 97 | 5/5 | ✅ |
| 4 | Variant B | 39 | 58 | 97 | 5/5 | ✅ |
| 5 | Stress | 38 | 56 | 94 | 5/5 | ✅ |
| 6 | Scope Boundary | 38 | 55 | 93 | 5/5 | ✅ |
| 7 | Adversarial | 37 | 54 | 91 | 5/5 | ✅ |

## Execution and visual evidence

`run/run_all.out` records the full regression suite. `run/inspect_images.out` confirms seven PNGs at 1120-1820 px wide, non-white fractions 0.0169-0.7478, and >100 unique RGB values each. All seven PNGs were also opened manually.

The shared R environment currently returns process code 2816 after successful package teardown. This is not Skill-specific: `run/r_package_exit_probe.R ggplot2` reproduces it, while `run/r_exit_probe.R` (base R only) exits 0. Every R audit script reached its explicit PASS sentinel and emitted parseable, non-empty artifacts; the independent Python contracts and image checks exit 0.

## Detailed Outputs

### Input 1 - Canonical: Named Okabe-Ito mapping for seven cell types plus unassigned

**Prompt:** Assign one CVD-safe Okabe-Ito color to each of these 7 cell types, reserve grey for ambient/unassigned. My UMAP has T, B, NK, monocyte, dendritic, platelet and erythroid cells plus unassigned cells; I'll also show a subset without the T cells.

**Generated code / run:** `run/regressions.R (named cell_colors, stable ggplot_build mapping, redundant shape)`

**Output:** The fixed named mapping stayed byte-for-byte stable after T cells were removed. Unassigned used #BBBBBB plus a distinct cross marker; R CIELAB minima after deutan/protan/tritan transforms were 14.93/20.71/16.17.

**Execution evidence:** Executed run/regressions.R on the 1,270-row synthetic UMAP; opened figs/i1_named_okabe_stability.png.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**
- [PASS] Every category is assigned through a named mapping and Unassigned is light grey - Seven chromatic names plus Unassigned=#BBBBBB were present.
- [PASS] Removing T cells does not recolor any remaining category - The full and subset ggplot_build mappings were identical for all shared levels.
- [PASS] All three CVD simulations produce finite positive minimum pairwise distances - R minima were 14.93, 20.71, and 16.17; Python independently returned 14.17, 13.96, and 10.97 in CAM02-UCS.
- [PASS] A redundant non-color encoding distinguishes the reserve class - Unassigned uses marker 4 while chromatic categories use marker 16.
- [PASS] The full and subset plots render non-blank with readable legends - Manual visual inspection confirmed stable colors, the grey cross class, and complete legends.

### Input 2 - Variant A: vik log-fold-change heatmap with symmetric q99 bounds

**Prompt:** Use a diverging Crameri vik palette for a log-fold-change heatmap with symmetric bounds at +/- the 99th percentile of |LFC|. Zero must map to pure white.

**Generated code / run:** `run/regressions.R (scale_fill_scico vik + odd-count custom gradient)`

**Output:** The fixed guidance correctly separates built-in near-neutral centres from an exact-white custom ramp. q99 was 4.814764, vik sampled #EBE5E0 at its centre, and the odd 101-color custom ramp sampled #FFFFFF exactly.

**Execution evidence:** Executed run/regressions.R on synthetic_skewed_lfc.csv; opened figs/i2_diverging_centres.png.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**
- [PASS] Bounds are symmetric at plus/minus the 99th percentile of absolute LFC - The computed limits were -4.814764 and +4.814764.
- [PASS] Zero is anchored at the built-in vik centre - midpoint=0 and symmetric limits place zero at the measured #EBE5E0 centre.
- [PASS] The output does not mislabel vik's centre as pure white - The output explicitly reports the near-neutral built-in centre.
- [PASS] A custom ramp can deliberately sample exact white at zero - The 101-color custom ramp's 51st color was #FFFFFF.
- [PASS] Both diverging arms and the neutral region are visually legible - Manual inspection found no blank panel or lost midpoint; the skewed positive block and negative block remain distinct.

### Input 3 - Edge: CVD and grayscale audit of sequential and rainbow-like candidates

**Prompt:** Run colorspace::cvd_emulator on the current palette and report whether the categories remain distinguishable under deuteranopia; also verify it prints correctly in grayscale. Candidates: viridis, cividis, batlow, turbo, rainbow.

**Generated code / run:** `run/regressions.R and run/regressions.py (desaturate/L* and complete CVD transforms)`

**Output:** The corrected workflow uses deutan/protan/tritan transforms and desaturates the actual palette. batlow remained luminance-monotonic; turbo was correctly identified as non-monotonic.

**Execution evidence:** Executed run/regressions.R and run/regressions.py; opened figs/i3_grayscale_cvd.png.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**
- [PASS] The grayscale check desaturates the actual palette - colorspace::desaturate(batlow) was rendered rather than a generic grey ramp.
- [PASS] batlow has monotonic CIELAB lightness - All successive L* differences had one direction.
- [PASS] turbo is not presented as luminance-monotonic - The regression asserted that turbo L* rises and then falls.
- [PASS] The CVD code performs deutan, protan, and tritan simulations and reports distances - Both R and Python produced finite minimum pairwise distances for all three simulations.
- [PASS] The simulated and grayscale panels are visually inspectable - Manual inspection confirmed six non-blank labeled swatches and visible turbo light-dark reversal.

### Input 4 - Variant B: Migrate sequential, signed, and cyclic matplotlib panels away from jet

**Prompt:** Find every plot in this notebook that uses cmap='jet' and replace it; the spatial map, the signed log-ratio panel and the phase panel are all affected.

**Generated code / run:** `run/regressions.py (batlow, symmetric vik q99, romaO)`

**Output:** The migration chose batlow for magnitude, vik with symmetric q99 bounds for signed data, and romaO for phase. Zero normalized to 0.5 and romaO/vikO/twilight seam distances were below 2.

**Execution evidence:** Executed run/regressions.py on synthetic_spatial_expr.npy; opened figs/i4_jet_migration_fixed.png.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**
- [PASS] The sequential panel no longer uses jet or rainbow - It uses cmcrameri batlow.
- [PASS] The signed panel uses a diverging palette and symmetric data-derived limits - vik uses plus/minus q99=5.956655 and maps zero to 0.5.
- [PASS] The phase panel uses a cyclic palette - romaO is used from 0 to 2*pi.
- [PASS] Cyclic palette endpoints close without an artificial seam - romaO, vikO, and twilight endpoint distances were each below 2 CAM02-UCS units.
- [PASS] All three migrated panels render with visible data and color bars - Manual inspection confirmed three non-blank, appropriately encoded panels.

### Input 5 - Stress: Run both shipped examples and assess 15-group and journal palettes

**Prompt:** Run the shipped examples, then color 15 clusters and tell me whether npg/aaas/lancet are safe for the reviewers.

**Generated code / run:** `run/skill/examples/*.R, run/skill/tests/*, and both regression scripts`

**Output:** Both shipped examples reached their PASS sentinels and emitted non-empty outputs. The four-panel example follows batlow/vik/named-Okabe-Ito guidance. Journal palettes had deutan minima below 10, and tab20/Paired/Set3 were correctly rejected as hue-only accessibility solutions.

**Execution evidence:** Executed copied fixed tests and examples from run/skill; opened figs/i5_palette_examples_fixed.png and verified all emitted PNGs with run/inspect_images.py.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

**Assertions:**
- [PASS] Both shipped R examples execute on self-contained synthetic data - palette_examples.R and palettes_phd.R ran and emitted non-empty PDF output.
- [PASS] The four-panel example follows the Skill's current palette guidance - It uses batlow, symmetric vik, named Okabe-Ito, and stable subsetting.
- [PASS] Journal palettes are not claimed to be universal accessibility defaults - Measured deutan minima were npg 9.66, aaas 8.96, and lancet 7.51.
- [PASS] The 15-group request is not answered with a supposedly CVD-safe hue-only palette - tab20, Paired, and Set3 each had deutan minimum distance below 10 and the output routes to redundant encodings.
- [PASS] The representative shipped example is visually sound - Manual inspection confirmed four populated panels, outlined midpoint points, and stable categorical colors.

### Input 6 - Scope Boundary: Thirty clusters with a request for hue-only identity colors

**Prompt:** I have 30 clusters and the journal wants one unique color per cluster. Just give me a CVD-safe 30-color palette; do not use shapes, labels, or facets.

**Generated code / run:** `run/regressions.R (30 labeled free-scale facets, one accessible accent)`

**Output:** The output declines to imply that 30 unique hues can be CVD-safe, then uses direct facet labels and a single accessible accent. All 30 labels are present and only one identity color is used.

**Execution evidence:** New input executed in run/regressions.R; opened figs/i6_thirty_groups_faceted.png.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100

**Assertions:**
- [PASS] The output refuses the false promise of 30 CVD-safe identity hues - It explicitly treats hue-only encoding beyond eight groups as unsafe.
- [PASS] A practical redundant alternative is produced - The plot uses direct facet labels rather than color identity.
- [PASS] All 30 clusters remain represented - The factor has 30 levels and the plot contains 30 labeled facets.
- [PASS] The alternative does not smuggle identity back into hue - ggplot_build found exactly one point color across all facets.
- [PASS] The 30-panel output is visually inspectable - Manual inspection confirmed filled free-scale panels and readable C01-C30 labels.

### Input 7 - Adversarial: Nonzero reference midpoint with missing matrix cells

**Prompt:** Plot a 0-to-1 fraction matrix where 0.5 is the biological reference, values above and below 0.5 are equally important, and some cells are missing. Use a publication-ready diverging encoding and make missing cells unambiguous.

**Generated code / run:** `run/regressions.py (masked array, TwoSlopeNorm(vcenter=0.5), set_bad('#BBBBBB'))`

**Output:** The output generalized the diverging principle to a scientifically meaningful reference of 0.5, masked 48 missing cells, and encoded them as #BBBBBB. The reference maps exactly to 0.5 in the norm.

**Execution evidence:** New input executed in run/regressions.py; opened figs/i7_nonzero_midpoint_missing.png.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100

**Assertions:**
- [PASS] The scientifically meaningful 0.5 reference maps to the diverging centre - TwoSlopeNorm(vcenter=0.5) returns 0.5 at the reference.
- [PASS] Missing values are not silently mapped to a quantitative color - The masked array uses cmap bad color #BBBBBB.
- [PASS] All missing cells are preserved as missing - The mask count is 48, matching the synthetic missing block.
- [PASS] The two arms use explicit symmetric conceptual bounds around the reference - The fraction limits are 0 and 1 around reference 0.5.
- [PASS] The reference and missing regions are visually distinct - Manual inspection shows a white reference block and a separate grey missing block.

## Static evaluation

| Category | Score | Note |
|---|---:|---|
| Functional Suitability | 12/12 | Completeness 4, correctness 4, appropriateness 4. Sequential, diverging, cyclic, categorical, CVD, grayscale, migration, and >8-group boundaries are consistent and executable. |
| Reliability | 10/12 | Fault tolerance 3, error reporting 3, recoverability 4. Version-introspection and design fallbacks are clear, although arbitrary non-finite data and custom reference points require agent judgment. |
| Performance Context | 8/8 | Token cost 4, efficiency 4. SKILL.md is 252 lines; the guide routes rather than duplicates, and executable depth lives in examples/tests. |
| Agent Usability | 15/16 | Learnability 4, consistency 4, feedback design 3, error prevention 4. The workflow is internally consistent and preventive; a compact result-report contract would further standardize responses. |
| Human Usability | 7/8 | Discoverability 4, forgiveness 3. Natural prompts cover common requests; unusual nonzero midpoints and missing encodings are handled by generalization rather than explicit examples. |
| Security | 11/12 | Credential safety 4, input validation 3, data safety 4. No secrets, shell interpolation, network calls, destructive operations, or data retention are present. |
| Maintainability | 12/12 | Modularity 4, modifiability 4, testability 4. Concise guide, two self-contained examples, and focused R/Python contract tests cleanly separate responsibilities. |
| Agent Specific | 18/20 | Trigger precision 4, progressive disclosure 4, composability 3, idempotency 4, escape hatches 3. The trigger is precise and >8/>20 group limits are explicit; response integration points remain informal. |

## Veto gates

- T1 Stability: PASS - every output was produced and checked; the R post-success exit is independently environment-wide.
- T2 Contract: PASS - required frontmatter and shipped paths are present; report schema validated.
- T3 Determinism: PASS - fixtures are fixed, examples seed randomness, and reruns reproduce asserted values.
- T4 Security: PASS - no raw-string execution, credential handling, network access, or destructive operation.
- M1 Scientific Integrity: PASS - all numeric claims are computed and saved.
- M2 Practice Boundaries: PASS - visualization guidance only.
- M3 Methodological Ground: PASS - encodings match data semantics and accessibility limits are explicit.
- M4 Code Usability: PASS - R/Python contracts and all seven outputs executed; checked artifacts are non-blank.

## Open recommendations

- P2: Add a compact response contract covering palette type, limits/midpoint, CVD minima, luminance verdict, redundant encoding, and visual inspection.
- P2: Add a compact example for arbitrary scientific reference points and explicit missing-value colors.

## Evidence index

- Full run: `run/run_all.out`
- R regressions: `run/regressions.R`, `run/regressions_r.out`
- Python regressions: `run/regressions.py`, `run/regressions_py.out`
- Fixed Skill snapshot and tests: `run/skill/`
- Pixel checks: `run/inspect_images.py`, `run/inspect_images.out`
- Runtime probes: `run/r_exit_probe.R`, `run/r_exit_probe.out`, `run/r_package_exit_probe.R`
- Figures: `figs/i1_named_okabe_stability.png` through `figs/i7_nonzero_midpoint_missing.png`
