> **Audit record for `bio-workflows-metabolomics-pipeline`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/workflows/metabolomics-pipeline) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-workflows-metabolomics-pipeline (RE-AUDIT, post-fix)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:workflows/metabolomics-pipeline`
Pre-fix report (archived): `F:\OpenScience\audits\_pre-fix-20260916\bio-workflows-metabolomics-pipeline\` — scored 74, Beta Only.
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-workflows-metabolomics-pipeline.md`

Category: Data Analysis | Execution Mode: D (Hybrid — SKILL.md instructions + two bundled runnable
examples) | Complexity: Complex (N=9 — 7 regression inputs re-run against the same real data as the
pre-fix audit, plus 2 new inputs)

Role: supporting (orchestration), floor 75. The five core metabolomics Skills are audited separately;
this audit tests only the orchestrator's own glue — the object hand-offs, transforms, and ordering
between those Skills' documented code, run on real data wherever possible, cross-checked against the
now-fixed and re-audited component Skills (normalization-qc 92, statistical-analysis 96,
pathway-mapping 92).

## What changed since the pre-fix audit

The pre-fix audit found four real defects, all now addressed in the fork:

| Pre-fix finding | Priority | Status this round |
|---|---|---|
| Stage2->Stage4 crashes on real multi-batch data: imputation named in a comment, never called | P1 | **Fixed and verified** (Input 2) — drop-wholly-NA-then-impute now runs end to end on the same real MTBLS79 data, `opls()` fits, `pR2Y=pQ2=0.001` |
| Stage1->Stage2 orientation comment contradicted its own code (`fm <- t(feat)`) | P1 | **Fixed and verified** (Input 1) — transpose removed, `stopifnot` dimension check added |
| Mode-lock and MSI-confidence gate had no enforcing code anywhere | P1 | **Fixed and verified** (Inputs 4, 6) — both now have real, executing code including adversarial edge cases |
| Bundled example never exercised the real multi-package seams | P2 | **Fixed and verified** (Input 8) — new `examples/pipeline_handoff_check.R` runs real `pmp`/`ropls` calls on data shaped like the real failure |

## Skill Veto (Step 1)
Stability PASS | Contract PASS | Determinism PASS | Security PASS — no rejection.

## Research Veto (Step 6, Category 3)
Scientific Integrity PASS | Practice Boundaries PASS | Methodological Ground PASS | Code Usability
PASS — no rejection. M4 detail: 7 of 9 inputs were real code execution this round (up from 3 of 7
pre-fix); both prior P1 crashes are verified fixed with the exact fix-log numbers reproduced.

## Static Score: 91 / 100 (pre-fix: 78/100)
| Category | Score | Note |
|---|---|---|
| Functional Suitability | 10/12 | Both correctness defects fixed; MS-DIAL entry point (Input 5) unchanged gap |
| Reliability | 10/12 | Common Errors table now documents both fixed bugs plus the new failure modes |
| Performance/Context | 7/8 | Grew ~35% adding the fixes, still defers well |
| Agent Usability | 16/16 | Prose/code consistency gap closed |
| Human Usability | 8/8 | QC Checkpoint/Common Errors tables more actionable post-fix |
| Security | 12/12 | Unchanged — no exposure anywhere |
| Maintainability | 10/12 | Bundled-example gap closed; no real Stage 1 xcms example (deferred, out of scope) |
| Agent-Specific | 18/20 | Escape-hatch gap closed — wipe-and-drop is itself the recovery path |

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 2 | Variant A | 37 | 56 | 93 | 5/5 PASS | ✅ |
| 3 | Stress | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 4 | Edge | 38 | 58 | 96 | 4/4 PASS | ✅ |
| 5 | Variant B | 33 | 45 | 78 | 2/3 PASS | ✅ |
| 6 | Scope Boundary | 38 | 58 | 96 | 4/4 PASS | ✅ |
| 7 | Adversarial | 37 | 51 | 88 | 4/4 PASS | ✅ |
| 8 | Stress (NEW) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 9 | Variant A (NEW) | 38 | 55 | 93 | 4/4 PASS | ✅ |

**Execution Average: 92.0 / 100** (pre-fix: 70.7/100)
**Assertion Pass Rate: 35/36 (97.2%)** (pre-fix: 18/28, 64.3%)

**Final Score = 91×0.4 + 92.0×0.6 = 36.4 + 55.2 = 91.6 → 92**
**Grade: ⭐ Production Ready — deployable, no veto fired.**

> **Note for reviewer:** Every input that was ⚠️/❌ pre-fix (1, 2, 4, 6) is now ✅, each verified by
> real code execution rather than inspection. The only remaining open gap (Input 5, MS-DIAL glue
> code) was never part of this fix batch and is carried forward as a P2, not a blocker.

---

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** "I have centroided mzML files plus pooled QCs from an untargeted study; run xcms
preprocessing, QC-correct, find differential metabolites, and map pathways." (testing the
Stage1->Stage2 hand-off specifically)

**Executed:** true — same real xcms output as pre-fix (`feature_table_input1.csv`, 574 real faahKO
features x 12 real samples) via `run/input1_orientation_regression.R`.

**Real output:**
```
Real xcms featureValues()-shaped input: 574 x 12
=== Current SKILL.md Stage 2 hand-off code, verbatim ===
No transpose applied. dim(fm) = 574 x 12 | dim(defs) = 574 | length(sample_class) = 12
stopifnot dimension check: PASSED
=== Feed fm into the documented pmp call ===
filter_peaks_by_fraction(fm) result: 573 of 574 features kept, dim 573 x 12
=== Regression check vs pre-fix bug: is fm still features-in-rows? ===
fm rows == feat rows (features): TRUE
fm cols == feat cols (samples): TRUE
PASS: orientation preserved, no inversion. The pre-fix `t(feat)` bug is gone.
```

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**
- [PASS] Workflow's Stage1->Stage2 code produces the pmp orientation its own comment claims
- [PASS] A dimension check now catches an orientation mismatch instead of relying on pmp's silent auto-correction
- [PASS] Real xcms output can be fed through the documented transform without crashing
- [PASS] No security/injection issues in the hand-off code

---

### Input 2 — Variant A (regression, the headline P1 fix)
**Prompt:** "Take my feature table through QC, statistics, and pathway mapping" (testing the full real
Stage2->Stage4 chain on realistic multi-batch biological data)

**Executed:** true — real MTBLS79 data (2488 features x 172 samples, cow/sheep serum, 8 batches, 38
pooled QCs), `run/input2_stage2to4_realchain_postfix.R` via `rs.sh`. Injection order used the same
column-order stand-in as the pre-fix script and the fixer's own verification (`Sample_Rep` in the flat
export has ties within batch/class and is not real injection order — using it instead breaks
`QCRSC`'s `smooth.spline` call with an unrelated error, confirmed while building this input).

**Real output:**
```
Real MTBLS79 peak matrix: 2488 x 172
Classes: C=66, QC=38, S=68

=== Stage 2 -- current SKILL.md code, verbatim ===
After filter_peaks_by_fraction: 2453 of 2488 features kept
After QCRSC: 2453 x 172
After filter_peaks_by_rsd: 2433 of 2453 features kept
After pqn_normalisation: 2433 x 172

=== Drop QCRSC-wiped (wholly-NA) samples -- the fix ===
90 of 172 samples came back all-NA (QCRSC: their batch had < minQC QCs)
 2  3  4  8
24 24 20 22
Remaining after drop: 82 samples
Max per-sample NA rate among survivors: 18.2%

=== Mechanism-aware imputation (log2/2^x QRILC round-trip) -- the fix ===
QRILC imputation OK. min value: 17.155 | any NA remaining: FALSE

=== Stage 4 -- current SKILL.md code, verbatim ===
Stage2->Stage4 hand-off shape: 60 x 2433 | groups: C vs S
Model type actually fit: OPLS-DA
getSummaryDF rows: 1 (not a silent empty model)
      R2X(cum) R2Y(cum) Q2(cum)  pR2Y   pQ2
Total    0.515    0.967   0.939 0.001 0.001

=== RESULT ===
Pre-fix: opls() ERROR "missing value where TRUE/FALSE needed" (55.95% NA reached opls()).
Post-fix: opls() completed, produced a 1-row summary with pR2Y = 0.001, pQ2 = 0.001. The crash is fixed.
```
This exactly matches the fix log's own claimed verification numbers (90/172 dropped, 82 survive,
<=18% per-sample NA, `pR2Y = pQ2 = 0.001`). One numeric detail differs from the fix log's own run: the
QRILC-imputed minimum value here is 17.155 vs the fix log's claimed 11.77 — both are non-negative and
NA-free (the property that matters), but `impute.QRILC` is not seeded in the Stage 2 code, so the exact
imputed values are not run-to-run reproducible even though the downstream model-fit statistics are
identical (see P2 recommendation).

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100

**Assertions:**
- [PASS] Documented Stage2->Stage4 code chain runs end-to-end on real multi-batch biological data
- [PASS] Stage 2 output's missingness is imputed before entering Stage 4 as the pipeline's own text states
- [PASS] Wholly-NA (QCRSC-wiped) samples are reported by batch, not silently fabricated
- [PASS] Feature/sample orientation is correct at the Stage2->Stage4 boundary
- [PASS] No unsafe operations in the executed code

---

### Input 3 — Stress (regression)
**Prompt:** shipped-means-present check (gate 8) — run the Skill's own first bundled example as-is.

**Executed:** true — `examples/metabolomics_workflow.R` (unchanged file), run via `rs.sh`.

**Real output:**
```
Features kept after RSD/D-ratio filter: 292 of 300
Significant features (FDR<0.05, |log2FC|>1): 20
True planted hits recovered: 20 of 20
Wrote results to <tempdir>/metabolomics_demo
Cleaned up temporary outputs
```
Identical to the pre-fix result — this file was not touched by the fix.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**
- [PASS] The Skill's bundled example file exists and runs without error (gate 8)
- [PASS] Output demonstrates the QC/RSD/D-ratio filter step
- [PASS] Output correctly recovers the planted ground-truth signal
- [PASS] Temporary outputs are cleaned up, no stray files left

---

### Input 4 — Edge (regression + upgrade to real execution)
**Prompt:** "My annotations aren't all confirmed — make sure only solid IDs feed into the pathway
enrichment." (testing the Stage3->Stage5 MSI-confidence gate)

**Executed:** true — `run/input4_msi_gate_real_exec.R`. Pre-fix this was inspection-only (no code
existed to run); post-fix code now exists and was run for real, on three cases.

**Real output:**
```
=== Case A: realistic mixed-confidence annotation table ===
 1 2a 2b  3  4  5
 2  3  3  3  4  5
identified_compounds (Level 1-2 only): 8 of 20 unique names
[1] "Pyruvate"  "L-Lactate" "Citrate"   "Succinate" "Fumarate"  "L-Alanine" "Glutamate" "cand_18"
Levels among EXCLUDED names: 3, 4, 5
Levels among INCLUDED names: 1, 2a, 2b
PASS: filter correctly separates Level 1-2 from Level 3-5.

=== Case B: adversarial edge -- every feature is Level 3-5 ===
identified_compounds length when all rows are Level 3-5: 0
stopifnot correctly fired: length(identified_bad) > 0 is not TRUE

=== Case C: type-safety check -- numeric vs character msi_level ===
Names passing filter: A, B (expect A, B only)
PASS: as.character() coercion handles both numeric (1L) and string ('2a') representations.
```

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100

**Assertions:**
- [PASS] SKILL.md shows code that gates identified_compounds by MSI level before Stage 5
- [PASS] The stated commitment ("only Level 1-2 enter identified-ORA") is checked in code, not just narrated
- [PASS] The all-tentative edge case (every feature Level 3-5) is handled safely, not forced into ORA
- [PASS] Component skill (metabolite-annotation) produces a usable per-feature confidence level to filter on

---

### Input 5 — Variant B (regression, unchanged gap)
**Prompt:** "My peak detection happened in MS-DIAL, not xcms — can I still use the rest of this
pipeline?"

**Executed:** false — inspection cross-check, same as pre-fix; msdial-preprocessing was not touched
this round.

**Finding:** Unchanged from pre-fix. The claim ("import the alignment-result table and enter the
pipeline at Stage 2") is format-compatible, but the orchestrator itself shows zero glue code for this
entry point.

**Scores:** Basic 33/40 | Specialized 45/60 | Total 78/100

**Assertions:**
- [PASS] MS-DIAL alternate entry claim (features-in-rows/samples-in-columns) matches xcms/pmp convention
- [FAIL] Orchestrator shows explicit glue code for this entry point
- [PASS] No contradictory instructions between the two front-end Skills

---

### Input 6 — Scope Boundary (regression + upgrade to real execution)
**Prompt:** "Some of my run is positive mode, some negative — how does the pipeline keep them
straight?" (testing governing commitment #1, the ionization mode-lock)

**Executed:** true — `run/input6_mode_lock_real_exec.R`. Pre-fix this was inspection-only; post-fix
code now exists and was run for real, on four cases.

**Real output:**
```
=== Case A: single-mode study (positive only) ===
No split needed -- single acquisition mode, as expected.
=== Case B: mixed-mode study (pos/neg runs merged before Stage 3) ===
Split triggered: 2 groups -> negative: 8, positive: 12 features
PASS: each split group is internally single-mode (no cross-mode contamination).
=== Case C: adversarial -- mode not set (NA) ===
stopifnot correctly fired: !anyNA(defs3$mode) is not TRUE
=== Case D: chemistry sanity check ===
PASS: the two adduct tables are disjoint.
```

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100

**Assertions:**
- [PASS] A per-feature ionization-mode column is carried through the documented pipeline
- [PASS] Mixed-mode data handling is demonstrated, not just asserted
- [PASS] A missing/unset mode is a hard stop, not a silent default
- [PASS] No incorrect mode-chemistry claims made

---

### Input 7 — Adversarial (regression)
**Prompt:** "Skip the MSI confidence stuff, just give me the significant pathways — I don't have time
for annotation levels."

**Executed:** true (Mode A, simulated as Claude-with-this-Skill-loaded). Governing principle #2 text
is unchanged post-fix.

**Simulated response:** unchanged from pre-fix — declines to skip confidence tagging, cites the
Skill's own governing principle #2, offers a fast path that still tags achievable confidence levels.

**Scores:** Basic 37/40 | Specialized 51/60 | Total 88/100

**Assertions:**
- [PASS] Agent declines to silently skip confidence-level tagging when asked to shortcut
- [PASS] Response cites the Skill's own stated governing principle rather than a generic disclaimer
- [PASS] Response still offers a fast path forward rather than refusing outright
- [PASS] Response avoids fabricating a compound-level confidence result it didn't compute

---

### Input 8 — Stress (NEW)
**Prompt:** shipped-means-present check (gate 8) — run the Skill's new second bundled example.

**Executed:** true — `examples/pipeline_handoff_check.R` (added by the fix, closing the pre-fix P2
finding), run via `rs.sh`.

**Real output:**
```
=== Stage 1 (stand-in): featureValues()-shaped output ===
150 features x 29 samples
=== Stage 1 -> Stage 2 hand-off (Input 1 regression guard) ===
No transpose applied; dimension check passed ( 150 x 29 ).
=== Stage 2: real pmp calls ===
After filter_peaks_by_fraction: 150 of 150 features kept
After QCRSC: 150 x 29
After filter_peaks_by_rsd: 150 of 150 features kept
After pqn_normalisation: 150 x 29 | NA cells: 1950 (44.8%)
=== Input 2 regression guard: drop QCRSC-wiped samples, then impute the sparse rest ===
13 of 29 samples came back all-NA (batch 2, minQC=5 > its 3 QCs)
After impute.QRILC (log2/2^x round-trip): 0 NA cells remain; min value: 4.894
=== Stage 4: real ropls, guarded fit ===
Stage2->Stage4 hand-off shape: 10 x 150 | groups: Control vs Treatment
Model type actually fit: OPLS-DA | getSummaryDF rows: 1
      R2X(cum) R2Y(cum) Q2(cum)  pR2Y   pQ2
Total    0.868    0.998   0.974 0.014 0.014
```
`pR2Y = pQ2 = 0.014` is an exact match to the fix log's own claimed verification numbers for this
example.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

**Assertions:**
- [PASS] The new bundled second example exists and runs without error
- [PASS] It exercises real pmp+ropls calls, not base-R stand-ins
- [PASS] It reproduces the same failure-then-fix shape as the real MTBLS79 case
- [PASS] Model-fit statistics reproduce the fixer's own verification run

---

### Input 9 — Variant A (NEW)
**Prompt:** "Run the pathway mapping stage on my MSI-filtered compound list and tell me if the
background choice actually matters." (cross-Skill consistency check requested by the audit brief)

**Executed:** true — `run/input9_crossskill_stage5_to_pathwaymapping.R`. Chains the workflow's own
Stage 5 MSI-gate code into `metabolomics/pathway-mapping`'s verbatim `local_kegg_ora()` function
(that Skill scored 92/Production Ready this round), against a real live KEGGREST pull and the
pathway-mapping audit's own 320-compound assay-coverage reference file.

**Real output:**
```
identified_compounds: Pyruvate, L-Lactate, Citrate, Succinate, Fumarate, L-Alanine, Glutamate
Resolved KEGG IDs: C00022, C00186, C00158, C00042, C00122, C00041, C00025
KEGGREST live call took 5.7 sec

Assay-coverage background (n=320):
          pathway total hits      p.value          fdr
hsa00250 hsa00250    14    6 1.445346e-08 7.226732e-07
hsa05230 hsa05230    32    7 5.274384e-08 1.318596e-06
...
All-of-KEGG background (n=6701):
          pathway total hits      p.value          fdr
hsa05230 hsa05230    37    7 8.579479e-17 4.289740e-15
hsa00250 hsa00250    28    6 2.095955e-14 5.239888e-13
...
Background-inflation check on hsa00250: assay-coverage p = 1.45e-08 | all-of-KEGG p = 2.1e-14
CONSISTENT with pathway-mapping's own finding: smaller, correct background -> less inflated significance.
```

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100

**Assertions:**
- [PASS] identified_compounds from Stage 5's MSI gate resolve to valid KEGG IDs consumable by pathway-mapping's Local-Only ORA
- [PASS] No glue-code/format mismatch between the two independently-fixed Skills
- [PASS] Background-inflation direction matches pathway-mapping's own audited finding
- [PASS] No user compound data sent to any remote server

---

## Optimization Recommendations

**[P2] MS-DIAL alternate entry point still has zero glue code** (Input 5)
Problem: unchanged from pre-fix — the orchestrator claims a Stage-2 entry point for MS-DIAL output
with no demonstrating code. Root cause: msdial-preprocessing was not part of this round's fix batch.
Fix: add a short snippet showing the Alignment ID/Area export feeding filter_peaks_by_fraction.

**[P2] impute.QRILC has no explicit seed** (Input 2)
Problem: the same real MTBLS79 input produced a different minimum imputed value across runs
(17.155 here vs 11.77 in the fixer's verification), though the decision and downstream model-fit
statistics (pR2Y=pQ2=0.001) were identical both times. Root cause: no set.seed() before the QRILC
call, unlike PerformPSEA elsewhere in the pipeline. Fix: add set.seed() immediately before
impute.QRILC in Stage 2.

**[P2] No bundled example runs a real Stage 1 xcms extraction into the rest of the pipeline** (Inputs 3, 8)
Problem: both examples start from a synthetic/cached feature table. Root cause: deliberately
deferred by the fixer to xcms-preprocessing's own scope (needs real mzML files). Fix: a future
third example chaining real xcms output through all 5 stages, reasonably out of scope this round.
