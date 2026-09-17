> **Audit record for `bio-metabolomics-isotope-tracing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/metabolomics/isotope-tracing) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-isotope-tracing

Generated: 2026-09-17
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:metabolomics/isotope-tracing`
Category: Data Analysis (3) | Execution Mode: A (Direct — SKILL.md code patterns, no `scripts/` CLI)
Complexity: Moderate → 5 inputs
Env: `untargeted-metabolomics-analyst` (isocor 2.2.4 Python; accucor 0.3.1.9000 R, real `extdata/` ground truth)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 53 | 90 | 5/5 PASS | ✅ |
| 2 | Variant A | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 3 | Edge | 34 | 44 | 78 | 3/4 PASS | ⚠️ |
| 4 | Variant B | 37 | 49 | 86 | 4/4 PASS | ✅ |
| 5 | Stress | 37 | 53 | 90 | 4/4 PASS | ✅ |

**Execution Average: 87.2 / 100**
**Assertion Pass Rate: 20/21 (95.2%)**

**Static Score: 94/100** (see `eval_report_..._result.json` → `static_score` for the 8-category breakdown)

**Final Score: 90/100 → ⭐ Production Ready** (Static 94×0.4 = 37.6 + Execution 87.2×0.6 = 52.3 = 89.9 → 90)

Skill Veto: PASS (T1–T4 all PASS). Research Veto (Category 3, applicable): PASS (M1–M4 all PASS; M3 flagged with a note, not a fail — see Input 3).

> **Note for reviewer:** Input 3 is the one row to read closely — it is where a real, if minor, methodological gap in the Skill's own documented steady-state snippet surfaced.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have M+0..M+5 areas for glutamine (C5H10N2O3) from a U-13C5-glutamine tracing experiment on a triple-quad (low-res). Apply natural-abundance correction with 98% tracer purity and give me the corrected MID and fractional enrichment."
**Data:** `data/glutamine_synthetic_raw_areas.csv` (SYNTHETIC).
**Executed:** true. Script: `run/input1_glutamine_correction.py`. Follows the exact `MetaboliteCorrectorFactory(...).correct()` pattern from SKILL.md, applied to a metabolite/tracer pair not in the Skill's own example (SKILL.md's inline example is glucose; this is glutamine), to test the pattern generalizes.

**Output:**
```
raw areas (M+0..M+5): [42000.0, 6100.0, 3200.0, 900.0, 1800.0, 15000.0]
corrected areas      : [44950.44, 3590.03, 2891.04, 732.09, 255.68, 16829.58]
corrected MID         : [0.6491, 0.0518, 0.0417, 0.0106, 0.0037, 0.243]
residuum               : [0.0, -0.0, 0.0, 0.0, -0.0, -0.0]
fractional enrichment  : 0.2794
MID sums to 1          : True
```

**Scores:** Basic: 37/40 | Specialized: 53/60 | Total: 90/100
**Assertions:**
- [PASS] Output reports corrected MID as a vector summing to 1 — verified `abs(sum(iso_fraction) - 1.0) < 1e-6` prints True.
- [PASS] Output does not fabricate DOI/PMID or invented statistical claims — all numbers derive from the documented `correct()` call, no citations invented.
- [PASS] Output stays within isotope-correction analysis, does not attempt flux fitting — script only computes MID/enrichment, matching the Skill's documented hand-off to INCA/13CFLUX2 for flux modeling.
- [PASS] Output reports both the corrected MID and fractional enrichment as requested — both printed.
- [PASS] No medical diagnostic/prescriptive claims made — pure lab-analysis context.
Assertion pass rate: 5/5

---

### Input 2 — Variant A
**Prompt:** "I have an El-MAVEN-style isotopologue CSV export (glucose-6-phosphate, 6-phospho-D-gluconate) from a 13C-glucose experiment on a low-resolution QqQ instrument, at 99% tracer purity. Run AccuCor natural-abundance correction and give me the corrected/normalized MID for glucose-6-phosphate."
**Data:** `data/accucor_real_sample_input.csv` — REAL data, copied unmodified from `accucor`'s own shipped `extdata/C_Sample_Input_Simple.csv` (not synthetic; see `data/data_README.md`).
**Executed:** true. Script: `run/input2_accucor_correction.R`, run via the env's `rs.sh` wrapper. Follows the SKILL.md pattern `accucor::natural_abundance_correction(path=..., resolution=..., purity=...)`.

**Ground truth check:** compared against the package's own shipped reference output (`extdata/C_Sample_Input_Simple_corrected.xlsx`, `Normalized` sheet).

**Output:**
```
Max abs difference vs ground truth: 2.775558e-17
Matches ground truth (tol 1e-6): TRUE
```
(full 7×11 Normalized MID table for glucose-6-phosphate matched cell-for-cell; see `run/` output for the full printout)

**Important process note:** the first attempt at this input, run without the `output_base` argument, caused `natural_abundance_correction()` to write its output file directly into the *shared* R package's `extdata/` directory (same filename as the shipped reference), because AccuCor's default output path is derived from the input path. The values it wrote were verified byte-identical to the original shipped reference (same computation on the same data), so no ground-truth data was corrupted, but this was re-run with an explicit `output_base` pointed at this audit's own `run/` directory to avoid ever writing into the shared, multi-agent environment again. Flagging this as a real trap for any other Mode-A/D use of this Skill's AccuCor pattern: **the SKILL.md code snippet does not mention `output_base` or that the function writes a file as a side effect at all** — see P1 recommendation.

**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100
**Assertions:**
- [PASS] Corrected values match AccuCor's own shipped reference output — verified, max diff 2.8e-17.
- [PASS] Output presents normalized MID per isotopologue (C_Label) per sample — full tibble printed.
- [PASS] Output does not fabricate values beyond what accucor computed — all values are `natural_abundance_correction()`'s own return object.
- [PASS] Comparison against ground truth explicitly performed and reported — max-diff check printed.
Assertion pass rate: 4/4

---

### Input 3 — Edge
**Prompt:** "I sampled fractional enrichment for citrate at 0, 5, 15, 30, 60, 90 min and got 0.00, 0.10, 0.20, 0.28, 0.34, 0.35. Is this at isotopic steady state? Also: I passed a 3-element vector to IsoCor's `correct()` for a 6-carbon metabolite by mistake — what happens?"
**Data:** synthetic time course, embedded in script (labelled synthetic in-script).
**Executed:** true. Script: `run/input3_edge_steadystate.py`. Part A follows the SKILL.md steady-state snippet exactly (`abs(fe[-1]-fe[-2]) < 0.02`); Part B reproduces the documented length-mismatch `ValueError`.

**Output:**
```
Part A -- steady-state check
  last-step change: 0.0100 (threshold <0.02)
  reached_plateau  : True

Part B -- length-mismatch error text (6-carbon formula, wrong 3-element input)
  ValueError: The length of the measured isotopic cluster (3) is different than the required
  number of measurements: 7 (i.e. N + 1, where N is the number of atoms that could be traced)
```

**Finding:** Part B is a clean match to the Common Errors table row ("`correct()` length mismatch in IsoCor... Pass M+0..M+n with n = count of tracer-element atoms"). Part A is where a real methodological gap surfaces: the sampled series (0.28 → 0.34 → 0.35) is still decelerating, not flat — the deltas are 0.08, 0.06, 0.01, which is a rapidly-slowing but not yet clearly-converged trend. SKILL.md's own snippet checks only the *last pair* against a fixed threshold, so it returns `reached_plateau: True` here and (if followed literally with no added caution) would license classical-MFA flux inference on a series whose convergence is genuinely borderline. This is not a "fallacy" (it doesn't invert a conclusion or substitute correlation for causation) — it's an incomplete robustness check, which is why it is scored as a P1 recommendation and a Research-Veto M3 PASS-with-note rather than a veto FAIL.

**Scores:** Basic: 34/40 | Specialized: 44/60 | Total: 78/100
**Assertions:**
- [PASS] Steady-state call correctly matches the SKILL.md-documented <2% threshold rule — 0.01 < 0.02 computed and applied correctly.
- [PASS] Output flags the documented `ValueError` for a length-mismatched isotopologue vector — exact match.
- [FAIL] Output does not overclaim flux-readiness from an unconverged/boundary time course — the literal SKILL.md threshold rule, applied as documented (last-pair-only), returns `True` on a series that is still visibly decelerating; nothing in SKILL.md prompts a check of the earlier deltas or the overall trend before calling plateau.
- [PASS] Output addresses both parts of the multi-part prompt (steady-state check + error explanation) — both present.
Assertion pass rate: 3/4

---

### Input 4 — Variant B
**Prompt:** "I want to know whether the pentose phosphate pathway (PPP) or glycolysis dominates glucose handling in my cancer cell line — which tracer should I use and what readout?"
**Executed:** false (Mode A / direct reasoning task — no code to run; this input tests the Decision Tree / tracer-selection guidance section of SKILL.md directly, as Claude-with-this-skill).
**Execution note:** no code generated or expected for this input; evaluated as a text response against SKILL.md's own Decision Tree row ("Distinguish two carbon entry points into one pool → Positional / partially-labeled tracer (e.g. 1,2-13C2-glucose) → The M+1 vs M+2 split of products separates PPP from glycolysis").

**Output (agent response, following SKILL.md's Decision Tree and Core Concepts sections):**
> Use [1,2-¹³C₂]-glucose (a positional, double-labeled tracer at C1/C2), not U-¹³C₆-glucose. Feed it to your cells, then measure the corrected MID (via LC-MS/GC-MS + IsoCor/AccuCor natural-abundance + tracer-purity correction) of downstream three-carbon glycolytic/PPP products (e.g., lactate). Readout: the **M+1 vs M+2 split**. The oxidative PPP step decarboxylates C1, so PPP-derived carbon keeps only the C2 label → M+1 in downstream three-carbon products; direct glycolysis retains both labeled carbons intact → M+2. A high M+1:M+2 ratio indicates PPP dominance; a high M+2:M+1 ratio indicates direct glycolytic flux. Apply the mandatory natural-abundance/tracer-purity correction *before* computing this ratio — uncorrected M+1 is partly natural-abundance noise for short-chain metabolites. This is a route/activity question (tracing), not a concentration question, so it does not need targeted-analysis abundance profiling.

**Scores:** Basic: 37/40 | Specialized: 49/60 | Total: 86/100
**Assertions:**
- [PASS] Recommended tracer and readout match the isotope-tracing literature (oxidative-PPP C1-decarboxylation logic) — textbook-correct 1,2-¹³C₂-glucose / M+1-vs-M+2 reasoning.
- [PASS] Output correctly stays in tracing scope rather than redirecting to abundance profiling — explicitly notes this is a route question, not a concentration question.
- [PASS] Answer names both the tracer AND the specific readout (M+1 vs M+2 split) — both present.
- [PASS] No prescriptive/diagnostic clinical claims about the cancer cell line — research-only framing.
Assertion pass rate: 4/4

---

### Input 5 — Stress
**Prompt:** "My alanine is TBDMS-derivatized for GC-MS (derivative adds C6H15Si to the C3H7NO2 backbone). I have M+0..M+3 raw areas from a U-13C3-alanine tracer at 98% purity. Correct for natural abundance including the derivative formula, AND separately: I tried to set a high-resolution correction by only giving `mz_of_resolution` without `resolution` — what error do I get?"
**Data:** `data/alanine_synthetic_raw_areas.csv` (SYNTHETIC).
**Executed:** true. Script: `run/input5_stress_gcms_derivative.py`. Part A follows the SKILL.md `derivative_formula` pattern (the fix for "GC-MS MID still wrong after correction" in the Common Errors table); Part B reproduces the documented "half-defined resolution" `ValueError`.

**Output:**
```
Part A -- corrected MID (with derivative_formula='C6H15Si'): [0.2635, 0.0, 0.7311, 0.0055]
Part A2 -- corrected MID (WITHOUT derivative formula, WRONG for GC-MS): [0.2405, 0.0063, 0.6682, 0.085]
MID differs from Part A by (max abs): 0.0795

Part B -- ValueError: MetaboliteCorrectorFactory was unable to select a correction strategy.
Please check your inputs.
```

**Finding:** Part A/A2 comparison confirms, with real numbers, exactly the failure mode SKILL.md warns about: omitting the derivative formula shifts the MID by up to 0.08 (8 percentage points) — a materially wrong result if not caught. Part B confirms a `ValueError` is indeed raised (matching "PASS" for existence of an error), but the message text is generic ("unable to select a correction strategy") rather than specifically naming the missing `resolution` parameter the way the Common Errors table implies — see P1 recommendation (same finding as Input 3 Part B).

**Scores:** Basic: 37/40 | Specialized: 53/60 | Total: 90/100
**Assertions:**
- [PASS] Derivative-formula correction demonstrably changes the MID vs. omitting it — 0.08 max-abs difference shown.
- [PASS] Documented half-defined-resolution error is reproduced as a `ValueError` — confirmed.
- [PASS] Both parts of the multi-part prompt are addressed with labeled output — Part A and Part B both present.
- [PASS] No fabricated claims about instrument-specific behavior beyond what the API returns — output limited to what `correct()` and the factory actually returned.
Assertion pass rate: 4/4

---

## Static Evaluation Notes (Step 2 — see JSON for full category breakdown)

- **Functional Suitability 11/12** — every documented code pattern (isocor low-res, accucor high-res/QqQ, MID/enrichment math, steady-state check, decision tree) is covered and, where testable, run-verified; docked 1 point for the steady-state check's incompleteness (Input 3).
- **Reliability 11/12** — Common Errors table causes are accurate; docked 1 point because the real error text for the half-defined-resolution case is more generic than the table implies (Inputs 3, 5).
- **Performance/Context 8/8** — SKILL.md ~187 lines, usage-guide separate, one reference example; clean progressive disclosure.
- **Agent Usability 14/16** — clear, consistent terminology and code patterns throughout; docked for the same steady-state under-specification affecting Feedback Design / Error Prevention.
- **Human Usability 7/8** — description uses strong natural trigger language; Category-3 scene override applied to Forgiveness (strict validation is correct design here), docked 1 point because isocor/accucor raise plain, non-Skill-specific `ValueError`s rather than structured codes.
- **Security 12/12** — no credentials, no destructive operations, no injection surface; pure numeric analysis.
- **Maintainability 11/12** — clean 3-file separation; only one worked example ships (no additional test fixtures).
- **Agent-Specific 20/20** — description precisely disambiguates from 4 adjacent Skills (targeted-analysis, xcms-preprocessing, pathway-mapping, flux-balance-analysis); verified idempotent; correctly hands flux-fitting off to INCA/13CFLUX2 instead of reimplementing it.

**Static Subtotal: 94/100**
