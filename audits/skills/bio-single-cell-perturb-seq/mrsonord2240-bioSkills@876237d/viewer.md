> **Audit record for `bio-single-cell-perturb-seq`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@876237d](https://github.com/mrsonord2240/bioSkills/tree/876237de72453b0651d8fe631c1201046d99c668/single-cell/perturb-seq) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-perturb-seq

Generated 2026-09-23 against `mrsonord2240/bioSkills@876237de72453b0651d8fe631c1201046d99c668:single-cell/perturb-seq`.

`auditor_independent: false`; note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

Prior canonical JSON and viewer were archived to `F:\OpenScience\audits\_pre-fix-20260923\bio-single-cell-perturb-seq`. Fresh scripts/logs: `run\phase2_20260923`.

| Input | Executed | Result | Total | Assertions |
|---|---:|---|---:|---:|
| Mixture guide assignment | yes | threshold fallback; optax missing | 76 | 3/4 |
| Real Mixscape | yes | NT 2386, KO 332, NP 112 | 90 | 4/4 |
| Seeded E-distance | yes | adjusted p=0.0201 | 91 | 4/4 |
| SCEPTRE | yes | package unavailable after GitHub install attempt | 42 | 1/3 |
| Pseudobulk + Milo | yes | 78x18,649; 208 neighborhoods | 92 | 4/4 |
| scMAGeCK boundary | yes | accurate non-fabrication handoff | 83 | 4/4 |
| Foundation-model guard | yes | required safeguards present | 92 | 4/4 |

Static 86/100; execution 80.9/100; score 83/100. Skill Veto passes. Research Veto M4 fails: SCEPTRE cannot be loaded in the declared environment, so the grade is **Reject** and deployable is false.

P0: repair and prove the SCEPTRE installation, then rerun exact calibration/discovery. P1: install/verify optax for primary mixture assignment. P2: add a small deterministic regression fixture.
