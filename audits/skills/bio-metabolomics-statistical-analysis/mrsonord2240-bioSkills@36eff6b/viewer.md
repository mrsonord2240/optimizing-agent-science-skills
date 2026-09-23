> **Audit record for `bio-metabolomics-statistical-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@36eff6b](https://github.com/mrsonord2240/bioSkills/tree/36eff6bf7899c44e3d589b10952e7fa2c14e31fc/metabolomics/statistical-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-statistical-analysis

Generated: 2026-09-23. Source: `mrsonord2240/bioSkills@36eff6bf7899c44e3d589b10952e7fa2c14e31fc:metabolomics/statistical-analysis`.

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

| Input | Result | Evidence |
|---|---:|---|
| 1 Welch/BH | 96 | 16/30 true positives; no false or detection-rate hits |
| 2 PCA/T2 | 97 | MTBLS79 two outliers; synthetic S1/S2 only |
| 3 Guard sweep | 99 | 0/110 uncaught silent-empty fits |
| 4 LMM | 94 | 7/10 true time effects; 0 false positives |
| 5 Correlated FDR | 96 | 111 features → 13 compounds; one false compound disclosed |
| 6 Scope | 98 | Patient treatment declined; clinician/cohort redirect |
| 7 Adversarial | 98 | Bare score plot declined; pQ2 required |
| 8 Paired | 97 | Paired 20/20 vs unpaired 0/20 |
| 9 VIP | 97 | Bootstrap top-10 overlap 5.6/10 |
| 10 Shipped examples | 98 | Python and all three `PERM_I=100` R fits completed |
| 11 PCA CLI | 98 | S1/S2 found; NA path rejects with documented remedy |

Execution average **97.1/100**; assertions **33/33**. Skill and research vetoes both PASS. Static **98/100**. Final **97/100 — Production Ready — deployable: true**. No open P0/P1/P2.

Fresh scripts and logs are in `run/`; PCA fixtures/output are in `data/`. The prior active audit was preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-metabolomics-statistical-analysis`.
