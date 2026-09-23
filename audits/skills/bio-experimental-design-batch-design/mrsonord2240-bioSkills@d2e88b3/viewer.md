> **Audit record for `bio-experimental-design-batch-design`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d2e88b3](https://github.com/mrsonord2240/bioSkills/tree/d2e88b38777dd154d642d15cefe7e2ad1ccb2a0f/experimental-design/batch-design) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-batch-design

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@d2e88b38777dd154d642d15cefe7e2ad1ccb2a0f:experimental-design/batch-design`  
Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Decision

**91/100 numerically; ❌ Reject; deployable: false.** The static score is 94 and the execution average is 88.1, but T1 operational stability fails: each valid workflow that loads `designit` or `sva` writes the expected, checked result and then segfaults on R process teardown in the dispatched `crispr-screen-analyst` environment. The environment-only probe `run/diagnose_package_exit.R` confirms that `library(designit)` alone reproduces the fault. The copied source files all parse cleanly (`run/parse_sources.out`).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical assignment | 32 | 49 | 81 | 4/4 | ⚠️ |
| 2 | Bridge-layout regression | 31 | 49 | 80 | 4/4 | ⚠️ |
| 3 | SVA missing-value regression | 34 | 50 | 84 | 4/4 | ⚠️ |
| 4 | Balance verifier regression | 38 | 58 | 96 | 4/4 | ✅ |
| 5 | Correction-boundary regression | 34 | 50 | 84 | 4/4 | ⚠️ |
| 6 | New determinism input | 34 | 50 | 84 | 3/4 | ⚠️ |
| 7 | New missing-column boundary | 38 | 57 | 95 | 4/4 | ✅ |
| 8 | Capacity boundary | 38 | 57 | 95 | 4/4 | ✅ |
| 9 | Bridge-coordinate boundary | 37 | 57 | 94 | 4/4 | ✅ |

Execution average: **88.1/100**. Assertion pass rate: **35/36 (97.2%)**.

## Vetoes and Static Review

| Gate | Result | Evidence |
|---|---|---|
| T1 Operational stability | **FAIL** | Valid package workflows 1, 2, 3, 5, and 6 end with a segmentation fault after producing correct results; the isolated `library(designit)` probe fails identically. |
| T2 Contract | PASS | Required frontmatter, documented scripts, and command interfaces exist. |
| T3 Determinism | PASS | The repeated same-seed assignment CSV was byte-identical. |
| T4 Security | PASS | No secrets, raw user-code execution, or destructive operation is present. |
| M1 Scientific integrity | PASS | All numerical results are from labelled synthetic audit data. |
| M2 Practice boundaries | PASS | This is design and analysis guidance, not individualized clinical advice. |
| M3 Methodological ground | PASS | Confounded ComBat is rejected; partial imbalance is modeled with batch; invalid layouts are stopped. |
| M4 Code usability | PASS | All four shipped R files parse and substantive bodies compute checked outputs; the distinct teardown failure is captured by T1. |

Static review: functional suitability 12/12; reliability 10/12; performance/context 7/8; agent usability 16/16; human usability 8/8; security 11/12; maintainability 12/12; agent-specific 18/20 = **94/100**.

## Detailed Outputs

### Input 1 — Canonical assignment

Prompt: Assign 24 samples to three batches while balancing condition and sex.

Executed: `run/in1_assign_canonical.sh` runs the copied `scripts/assign_batches.R samples24.csv 3 8 condition,sex layout24.csv 10000 17`.

Result: `layout24.csv` exists. The logged condition and sex tables are both 4/4/4 across batches. The process then reports `Segmentation fault` on teardown. Assertions: output exists PASS; condition balanced PASS; sex balanced PASS; explicit verification PASS.

### Input 2 — Reference/bridge layout

Prompt: Place 60 samples in four TMT 16plexes with channel 16 reserved for a pooled bridge.

Executed: `run/in2_bridge_canonical.sh` runs the exact copied bridge script.

Result: all four plexes contain 15 biological rows; channel 16 is unassigned. Condition is 7/7/8/8; the shared checker warns that the site table has spread 2. The process then segfaults after output. Assertions: bridge reservation PASS; capacity PASS; condition representation PASS; soft warning PASS.

### Input 3 — SVA with missing values

Prompt: Estimate hidden structure in a matrix that contains missing intensity values.

Executed: `run/in3_sva_na.sh` calls `run/test_sva_missing.R`, which sources copied `examples/batch_design.R`.

Result: the example reports 282/24000 missing cells, retains 766/1000 complete rows, estimates one surrogate variable, and labels ComBat output as visualization-only. It then segfaults during teardown. All four scientific output assertions pass.

### Input 4 — Balance verifier

Prompt: Check a returned plate map that may be balanced, avoidably uneven, or confounded.

Executed: `run/in4_balance_cases.sh` calls `run/check_balance_cases.R`.

Result: a balanced condition/sex map passed; a spread-3 map emitted the expected warning; a confounded map stopped. All four assertions pass and the R process exits cleanly because it does not load the affected packages.

### Input 5 — Correction boundary

Prompt: Can ComBat rescue complete batch-condition confounding, and what should be done with partial imbalance?

Executed: `run/in5_combat_claims.sh` calls `run/test_combat_design_claims.R` on seeded synthetic matrices.

Result: ComBat rejects perfect confounding and a `condition + batch` limma design is estimable for partial imbalance. The process then segfaults at teardown. Four content and scope assertions pass.

### Input 6 — Determinism

Prompt: Repeat the same seeded assignment and confirm reproducibility.

Executed: `run/in6_determinism.sh` repeats the documented command with seed 17.

Result: `layout24_repeat.csv` is byte-identical to `layout24.csv`; its balance tables are again 4/4/4. The only failed assertion is successful process termination, because the same teardown segmentation fault recurred.

### Inputs 7–9 — Input-validation boundaries

Executed scripts: `run/in7_missing_covariate.sh`, `run/in8_over_capacity.sh`, and `run/in9_invalid_reserved_channel.sh`.

Results: each deliberately invalid request was rejected before a layout could be written: respectively missing `sex`, 60 samples for 24 slots, and reserved channel 17 in a 16-channel plex. All 12 assertions pass. The wrapper treats these intended rejections as successful tests.

## Raw Evidence

Every script and terminal output is under [`run/`](run/). `run/scripts/` and `run/examples/` are byte-for-byte copies of the exact source-tip artifacts executed outside the source worktree. `run/parse_sources.out` records syntax success for all four shipped R files; `run/diagnose_package_exit.out` records the minimal designated-environment teardown fault.

## Recommendation

**P0 — repair the designated R environment.** Under `crispr-screen-analyst`, a bare `library(designit)` completes its body then exits with a segmentation fault. Repair or replace the R/designit runtime under the environment tooling policy, prove a clean load exits 0, and repeat this Phase 2 audit. The source worktree needs no audit-driven modification for this finding.
