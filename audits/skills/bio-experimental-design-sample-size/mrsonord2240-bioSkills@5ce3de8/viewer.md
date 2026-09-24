> **Audit record for `bio-experimental-design-sample-size`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5ce3de8](https://github.com/mrsonord2240/bioSkills/tree/5ce3de8235a0bc77f51bd2aecc5ca599cfb6862e/experimental-design/sample-size) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-sample-size

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@5ce3de8235a0bc77f51bd2aecc5ca599cfb6862e:experimental-design/sample-size`

## Auditor and integrity

- Auditor: `Codex /root/p2_sample_size_clean_rerun`
- `auditor_independent`: `false`
- Required final-pass note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`
- Source start and end: clean at the exact pushed tip. No source files were modified.
- Superseded f3400084 report and viewer were archived at `F:\OpenScience\audits\_pre-fix-20260923\bio-experimental-design-sample-size\f3400084_phase2_invalidated_20260923\` before this report was written.
- Runtime: owned WSL process trees only, using R 4.4.3 with the private sample-size library (`ssizeRNA 1.3.3`, `PROPER 1.38.0`, `DESeq2 1.46.0`, `edgeR 4.4.2`, `pwr 1.3.0`). No shared environment was modified.
- PID evidence: `run/phase2_final_5ce3de8_pid_owned_20260923/logs/pids.tsv`. Each label records its Bash PID, direct R child PID, and natural completion code; no external PID was acted upon.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | 37 | 56 | 93 | 4/4 | ✅ COMPLETED |
| 2 | Variant A | 38 | 56 | 94 | 4/4 | ✅ COMPLETED |
| 3 | Variant B | 37 | 55 | 92 | 4/4 | ✅ COMPLETED |
| 4 | Edge | 38 | 56 | 94 | 4/4 | ✅ COMPLETED |
| 5 | Stress | 36 | 55 | 91 | 4/4 | ✅ COMPLETED |
| 6 | Scope Boundary | 37 | 56 | 93 | 4/4 | ✅ COMPLETED |
| 7 | Adversarial | 38 | 57 | 95 | 4/4 | ✅ COMPLETED |

**Execution average:** 93.1 / 100
**Assertions:** 28 / 28
**Research veto:** PASS (M1–M4)

## Executed code and outputs

All execution scripts, copied shipped source, synthetic fixtures, stdout/stderr, and PID records are under `run/phase2_final_5ce3de8_pid_owned_20260923/` and `data/phase2_final_5ce3de8_20260923/`.

### 1. Canonical — copied shipped example

Executed copied `examples/sample_size_estimation.R` with `run_owned_r.sh input01_canonical_example ...`; it exited 0. Key output:

```text
Minimum n per group ...: 46 (achieved power 0.801)
fc=1.5 -> n=48 per group
fc=2.0 -> n=17 per group
fc=3.0 -> n=9 per group
At n=6/group: BH average power = 0.000, true FDR = NaN (zero discoveries, NOT "FDR unknown").
```

### 2. Variant A — scalar no-pilot and fixed budget

`input02_scalar_budget.R` set a seed, asserted finite scalar `n`, and checked the fixed-budget interpretation. It exited 0:

```text
OK scalar n=47 achieved_power=0.810; fixed_n_power=0.000 true_fdr=NaN_zero_discoveries
```

### 3. Variant B — real pilot-vector route

`input03_vector_vary.R` created a fresh synthetic 4-vs-4 count pilot, fitted DESeq2, extracted normalized means and dispersions, then called `ssizeRNA_vary`. It exited 0:

```text
OK DESeq2-pilot vector n=26 achieved_power=0.820 genes=240
```

An earlier diagnostic with manually invented linear vectors is retained in the run logs but excluded from scoring because the Skill specifies pilot-derived vectors; it failed inside ssizeRNA integration. The scored run uses the exact documented pilot-vector workflow.

### 4. Edge — shipped low-maxN contract

`input04_low_maxn.R` sourced the copied shipped example and called its exact `safe_ssize()` and `require_reachable_n()` helpers at `maxN=2`. It completed the full example and exited 0 after asserting:

```text
OK source low-maxN contract emits documented unreachable-target message
```

### 5. Stress — copied PROPER wrapper

The copied `scripts/proper_power.R` consumed the fresh 240-gene pilot and exited 0:

```text
Nreps: 3 6 10
Marginal power: 0.278 0.556 0.778
OK: marginal power per Nreps = 3:0.278  6:0.556  10:0.778
```

`summaryPower` also printed nominal and actual FDR fields, so the result is not mistaken for an automatically achieved nominal FDR claim.

### 6. Scope boundary — copied donor-pseudobulk wrapper

The copied `scripts/pseudobulk_donor_ssize.R` consumed a fresh synthetic eight-donor, 60-cell-per-donor fixture and exited 0:

```text
OK: pseudobulk median dispersion 0.160; minimum donors per group = 38 (fc=1.50, achieved power 0.809)
```

### 7. Adversarial multiplicity check — proteomics

`input07_proteomics.R` verified the documented panel-wide adjustment and exited 0:

```text
OK proteomics unadjusted_n=11.94 adjusted_n=43.26
```

## Static evaluation

| Category | Score |
|---|---:|
| Functional suitability | 11 / 12 |
| Reliability | 10 / 12 |
| Performance and context | 7 / 8 |
| Agent usability | 15 / 16 |
| Human usability | 8 / 8 |
| Security | 11 / 12 |
| Maintainability | 11 / 12 |
| Agent-specific quality | 19 / 20 |
| **Static subtotal** | **92 / 100** |

## Final

- Static weighted: 36.8
- Dynamic weighted: 55.9
- Final: **93 / 100 — ⭐ Production Ready**
- Deployable: **true**
- Recommendations: none (no open P0 or P1).

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@5ce3de8235a0bc77f51bd2aecc5ca599cfb6862e:experimental-design/sample-size`
- `auditor_independent:false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@5ce3de8235a0bc77f51bd2aecc5ca599cfb6862e:experimental-design/sample-size`
- `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`
