> **Audit record for `bio-causal-genomics-mediation-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@e46d106](https://github.com/mrsonord2240/bioSkills/tree/e46d106e931f1db5ed963fa29af3f8a22402915d/causal-genomics/mediation-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-mediation-analysis

Generated: 2026-09-23  
Source: `mrsonord2240/bioSkills@e46d106e931f1db5ed963fa29af3f8a22402915d:causal-genomics/mediation-analysis`  
Audit: final pass, Phase 2. `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.

The prior 2026-09-17 audit has been preserved at `F:/OpenScience/audits/_pre-fix-20260917c/bio-causal-genomics-mediation-analysis/`.

## Summary

| Input | Type | Basic | Specialized | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical eQTL mediation | 36 | 55 | 91 | 3/3 | ✅ |
| 2 | CMAverse 4-way | 36 | 54 | 90 | 3/3 | ✅ |
| 3 | Small-n edge | 35 | 53 | 88 | 3/3 | ✅ |
| 4 | MVMR mediation | 36 | 55 | 91 | 3/3 | ✅ |
| 5 | HIMA categorical batch | 35 | 56 | 91 | 3/3 | ✅ |
| 6 | Clinical scope boundary | 38 | 55 | 93 | 3/3 | ✅ |
| 7 | Deadline pressure | 38 | 54 | 92 | 3/3 | ✅ |
| 8 | medDML stress | 37 | 55 | 92 | 3/3 | ✅ |
| 9 | Two-step MR violation | 37 | 57 | 94 | 3/3 | ✅ |
| 10 | BCa case sensitivity | 38 | 55 | 93 | 3/3 | ✅ |
| 11 | Cell composition | 37 | 55 | 92 | 3/3 | ✅ |
| 12 | Fixed E-value code | 38 | 57 | 95 | 3/3 | ✅ |
| 13 | Shipped examples | 36 | 55 | 91 | 3/3 | ✅ |
| 14 | HIMA CLI | 35 | 54 | 89 | 3/3 | ✅ |

Execution average: **91.6 / 100**. Assertion pass rate: **42 / 42**.

Static score: **92 / 100**. Final score: **92 / 100 — ⭐ Production Ready**. Deployable: **true**. Skill Veto: **PASS**. Research Veto: **PASS**.

## What ran

All code lives in `run/`; all synthetic inputs are labelled there or in `data/`.

1. `input1_canonical_eqtl.R` fit fresh mediator and binary-outcome models, bootstrapped ACME, and printed the rho grid. It classified the low crossing value as highly sensitive.
2. `input2_cmaverse_4way.R` bootstrapped a fresh logistic 4-way decomposition. Its table contained `ERintref`, `ERintmed`, `pm`, `int`, and `pe`, matching the current reference.
3. `input3_edge_smalln.R` intentionally used n=60. It reported the n>=200 floor violation, wide uncertainty, and a sensitivity grid.
4. `input4_mvmr_mediation.R` produced conditional F values 13.21 and 8.27, warned for weak exposure-2 instruments, and calculated an indirect CI of [-0.3309, -0.1576].
5. `input5_hima_highdim.R` reproduced factor rejection, then completed dummy-coded HIMA and recovered `gene_1991` with no false positives. It verified the list return type.
6. `input06_scope_response.md` declined an individual dose recommendation and sent the decision to the prescribing clinician.
7. `input07_deadline_response.md` rejected proof-of-mechanism language and retained the sensitivity requirement.
8. `input8_meddml_doubleml.R` returned the documented 3x6 result matrix at n=300 and n=800. The n=150 unnamed, collinear case produced the documented `subscript out of bounds` recovery scenario.
9. `input9_twostep_mr_mediation.R` showed naive overlap bias (0.4401 vs planted 0.30) and reduced it after the Steiger-style exclusion (0.3555).
10. `input10_bca_case_sensitivity.R` got the expected wrong-case error and a successful lowercase `bca` bootstrap, then printed the current SKILL.md correction.
11. `input11_cell_composition_response.md` specified Houseman/reference-free RPC plus `COV.XM` and `COV.MY` for `hima_classic()`.
12. `input12_evalue_fixed.R` ran `evalues.RR(acme_rr, lo=acme_lower_rr)` exactly as fixed. Package values 1.92449980 and 1.43166248 matched independent arithmetic to below 1e-8.
13. Direct current source examples produced multi-gene eQTL output, sensitivity tables/PDF notifications, and MVMR totals/direct/indirect values. `runtime_exit_probe.sh` showed that `library(mediation)`, `library(TwoSampleMR)`, and `library(HIMA)` independently exit 139 in this shared runtime; the analysis outputs were checked before that external teardown fault.
14. `input14_hima_cli.sh` exercised the documented CLI on fresh n=300/p=200 data with one NA phenotype row and a three-level batch. It wrote the parseable empty `input14_hima_output.csv`, an allowed zero-discovery result.

`static_checks.sh` parsed every shipped R file and checked every `SKILL.md`-referenced artifact exists.

## Assertions

Every input passed three assertions: its requested method or boundary was addressed, its central safety/method rule was retained, and its result or response was checkable from saved output. The complete, per-assertion evidence is in [the JSON report](eval_report_bio-causal-genomics-mediation-analysis_result.json).

## Findings

No Skill-source P0 or P1 is open. One P2 is external to the Skill: the supplied R stack exits 139 after minimal `mediation`, `TwoSampleMR`, or `HIMA` loads. Because the analytical values/files are correct and the probe fails without any Skill code, this is recorded for the environment owner rather than scored as a Skill code defect.
