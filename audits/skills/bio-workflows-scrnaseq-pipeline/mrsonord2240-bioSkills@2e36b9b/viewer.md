> **Audit record for `bio-workflows-scrnaseq-pipeline`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@2e36b9b](https://github.com/mrsonord2240/bioSkills/tree/2e36b9b60a6db36a41843cd3bc5f7fcf476e9c15/workflows/scrnaseq-pipeline) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Re-audit Viewer — bio-workflows-scrnaseq-pipeline

Exact commit: 2e36b9b60a6db36a41843cd3bc5f7fcf476e9c15
Evidence: run/reaudit_fixed_findings.py/.out

| Measure | Result |
|---|---:|
| Assertions | 6 / 6 PASS |
| Open P0/P1/P2 | 0 |
| Result | Production Ready |

The committed skill now includes multi-sample integration, pseudobulk DE,
differential abundance, declared QC checkpoints, MAD-adaptive QC, and
raw/feature-name validation. The exact-commit audit exited 0.
