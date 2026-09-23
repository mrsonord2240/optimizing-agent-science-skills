> **Audit record for `bio-experimental-design-power-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@57a06f8](https://github.com/mrsonord2240/bioSkills/tree/57a06f815adfe5c601e399dd72e3ba82249ef370/experimental-design/power-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-power-analysis

Generated: 2026-09-23  
Source: `mrsonord2240/bioSkills@57a06f815adfe5c601e399dd72e3ba82249ef370:experimental-design/power-analysis`

**❌ Reject — 88/100; deployable: false.** This is a fresh corrective audit. The preceding canonical artifact is retained at `F:\OpenScience\audits\_invalidated-process-intervention-20260923\bio-experimental-design-power-analysis` because another worker terminated R processes; neither its verdict nor its PID evidence was reused.

Every input ran as an isolated auditor-owned process in `crispr-screen-analyst`, with per-run PID, start/end time, command, exit status, and an explicit `intervention: none` record in `run/*.execution.json`. All seven formal inputs, source parsing, the two shipped examples, and the determinism check completed with exit code 0. The only stderr messages were locale startup warnings.

## Independent realized-FDR assessment

The freshly run, unmodified `examples/rnaseq_power.R` printed a nominal FDR of 0.05 but Actual FDR of **0.3692738, 0.1849111, 0.1024990, and 0.0598908** at 3, 5, 8, and 12 replicates. `SKILL.md` tells users to read marginal power as a target-FDR curve but does not require Actual FDR to meet the target, reject failed designs, increase simulation count, or revise the model. The separate freshly run pseudobulk source example likewise reports FDR=0.133 at 12 donors. This is a methodological veto (M3), not an operational failure.

| Input | Executed | Result |
|---|---:|---|
| Canonical bulk + shipped PROPER | yes | Runs; FDR acceptance missing |
| Budget variant | yes | Pass |
| Boundary behavior | yes | Pass; no reusable preflight guard |
| Shipped pseudobulk | yes | Runs; FDR acceptance missing |
| Proteomics + ATAC | yes | Pass |
| Clinical scope | yes | Pass |
| Observed-power adversarial case | yes | Pass |

P0: Require `Actual FDR <= target` within a stated simulation tolerance before using a candidate’s power; otherwise reject it, increase `nsims`, and revise/refit the design model. Apply this to both PROPER and pseudobulk outputs.

P1: Add a runnable `rnapower()` argument validator.

The full machine-readable record is `eval_report_bio-experimental-design-power-analysis_result.json`.
