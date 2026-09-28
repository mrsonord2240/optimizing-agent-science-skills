> **Audit record for `bio-data-visualization-color-palettes`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@99b1d0a](https://github.com/mrsonord2240/optimized-scientific-skills/tree/99b1d0ad49174e647b358c58d487f5c20aa56c5c/skills/bio-data-visualization-color-palettes) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-27 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-color-palettes

Generated: 2026-09-27

## Summary

This independent round-two re-audit held provider commit `99b1d0ad49174e647b358c58d487f5c20aa56c5c` immutable. It reran all seven archived inputs and added two genuinely new cases inside the eighth scored stress input, for nine distinct executed cases.

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 57 | 95 | 5/5 | ✅ |
| 2 | Variant A | 39 | 58 | 97 | 5/5 | ✅ |
| 3 | Edge | 39 | 58 | 97 | 5/5 | ✅ |
| 4 | Variant B | 39 | 58 | 97 | 5/5 | ✅ |
| 5 | Stress | 38 | 56 | 94 | 5/5 | ✅ |
| 6 | Scope Boundary | 38 | 55 | 93 | 5/5 | ✅ |
| 7 | Adversarial | 38 | 58 | 96 | 5/5 | ✅ |
| 8 | Stress | 39 | 59 | 98 | 5/5 | ✅ |

**Execution average:** 95.9/100  
**Assertion pass rate:** 40/40 (100%)  
**Executed:** 8/8 scored inputs; 9/9 distinct cases  
**Vetoes:** none  
**Open findings:** 0 P0, 0 P1, 0 P2

## Detailed outputs

### Input 1 — Canonical: Named Okabe-Ito mapping for seven cell types plus unassigned

**Prompt:** Assign stable colors to seven cell types plus Unassigned, preserve identities after subsetting, and check CVD behavior.

**Output:** A named seven-color Okabe-Ito mapping plus Unassigned=#BBBBBB remained stable after T cells were removed. Unassigned also used a cross marker. R CIELAB minima after deutan/protan/tritan transforms were 14.93/20.71/16.17.

**Execution evidence:** `run/regressions.R; figs/i1_named_okabe_stability.png`

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**
- [PASS] Every category is assigned through a named mapping and Unassigned is light grey — Seven chromatic names plus Unassigned=#BBBBBB were present.
- [PASS] Removing T cells does not recolor any remaining category — Full and subset ggplot_build mappings were identical for shared levels.
- [PASS] All three CVD simulations produce finite positive minimum distances — R minima were 14.93, 20.71, and 16.17; Python independently returned 14.17, 13.96, and 10.97.
- [PASS] A redundant non-color encoding distinguishes the reserve class — Unassigned uses marker 4 while chromatic categories use marker 16.
- [PASS] The full and subset plots render non-blank with readable legends — The opened figure showed stable colors, the grey cross class, and complete legends.

### Input 2 — Variant A: vik log-fold-change heatmap with symmetric q99 bounds

**Prompt:** Use vik for a signed LFC heatmap, anchor zero, derive symmetric robust bounds, and compare its built-in centre to an exact-white custom ramp.

**Output:** The q99 absolute-LFC bound was 4.814764. vik sampled #EBE5E0 at the centre, while the odd 101-color custom ramp sampled #FFFFFF exactly; both arms and the neutral region remained visible.

**Execution evidence:** `run/regressions.R; figs/i2_diverging_centres.png`

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**
- [PASS] Bounds are symmetric at plus/minus the 99th percentile of absolute LFC — The computed limits were -4.814764 and +4.814764.
- [PASS] Zero is anchored at the built-in vik centre — midpoint=0 and symmetric limits place zero at #EBE5E0.
- [PASS] The output does not mislabel vik's centre as pure white — The measured near-neutral centre is reported explicitly.
- [PASS] A custom ramp can deliberately sample exact white at zero — The 101-color custom ramp's 51st color was #FFFFFF.
- [PASS] Both diverging arms and the neutral region are visually legible — The opened heatmaps showed the positive block, negative block, and midpoint without blank panels.

### Input 3 — Edge: CVD and grayscale audit of sequential and rainbow-like candidates

**Prompt:** Audit batlow and turbo under grayscale plus deutan, protan, and tritan simulation, and report whether luminance is monotonic.

**Output:** The actual batlow palette remained luminance-monotonic after desaturation; turbo rose then fell in L*. All three CVD transformations returned finite positive distances and the six swatches rendered correctly.

**Execution evidence:** `run/regressions.R and run/regressions.py; figs/i3_grayscale_cvd.png`

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**
- [PASS] The grayscale check desaturates the actual palette — colorspace::desaturate(batlow) was rendered, not a generic grey ramp.
- [PASS] batlow has monotonic CIELAB lightness — All successive L* differences had one direction.
- [PASS] turbo is not presented as luminance-monotonic — The regression asserted that turbo L* rises and then falls.
- [PASS] The CVD code performs all three simulations and reports distances — Both R and Python produced finite minima for deutan/protan/tritan variants.
- [PASS] The simulated and grayscale panels are visually inspectable — The opened figure showed six labeled, populated swatches and turbo's light-dark reversal.

### Input 4 — Variant B: Migrate sequential, signed, and cyclic panels away from jet

**Prompt:** Replace jet across a magnitude panel, a signed panel, and a phase panel with semantically correct palettes and preserve cyclic closure.

**Output:** The migration used batlow for magnitude, vik with symmetric q99=5.956655 for signed data, and romaO for phase. Zero normalized to 0.5; tested cyclic seams stayed below two CAM02-UCS units.

**Execution evidence:** `run/regressions.py; figs/i4_jet_migration_fixed.png`

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**
- [PASS] The sequential panel no longer uses jet or rainbow — It uses cmcrameri batlow.
- [PASS] The signed panel uses a diverging palette and symmetric data-derived limits — vik uses plus/minus q99 and maps zero to 0.5.
- [PASS] The phase panel uses a cyclic palette — romaO is used from zero to 2*pi.
- [PASS] Cyclic endpoints close without an artificial seam — romaO, vikO, and twilight endpoint distances were each below two CAM02-UCS units.
- [PASS] All three panels render with visible data and color bars — The opened output contained three populated, appropriately encoded panels.

### Input 5 — Stress: Run shipped examples and assess many-group and journal palettes

**Prompt:** Run both shipped examples, then assess a 15-group request and the npg/aaas/lancet palettes for accessibility claims.

**Output:** Both examples reached PASS sentinels and emitted non-empty artifacts. The representative figure used batlow, symmetric vik, and stable named mappings. Journal and many-group palettes retained close CVD pairs, so the output did not claim universal safety.

**Execution evidence:** `run/skill/examples, run/run_fixed_tests.R, run/regressions.*, figs/i5_palette_examples_fixed.png`

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

**Assertions:**
- [PASS] Both shipped R examples execute on self-contained synthetic data — Both ran and emitted non-empty PDF output.
- [PASS] The four-panel example follows the current guidance — It uses batlow, symmetric vik, named Okabe-Ito, and stable subsetting.
- [PASS] Journal palettes are not claimed as universal accessibility defaults — Measured deutan minima were npg 9.66, aaas 8.96, and lancet 7.51.
- [PASS] The 15-group request is not answered with a supposedly CVD-safe hue-only palette — tab20, Paired, and Set3 each had a deutan minimum below 10.
- [PASS] The representative shipped example is visually sound — The opened four-panel figure was populated and its categorical identities stayed stable.

### Input 6 — Scope Boundary: Thirty clusters with a request for hue-only identity colors

**Prompt:** Give me 30 unique CVD-safe identity hues and do not use labels, shapes, or facets.

**Output:** The response declined the false accessibility promise and produced 30 directly labeled facets using one accessible accent. All clusters remained represented without smuggling identity back into hue.

**Execution evidence:** `run/regressions.R; figs/i6_thirty_groups_faceted.png`

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100

**Assertions:**
- [PASS] The output refuses the false promise of 30 CVD-safe identity hues — Hue-only encoding beyond eight groups is identified as unsafe.
- [PASS] A practical redundant alternative is produced — The plot uses direct facet labels.
- [PASS] All 30 clusters remain represented — The factor has 30 levels and the opened plot has 30 labeled facets.
- [PASS] The alternative does not smuggle identity back into hue — ggplot_build found exactly one point color across all facets.
- [PASS] The 30-panel output is visually inspectable — The opened output showed populated C01-C30 facets with readable labels.

### Input 7 — Adversarial: Nonzero 0.5 reference with missing matrix cells

**Prompt:** Plot a 0-to-1 fraction matrix centered on the scientific reference 0.5 and make missing cells unambiguous.

**Output:** TwoSlopeNorm mapped the declared reference to 0.5, 48 missing cells stayed masked, and #BBBBBB separated missingness from the quantitative palette. The opened figure showed distinct white-reference and grey-missing regions.

**Execution evidence:** `run/regressions.py; figs/i7_nonzero_midpoint_missing.png`

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100

**Assertions:**
- [PASS] The 0.5 scientific reference maps to the diverging centre — TwoSlopeNorm(vcenter=0.5) returns 0.5 at the reference.
- [PASS] Missing values are not silently mapped to a quantitative color — The copied colormap uses #BBBBBB as its bad color.
- [PASS] All missing cells are preserved as missing — The mask count is 48, matching the synthetic block.
- [PASS] The response reports reference, bounds, and masked count — The current guidance explicitly requires these fields.
- [PASS] Reference and missing regions are visually distinct — The opened figure shows the white reference block separately from the grey missing block.

### Input 8 — Stress: Two new cases: response contract and arbitrary physical reference

**Prompt:** Case A: return a complete palette-audit contract for a masked sequential heatmap. Case B: center a physical scale on 37.2, mask NaN and both infinities, and reject a reference on a bound.

**Output:** Case A emitted all seven contract fields with cividis, percentile bounds, 30 masked cells, monotonic L*, explicit not-applicable CVD entries, a redundant-encoding rationale, and an inspection artifact. Case B mapped 37.2 to 0.5, masked five NaN/+Inf/-Inf cells in grey, and raised ValueError when vmin equaled the reference.

**Execution evidence:** `run/input8_response_contract.json, run/input9_response_contract.json, run/regressions.py, figs/i8_response_contract.png, figs/i9_arbitrary_reference_nonfinite.png`

**Scores:** Basic 39/40 | Specialized 59/60 | Total 98/100

**Assertions:**
- [PASS] Case A contains every response-contract field — The JSON has exactly palette/type, normalization/bounds/reference, missingness, CVD, luminance, redundant encoding, and visual inspection.
- [PASS] Case A computes rather than invents contract values — Bounds, 30 masked cells, and minimum L* delta came from the saved synthetic array.
- [PASS] Case B maps the arbitrary reference 37.2 to the palette centre — TwoSlopeNorm returned exactly 0.5 for 37.2.
- [PASS] Case B preserves all NaN, +Inf, and -Inf cells as missing — Five mixed non-finite cells remained masked and used #BBBBBB.
- [PASS] Both new figures are non-blank and independently inspectable — Both opened outputs showed the expected scale, reference behavior, and visible grey missing cells; pixel checks also passed.

## Static evaluation

| Category | Score | Note |
|---|---:|---|
| Functional Suitability | 12/12 | Completeness 4, correctness 4, appropriateness 4. Sequential, diverging, cyclic, categorical, CVD, grayscale, many-group, nonzero-reference, and missing-value workflows are complete and consistent. |
| Reliability | 11/12 | Fault tolerance 4, error reporting 3, recoverability 4. Non-finite values are explicitly masked and invalid diverging bounds are rejected; underlying library errors remain plain rather than structured. |
| Performance / Context | 8/8 | Token cost 4, efficiency 4. SKILL.md is 283 lines, the guide routes instead of duplicating, and executable depth remains in examples/tests. |
| Agent Usability | 16/16 | Learnability 4, consistency 4, feedback design 4, error prevention 4. The seven-field response checklist makes completion and verification observable. |
| Human Usability | 8/8 | Discoverability 4, forgiveness 4. Natural prompts cover standard cases, while arbitrary references and NaN/infinity handling are explicit. |
| Security | 12/12 | Credential safety 4, input validation 4, data safety 4. There are no secrets, raw-string execution, network calls, destructive operations, or data-retention hazards; bounds and finite values are checked. |
| Maintainability | 12/12 | Modularity 4, modifiability 4, testability 4. A concise guide, self-contained examples, and focused R/Python contract tests cleanly separate responsibilities. |
| Agent-Specific | 19/20 | Trigger precision 4, progressive disclosure 4, composability 4, idempotency 4, escape hatches 3. The response contract creates a clean integration seam; broad stop/handoff guidance is naturally limited for this advisory visualization Skill. |

## Veto gates

- T1 Stability: PASS — all outputs were produced and checked; the R package-teardown exit is environment-wide.
- T2 Contract: PASS — required frontmatter, shipped paths, and report fields are present and consistent.
- T3 Determinism: PASS — saved fixtures and fixed seeds reproduce asserted values.
- T4 Security: PASS — no raw-string execution, credential handling, network access, or destructive operations.
- M1 Scientific Integrity: PASS — every numerical claim is computed and preserved in run evidence.
- M2 Practice Boundaries: PASS — visualization guidance only.
- M3 Methodological Ground: PASS — encodings match data semantics and accessibility limitations are explicit.
- M4 Code Usability: PASS — all R/Python PASS sentinels and checked artifacts were produced.

## Environment-exit distinction

Every R Skill run reached its PASS sentinel and emitted checked output before the shared launcher returned exit 2816. `run/r_exit_probe.R` exited 0; `run/r_package_exit_probe.R` printed `loaded ggplot2 4.0.3` and then returned 2816. This reproduces the teardown behavior without Skill code, so it is recorded as environment behavior rather than an execution failure.

## Source integrity

`run/source_integrity_before.out` and `run/source_integrity_after.out` are byte-identical. Both record provider HEAD `99b1d0ad49174e647b358c58d487f5c20aa56c5c`, an empty status, and the same SHA-256 digest for every Skill file.

## Open recommendations

None. The two prior P2 findings are closed by the response contract and explicit arbitrary-reference/non-finite guidance, and the independent runs found no replacement defects.

## Evidence index

- Full run: `run/run_all.ps1`, `run/run_all.out`
- R regressions and environment probes: `run/regressions.R`, `run/regressions_r.out`, `run/r_exit_probe.*`, `run/r_package_exit_probe.*`
- Python regressions and new response contracts: `run/regressions.py`, `run/regressions_py.out`, `run/input8_response_contract.json`, `run/input9_response_contract.json`
- Fixed Skill snapshot and tests: `run/skill/`, `run/fixed_contracts_*.out`, `run/fixed_examples_r.out`
- Pixel checks and manual visual review: `run/inspect_images.py`, `run/inspect_images.out`, `figs/i1_*.png` through `figs/i9_*.png`
- Provider immutability: `run/source_integrity.ps1`, `run/source_integrity_before.out`, `run/source_integrity_after.out`
