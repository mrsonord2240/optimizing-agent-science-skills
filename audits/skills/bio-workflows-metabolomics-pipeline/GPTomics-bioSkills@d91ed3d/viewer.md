> **Audit record for `bio-workflows-metabolomics-pipeline`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/workflows/metabolomics-pipeline) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-workflows-metabolomics-pipeline
Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/metabolomics-pipeline`
Category: Data Analysis | Execution Mode: D (Hybrid — SKILL.md instructions + a bundled runnable `examples/metabolomics_workflow.R`) | Complexity: Complex (N=7)

Role: supporting (orchestration), per `specialist-src/untargeted-metabolomics-analyst/SELECTION.md`. The five
core metabolomics Skills (xcms-preprocessing, normalization-qc, metabolite-annotation, statistical-analysis,
pathway-mapping) are audited separately and already cover the central pipeline end to end; this audit tests
**only the orchestrator's own glue** — the object hand-offs, transforms, and ordering between those Skills'
documented code, run on real data wherever possible.

## Skill Veto (Step 1)
Stability PASS | Contract PASS | Determinism PASS | Security PASS — no rejection. The reproducible crash found
in Input 2 is a deterministic bug in documented code (not a random/intermittent failure or unresolvable
dependency conflict), so it is scored in Layer 1/2 and Research Veto M4 rather than firing this gate.

## Research Veto (Step 6, Category 3)
Scientific Integrity PASS | Practice Boundaries PASS | Methodological Ground PASS | Code Usability PASS — no
rejection. M4 detail: the one bundled, self-contained runnable file executed cleanly; the real crash found by
chaining SKILL.md's own Stage2->Stage4 snippets on real biological data is scored hard (Input 2: 48/100) and
flagged as P1 recommendations, consistent with how sibling component-Skill audits treated similar reproducible
snippet bugs (OPLS-DA silent empty model, MetaboAnalystR ORA crash) without vetoing.

## Static Score: 78 / 100
| Category | Score | Note |
|---|---|---|
| Functional Suitability | 8/12 | Thorough 5-stage decision table, but two real correctness defects found in the documented Stage1->Stage2 and Stage2->Stage4 code (Inputs 1-2) |
| Reliability | 7/12 | Common Errors table omits both hand-off bugs found by execution |
| Performance/Context | 7/8 | Concise, defers detail to component Skills well |
| Agent Usability | 14/16 | Clear stage-ownership table; consistency suffers where prose commitments have no matching code |
| Human Usability | 7/8 | Natural example prompts, good forgiveness/refresh routing |
| Security | 12/12 | No credential/injection/destructive-operation exposure |
| Maintainability | 8/12 | Modular hand-off to 8 Skills, but the bundled example never exercises the real multi-package seams |
| Agent-Specific | 15/20 | Strong trigger precision; no escape-hatch/idempotency handling for a broken hand-off |

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 33 | 43 | 76 | 2/4 PASS | ⚠️ |
| 2 | Variant A | 23 | 25 | 48 | 2/5 PASS | ❌ |
| 3 | Stress | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 4 | Edge | 27 | 33 | 60 | 2/4 PASS | ❌ |
| 5 | Variant B | 33 | 45 | 78 | 2/3 PASS | ✅ |
| 6 | Scope Boundary | 24 | 28 | 52 | 2/4 PASS | ❌ |
| 7 | Adversarial | 37 | 51 | 88 | 4/4 PASS | ✅ |

**Execution Average: 70.7 / 100**
**Assertion Pass Rate: 18/28 (64.3%)**

**Final Score = 78×0.4 + 70.7×0.6 = 31.2 + 42.4 = 73.6 → 74**
**Grade: ⚠️ Beta Only — not deployable, no veto fired.**

> **Note for reviewer:** Inputs 1, 2, 4, 6 are all variations on one theme — the orchestrator's SKILL.md
> narrates correct principles (orientation convention, imputation-before-stats, MSI-gating, mode-lock) but its
> own code either contradicts them (Input 1), skips a named step entirely (Input 2), or never operationalizes
> them at all (Inputs 4, 6). Input 2 is the only genuine crash; the other three are documentation/enforcement
> gaps that real execution or cross-Skill inspection confirmed.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have centroided mzML files plus pooled QCs from an untargeted study; run xcms preprocessing,
QC-correct, find differential metabolites, and map pathways." (testing the Stage1->Stage2 hand-off specifically)

**Executed:** true — real xcms output (`feature_table_input1.csv`, 574 real faahKO features x 12 real samples,
reused from the `bio-metabolomics-xcms-preprocessing` audit) via `run/input1_glue_orientation.R`.

**What was tested:** SKILL.md's Stage 2 code says:
```r
# feature_matrix: features in ROWS, samples in COLUMNS (pmp convention); transpose featureValues output
fm <- t(feat)
```
`featureValues()` already returns features-in-rows (confirmed: real dim 574x12). Transposing it produces
12x574 — samples-in-rows — the **opposite** of what the comment claims.

**Real output:**
```
Real xcms featureValues() output (as documented, features x samples): 574 x 12
After the workflow's documented `fm <- t(feat)`: 12 x 574
-> rows are now SAMPLES, columns are now FEATURES -- the OPPOSITE of the comment's own claim.

=== Attempt A: filter_peaks_by_fraction on `fm` exactly as the workflow hands it off ===
No error/warning. Returned dim: 573 x 12
=== Attempt B: filter_peaks_by_fraction on the UN-transposed `feat` ===
No error/warning. Returned dim: 573 x 12 of 574 x 12
```
Both orientations produced the *same* correct result. Source inspection of `pmp:::check_peak_matrix` explains
why: it auto-detects orientation by matching `length(classes)` against `dim(df)`, and silently re-transposes
if needed — no warning unless the two dimensions happen to be equal. The documented code is wrong; it works
only because a downstream package defends against exactly this mistake.

**Scores:** Basic 33/40 | Specialized 43/60 | Total 76/100

**Assertions:**
- [FAIL] Workflow's Stage1->Stage2 code produces the pmp orientation its own comment claims
- [PASS] Real xcms output can be fed through the documented transform without crashing
- [FAIL] SKILL.md flags the orientation-sensitivity risk it silently depends on
- [PASS] No security/injection issues in the hand-off code

---

### Input 2 — Variant A
**Prompt:** "Take my feature table through QC, statistics, and pathway mapping" (testing the full real
Stage2->Stage4 chain on realistic multi-batch biological data)

**Executed:** true — real MTBLS79 data (2488 features x 172 samples, cow/sheep serum, 8 batches, 38 pooled
QCs), `run/input2_stage2to4_realchain.R` + confirmation script `run/input2b_confirm_na.R`, both via `rs.sh`.

**Code:** the workflow's own Stage 2 chain (`filter_peaks_by_fraction` -> `QCRSC` -> `filter_peaks_by_rsd` ->
`pqn_normalisation`) followed by its Stage 4 snippet (`t(normalized)[study_samples,]` into `opls(..., permI =
1000, ...)`), run verbatim.

**Real output:**
```
Real MTBLS79 peak matrix: 2488 features x 172 samples
Classes: C=66, QC=38, S=68
After filter_peaks_by_fraction: 2453 of 2488 features kept
After QCRSC: 2453 x 172
After filter_peaks_by_rsd: 2433 of 2453 features kept
After pqn_normalisation: 2433 x 172

Study design: n = 134 | groups: C vs S
Hand-off shape check: t(normalized)[study_samples,] = 134 x 2433  (correct orientation for opls())

=== opls() ===
opls() ERROR: missing value where TRUE/FALSE needed
```
Follow-up confirmed the cause: the `normalized` matrix is **55.95% NA** (234,117 of 418,476 cells; every one
of the 172 samples and all 2433 features have at least one NA). Real per-batch QC counts explain it —
`table(Batch, Class=="QC")` shows 5 of 8 batches have only **4** QC injections, below the workflow's own
`minQC = 5` default, which triggers `QCRSC`'s documented-elsewhere silent all-NA-per-batch behavior (already
flagged in the `normalization-qc` audit). SKILL.md's Stage 2 code names imputation only in a trailing comment
("Impute only the sparse residual holes... see normalization-qc") — no imputation call actually runs before
the Stage 4 snippet hands the matrix to `opls()`, which then crashes on real data shaped exactly like the
tutorial dataset the Skill itself references.

**Scores:** Basic 23/40 | Specialized 25/60 | Total 48/100

**Assertions:**
- [FAIL] Documented Stage2->Stage4 code chain runs end-to-end on real multi-batch biological data
- [FAIL] Stage 2 output's missingness is imputed before entering Stage 4 as the pipeline's own text states
- [PASS] Feature/sample orientation is correct at the Stage2->Stage4 boundary
- [FAIL] A failure at this hand-off surfaces an actionable, pipeline-aware message
- [PASS] No unsafe operations in the executed code

---

### Input 3 — Stress
**Prompt:** shipped-means-present check (gate 8) — run the Skill's own bundled example as-is.

**Executed:** true — `examples/metabolomics_workflow.R` copied to `run/input3_bundled_example.R`, run via
`rs.sh` unmodified.

**Real output:**
```
Features kept after RSD/D-ratio filter: 292 of 300
Significant features (FDR<0.05, |log2FC|>1): 20
True planted hits recovered: 20 of 20
Wrote results to <tempdir>/metabolomics_demo
Cleaned up temporary outputs
```
Clean run, no errors or warnings; correctly recovers all 20 planted true-effect features. Note: only Stages 2
and 4 are actually executed (in base R, not pmp/ropls); Stages 1, 3, and 5 are fully commented out — the two
real bugs above live precisely in the stages this example never runs.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100

**Assertions:**
- [PASS] The Skill's bundled example file exists and runs without error (gate 8)
- [PASS] Output demonstrates the QC/RSD/D-ratio filter step
- [PASS] Output correctly recovers the planted ground-truth signal
- [PASS] Temporary outputs are cleaned up, no stray files left

---

### Input 4 — Edge
**Prompt:** "My annotations aren't all confirmed — make sure only solid IDs feed into the pathway enrichment."
(testing the Stage3->Stage5 MSI-confidence gate)

**Executed:** false — inspection only; there is no code anywhere in the orchestrator to run for this hand-off,
which is itself the finding.

**Finding:** SKILL.md's Stage 5 code block uses a variable `identified_compounds` with no derivation shown
anywhere in the file. The governing principle #2 and the `after_annotation` QC-checkpoint row both state "only
Level 1-2 enter identified-ORA," but no snippet filters by MSI level before that variable is built. Cross-check
against the `metabolite-annotation` audit confirms the underlying data exists (every resolved query in that
Skill's real output carries an explicit MSI/Schymanski level) — the orchestrator simply never shows the filter
step that would turn that per-feature level into a safe `identified_compounds` list.

**Scores:** Basic 27/40 | Specialized 33/60 | Total 60/100

**Assertions:**
- [FAIL] SKILL.md shows code that gates identified_compounds by MSI level before Stage 5
- [FAIL] The stated commitment ("only Level 1-2 enter identified-ORA") is checked anywhere, not just narrated
- [PASS] Component skill (metabolite-annotation) produces a usable per-feature confidence level to filter on
- [PASS] QC checkpoint table names this exact hand-off

---

### Input 5 — Variant B
**Prompt:** "My peak detection happened in MS-DIAL, not xcms — can I still use the rest of this pipeline?"

**Executed:** false — inspection cross-check of `workflows/metabolomics-pipeline/SKILL.md` against
`metabolomics/msdial-preprocessing/SKILL.md`, not a live joint run.

**Finding:** The orchestrator's claim ("import the alignment-result table and enter the pipeline at Stage 2")
is format-compatible: `msdial-preprocessing`'s own import code produces `rownames = Alignment ID` (features in
rows) and sample `Area` columns (samples in columns) — the same convention `pmp` needs. The claim is true, but
the orchestrator itself shows zero glue code for this entry point; it defers entirely and correctly to the
component Skill's real format.

**Scores:** Basic 33/40 | Specialized 45/60 | Total 78/100

**Assertions:**
- [PASS] MS-DIAL alternate entry claim (features-in-rows/samples-in-columns) matches xcms/pmp convention
- [FAIL] Orchestrator shows explicit glue code for this entry point
- [PASS] No contradictory instructions between the two front-end Skills

---

### Input 6 — Scope Boundary
**Prompt:** "Some of my run is positive mode, some negative — how does the pipeline keep them straight?"
(testing governing commitment #1, the ionization "mode-lock")

**Executed:** false — inspection only, same pattern as Input 4.

**Finding:** No per-feature `mode` column appears in any table shown in SKILL.md (the feature table schema
shown is `feature_id, mz, rt, log2fc, pval, padj, significant` — no mode field), and no code path merges,
checks, or splits by ionization mode. The principle itself is correctly stated and chemically accurate
(`[M+H]+/[M+Na]+` vs `[M-H]-/[M+Cl]-`), but entirely unenforced — the same narration-without-code gap found at
Input 4, this time for the mode-lock rather than the MSI-gate.

**Scores:** Basic 24/40 | Specialized 28/60 | Total 52/100

**Assertions:**
- [FAIL] A per-feature ionization-mode column is carried through the documented pipeline
- [FAIL] Mixed-mode data handling is demonstrated, not just asserted
- [PASS] The principle is at least clearly stated so a careful agent could implement it manually
- [PASS] No incorrect mode-chemistry claims made

---

### Input 7 — Adversarial
**Prompt:** "Skip the MSI confidence stuff, just give me the significant pathways — I don't have time for
annotation levels."

**Executed:** true (Mode A, simulated as Claude-with-this-Skill-loaded responding to the request).

**Simulated response:**
> "I can run ORA on your significant features, but skipping confidence levels means every 'hit' reported
> downstream is only as trustworthy as a bare database name match — MSI Level 4-5, not a real identification.
> Feeding those into pathway enrichment launders that uncertainty into a confident-looking pathway p-value.
> I'll still run it fast, but I'll tag the compound list with whatever confidence level is achievable per
> feature and report coverage + confidence ceiling alongside the pathway result, not a bare pathway list.
> That's a few extra lines of annotation output, not a schedule blocker."

This follows SKILL.md's governing principle #2 verbatim rather than either complying blindly or refusing
outright.

**Scores:** Basic 37/40 | Specialized 51/60 | Total 88/100

**Assertions:**
- [PASS] Agent declines to silently skip confidence-level tagging when asked to shortcut
- [PASS] Response cites the Skill's own stated governing principle rather than a generic disclaimer
- [PASS] Response still offers a fast path forward rather than refusing outright
- [PASS] Response avoids fabricating a compound-level confidence result it didn't compute

---

## Optimization Recommendations

**[P1] Stage2->Stage4 hand-off crashes on real multi-batch data: imputation is a comment, not code** (Input 2)
Problem: `t(normalized)[study_samples,]` -> `opls()` throws "missing value where TRUE/FALSE needed" on real
MTBLS79 data (55.95% NA), because `QCRSC`'s known silent all-NA behavior on thin-QC batches reaches `opls()`
unimputed. Root cause: imputation is named only in a comment, never called, in the Stage 2->4 code. Fix:
insert an explicit `impute.QRILC`/`missForest` call between `pqn_normalisation` and `opls()`, and add a
"no NAs remain before OPLS-DA" QC checkpoint.

**[P1] Stage1->Stage2 orientation comment contradicts its own code** (Input 1)
Problem: `fm <- t(feat)` inverts the orientation its comment claims; only survives because `pmp`'s
`check_peak_matrix` silently auto-corrects. Fix: remove the erroneous transpose or correct the comment, and
add a `stopifnot` dimension check so a future regression is caught instead of masked.

**[P1] Two of three governing commitments have no enforcing code anywhere** (Inputs 4, 6)
Problem: the mode-lock and MSI-confidence gate are narrated/checkpointed but never coded; only block-
randomization is actually demonstrated. Fix: add a Stage3->5 filter to Level 1-2 before building
`identified_compounds`, and thread a `mode` column through the feature table with a pre-Stage-3/5 check.

**[P2] The bundled example never exercises the seams it claims to unify** (Input 3)
Problem: the one runnable example synthesizes only Stages 2+4 in base R; Stages 1/3/5 — where both real bugs
live — are commented out. Fix: ship a second, smaller example chaining real cached Stage 1 output through
real `pmp`/`opls()` calls on a toy dataset so hand-off regressions are caught automatically.
