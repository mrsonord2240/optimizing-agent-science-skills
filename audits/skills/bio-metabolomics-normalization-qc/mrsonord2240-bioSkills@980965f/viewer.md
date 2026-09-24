> **Audit record for `bio-metabolomics-normalization-qc`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@980965f](https://github.com/mrsonord2240/bioSkills/tree/980965fb613fd6c6dbbabe8d51c2b54eae3d8f34/metabolomics/normalization-qc) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-normalization-qc

## Canonical final summary

**Final:** 93/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@980965fb613fd6c6dbbabe8d51c2b54eae3d8f34:metabolomics/normalization-qc`
Final-pass note: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.

## Verdict

**93/100 — Production Ready — deployable.** Both veto gates pass. Twelve inputs were freshly executed: all nine inherited regressions and three new Phase 2 probes. One P1 remains: the QCRSC all-NA guard is global, not per batch, and misses a sparse-QC batch when another batch is valid. Under the governing rubric this is nonblocking: all floors pass, no veto fired, and there is no open P0, so promotion is allowed while the P1 is scheduled for follow-up.

## Veto gates

| Gate | Result | Evidence |
|---|---|---|
| T1 stability | PASS | Structural precheck passed; every standalone required runtime completed. |
| T2 contract | PASS | Frontmatter and shipped paths are present. |
| T3 determinism | PASS | Seeded synthetic runs and stable package paths were used. |
| T4 security | PASS | No raw user-code execution, credentials, or destructive commands. |
| M1 scientific integrity | PASS | All numerical claims below are fresh execution output. |
| M2 practice boundaries | PASS | No diagnosis or treatment recommendation. |
| M3 methodological ground | PASS | Held-out-QC, confound, QRILC, and overfit safeguards passed their tests. |
| M4 code usability | PASS | Both shipped R files parse and run; the mixed-batch logical gap is reported as P1. |

## Static evaluation — 92/100

| Category | Score | Note |
|---|---:|---|
| Functional suitability | 12/12 | Covers the claimed pipeline stages. |
| Reliability | 9/12 | Per-batch QCRSC guard gap remains. |
| Performance/context | 7/8 | Compact for its specialized workflow. |
| Agent usability | 15/16 | Clear decision trees and runnable patterns. |
| Human usability | 8/8 | Natural triggers and useful guardrails. |
| Security | 11/12 | No credential or destructive-operation exposure. |
| Maintainability | 11/12 | Localized script; localized guard repair needed. |
| Agent-specific | 19/20 | Strong triggers, handoffs, and escape hatches. |

## Fresh dynamic execution — 92.9/100

| # | Type | Fresh run result | Score | Assertions |
|---:|---|---|---:|---:|
| 1 | Canonical | MTBLS79 2488 -> 2370 -> 2343; held-out QC RSD 0.2298 -> 0.0780. | 96 | 5/5 |
| 2 | Variant A | PQN `pqn_coef` API present; reconstruction 2.91e-11; 999-shuffle guard run. | 94 | 4/4 |
| 3 | Variant B | QRILC log2/2^x P0 regression: 0 negative cells; minimum 4.76. | 97 | 5/5 |
| 4 | Edge | 3-QC batch all-NA path caught; coarse fallback used. | 94 | 4/4 |
| 5 | Stress | Perfect batch/group confound p=5.9e-13; ComBat declined. | 96 | 5/5 |
| 6 | Scope boundary | 85/15 imbalance FPR raw/naive/protected: 53.7/0.0/1.9%. | 93 | 4/4 |
| 7 | Adversarial | Span 0.50 -> 0.30 worsened held-out QC RSD 0.0823 -> 0.2090 and biological RSD 0.3152 -> 0.3425. | 93 | 4/4 |
| 8 | Edge | Old raw QRILC guard fired; non-positive data fails loudly. | 95 | 4/4 |
| 9 | Edge | SummarizedExperiment `colData(...$pqn_coef)` works; reconstruction 3.64e-12. | 95 | 4/4 |
| 10 | Variant B | New D-ratio function and CLI: 30 clean retained, 30 noisy rejected. | 96 | 4/4 |
| 11 | Stress | New shipped example: RSD 0.271 -> 0.235, 149 features, zero NAs, group p=0.613. | 95 | 5/5 |
| 12 | Edge | Global QCRSC guard passed even though sparse batch B2 was entirely NA. | 71 | 3/4 |

Assertion pass rate: **51/52 (98.1%)**.

## Detailed output checks

### Inputs 1–5 — core and fixed regressions

The real MTBLS79 path supplied non-circular held-out-QC evidence. The fixed QRILC call avoided impossible negative intensities on the exact historical P0 scenario. A single under-QC batch confirmed the documented guard and fallback work when the entire result is invalid. A perfect analytical-batch/group confound was identified before an invalid ComBat attempt.

### Inputs 6–9 — boundaries and object variants

The non-perfect imbalance probe did not force a predicted false-positive direction; the Skill's current degree-scaled caveat fits that result. The adversarial span test proved why held-out metrics are required. The QRILC safety guard handled both the old bug and non-positive inputs safely. Both pmp object types expose the documented PQN factor route.

### Inputs 10–11 — Phase 2 additions

`scripts/robust_dratio_filter.R` passed sourced and CLI execution against planted truth. `examples/normalize_data.R` ran exactly as shipped, now preserving a sparse biological effect instead of applying it to every feature; it produced the intended untripped, permutation-based group guardrail.

### Input 12 — P1 mixed-batch probe

With B1 containing eight QCs and B2 containing three, `QCRSC(minQC=5)` gave valid B1 values and all-NA B2 values. The shipped assertion `any(rowSums(!is.na(out_mat)) > 0)` returned `TRUE`, so it would permit the invalid B2 values downstream. The prose says to check per batch, but the shown code does not do that.

## Recommendation

**P1 — Make the QCRSC all-NA guard per batch.** Iterate over `unique(batch_id)` after correction and stop if any batch's corrected submatrix is entirely NA. Add this exact mixed valid/sparse-QC scenario as a regression test. This is a nonblocking improvement under the audit rubric, not a promotion hold.

## Evidence and artifact locations

- Fresh-evidence index: [phase2_evidence_summary.md](F:/OpenScience/audits/bio-metabolomics-normalization-qc/phase2_evidence_summary.md)
- Scripts and raw runner log: [run](F:/OpenScience/audits/bio-metabolomics-normalization-qc/run)
- Preserved prior audit: [pre-fix archive](F:/OpenScience/audits/_pre-fix-20260923/bio-metabolomics-normalization-qc)
