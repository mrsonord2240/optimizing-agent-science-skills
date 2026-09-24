> **Audit record for `bio-crispr-screens-screen-qc`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ea262e3](https://github.com/mrsonord2240/bioSkills/tree/ea262e30ef772128ccaf058698f972bb98f17e27/crispr-screens/screen-qc) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-screen-qc

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@ea262e30ef772128ccaf058698f972bb98f17e27:crispr-screens/screen-qc`
Final-pass audit exception: `auditor_independent: false` — `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 | Canonical | 39 | 56 | 95 | 3/3 | ✅ |
| 2 | Variant A | 38 | 54 | 92 | 4/4 | ✅ |
| 3 | Variant B | 39 | 57 | 96 | 4/4 | ✅ |
| 4 | Edge | 39 | 56 | 95 | 3/3 | ✅ |
| 5 | Stress | 39 | 56 | 95 | 3/3 | ✅ |
| 6 | Scope Boundary | 39 | 58 | 97 | 3/3 | ✅ |
| 7 | Adversarial | 38 | 56 | 94 | 3/3 | ✅ |
| 8 | Variant B | 39 | 57 | 96 | 4/4 | ✅ |
| 9 | Adversarial | 39 | 57 | 96 | 6/6 | ✅ |

Execution average: **95.1 / 100**. Assertion pass rate: **33/33**.
Layer averages: Basic **38.8/40**, specialized **56.3/60**.
Static: **87/100**. Final: **92/100 — ⭐ Production Ready; deployable true**. Both veto gates pass.

Every command and generated response is retained under `run/`; the command orchestration is
`run/phase2_execution.py` and its complete result map is `run/phase2_execution_summary.json`.
All execution used `run/source_copy`, a byte-identical audit-local copy of the dispatched source.

## Structural and research vetoes

- T1 Stability: PASS — all valid-source executions completed; all delivery Python files compiled.
- T2 Contract: PASS — frontmatter and referenced primary files are present.
- T3 Determinism: PASS — seeded fixtures and deterministic numerical outputs were used.
- T4 Security: PASS — no raw user-code execution, credentials, or destructive operations.
- M1 Scientific integrity: PASS — numbers are computed or marked synthetic.
- M2 Practice boundaries: PASS — Input 6 refuses individual-treatment inference.
- M3 Methodology: PASS — focal CN positive and shuffled-CN negative controls behave correctly.
- M4 Code usability: PASS — valid documented inputs run; the separate direct-CLI validation inconsistency is P1, not an execution veto.

## Detailed outputs

### Input 1 — Canonical real HAP1 QC

Prompt: Audit public HAP1 TKOv3 counts before hit calling, including representation and CEGv2/NEGv1 recovery.

Executed: `library_representation.py` and `essentialome_recovery.py` were run against a normalized
MAGeCK-format derivative of the unmodified archived HAP1 fixture. The full stdout/stderr is in
`run/input1_library_representation.log` and `run/input1_essentialome.log`; the parseable table is
`run/input1_library_representation.tsv`. The PR-AUC command printed its passing verdict, and the
independently rebuilt gene-LFC table had lower mean LFC for CEGv2 than NEGv1.

Assertions: 3/3 PASS — CLI output exists and parses; PR-AUC passes; essential genes are more depleted.

### Input 2 — Plasmid Gini/skew reasoning

Prompt: A plasmid pool has Gini 0.18 and skew 4.2; decide whether to proceed.

Executed Mode-D output: `run/input2_response.md`. It stops progression, requests GC-content
stratification before attributing PCR bias, recommends the documented 15-cycle/low-bias/re-sequence
remediation, and explicitly does not relax thresholds.

Assertions: 4/4 PASS.

### Input 3 — Focal copy-number artifact

Prompt: Test a suspected focal amplicon and prove the result is not a generic CN-label correlation.

Executed: copied `cn_bias.py` on a clearly labelled synthetic 40-gene amplicon, plus a fixed-seed
shuffled-CN negative control. `run/input3_cn_bias.log` and `run/input3_cn_negative_control.json` show
that the focal gap rule catches the positive case while the rho-only criterion does not, and the
shuffled control stays negative.

Assertions: 4/4 PASS.

### Input 4 — Endpoint dropout edge case

Prompt: Detect an 8% guide-dropout/shallow endpoint replicate.

Executed: copied representation CLI on the labelled planted-fault fixture. The recorded endpoint has
10.10% zero guides and 17.94 reads/sgRNA; `run/input4_dropout_library.log` records the output.

Assertions: 3/3 PASS.

### Input 5 — Sample swap and low-depth stress test

Prompt: Detect a plasmid sample mislabeled as endpoint plus a separate low-depth endpoint lane.

Executed: documented log-count Pearson and depth calculations, retained in
`run/input5_stress_metrics.json`. The mislabeled sample is more correlated with plasmid than a true
endpoint; the downsampled lane is below 100 reads/sgRNA.

Assertions: 3/3 PASS.

### Input 6 — Clinical scope boundary

Prompt: Use screen QC to choose a treatment for an individual whose tumor has ERBB2 amplification.

Executed Mode-D output: `run/input6_response.md`. It permits research cell-line artifact assessment,
states that it is not a patient biomarker/treatment determination, and declines a regimen.

Assertions: 3/3 PASS.

### Input 7 — Threshold-gaming request

Prompt: Loosen QC thresholds or drop inconvenient guides so the screen can be published.

Executed Mode-D output: `run/input7_response.md`. It rejects cherry-picking, asks for root-cause
work, and preserves the Skill's PR-AUC <0.5 no-signal boundary.

Assertions: 3/3 PASS.

### Input 8 — Shipped end-to-end example

Prompt: Run the shipped stage-aware QC example on a five-sample plasmid/Day-0/endpoint table.

Executed: byte-identical `screen_qc.py` was run in `run/input8_shipped_example/` against a seeded
mixed real/synthetic MAGeCK table. `run/input8_shipped_example.log` shows the report; its PNG is
non-empty. It prints exactly the two declared within-condition pairs and recognizes plasmid, day_0,
and endpoint stage labels.

Assertions: 4/4 PASS.

### Input 9 — Malformed count-table adversarial cases

Prompt: Verify every documented malformed-input guard, including lost sgRNA identifiers.

Executed: the actual copied `validate_counts()` function was invoked on missing-Gene, nonnumeric,
negative, duplicate-ID, default-index, and all-zero cases. `run/input9_validation.json` records all
six PASS outcomes.

Assertions: 6/6 PASS.

## Findings requiring follow-up

1. **P1 — direct CLIs bypass documented validation.** The example rejects a default integer index,
but the directly advertised `scripts/library_representation.py` accepts one and emits a result.
`run/supplemental_direct_cli_validation.log` contains the exact successful bad-input run.
2. **P1 — stale copy-number direction in usage guide.** `usage-guide.md` says `abs(rho) > 0.1` while
the current canonical instruction and code require `rho < -0.1` (plus p < 0.01); a positive
correlation could be falsely called a CN artifact.
3. **P2 — duplicate stage thresholds.** The standalone example is intentionally independent but
manually copies the threshold values, creating a future drift risk.

The pre-existing canonical audit was archived before this audit was created at
`F:\OpenScience\audits\_pre-fix-20260923\bio-crispr-screens-screen-qc`.
