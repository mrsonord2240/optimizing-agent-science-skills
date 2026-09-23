> **Audit record for `bio-microbiome-functional-prediction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ea6cfef](https://github.com/mrsonord2240/bioSkills/tree/ea6cfef4d791daeed8aab68e9a4519952b7bb1b1/microbiome/functional-prediction) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Final-pass Phase 2 audit — bio-microbiome-functional-prediction

Evaluated 2026-09-23 against `mrsonord2240/bioSkills@ea6cfef4d791daeed8aab68e9a4519952b7bb1b1:microbiome/functional-prediction`.

Final result: **93/100 — Production Ready — deployable: true**. Both veto gates pass. This directed final-pass record intentionally sets `auditor_independent: false` with note `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

The prior September 19 audit is preserved unchanged at `F:\OpenScience\audits\_pre-fix-20260923\bio-microbiome-functional-prediction\`.

| Input | Fresh execution | Result | Score |
|---|---|---:|---:|
| Canonical PICRUSt2 | Exact 2.6.3, documented `-p`, mp, NSTI 2 | 503 pathways and KO/EC/NSTI tables | 94 |
| QIIME2 route | Direct source-route assertions | q2-picrust2 handoff correct | 86 |
| Poor-reference edge | Exact 2.6.3 on 11 ASVs | Correct `min_align` hard abort, no NSTI output | 92 |
| NSTI reporter | Shipped Python script, fresh pipeline output | mean 0.077, median 0.001, 3/751 and 0.0% at 2 | 95 |
| CoDA stress | ALDEx2, MaAsLin2, LinDA on fresh pathways | 275/421 hits; 2 raw vs 242 normalized; 469 LinDA fits | 94 |
| Marine scope | Direct source-route assertions | FAPROTAX/shotgun boundary correct | 92 |
| Activity adversary | Direct source guard assertions | potential-not-activity and circularity protections correct | 92 |

Assertions: **28/28 passed**. Execution average: **92.1/100**. The sole P2 asks for a clearer tens-of-minutes runtime-planning note near the central command.

## Evidence executed

- `run/20_p2_prepare_inputs.sh`: fresh BIOM-to-TSV export reproduced the `# Constructed from biom file` line, then stripped it before PICRUSt2.
- `run/21_p2_picrust2_full_adapted.sh`: fresh end-to-end exact-version workflow. The initially inventory-named shared `picrust2` environment was found drifted to 2.0.3-b and missing its reference HMM; an isolated 2.6.3 environment was installed and confirmed before this evidence run. The source itself was unchanged.
- `run/22_p2_nsti_report.sh`, `run/23_p2_synthetic_edge.sh`, `run/24_p2_coda_linda.R`, and `run/25_p2_skill_guards.py`: all executed and retained with their outputs/work products.
