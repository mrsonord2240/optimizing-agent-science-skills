> **Audit record for `bio-proteomics-quantification`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@fb1efc1](https://github.com/mrsonord2240/bioSkills/tree/fb1efc10a979717f1fc66a48a6a8b12e95aa6401/proteomics/quantification) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-quantification

Generated: 2026-09-23 · final-pass Phase 2 fresh audit

Source: `mrsonord2240/bioSkills@fb1efc10a979717f1fc66a48a6a8b12e95aa6401:proteomics/quantification`

Result: **91/100 numeric score, ❌ Reject, not deployable.** The score is overridden by the required veto: core R paths write and validate output, then terminate with exit 11 in the required environment. `auditor_independent: false` is deliberately set because this is the final-pass exception; see `_final_pass/bio-proteomics-quantification/CHECKPOINT.md`.

Prior report preservation: the superseded 2026-09-15 JSON and viewer are copied to `F:\OpenScience\audits\_pre-fix-20260923\bio-proteomics-quantification\` before this report replaced them.

## Summary

| Input | Route | Result | Executed |
|---|---|---:|---|
| 1 | MaxQuant to MSstats TMP | 82, partial: output then exit 11 | yes |
| 2 | Whole-table iq MaxLFQ | 93 | yes |
| 3 | SILAC on/off ratios | 92 | yes |
| 4 | TMT10 reporters | 75, partial: output then exit 11 | yes |
| 5 | SL plus IRS two-plex bridge | 91 | yes |
| 6 | Patient-treatment scope boundary | 84 | no, correct refusal-only route |
| 7 | AP-MS control-IP scoring | 94 | yes |
| 8 | TMTpro 16plex CoA | 78, partial: output then exit 11 | yes |
| 9 | DIA-NN-style input to iq | 80, partial: output then exit 11 | yes |
| 10 | Fresh SILAC incorporation sweep | 96 | yes |
| 11 | Fresh AP-MS dead-control test | 95 | yes |
| 12 | Fresh SILAC fallback/all-Pro guard | 95 | yes |
| 13 | Shipped Python example | 95 | yes |

Execution average: **88.5/100**. Assertions: **48/52**. Calls made: **12/13**; Input 6 has no safe executable route.

## Evidence

Scripts, copied source files, and complete stdout/stderr are in [phase2_20260923](F:/OpenScience/audits/bio-proteomics-quantification/run/phase2_20260923). Persisted outputs independently parsed by `verify_outputs.py`:

```
MSstats=2305x11 proteins=296 | MaxLFQ=(299, 8) |
DIA-NN-MaxLFQ=(947, 8) | TMT-RDS=present
```

TMT output assertions succeeded before teardown: `matrix=24x10 negatives=0 nas=0`. The TMTpro CoA route also succeeded before teardown: `TMT16=16 TMT18=FALSE coa=16x16 corrected=100x16`.

The failure is reproducible outside the workflows: `probe_r_exit.R` exits 0 for base R and exit 11 after loading each of MSnbase, MSstats, or Arrow. The Phase-1 checkpoint identifies the known mzR/Rcpp mismatch and failed private source build. No source, shared package, worktree, or records-repository file was changed during this audit.

## Gates and final calculation

| Gate | Result | Reason |
|---|---|---|
| T1 Operational stability | FAIL | Core documented R workflows terminate nonzero in the specified environment. |
| T2 Contract | PASS | Required frontmatter and bundled files are present. |
| T3 Determinism | PASS | Seeded/fixture routes are repeatable. |
| T4 Security | PASS | No raw user code execution, credentials, network, or destructive operations. |
| M1 Scientific integrity | PASS | Persisted values and source claims were checked. |
| M2 Practice boundaries | PASS | Explicit clinical stop condition. |
| M3 Methodological baseline | PASS | Correct separation of quantification methods and their error models. |
| M4 Code usability | FAIL | Required R routes do not cleanly run in this deployment environment. |

`94 × 0.4 + 88.5 × 0.6 = 90.7`, rounded to 91. The two veto failures force **Reject** and `deployable: false`.

## Required remediation

P0: create a private, mutually compatible compiled R 4.4.3 package set (at minimum Rcpp, mzR, MSnbase, MSstats, and Arrow), then rerun Inputs 1, 4, 8, and 9 and require both asserted output and exit 0. The source itself was not edited because the checkpoint establishes this is an environment ABI issue, not a safe source-side correction.
