> **Audit record for `bio-experimental-design-randomization-blocking`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c19ca21](https://github.com/mrsonord2240/bioSkills/tree/c19ca21cc60b9007bd955ebe4b31ead3ccf687e4/experimental-design/randomization-blocking) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-experimental-design-randomization-blocking final-pass audit

## Canonical final summary

**Final:** 93/100 — ⭐ Production Ready; deployable: true.
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

**93/100 ⭐ — Production Ready.** Exact source: `mrsonord2240/bioSkills@c19ca21cc60b9007bd955ebe4b31ead3ccf687e4:experimental-design/randomization-blocking`; source unchanged; `auditor_independent: false`.

Eight scored private same-tip inputs completed naturally with **17/17 assertions**: donor aggregation, constrained block allocation, RCBD, split-plot, factorial, scope/adversarial boundaries, and the exact corrected designit `processing_day` allocation. The retained primary-tool rerun used designit 0.5.1, exited 0, produced a 24-row layout, verified 4/4 treatment balance for each processing day, and persisted `outputs/input08_designit_layout.csv`; the earlier output-path harness failure is excluded setup evidence.

Score arithmetic: static 95 × 0.4 = 38.0; dynamic 729/8 = 91.125, × 0.6 = 54.675 → 54.7; total 92.675 → **93**.

The sole P2 recommendation is to revalidate the unrun optional Latin-square and auxiliary simulation routes. Their prior evidence was not carried into this eight-input score.
