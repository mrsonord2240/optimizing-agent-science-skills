> **Audit record for `bio-workflows-proteomics-pipeline`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ef9b7ee](https://github.com/mrsonord2240/bioSkills/tree/ef9b7eed11c0dcbea3820d6b97cf7fd8b7c702e4/workflows/proteomics-pipeline) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-workflows-proteomics-pipeline

Generated: 2026-09-23  
Source: `mrsonord2240/bioSkills@ef9b7eed11c0dcbea3820d6b97cf7fd8b7c702e4:workflows/proteomics-pipeline`  
Final-pass metadata: `auditor_independent: false` — `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 | Canonical MaxQuant + batch | 38 | 57 | 95 | 4/4 | ✅ |
| 2 | DIA-NN parquet | 37 | 56 | 93 | 4/4 | ✅ |
| 3 | Three-condition dose series | 38 | 57 | 95 | 4/4 | ✅ |
| 4 | Shuffled annotation | 38 | 58 | 96 | 4/4 | ✅ |
| 5 | TMT10 correction | 36 | 54 | 90 | 4/4 | ✅ |
| 6 | MSstats feature model | 36 | 55 | 91 | 4/4 | ✅ |
| 7 | SILAC raw-p shortcut | 38 | 57 | 95 | 4/4 | ✅ |
| 8 | ICU triage scope boundary | 39 | 55 | 94 | 4/4 | ✅ |
| 9 | Empty-directory example | 37 | 57 | 94 | 4/4 | ✅ |
| 10 | Missing TMT Norm channel | 36 | 53 | 89 | 4/4 | ✅ |

Execution average: **93.2 / 100**. Assertion pass rate: **40/40**.  
Static score: **92 / 100**. Final score: **93 / 100 — ⭐ Production Ready**.  
Deployable: **true**. Structural and research vetoes: **PASS**.

## What Ran

All runtime evidence, copied candidate scripts, input fixtures, logs, exit-code records, and the independent `phase2_assert.py` checks are in `run/phase2_final_20260923/`.

- Input 1: 1,323 rows; 62 calls; batch covariate; 18 non-estimable values surfaced.
- Input 2: finite 887 x 8 DIA-NN matrix.
- Input 3: no-complete-case PCA correctly falls back to correlation; High_vs_Ctl 20 and Low_vs_Ctl 0 calls.
- Input 4: shuffled annotation preserves the 62-call result.
- Input 5: 24 x 10 nonnegative TMT reporter matrix.
- Input 6: 296 MSstats comparisons with `Protein`, `log2FC`, and `adj.pvalue`.
- Input 7: 453 SILAC proteins tested; 49 BH calls.
- Input 8: no code was appropriate; the Skill declines individual ICU triage and supplies the clinical handoff.
- Input 9: standalone example created its simulated input, result CSV, and four PDFs.
- Input 10: missing `Norm` channel stopped before result creation; all six candidate scripts separately parsed.

## Caveats and recommendations

Seven positive R routes returned host status 11 only after writing artifacts that passed independent parsing. This is recorded as P1 rather than hidden; reproduce in a compatible/isolated native-extension environment. The multiplex route's `Norm` preflight was freshly executed, but a compact source-controlled positive multiplex fixture is still needed for repeatable full-bridge verification.

The September 15 audit was preserved before this audit at `F:/OpenScience/audits/_pre-fix-20260923/bio-workflows-proteomics-pipeline/`. The final-pass checkpoint is `F:/OpenScience/audits/_final_pass/bio-workflows-proteomics-pipeline/CHECKPOINT.md`.
