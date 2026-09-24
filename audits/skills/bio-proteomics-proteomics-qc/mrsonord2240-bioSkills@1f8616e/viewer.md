> **Audit record for `bio-proteomics-proteomics-qc`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1f8616e](https://github.com/mrsonord2240/bioSkills/tree/1f8616e8d39c2f14c16a01a4330bd0d94762b762/proteomics/proteomics-qc) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-proteomics-qc

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@1f8616e8d39c2f14c16a01a4330bd0d94762b762:proteomics/proteomics-qc`
Final-pass metadata: `auditor_independent: false` — `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Decision

**93/100 — ⭐ Production Ready — deployable: true.** Structural and research vetoes both passed. The sole open issue is P1: `diann_level1.py` needs a friendly preflight for a real DIA-NN report that lacks `Predicted.RT`, `FWHM`, and `Quantity.Quality`.

## Fresh execution summary

| Input | Type | Basic | Specialized | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical raw-first MaxQuant QC | 38/40 | 56/60 | 94 | 4/4 | ✅ |
| 2 | PTXQC with/without Pandoc | 37/40 | 56/60 | 93 | 4/4 | ✅ |
| 3 | Real DIA-NN Level-1 compatibility | 31/40 | 46/60 | 77 | 3/4 | ⚠️ |
| 4 | Raw-versus-LFQ loading failure | 38/40 | 57/60 | 95 | 4/4 | ✅ |
| 5 | TMT within-plex balance | 38/40 | 56/60 | 94 | 4/4 | ✅ |
| 6 | Fully confounded batch stress | 38/40 | 56/60 | 94 | 4/4 | ✅ |
| 7 | C2/T3 sample swap | 38/40 | 57/60 | 95 | 4/4 | ✅ |
| 8 | Repeated PCA determinism | 39/40 | 57/60 | 96 | 4/4 | ✅ |
| 9 | New 2/1/1 design edge | 39/40 | 58/60 | 97 | 4/4 | ✅ |
| 10 | New all-singleton boundary | 39/40 | 57/60 | 96 | 4/4 | ✅ |

Execution average: **93.1/100**. Assertion pass rate: **39/40 (97.5%)**.

## What ran

All commands are saved in [`execute_phase2.ps1`](run/phase2_final_20260923/execute_phase2.ps1). It compiled all shipped Python files; ran the seeded example twice; ran each shipped CLI; and ran both saved PTXQC R scripts through `r.sh`. The generated dynamic-audit code is [`phase2_dynamic.py`](run/phase2_final_20260923/phase2_dynamic.py); it imports the byte-identical copied branch scripts in `run/phase2_final_20260923/scripts/`.

Key printed evidence:

- Example output was byte-identical twice. It flagged `ctrl_3` at 0.30x total signal, removed one contaminant row, and produced the expected 0.973–0.975 replicate correlations.
- The canonical eight-sample matrix produced 12 `measured` replicate pairs, median linear CVs of 24.27% and 23.57%, and three `tested` PCA/batch rows.
- The failed-loading control flagged only `T4` on raw `Intensity`; LFQ flagged none. It removed 60 contaminant/decoy rows.
- The inline TMT block produced zero baseline flags and flagged planted A/127C at 0.281x.
- The swap helper flagged only `C2` and `T3`; the 2/1/1 and 1/1/1 designs retained machine-readable `not_measurable_n1`, `fallback_all_samples`, and `not_testable` states.
- PTXQC 1.1.5 without Pandoc produced PDF, mzQC, YAML and an 8x13 heatmap but no HTML; with Pandoc 3.11 it also created a 1,367.4 kB HTML report.
- The archived real DIA-NN report has only `Run`, `RT`, and `Global.Q.Value` from the Level-1 helper's required fields. Its direct CLI call raises `KeyError: ['Predicted.RT', 'FWHM']`. The helper completed on an explicitly labelled conformant fixture, returning eight no-flag runs.

## Veto gates

| Gate | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | Shipped Python compiles; all intended paths ran; one incompatible DIA-NN schema fails rather than silently generating a result. |
| T2 Contract | PASS | Frontmatter, references, scripts, CLI headers and return/status contracts are present. |
| T3 Determinism | PASS | Two helper PCA calls and two example runs were identical with full SVD and `random_state=0`. |
| T4 Security | PASS | No secrets, destructive operations, or raw user-code execution. |
| M1 Scientific integrity | PASS | Fixture findings are labelled derived; no external outcome claims were fabricated. |
| M2 Practice boundaries | PASS | QC results are not clinical diagnosis or unapproved treatment advice. |
| M3 Methodological ground | PASS | Raw-before-normalization, scale-correct CV, no-replicate status and confounding stop conditions reproduced. |
| M4 Code usability | PASS | The scripts execute on their documented/conformant inputs; Input 3 records the usability P1 separately. |

## Open issue

**P1 — Preflight the DIA-NN Level-1 column contract (Input 3).** Validate all six required fields before calculation and give an actionable `ValueError` that names the missing fields and the appropriate vendor/run-metrics export route. The current raw `KeyError` is not sufficient for a legitimate DIA-NN report that does not export RT prediction, peak width, or quantity quality.

## Artifact map

- Fresh scripts and logs: [`run/phase2_final_20260923`](run/phase2_final_20260923/)
- Machine-readable report: [`eval_report_bio-proteomics-proteomics-qc_result.json`](eval_report_bio-proteomics-proteomics-qc_result.json)
- Preserved September 15 audit: `F:/OpenScience/audits/_pre-fix-20260923/bio-proteomics-proteomics-qc/`
