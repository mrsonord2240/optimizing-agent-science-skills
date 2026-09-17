> **Audit record for `bio-metabolomics-targeted-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/metabolomics/targeted-analysis) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-targeted-analysis
Generated: 2026-09-17
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:metabolomics/targeted-analysis`
Category: Data Analysis | Execution Mode: A (Direct) | Complexity: Moderate (N=5)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A | 35 | 49 | 84 | 4/4 PASS | ✅ |
| 3 | Edge | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 4 | Variant B | 37 | 57 | 94 | 4/4 PASS | ✅ |
| 5 | Stress | 32 | 52 | 84 | 4/4 PASS | ✅ |

**Execution Average: 89.2 / 100**
**Assertion Pass Rate: 20/20 (100%)**
**Static Score: 90/100**
**Final Score: 90/100 — ⭐ Production Ready — deployable, no veto**

## Skill Veto (Step 1)
Stability PASS · Contract PASS · Determinism PASS · Security PASS

## Research Veto (Step 6, Category 3 — Data Analysis)
Scientific Integrity PASS · Practice Boundaries PASS · Methodological Ground PASS
(with a P1 finding, see below) · Code Usability PASS

## Environment
R via `F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\rs.sh` (R 4.4.3, base R +
ggplot2 3.5+, no additional packages needed — this Skill's examples use only base R and ggplot2,
both already smoke-tested in `TOOLS.md`). All 5 inputs' scripts are in `run\`; all synthetic
input data (explicitly labelled synthetic, with planted known concentrations / planted
interferences / planted QC failures) is in `data\`.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have LC-MS/MS calibration standards and unknown plasma samples for an SIL-IS-
normalized assay. Build a 1/x^2-weighted calibration curve, accept it by back-calculated %RE (not
R-squared), and report concentrations for my unknown samples, flagging anything below the LLOQ."

**Script:** `run/input1_canonical.R` · **Data:** `data/input1_calibration_standards.csv`,
`data/input1_unknown_samples.csv` (6 unknowns with planted true concentrations 3–700 ng/mL)

**Output (executed, exit 0):**
```
=== Calibration back-calculation (weighted 1/x^2) ===
  conc_ngml re_pct pass
1         2  -0.47    1
...
9      1000  -0.60    1
LLOQ set to: 2 ng/mL

=== Unknown sample quantification vs planted true concentration ===
  sample true_conc_ngml conc_est pct_error_vs_truth reportable
1     U1             15    14.84              -1.09       TRUE
2     U2             40    39.72              -0.71       TRUE
3     U3             80    79.61              -0.48       TRUE
4     U4            300   300.43               0.14       TRUE
5     U5            700   706.43               0.92       TRUE
6     U6              3     2.99              -0.22       TRUE

All non-below-LLOQ samples within +-15% of planted truth: TRUE
```
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 4/4 PASS — see JSON for full text/justification per assertion.
**Notes:** Planted-truth recovery within 1.1% max error across 3 orders of magnitude confirms the
weighted-calibration + IS-normalization code pattern is correct and directly usable.

---

### Input 2 — Variant A (advisory, no code)
**Prompt:** "My panel has 40 chemically diverse metabolites and one global internal standard —
where is my accuracy at risk?"

**Response:** `run/input2_variantA_response.md` (full text)

Summary: correctly applies SKILL.md's "One IS shared across chemically diverse analytes" failure
mode — precision (CV) stays good because the IS still corrects injection/drift variance, but
accuracy decouples for analytes chemically/retention-time-distant from the single global IS.
Recommends RT/chemistry clustering, flagging distant analytes as lower-confidence, running the
IS-normalized matrix-factor check specifically on them, and escalating to per-analyte SIL-IS if
the study needs absolute (not just relative) accuracy. Explicitly notes the answer assumes
exploratory scope per the skill's own Decision Tree and flags escalation if the study is
regulated.

**Scores:** Basic 35/40 | Specialized 49/60 | Total 84/100
**Assertions:** 4/4 PASS

---

### Input 3 — Edge
**Prompt:** "My lowest calibrator (2 ng/mL) is at the noise floor and I only have one transition
(no qualifier) for this analyte. Estimate the LOD/LLOQ from my blank data, and tell me whether a
single-transition method is defensible for a regulatory submission."

**Script:** `run/input3_edge_lod_lloq.R` · **Data:** `data/input3_edge_blanks.csv` (5 blank
replicates)

**Output (executed, exit 0):**
```
=== LOD estimate from blank scatter (S/N~3 convention) ===
Mean blank ratio: 0.001068  SD: 8.758e-05
LOD: 1.329 ng/mL
Stated lowest calibrator: 2 ng/mL -- LOD below lowest calibrator: TRUE

=== Single-transition defensibility ===
SKILL.md states verbatim: "A single-transition method has no defense against isobaric
interference and is a documented compromise, not a default." ...flagged as a named limitation...
```
**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100
**Assertions:** 4/4 PASS
**Notes:** LOD (1.33 ng/mL) sits below the stated LLOQ (2 ng/mL), correctly showing the LLOQ here
is accuracy-bound, not noise-bound — matches the skill's own distinction between LOD (S/N~3
convention) and LLOQ (accuracy/precision criteria).

---

### Input 4 — Variant B
**Prompt:** "Compute the qualifier/quantifier ion ratio for my QC samples and flag anything
outside ±30% of the calibrator ratio. Estimate the IS-normalized matrix factor across 6 matrix
lots."

**Script:** `run/input4_variantB_ion_ratio_matrix_factor.R` · **Data:**
`data/input4_ion_ratio_matrix_factor.csv` (6 clean QC-mid lots + 1 planted isobaric-interference
sample)

**Output (executed, exit 0):**
```
=== QC-mid ion ratios across 6 lots ===
  lot ion_ratio id_confirmed
1  L1 0.3911290         TRUE
...
6  L6 0.3928571         TRUE

=== Planted-interference sample ===
         lot ion_ratio id_confirmed
7 INTERFERED 0.1666667        FALSE

=== IS-normalized matrix factor across 6 lots ===
Mean IS-normalized MF: 0.982
MF CV%: 4.44 -- ICH M10/Matuszewski threshold: <=15% across >=6 lots
MF CV PASS: TRUE
```
**Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100
**Assertions:** 4/4 PASS
**Notes:** The planted isobaric interference (ion ratio 0.167 vs. calibrator 0.39) was correctly
distinguished from all 6 clean lots (0.390–0.393) — the ion-ratio confirmation code works exactly
as documented.

---

### Input 5 — Stress
**Prompt:** "Here is 2-day, 3-replicate QC data at LLOQ/LOW/MID/HIGH for a clinical PK assay, plus
a blank injected after the ULOQ calibrator. Run the full ICH M10 acceptance check and tell me
whether this assay is fit for a regulated PK decision."

**Script:** `run/input5_stress_ich_m10.R` · **Data:** `data/input5_ich_m10_validation.csv`,
`data/input5_carryover_blanks.csv` (planted: an LLOQ-level replicate-3 outlier both days, and a
high blank-after-ULOQ carryover signal)

**Output (executed, exit 0):**
```
=== Intra-day accuracy & precision ===
 qc_level day   mean_re     cv_pct acc_pass prec_pass
     LLOQ   1 3.3333333 21.6844027     TRUE     FALSE
     LLOQ   2 4.6666667 20.6097958     TRUE     FALSE
     ... (LOW/MID/HIGH all TRUE/TRUE)

=== Inter-day (pooled) accuracy & precision ===
     LLOQ 4.0000000 18.9279035     TRUE      TRUE   <- pooled CV masks the intra-day failure
     ... (LOW/MID/HIGH all TRUE/TRUE)

=== Carryover ===
Carryover as % of LLOQ: 427.2 % -- ICH M10 threshold: <=20%
Carryover PASS: FALSE

=== OVERALL ASSAY VERDICT ===
Assay fit for regulated PK decision (ICH M10, this data subset): FALSE
```
**Scores:** Basic 32/40 | Specialized 52/60 | Total 84/100
**Assertions:** 4/4 PASS

**Finding (P1, see recommendations):** SKILL.md's Quantitative Thresholds table requires both
intra- and inter-day precision acceptance but never states how "inter-day" should be computed. A
naive pooled-SD inter-day CV (18.9%, PASS) would, alone, have missed the real intra-day LLOQ
precision failure (20.6–21.7%, FAIL both days) — the correct approach is a nested/ANOVA
variance-components model, which SKILL.md does not mention. Because SKILL.md does explicitly
require checking *both* tiers, the generated code checked intra-day separately and reached the
correct overall "not fit for use" verdict — so no output was actually wrong — but an agent that
implemented only the stated "inter-day acceptance" threshold literally, without independently
deciding to also check intra-day, could reach a false PASS. Recorded as a P1, not a veto (see
`scientific_veto.md` M3: no output in this audit actually inverted a conclusion).

---

## Reviewer note
Check the Input 5 finding above first — it is the one place this Skill's guidance (a stated
threshold with no accompanying formula) created real risk, even though the executed output
itself reached the correct conclusion. All other findings are P2 polish items.
