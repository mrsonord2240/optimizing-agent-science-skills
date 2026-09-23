> **Audit record for `bio-experimental-design-power-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3b1beb2](https://github.com/mrsonord2240/bioSkills/tree/3b1beb228f540a2b0e5ee138bd8f6646997f4f4e/experimental-design/power-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-power-analysis

Source: `mrsonord2240/bioSkills-Improved@3b1beb228f540a2b0e5ee138bd8f6646997f4f4e:experimental-design/power-analysis`  
Generated: 2026-09-23

**✅ Production Ready — 94/100; deployable true.** This is a fresh corrective Phase 2 audit. The preceding rejected audit was preserved under `F:\OpenScience\audits\_pre-fix-20260923-corrected-3b1beb2\bio-experimental-design-power-analysis` before the run; none of its result or process evidence was reused.

All seven formal inputs, parse/package checks, both exact source examples, and determinism completed with exit 0 as isolated auditor-owned processes. Each `run/*.execution.json` records the direct-child PID and `intervention: none`.

## Corrective evidence

- The fresh bulk source run prints Actual FDR 0.3692738, 0.1849111, 0.1024990, and 0.0598908 at nominal 0.05, then marks all four candidates `REJECT` and directs the user not to report/select them.
- The fresh pseudobulk source run marks FDR 0.000 `ACCEPT` and FDR 0.133 `REJECT`.
- The independent guard probe maps FDR 0.04/0.06/NaN to ACCEPT/REJECT/REJECT and rejects invalid alpha, CV, and unit/invalid effects before RNASeqPower runs.

The full structured record is `eval_report_bio-experimental-design-power-analysis_result.json`.
