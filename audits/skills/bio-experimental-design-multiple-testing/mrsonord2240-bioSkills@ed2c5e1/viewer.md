> **Audit record for `bio-experimental-design-multiple-testing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ed2c5e1](https://github.com/mrsonord2240/bioSkills/tree/ed2c5e1ce6545d9b5dc0a84ff4fc719a580e4a56/experimental-design/multiple-testing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-multiple-testing

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@ed2c5e1ce6545d9b5dc0a84ff4fc719a580e4a56:experimental-design/multiple-testing`

Mode: D (direct decision workflow plus R script) · Category: Data Analysis · Complexity: Complex (7 inputs)

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical genome-wide discovery | 36 | 55 | 91 | 4/4 | ✅ |
| 2 | Variant A: local FDR + FCR | 37 | 55 | 92 | 4/4 | ✅ |
| 3 | Edge: small family | 38 | 56 | 94 | 4/4 | ✅ |
| 4 | Variant B: IHW function + CLI | 36 | 57 | 93 | 4/4 | ✅ |
| 5 | Stress: shipped example | 22 | 31 | 53 | 3/4 | ❌ |
| 6 | Scope boundary: confirmatory endpoints | 36 | 54 | 90 | 4/4 | ✅ |
| 7 | Adversarial: outcome-linked filter | 37 | 55 | 92 | 4/4 | ✅ |

Execution average: **86.4 / 100** · Assertions: **27 / 28** · Static score: **78 / 100** · Weighted score: **83 / 100**.

## Veto result

Skill Veto: PASS. Research Veto: **FAIL (M4 Code Usability)**. The shipped complete example exited 139 in four of four direct runs, even though each run emitted its expected intermediate table. That makes the grade **Reject** and `deployable: false`.

## Detailed execution evidence

### Inputs 1–4 — executed R/Python workflows

`run/audit_multiple_testing.R` created seeded synthetic data and executed the documented BH, BY, qvalue, local-FDR, FCR, sourceable `ihw_safe()`, and CLI paths. `run/audit_statsmodels.py` executed the explicit Python FDR methods.

- Input 1: BH 202, BY 94, qvalue 210 discoveries; pi0 0.8444; explicit Python BH/BY 4/3 rejections.
- Input 2: lfdr < 0.2 selected 237, mean lfdr 0.0614; selected FCR confidence level 0.997980 for 202 intervals.
- Input 3: `qvalue(..., lambda=0)` on 30 all-null values returned pi0 1 and no calls.
- Input 4: sourceable wrapper and CLI both used IHW on attempt 1 and produced 73 discoveries; CLI wrote 1,800 valid rows.

### Input 5 — shipped example failure

`run/run_shipped_example.sh` invoked `examples/multiple_testing_correction.R` through the designated `crispr-screen-analyst/r.sh`, with an audit-owned 90-second process-group bound. Each of four direct executions printed:

```text
BH mean FDP = 0.046
q-value: pi0 = 0.912, discoveries at q<0.05 = 98
IHW discoveries at FDR 0.05 = 85 (vs BH = 93)
```

but every process exited `139` (`Segmentation fault`). The bound did not time out; this was a real crash after output. Repetition status is saved in `run/output/repeat_status.txt`.

### Inputs 6–7 — direct decision workflow

The complete Skill-directed outputs are saved in `run/input6_scope_boundary.md` and `run/input7_adversarial_filter.md`. Input 6 correctly hands confirmatory endpoint multiplicity to the dedicated clinical skill; Input 7 rejects a t-statistic prefilter as outcome-linked and anti-conservative.

## Audit files

- `run/audit_multiple_testing.R` and `run/audit_statsmodels.py`: reproducible dynamic regression runs.
- `run/run_shipped_example.sh` and `run/repeat_shipped_example.sh`: owned, bounded full-example executions.
- `data/`: seeded synthetic inputs.
- `run/output/`: parsed run outputs and repetition status.

## Required fix

P0: Make the shipped example exit cleanly. Reuse the tested `scripts/ihw_safe.R` wrapper rather than maintain a divergent inline child-process IHW implementation, and prove repeated zero-exit runs before a new audit.
