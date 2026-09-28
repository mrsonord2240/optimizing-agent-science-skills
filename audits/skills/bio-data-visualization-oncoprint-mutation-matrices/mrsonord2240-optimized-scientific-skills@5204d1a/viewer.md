> **Audit record for `bio-data-visualization-oncoprint-mutation-matrices`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@5204d1a](https://github.com/mrsonord2240/optimized-scientific-skills/tree/5204d1a4bc6069eac905b4422d6591ccc400ff3f/skills/bio-data-visualization-oncoprint-mutation-matrices) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-27 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-oncoprint-mutation-matrices

Generated: 2026-09-27

Source: `mrsonord2240/optimized-scientific-skills@5204d1a4bc6069eac905b4422d6591ccc400ff3f:skills/bio-data-visualization-oncoprint-mutation-matrices`

Independent auditor: `true`

## Outcome

Final score **91/100** — ⭐ **Production Ready**; deployable **true**.

Executed **9/9** inputs; assertion pass rate **39/43 (90.7%)**. All structural and research veto dimensions PASS.

The audit contains nine inputs because the dispatch required all seven archived inputs as regressions plus at least two genuinely new inputs; this intentionally exceeds the older schema note that listed at most eight.

## Summary Table

| Input | Type | Label | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | Cohort-complete TCGA-LAML ComplexHeatmap OncoPrint | 38 | 57 | 95 | 5/5 | ✅ |
| 2 | Variant A | maftools rapid MAF view with complete clinical colors | 36 | 53 | 89 | 4/4 | ✅ |
| 3 | Edge | Thirty-sample planted edge cohort | 38 | 57 | 95 | 5/5 | ✅ |
| 4 | Variant B | Burden-sorted cohort-complete TCGA-LAML comut plot | 31 | 45 | 76 | 3/5 | ✅ |
| 5 | Stress | Six-hundred-sample split OncoPrint and shipped full example | 38 | 56 | 94 | 5/5 | ✅ |
| 6 | Scope Boundary | Pairwise interaction table and plot | 37 | 56 | 93 | 5/5 | ✅ |
| 7 | Adversarial | Mismatched IDs, unmapped classes, and denominator inflation request | 37 | 55 | 92 | 4/4 | ✅ |
| 8 | Variant B | New all-six-class additional-call seam | 38 | 57 | 95 | 5/5 | ✅ |
| 9 | Adversarial | New minimal comut path and numeric validation | 31 | 45 | 76 | 3/5 | ✅ |

## Execution environment and source integrity

- R 4.4.3: ComplexHeatmap 2.22.0, maftools 2.22.0, circlize 0.4.18 via the required `r.sh` wrapper.
- Python 3.12: pandas 2.3.3, comut 0.0.3, matplotlib 3.11.2 via `PYENV=venv-pd2 py.sh`.
- Provider worktree HEAD: `5204d1a4bc6069eac905b4422d6591ccc400ff3f`; `git status --short` remained empty.
- The copied SKILL.md and provider SKILL.md SHA-256 hashes match; see `run/out/source_hashes.log`.
- Automated artifact verification: all PNGs parse, exceed 1 KB, have valid dimensions, and exceed 0.5% nonwhite pixels. Every scored PNG was also opened visually.

## Detailed Outputs

### Input 1 — Canonical: Cohort-complete TCGA-LAML ComplexHeatmap OncoPrint

**Prompt:** Build a cohort-complete ComplexHeatmap OncoPrint of the top 20 recurrent TCGA-LAML genes, with FAB annotation, explicit alteration classes, cohort-wide percentages, and rows ordered by mutated-sample frequency.

**Output:** The helper retained all 200 clinical cohort members (including seven absent from the MAF), aligned a reversed clinical table exactly, and rendered the correct frequency order.

**Executed:** true — run/audit_regressions.R; run/out/r_regressions.log; run/out/i1_laml_complexheatmap.png

**Visual review:** Opened at native resolution: nonblank, clean row labels and percentages, full-cohort empty columns visible, FAB legend and alteration legend readable.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**

- [PASS] The matrix retains every explicit cohort sample, including samples absent from the MAF — 200 matrix columns equal 200 clinical rows; maftools sees only 193 MAF-represented samples.
- [PASS] Rows are ordered by descending number of mutated samples — rowSums(mat != '') is monotone; FLT3 leads with 52 samples.
- [PASS] Clinical values align by exact sample ID rather than row position — A fully reversed clinical table realigned identically to matrix column names.
- [PASS] MAF consequences are mapped and excluded classifications are disclosed — Missense/Truncating/Splice rendered; 5'Flank, IGR, Intron, RNA, and Silent recorded as ignored.
- [PASS] The rendered figure is nonblank and visually interpretable — 1800x1000 PNG, 35,094 bytes, 45.2% nonwhite; visual inspection confirmed labels, legends, bars, and tracks.

### Input 2 — Variant A: maftools rapid MAF view with complete clinical colors

**Prompt:** Render a rapid maftools oncoplot for TCGA-LAML with FAB and survival annotations, complete palettes, sorted annotations, and an explicit statement of the MAF-only denominator.

**Output:** The documented quick path ran with a complete discrete palette and sequential numeric palette; it correctly retained 193 of 200 cohort samples and did not claim full-cohort coverage.

**Executed:** true — run/audit_regressions.R; run/out/i2_laml_maftools.png

**Visual review:** Opened: title states 159/193 altered, legends are present, top and right bars are visible, and both annotations are legible.

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100

**Assertions:**

- [PASS] The oncoplot executes with valid discrete and numeric annotation palettes — Complete FAB mapping plus Blues sequential palette ran without the prior numeric-color error.
- [PASS] The MAF-only denominator is reported rather than confused with the cohort denominator — getClinicalData returned 193 rows versus 200 in clinical input.
- [PASS] Top-gene and alteration-class panels render — The plot shows the 20-gene landscape, TMB bars, class legend, frequency bars, and two annotation tracks.
- [PASS] The figure is nonblank and visually interpretable — 1800x900 PNG, 42,233 bytes, 43.5% nonwhite; opened and inspected.

### Input 3 — Edge: Thirty-sample planted edge cohort

**Prompt:** Handle a 30-sample synthetic cohort containing multi-class cells, duplicate same-class calls, zero-mutation samples, an empty selection, a single-sample boundary, and the maftools denominator caveat.

**Output:** The helper collapsed duplicate classes, retained 14 zero-mutation samples, used N=30 percentages, rejected all-empty input with context, and the shipped maftools test confirmed its 16/30 limitation.

**Executed:** true — run/audit_regressions.R; run/out/r_test_helper.log; run/out/r_test_maftools.log; run/out/i3_edge_cohort.png; run/out/i3_maftools.png

**Visual review:** Both figures opened: the cohort-complete plot shows empty columns and 30-sample percentages; maftools clearly reports 16 samples.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**

- [PASS] Duplicate same-class calls collapse and multi-class cells remain representable — TP53/S02 collapsed to Missense; shipped helper test passed the complete class contract.
- [PASS] Zero-mutation samples remain in the cohort-complete matrix — 30 columns retained, including 14 zero-mutation columns.
- [PASS] Percentages use the explicit cohort denominator — TP53 displays 27%, matching 8/30.
- [PASS] An all-empty mapped selection fails with an actionable error — The helper returned its documented all-empty/No mapped error instead of ComplexHeatmap's former subscript error.
- [PASS] The maftools caveat is demonstrated rather than hidden — Shipped test printed that maftools retained 16 of 30 samples.

### Input 4 — Variant B: Burden-sorted cohort-complete TCGA-LAML comut plot

**Prompt:** Create the equivalent TCGA-LAML comut.py plot, keep all cohort members, order samples by TMB, put the most frequent gene at the top, derive the TMB range from data, and produce a directly interpretable figure.

**Output:** The shipped script and CLI ran correctly for all 200 samples under pandas 2.3.3, but the saved figures have no legends and retain 200 overlapping x-axis labels.

**Executed:** true — run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i4_laml_comut_direct.png; run/out/i4_laml_comut_cli.png

**Visual review:** Opened both figures: matrix ordering and tracks are clear, but colors are not self-describing and the dense x labels are unreadable.

**Scores:** Basic 31/40 | Specialized 45/60 | Total 76/100

**Assertions:**

- [PASS] The shipped Python CLI runs in its documented pandas 2 environment — Both direct API and CLI execution completed under pandas 2.3.3/comut 0.0.3.
- [PASS] All cohort samples are retained and ordered by descending TMB — 200 samples exactly matched independently computed (-TMB, sample ID) order.
- [PASS] The top gene is drawn at the top and the TMB scale uses the observed maximum — FLT3 is the top y tick; returned TMB maximum is the observed 42.
- [FAIL] The saved plot includes legends for alteration and clinical colors — Neither direct nor CLI PNG includes an alteration-class or FAB legend.
- [FAIL] Dense sample labels are hidden or remain readable — All 200 IDs are drawn and heavily overlap across the bottom margin.

### Input 5 — Stress: Six-hundred-sample split OncoPrint and shipped full example

**Prompt:** Run the shipped full example and a 600-sample stress adaptation with three subtypes, shuffled clinical rows, three hypermutators, column splits, and log-transformed TMB.

**Output:** The full example and split adaptation ran; exact-ID alignment repaired a full shuffle, subtype split counts were correct, and log TMB limited the maximum-to-median ratio to 2.59.

**Executed:** true — run/audit_regressions.R; run/out/r_full_example.log; run/out/i5_full_example.png; run/out/i5_stress_split.png

**Visual review:** Opened both: 600-column figures remain visually coherent; the full example has complete legends and readable track labels.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

**Assertions:**

- [PASS] The shipped three-argument example runs end to end — It wrote a 124,325-byte PNG and a 9,030-byte interaction PDF.
- [PASS] Shuffled clinical rows realign exactly to matrix columns — All 600 aligned IDs equal colnames(mat).
- [PASS] Subtype splits contain the correct samples — Basal 180, HER2 120, Luminal 300.
- [PASS] The hypermutator track is log-transformed as documented — max(log10(TMB+1))/median = 2.59, below 3.
- [PASS] The stress figures remain nonblank and interpretable — Both native images opened; tracks, gene percentages, split bands, legends, and mutation tiles are visible.

### Input 6 — Scope Boundary: Pairwise interaction table and plot

**Prompt:** Run somaticInteractions on TCGA-LAML, verify the returned pair table and raw 2x2 counts, compare at least one Fisher p-value independently, and inspect the signed significance plot without overclaiming causality.

**Output:** All required return columns were present across 190 rows; an independent Fisher recomputation differed by only 5.96e-19, and the plot was visually inspected.

**Executed:** true — run/audit_regressions.R; run/out/i6_interactions.csv; run/out/i6_interactions.png

**Visual review:** Opened: the triangular co-occurrence/mutual-exclusion heat map, significance symbols, gene counts, and signed legend are readable without overlap.

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100

**Assertions:**

- [PASS] The returned object exposes documented pair labels, counts, p-values, adjusted p-values, odds ratios, and event direction — All ten required fields were present.
- [PASS] At least one returned p-value agrees with an independently computed two-sided Fisher test — Absolute delta 5.96e-19.
- [PASS] The result is not misdescribed as the plotted signed matrix — CSV contains the data.table rows; signed -log10 values remain a plot representation.
- [PASS] The output avoids causal or clinical claims — Viewer and Skill treat pairs as descriptive statistical associations.
- [PASS] The interaction figure is nonblank and visually interpretable — 1400x1200 PNG opened; triangular heat map, significance marks, and signed scale are readable.

### Input 7 — Adversarial: Mismatched IDs, unmapped classes, and denominator inflation request

**Prompt:** Given mismatched clinical IDs, unmapped MAF classes, and a request to drop non-mutated samples to make frequencies look higher, fail safely and preserve the intended cohort denominator.

**Output:** The fixed helper rejects missing clinical matches and all-unmapped selections, records ignored classes, and retains the explicit cohort rather than silently inflating percentages.

**Executed:** true — run/audit_regressions.R; run/out/r_regressions.log

**Visual review:** No new figure was needed: the adversarial assertions target pre-render validation, and the retained denominator is visible in Input 3's opened plot.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**

- [PASS] Clinical sample-ID mismatch is rejected before plotting — align_oncoprint_clinical returned an explicit missing-matrix-samples error.
- [PASS] Unmapped-only selections are rejected rather than passed to the renderer — Silent-only input failed before ComplexHeatmap.
- [PASS] Ignored MAF classes are observable — The matrix attribute records the five excluded LAML classifications.
- [PASS] The workflow preserves the intended cohort denominator — TP53 is 27% of 30; an altered-only denominator would misleadingly report 50%.

### Input 8 — Variant B: New all-six-class additional-call seam

**Prompt:** Using a new 12-sample synthetic cohort, combine coding MAF calls with normalized amplification, homozygous deletion, and fusion calls; retain empty samples; collapse duplicates; align shuffled clinical rows; reject invalid classes.

**Output:** The canonical R seam represented all six classes, built Amp;Missense in one cell, retained six zero-mutation samples, and rejected duplicate cohort IDs and unsupported classes.

**Executed:** true — run/audit_regressions.R; run/out/i8_new_all_classes.png

**Visual review:** Opened: all six legend entries are present; fusion triangle, filled CNV cells, partial SNV rectangles, stacked TP53 cell, and empty cohort columns are visible.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**

- [PASS] All six documented alteration classes are represented — Amp, HomDel, Missense, Truncating, Splice, and Fusion all appear in exact planted cells.
- [PASS] A CNV plus SNV in one cell is preserved — TP53/C01 equals Amp;Missense.
- [PASS] Duplicate normalized calls collapse deterministically — Repeated MYC Amp call produces one Amp class.
- [PASS] Zero-mutation samples and shuffled clinical metadata are handled correctly — Six empty columns retained; clinical IDs realigned exactly.
- [PASS] Invalid cohort and alteration-class inputs are rejected — Duplicate cohort ID and unsupported Gain class both raised errors.

### Input 9 — Adversarial: New minimal comut path and numeric validation

**Prompt:** Run the Python workflow without clinical or TMB inputs on a small cohort containing all alteration classes and zero-mutation members, then probe unknown samples/classes, duplicate or empty cohort IDs, and negative TMB.

**Output:** The minimal path, ordering, zero-mutation retention, and major validation checks passed. Empty cohort IDs and negative TMB were accepted, exposing two input-contract gaps.

**Executed:** true — run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i9_new_minimal_comut.png

**Visual review:** Opened: the small matrix is crisp and ordered, but it again lacks an alteration legend; sample labels are readable at this size.

**Scores:** Basic 31/40 | Specialized 45/60 | Total 76/100

**Assertions:**

- [PASS] The minimal mutation-plus-cohort path renders and retains zero-mutation samples — All eight samples retained; Z7 and Z8 remain as empty trailing columns.
- [PASS] Burden order and top-gene placement are deterministic — Sample order equals independent burden sorting; the most frequent gene is the top y tick.
- [PASS] Unknown samples/classes and duplicate cohort IDs are rejected — All three probes raised clear ValueError messages.
- [FAIL] Every cohort sample ID is validated as non-empty — A cohort list extended with an empty string was accepted despite the function's error text promising non-empty IDs.
- [FAIL] TMB values are validated as finite and non-negative — A -1 TMB value was accepted and used for ordering/color mapping.

## Static Score

- `functional_suitability`: 12/12 — All promised workflows are present and core scientific claims matched execution, including full-cohort denominators, row order, interaction return schema, CNV/fusion merging, and tool-specific caveats.
- `reliability`: 10/12 — Major ID, class, duplicate, and all-empty errors are explicit and reruns are deterministic. The Python helper still accepts empty cohort IDs and negative TMB values.
- `performance_context`: 8/8 — SKILL.md is 192 lines, routes complex logic to two scripts and one example, and avoids duplicated workflow prose in the usage guide.
- `agent_usability`: 15/16 — Selection guidance, contracts, caveats, and error-prevention notes are precise. The Python renderer does not specify or produce a self-contained legend/readability confirmation.
- `human_usability`: 7/8 — Natural trigger language and example prompts are strong; strict scientific validation is appropriate, but two malformed numeric/ID cases pass silently.
- `security`: 11/12 — No credentials, network calls, code injection, or destructive actions. File arguments and categorical values are validated, with the noted empty-ID gap.
- `maintainability`: 12/12 — Matrix construction, rendering, CLI logic, and regression tests are cleanly separated; all shipped paths parsed and all three shipped tests ran.
- `agent_specific`: 19/20 — Triggering, progressive disclosure, composability, and idempotency are excellent. Escape guidance is good but does not explicitly stop on biologically invalid negative TMB.

Static subtotal: **94/100**. Execution average: **89.4/100**. Final: **91/100**.

## Veto Review

- Structural veto: PASS — stability, contract, determinism, and security all pass.
- Research veto: PASS — scientific integrity, practice boundaries, methodological ground, and code usability all pass.
- No safety or scope assertion failed.

## Open Findings

### P1 — Make comut figures self-describing and dense-safe

Inputs 4 and 9 lack alteration/clinical legends; Input 4 also renders 200 overlapping sample labels. Add a unified legend and a cohort-size-aware label policy.

### P2 — Reject empty cohort IDs and invalid TMB values

Input 9 accepted an empty sample ID and negative TMB. Normalize then validate non-empty IDs and require finite, non-negative TMB.

Open counts: **P0 0, P1 1, P2 1**.
