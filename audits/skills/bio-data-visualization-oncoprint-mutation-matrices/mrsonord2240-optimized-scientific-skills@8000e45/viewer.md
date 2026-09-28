> **Audit record for `bio-data-visualization-oncoprint-mutation-matrices`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@8000e45](https://github.com/mrsonord2240/optimized-scientific-skills/tree/8000e4567f1b47a812706874f7091fdc21816df2/skills/bio-data-visualization-oncoprint-mutation-matrices) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-27 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-oncoprint-mutation-matrices

Generated: 2026-09-27

Source: `mrsonord2240/optimized-scientific-skills@8000e4567f1b47a812706874f7091fdc21816df2:skills/bio-data-visualization-oncoprint-mutation-matrices`

Independent auditor: `true`

## Outcome

Final score **97/100** — ⭐ **Production Ready**; deployable **true**.

Executed **11/11** inputs; assertion pass rate **53/53 (100.0%)**. All structural and research veto dimensions PASS.

The audit contains eleven inputs because the dispatch required all nine archived round-one inputs as regressions plus at least two genuinely new round-two inputs; this intentionally exceeds the older schema note that listed at most eight.

## Summary Table

| Input | Type | Label | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | Cohort-complete TCGA-LAML ComplexHeatmap OncoPrint | 38 | 57 | 95 | 5/5 | ✅ |
| 2 | Variant A | maftools rapid MAF view with complete clinical colors | 36 | 53 | 89 | 4/4 | ✅ |
| 3 | Edge | Thirty-sample planted edge cohort | 38 | 57 | 95 | 5/5 | ✅ |
| 4 | Variant B | Burden-sorted cohort-complete TCGA-LAML comut plot | 38 | 57 | 95 | 5/5 | ✅ |
| 5 | Stress | Six-hundred-sample split OncoPrint and shipped full example | 38 | 56 | 94 | 5/5 | ✅ |
| 6 | Scope Boundary | Pairwise interaction table and plot | 37 | 56 | 93 | 5/5 | ✅ |
| 7 | Adversarial | Mismatched IDs, unmapped classes, and denominator inflation request | 37 | 55 | 92 | 4/4 | ✅ |
| 8 | Variant B | New all-six-class additional-call seam | 38 | 57 | 95 | 5/5 | ✅ |
| 9 | Adversarial | New minimal comut path and numeric validation | 38 | 57 | 95 | 5/5 | ✅ |
| 10 | Edge | Exact sample-label threshold and unified-legend boundary | 39 | 58 | 97 | 5/5 | ✅ |
| 11 | Adversarial | Normalized-ID collisions and file-level invalid TMB | 39 | 59 | 98 | 5/5 | ✅ |

## Execution environment and source integrity

- R 4.4.3: ComplexHeatmap 2.22.0, maftools 2.22.0, circlize 0.4.18 via the required `r.sh` wrapper.
- Python 3.12: pandas 2.3.3, comut 0.0.3, matplotlib 3.11.2 via `PYENV=venv-pd2 py.sh`.
- Provider worktree HEAD: `8000e4567f1b47a812706874f7091fdc21816df2`; `git status --short` remained empty.
- The copied SKILL.md and provider SKILL.md SHA-256 hashes match; see `run/out/source_hashes.log`.
- Automated artifact verification: all scored PNGs parse, exceed 1 KB, have valid dimensions, and exceed 0.5% nonwhite pixels. Sixteen scored PNGs were opened in the contact sheet; four round-two-critical figures were also opened at native resolution.

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

**Output:** The shipped script and CLI retained all 200 samples in deterministic TMB order, rendered complete alteration and FAB legends, and automatically hid the unreadable dense sample labels.

**Executed:** true — run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i4_laml_comut_direct.png; run/out/i4_laml_comut_cli.png

**Visual review:** Opened both figures: the mutation/FAB legends are complete and readable, while the 200 dense sample labels are correctly absent.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**

- [PASS] The shipped Python CLI runs in its documented pandas 2 environment — Both direct API and CLI execution completed under pandas 2.3.3/comut 0.0.3.
- [PASS] All cohort samples are retained and ordered by descending TMB — 200 samples exactly matched independently computed (-TMB, sample ID) order.
- [PASS] The top gene is drawn at the top and the TMB scale uses the observed maximum — FLT3 is the top y tick; returned TMB maximum is the observed 42.
- [PASS] The saved plot includes legends for alteration and clinical colors — Rendered legend text contains Mutations, Clinical, every observed alteration class, and all eight FAB values.
- [PASS] Dense sample labels are hidden or remain readable — Rendered-text inspection found no visible x-axis sample labels for the 200-sample cohort.

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

**Output:** The minimal path, ordering, zero-mutation retention, and all validation checks passed; empty cohort IDs and negative TMB were rejected with explicit ValueError messages.

**Executed:** true — run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i9_new_minimal_comut.png

**Visual review:** Opened: the small matrix is crisp and ordered, its alteration legend is complete, and its eight sample labels are readable.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**

- [PASS] The minimal mutation-plus-cohort path renders and retains zero-mutation samples — All eight samples retained; Z7 and Z8 remain as empty trailing columns.
- [PASS] Burden order and top-gene placement are deterministic — Sample order equals independent burden sorting; the most frequent gene is the top y tick.
- [PASS] Unknown samples/classes and duplicate cohort IDs are rejected — All three probes raised clear ValueError messages.
- [PASS] Every cohort sample ID is validated as non-empty — An empty cohort ID was rejected with 'must not be empty or NA'.
- [PASS] TMB values are validated as finite and non-negative — A -1 TMB value was rejected with 'finite and non-negative'.

### Input 10 — Edge: Exact sample-label threshold and unified-legend boundary

**Prompt:** Render a 50-sample comut plot and a 51-sample version with mutation and four-level clinical tracks. Verify the default visibility boundary, force 51 labels with an override, hide all labels with threshold zero, and confirm every displayed color is named in the artifact.

**Output:** At exactly 50 samples every ordered label rendered; at 51 the labels were absent by default; threshold 51 restored all 51; threshold zero hid all 50. Mutation and clinical legend groups and every observed value rendered with nonzero text bounds.

**Executed:** true — run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i10_boundary_50_labels.png; run/out/i10_boundary_51_hidden.png; run/out/i10_boundary_51_forced.png

**Visual review:** Opened all three: legends are complete; 50 labels are individually rendered, the 51-label default is clean, and the forced 51-label override behaves as documented.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**

- [PASS] The default policy renders all sample labels at the documented 50-sample boundary — The 50 rendered labels exactly equal plot.samples in deterministic order.
- [PASS] The default policy hides sample labels immediately above the boundary — The 51-sample figure has zero visible x-label text artists.
- [PASS] The documented threshold override can force or suppress labels — Threshold 51 rendered all 51 labels; threshold 0 hid all labels in the 50-sample plot.
- [PASS] The unified legend names both track groups and all observed values — Rendered text includes Clinical, Mutations, Alpha/Beta/Gamma/Delta, and Missense/Truncating/Splice.
- [PASS] Every boundary figure is nonblank and visually coherent — Three PNGs are 1220 pixels wide, 20-43 KB, and 40.4-41.3% nonwhite; all were opened.

### Input 11 — Adversarial: Normalized-ID collisions and file-level invalid TMB

**Prompt:** Run the CLI with surrounding whitespace in otherwise valid IDs, then submit a cohort whose IDs collide after stripping, a quoted whitespace-only cohort ID, and infinite TMB. Also probe NaN, positive/negative infinity, and a small negative TMB through the public function.

**Output:** Valid surrounding whitespace normalized to N01/N02/N03 and rendered through both API and CLI. Duplicate-after-strip, whitespace-only, NaN, both infinities, and negative TMB were all rejected; CLI transcripts retained the documented error messages.

**Executed:** true — run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i11_validation_cli.log; run/out/i11_normalized_ids.png; run/out/i11_normalized_ids_cli.png

**Visual review:** Opened direct and CLI figures: both show the same normalized sample order, complete clinical/mutation legends, readable labels, and valid zero-based TMB mapping.

**Scores:** Basic 39/40 | Specialized 59/60 | Total 98/100

**Assertions:**

- [PASS] Surrounding ID whitespace is normalized consistently across mutation, clinical, TMB, and cohort inputs — The direct and CLI paths produced ordered samples N01, N02, N03 and nonblank figures.
- [PASS] Cohort IDs that collide after normalization are rejected — Both direct and CLI probes reported that IDs must be unique after normalization.
- [PASS] A file-level whitespace-only cohort ID is rejected — The quoted TSV value reached validation and produced 'must not be empty or NA'.
- [PASS] Non-finite and negative TMB values are rejected — NaN, +Inf, -Inf, and -0.01 failed directly; CLI infinite TMB failed with the documented message.
- [PASS] Validation failures do not create output figures — All three invalid CLI calls returned nonzero and the should-not-exist targets were absent.

## Static Score

- `functional_suitability`: 12/12 — All promised workflows are present and core scientific claims matched execution, including full-cohort denominators, row order, interaction return schema, CNV/fusion merging, and tool-specific caveats.
- `reliability`: 12/12 — Major ID, class, duplicate, all-empty, label-threshold, and burden-value failures are explicit; valid reruns and invalid-input rejection are deterministic.
- `performance_context`: 8/8 — SKILL.md is concise, routes complex logic to two scripts and one example, and avoids duplicated workflow prose in the usage guide.
- `agent_usability`: 16/16 — Selection guidance, contracts, output expectations, legend policy, label threshold, caveats, and error-prevention notes are precise and executable.
- `human_usability`: 8/8 — Natural trigger language is strong; defaults produce self-describing dense-safe artifacts, and the documented override preserves intentional control.
- `security`: 12/12 — No credentials, network calls, code injection, or destructive actions; identifiers, categorical values, and numeric burden data are validated before rendering.
- `maintainability`: 12/12 — Matrix construction, rendering, CLI logic, and regression tests are cleanly separated; all shipped paths parsed and all three shipped tests ran.
- `agent_specific`: 20/20 — Triggering, progressive disclosure, composability, idempotency, strict stop conditions, and explicit CLI overrides are all well calibrated.

Static subtotal: **100/100**. Execution average: **94.4/100**. Final: **97/100**.

## Veto Review

- Structural veto: PASS — stability, contract, determinism, and security all pass.
- Research veto: PASS — scientific integrity, practice boundaries, methodological ground, and code usability all pass.
- No safety or scope assertion failed.

## Open Findings

No open recommendations. The round-one P1 legend/dense-label finding and P2 ID/TMB-validation finding both passed regression and two new boundary/adversarial scenarios.

Open counts: **P0 0, P1 0, P2 0**.
