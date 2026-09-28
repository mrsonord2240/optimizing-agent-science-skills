> **Audit record for `bio-clinical-databases-acmg-classification`**
> - Audited working candidate `926ce0436d0d9fd1fb73a5f2b83728adfb622cf6f8ec41c8c00ad8d8300e8c07`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/clinical-databases/acmg-classification), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-clinical-databases-acmg-classification

Generated: 2026-09-28

Candidate: `sha256-manifest-v1:926ce0436d0d9fd1fb73a5f2b83728adfb622cf6f8ec41c8c00ad8d8300e8c07`

## Decision

**Rejected for candidate-ready transition.** Final diagnostic score is 76/100, but the Research Veto fails Methodological Ground. Static 76, execution 75.9, Layer 1 average 31.4/40, Layer 2 average 44.4/60, and assertions 26/35 all miss one or more production floors.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 34 | 50 | 84 | 4/5 | ✅ |
| 2 | Variant A | 30 | 43 | 73 | 4/5 | ⚠️ |
| 3 | Edge | 36 | 53 | 89 | 4/5 | ✅ |
| 4 | Variant B | 23 | 24 | 47 | 2/5 | ⚠️ |
| 5 | Stress | 27 | 35 | 62 | 3/5 | ⚠️ |
| 6 | Scope Boundary | 33 | 49 | 82 | 4/5 | ✅ |
| 7 | Adversarial | 37 | 57 | 94 | 5/5 | ✅ |

## Veto gates

- Structural veto: PASS.
- Scientific integrity: PASS.
- Practice boundaries: PASS.
- Methodological Ground: **FAIL** — retired evidence and evidence-family double counting can change classifications; exact documented predictor endpoints are also wrong.
- Code usability: PASS.

## Detailed outputs

### Input 1 — Guarded synthetic germline evidence ledger

**Prompt:** Run the shipped training example for a synthetic germline variant and inspect predictor selection, PS3 calibration, unresolved context, classification output, and the non-diagnostic qualified-review boundary.

**Observed output:** The demo exited zero, used one predictor, mapped OddsPath 8 to PS3 Moderate, printed unresolved context and the qualified-review boundary; it remains a compact sketch rather than a complete versioned evidence ledger.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100

**Assertions:**

- [PASS] The shipped standalone demonstration executes successfully. — Exit status was zero and output was retained in standalone-demo.log.
- [PASS] The demonstration uses one computational predictor and does not stack discordant BP4 evidence. — Output retained REVEL only and contained no BP4 criterion.
- [PASS] OddsPath 8 is represented as PS3 Moderate. — The retained criteria list contains PS3_Moderate.
- [PASS] The output states unresolved disease, transcript, VCEP, and assay-validity context plus a non-diagnostic qualified-review boundary. — All four unresolved fields and the medical-use guard were printed.
- [FAIL] The demonstration emits a complete versioned evidence ledger with sources, overrides, exclusions, and access dates. — The compact demo warns that context is unresolved but does not emit the complete ledger promised by the main workflow.

Raw observations: `evidence/execution.json`.

### Input 2 — PVS1 prerequisites and splice stop states

**Prompt:** Exercise LoF-mechanism and transcript-relevance gates, NMD and 10 percent branches, canonical-splice consequence and rescue review, plus contradictory NMD inputs.

**Observed output:** The prerequisite gates, NMD and 10 percent branches, and splice review stop states passed, but contradictory NMD inputs silently produced PVS1 Very Strong.

**Scores:** Basic 30/40 | Specialized 43/60 | Total 73/100

**Assertions:**

- [PASS] PVS1 is withheld when the LoF disease mechanism is not established. — The function returned no evidence.
- [PASS] PVS1 is withheld for a disease-irrelevant transcript. — The function returned no evidence.
- [PASS] Canonical splice calls stop for missing consequence or rescue-transcript review. — Both incomplete cases returned PVS1_REVIEW_REQUIRED.
- [PASS] NMD and exact/above 10 percent branches produce the documented strengths. — Very Strong, Moderate, and Strong observations matched the documented branches.
- [FAIL] Contradictory splice NMD signals are rejected before strength assignment. — is_nmd_predicted=False with splice_consequence=nmd returned PVS1_VeryStrong.

Raw observations: `evidence/execution.json`.

### Input 3 — Brnich OddsPath exact boundaries and mirrors

**Prompt:** Evaluate exact and adjacent pathogenic and benign Brnich Table 3 OddsPath boundaries, nonpositive and non-finite inputs, and agreement between code and reference prose.

**Observed output:** All 14 exact/adjacent OddsPath cases and invalid-domain guards passed; one failure-mode sentence still calls greater than 4.3 Strong, contradicting the corrected table and code.

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100

**Assertions:**

- [PASS] Pathogenic OddsPath bands implement Supporting, Moderate, Strong, and Very Strong at the documented boundaries. — All pathogenic exact and adjacent cases matched Brnich Table 3.
- [PASS] Benign mirror bands implement Supporting, Moderate, and Strong at the documented boundaries. — All benign exact and adjacent cases matched.
- [PASS] Nonpositive, non-finite, boolean, and string OddsPath inputs are rejected. — All six invalid probes raised actionable type or value errors.
- [PASS] The reference threshold table agrees with the executable mapping. — The table uses greater than 2.1, 4.3, 18.7, and 350 and the reciprocal benign mirrors.
- [FAIL] All Brnich explanatory prose is internally consistent with the corrected table. — Failure mode 6 still states that greater than 4.3 is required for Strong before its next sentence correctly calls that band Moderate.

Raw observations: `evidence/execution.json`.

### Input 4 — Tavtigian scoring and evidence-family integrity

**Prompt:** Exercise all classification endpoints, unknown and duplicate criteria, PVS1 subsumption, multiple strengths from one criterion family, opposing predictor codes, and criteria retired by current ClinGen guidance.

**Observed output:** Numeric endpoints, exact duplicate rejection, and basic subsumption passed; retired PP5/BP6, same-family multiple strengths, aliases, and opposed computational evidence remain accepted and can change a category.

**Scores:** Basic 23/40 | Specialized 24/60 | Total 47/100

**Assertions:**

- [PASS] The 10, 9, 6, 5, -1, -6, and -7 Tavtigian classification endpoints are correct. — All seven endpoint fixtures matched.
- [PASS] Unknown criteria, exact duplicates, and a string in place of a criterion sequence are rejected. — All three basic validation probes raised.
- [FAIL] Only one strength or alias from each ACMG evidence family can be counted. — PVS1 Very Strong plus PVS1 Strong scored 12; PM2 plus PM2 Supporting was also double-counted.
- [FAIL] ClinGen-retired PP5 and BP6 are rejected by the current-rule scorer. — Both remain in STRENGTH_POINTS; PP5 changed a five-point VUS fixture to six-point Likely Pathogenic.
- [FAIL] Opposing computational evidence is surfaced as a conflict instead of arithmetically cancelled. — PP3 Strong plus BP4 Strong was accepted and returned a zero-point VUS without a conflict field.

Raw observations: `evidence/execution.json`.

### Input 5 — Bergquist and Pejaver calibrated predictor endpoints

**Prompt:** Re-run the full AlphaMissense interval table including the -3/+3 point bands and fresh exact REVEL, BayesDel, and SpliceAI endpoint cases with invalid-domain controls.

**Observed output:** All 17 AlphaMissense cases and all SpliceAI cases passed, including explicit +/-3 point labels; four REVEL and two BayesDel exact benign endpoints were assigned to the next weaker band or to no evidence.

**Scores:** Basic 27/40 | Specialized 35/60 | Total 62/100

**Assertions:**

- [PASS] All Bergquist AlphaMissense intervals, including the indeterminate interval, match the cited table. — All 17 exact and fresh values matched.
- [PASS] The Bergquist -3 and +3 point intervals remain explicit point codes. — BP4_3pt and PP3_3pt were returned and carry -3/+3 points.
- [PASS] Out-of-domain AlphaMissense inputs and exact SpliceAI endpoints are handled correctly. — All invalid AlphaMissense probes rejected; SpliceAI 0.10, 0.15, and 0.20 matched.
- [FAIL] REVEL exact benign-side endpoints use the inclusive boundaries documented by the candidate. — 0.003, 0.016, 0.183, and 0.290 were placed in the next interval or made indeterminate.
- [FAIL] BayesDel exact benign-side endpoints use the inclusive boundaries documented by the candidate. — -0.36 became Supporting and -0.18 became indeterminate rather than Moderate and Supporting.

Raw observations: `evidence/execution.json`.

### Input 6 — Population and somatic evidence validation

**Prompt:** Exercise Whiffin, BS1/BA1, all six distinct AMP tiers, germline/somatic vocabulary separation, strict numeric/enumerated validation, provenance, and access-date validation.

**Observed output:** Population helpers, numeric guards, all six somatic tiers, and the qualified-review boundary passed; the YYYY-MM-DD regex accepted the impossible date 2026-99-99.

**Scores:** Basic 33/40 | Specialized 49/60 | Total 82/100

**Assertions:**

- [PASS] Whiffin, PM2 Supporting, BS1, and BA1 bounded cases produce the documented outcomes. — All four population cases matched and invalid numeric domains rejected.
- [PASS] Germline and somatic classification vocabularies remain separate. — Germline returned P/LP/VUS/LB/B vocabulary while somatic returned Tier labels.
- [PASS] Tier I-A, I-B, II-C, II-D, III, and IV are independently reachable. — All six tier cases matched and III/IV had distinct rationales.
- [PASS] Somatic enum conflicts, empty provenance, and unsupported oncogenic evidence are rejected. — All four invalid somatic probes raised actionable errors.
- [FAIL] The access date is a real calendar date, not only a digit pattern. — 2026-99-99 was accepted and preserved in a Tier III result.

Raw observations: `evidence/execution.json`.

### Input 7 — Current public GeneBe and ClinGen CSpec interfaces

**Prompt:** Run the shipped bounded live smoke and direct candidate helpers against current public GeneBe coordinate and CSpec versioned-gene routes, including invalid preflight inputs and the no-PHI boundary.

**Observed output:** The shipped live smoke and independent direct calls passed: GeneBe returned one public documentation-example record and CSpec returned six GATM version records; preflight guards ran before requests.

**Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100

**Assertions:**

- [PASS] The current GeneBe coordinate helper succeeds and returns a parsed variant list. — One record was returned for the public documentation coordinate.
- [PASS] The current ClinGen CSpec versioned-gene helper succeeds and returns version identifiers. — Six GATM version records were returned.
- [PASS] Invalid chromosome, position, symbol, and timeout inputs fail before a network request. — All four preflight cases rejected.
- [PASS] The former CSpec UI route is marked stale and the current REST workflow is documented. — Both statements are present in the reference.
- [PASS] The public-interface workflow explicitly prohibits PHI and uses only public examples. — The skill and live-smoke docstring prohibit patient/private data; retained inputs are public documentation examples.

Raw observations: `evidence/execution.json`.

## Open findings

- P0 ACMG-006: current evidence-family and strict-validation defects remain open.
- P1 ACMG-002: contradictory PVS1 NMD fields remain open.
- P2 ACMG-001: one residual Brnich prose contradiction remains open.

See `finding-ledger.md`, `scientific-source-notes.md`, and `execution-classifications.json` for the compact evidence map and documented-only surfaces.
