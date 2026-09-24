> **Audit record for `bio-metabolomics-isotope-tracing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3b43742](https://github.com/mrsonord2240/bioSkills/tree/3b437423563329fb137fa6fae8adb9563196fa13/metabolomics/isotope-tracing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-isotope-tracing

## Canonical final summary

**Final:** 95/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23

Source: mrsonord2240/bioSkills@3b437423563329fb137fa6fae8adb9563196fa13:metabolomics/isotope-tracing

Final-pass metadata: auditor_independent: false — final pass: fixed and audited under one brief, see CHECKPOINT.md.

Prior report preserved at F:\OpenScience\audits\_pre-fix-20260923\bio-metabolomics-isotope-tracing; copied report SHA-256 matched C7FE3DD072CD08080BD1B01BB63D607C358CFA0D127A9878495C74A10E163A93.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---:|---:|---:|---|---|---|
| 1 | Canonical | 37 | 55 | 92 | 4/4 PASS | true | PASS |
| 2 | Variant A | 38 | 57 | 95 | 4/4 PASS | true | PASS |
| 3 | Edge | 38 | 56 | 94 | 4/4 PASS | true | PASS |
| 4 | Variant B | 37 | 54 | 91 | 4/4 PASS | false | PASS |
| 5 | Stress | 38 | 57 | 95 | 4/4 PASS | true | PASS |
| 6 | Scope Boundary | 36 | 54 | 90 | 4/4 PASS | false | PASS |
| 7 | Adversarial | 38 | 57 | 95 | 4/4 PASS | true | PASS |
| 8 | Adversarial | 37 | 56 | 93 | 4/4 PASS | true | PASS |
| 9 | Scope Boundary | 37 | 56 | 93 | 4/4 PASS | false | PASS |

Execution average: 93.1/100. Assertion pass rate: 36/36. Final: 95/100, Production Ready, deployable true.

## Veto Gates

- Skill veto: PASS — stable, conformant frontmatter, deterministic numeric code, no raw-user-code execution.
- Research veto: PASS — no fabricated evidence, no clinical conclusion, valid correction/steady-state methodology, and saved executable evidence.

## Detailed Outputs

### Input 1 — Canonical 13C glutamine correction (prior regression)

Prompt: Correct synthetic M+0..M+5 C5H10N2O3 low-resolution U-13C5 areas at 98% purity and report MID/enrichment.

Execution: true — run/finalpass2/input1_glutamine_correction.py.

Output: corrected MID [0.649114, 0.051842, 0.041749, 0.010572, 0.003692, 0.24303]; fractional enrichment 0.279395. Runtime assertions confirmed normalized MID, six states, and bounded enrichment.

### Input 2 — Variant A AccuCor real-reference correction (prior regression)

Prompt: Correct the real AccuCor example-derived isotopologue export, compare glucose-6-phosphate against its shipped reference, and preserve package data.

Execution: true — run/finalpass2/input2_accucor_correction.R through rs.sh; supporting high-resolution smoke: input2_highres_documented_smoke.R.

Output: maximum absolute difference 2.775558e-17; isolated output workbook exists; extdata hash and file count are unchanged. The resolution=100000 documented call completed with 99 normalized rows.

### Input 3 — Edge steady-state and wrong-length cluster (prior regression)

Prompt: Assess citrate enrichment 0.00, 0.10, 0.20, 0.28, 0.34, 0.35 and test an invalid three-value C6 IsoCor cluster.

Execution: true — run/finalpass2/input3_steady_state_and_length_error.py.

Output: deltas [0.1, 0.1, 0.08, 0.06, 0.01] produce still labeling; live error names measured length 3 and required length 7.

### Input 4 — Variant B tracer choice (prior regression)

Prompt: Choose a tracer/readout to distinguish PPP from glycolysis.

Execution: false — Mode A reasoning only, recorded in run/finalpass2/input4_tracer_choice.md; no executable tool applies.

Output: 1,2-13C2-glucose and downstream M+1 versus M+2 split, with correction required before MID interpretation.

### Input 5 — Stress GC-MS derivative and factory error (prior regression)

Prompt: Correct TBDMS-derivatized alanine, compare omission of the derivative formula, and reproduce the incomplete high-resolution error.

Execution: true — run/finalpass2/input5_gcms_derivative_and_error.py.

Output: derivative omission changes the MID by 0.079513; derivative-aware MID is normalized; live factory error exactly matches SKILL.md.

### Input 6 — Scope boundary pool versus flux (prior regression)

Prompt: Explain an increased intermediate pool with decreased downstream flux, and give cold-quench guidance.

Execution: false — Mode A reasoning only, recorded in run/finalpass2/input6_redundancy_content_check.md; no executable tool applies.

Output: pool amount and labeling are separated; quench is fast, standardized, and -40 to -80 C.

### Input 7 — Adversarial plateau cases (prior regression)

Prompt: Check near-flat, truly plateaued, and only-two-timepoint series.

Execution: true — run/finalpass2/input7_plateau_edge_cases.py.

Output: near-flat -> still labeling; true plateau -> plateau; two points -> insufficient timepoints to assess steady state.

### Input 8 — Fresh 15N correction

Prompt: Correct synthetic M+0..M+2 15N-glutamine data and report MID/enrichment.

Execution: true — run/finalpass2/input8_15n_correction.py.

Output: corrected MID [0.811824, 0.137847, 0.050329]; enrichment 0.119252; assertions confirmed three states, normalization, and bounded enrichment.

### Input 9 — Fresh no-tracer scope boundary

Prompt: Can one untreated and one treated citrate pool concentration establish increased flux or classical 13C-MFA?

Execution: false — Mode A reasoning only, recorded in run/finalpass2/input9_no_timecourse_handoff.md; no code applies.

Output: the claim is refused; pools route to targeted-analysis; empirical flux needs corrected tracer data plus steady-state/INST-MFA discipline.

## Assertions

Each input has four scored PASS assertions in the JSON report: completion/correctness, stated output or guardrail, scope/scientific boundary, and documented behavior. All 36 passed.

## Audit artifacts

- Scripts, copied shipped example, and checked outputs: F:\OpenScience\audits\bio-metabolomics-isotope-tracing\run\finalpass2
- Archived prior audit: F:\OpenScience\audits\_pre-fix-20260923\bio-metabolomics-isotope-tracing
- Recommendations: none. No P0 or P1 findings remain.
