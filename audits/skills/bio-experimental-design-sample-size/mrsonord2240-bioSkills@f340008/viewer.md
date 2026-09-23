> **Audit record for `bio-experimental-design-sample-size`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@f340008](https://github.com/mrsonord2240/bioSkills/tree/f3400084fa984a8533bba8f69a15301619fe6a0e/experimental-design/sample-size) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-sample-size

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@f3400084fa984a8533bba8f69a15301619fe6a0e:experimental-design/sample-size`

This is a fresh Phase 2 rerun. Before it began, the invalidated report, viewer, data, and run directory were preserved at `F:\OpenScience\audits\_invalidated-pid-interference-20260923\bio-experimental-design-sample-size`. No verdict or runtime evidence from that archive was used here.

## Auditor and source integrity

- Auditor: `Codex /root/p2_sample_size_clean_rerun`
- Independent-auditor metadata: `false` (final-pass program rerun)
- Worktree: `F:\OpenScience\wt\experimental-design-sample-size`
- Branch / tip: `fix/experimental-design-sample-size` / `f3400084fa984a8533bba8f69a15301619fe6a0e`
- Source state before and after: clean (`git diff --quiet` exit 0; no porcelain or untracked output)
- Runtime: supported `crispr-screen-analyst/r.sh`, R 4.4.3 / Bioconductor 3.20 package route. A WSL R 4.5.2 probe was not used because ssizeRNA, PROPER, DESeq2, and pwr were absent.
- Process safety: every considered dynamic run was foregrounded by `run_r_owned_heartbeat.sh`, which logged its Bash PID, direct R-child PID, start, natural completion, and exit. No PID was enumerated for action, signalled, or terminated. The final shipped-example evidence is `input01_shipped_example_isolated_final`; earlier overlapping launch attempts are retained as orchestration diagnostics only and excluded from scoring.
- Parse check: all three shipped R files parsed (`OK parse: 3 shipped R files parsed`).

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | 23 | 35 | 58 | 2/4 | ❌ PARTIAL |
| 2 | Variant A | 31 | 45 | 76 | 3/4 | ❌ PARTIAL |
| 3 | Variant B | 23 | 34 | 57 | 2/4 | ❌ ERROR |
| 4 | Edge | 22 | 32 | 54 | 2/4 | ❌ ERROR |
| 5 | Stress | 31 | 46 | 77 | 3/4 | ❌ PARTIAL |
| 6 | Scope Boundary | 31 | 46 | 77 | 3/4 | ❌ PARTIAL |
| 7 | Adversarial | 37 | 57 | 94 | 4/4 | ✅ COMPLETED |

**Execution average:** 70.4 / 100  
**Assertions:** 19 / 28  
**Research Veto M4:** FAIL — copied shipped runtime paths exit 139.

## Fresh execution evidence

### 1. Copied shipped end-to-end example

`examples/sample_size_estimation.R` was copied into the audit area and run in final isolated form under Bash PID `214479` and R PID `214481`. It produced no calculation stdout and exited `139` after natural wait. This fails the runnable end-to-end assertion.

### 2. Scalar ssizeRNA and fixed-budget check

Fresh synthetic invocation printed:

```text
OK scalar: n=47 achieved_power=0.810; budget_n6_power=0.000 fdr=NaN-zero-discoveries
```

The owned process nevertheless exited `139`. The numeric assertions pass; executable usability does not.

### 3. Vector ssizeRNA route

A finite, positive 300-gene vector fixture reached `ssizeRNA_vary()` and failed:

```text
Error in integrate(sigmaFun, 0, Inf, abs.tol = 1e-10) :
  non-finite function value
```

The displayed scalar-versus-vector rule alone does not preflight this numerical failure.

### 4. Infeasible ceiling

The very-low `maxN=2` edge case did not return the described `NA`; it raised:

```text
Error in if (...) : argument is of length zero
Calls: ssizeRNA_single -> ssize.twoSampVaryDelta
```

The subsequent `is.na(n)` guard is therefore unreachable for this case.

### 5. Copied PROPER wrapper

An audit-generated 240-gene, 4v4 count CSV drove the copied `scripts/proper_power.R`. It printed three simulations, `Nreps1 = 3, 6, 10`, marginal powers `0.111, 0.111, 0.667`, and `summaryPower()` with nominal/actual FDR. It then exited `139` after printing its OK line.

### 6. Copied donor-pseudobulk wrapper

An audit-generated 8-donor, 160-gene, 24-cells-per-donor RDS/CSV fixture drove `scripts/pseudobulk_donor_ssize.R`. It printed:

```text
OK: pseudobulk median dispersion 0.018; minimum donors per group = 10 (fc=1.50, achieved power 0.848)
```

It correctly treats the statistical unit as donors, then exits `139` after output.

### 7. Proteomics multiplicity route

This route completed with exit `0` and printed:

```text
OK proteomics: unadjusted_n=11.94 adjusted_5000_feature_n=43.26
```

## Final result

Static score: **86 / 100**. Dynamic score: **70.4 / 100**. Diagnostic weighted score: **77 / 100**.

**Grade: Reject. Deployable: false.** The Research Veto’s Code Usability gate overrides the numeric diagnostic score because copied shipped R paths naturally exit `139` in the designated supported environment.

### Recommendations

- **P0 — Repair the R runtime exit-139 failure.** Use a private supported R 4.4 / Bioconductor 3.20 runtime with ssizeRNA 1.3.3, PROPER 1.38.0, and DESeq2 1.46.0; do not mutate the shared environment. Re-run copied shipped example, PROPER, and pseudobulk scripts and require zero exit status.
- **P1 — Preflight the infeasible `maxN` path.** Catch estimator errors separately from `NA` and test a very-low-ceiling example.
- **P1 — Validate `ssizeRNA_vary` vectors.** Add range and finiteness checks plus a recovery message for `integrate()` failures.

## Files

- Fresh scripts, source copy, PID logs, and stdout/stderr: `run\phase2_pid_owned_20260923\`
- Fresh synthetic fixtures: `data\phase2_pid_owned_20260923\`
- Invalidated prior audit archive: `F:\OpenScience\audits\_invalidated-pid-interference-20260923\bio-experimental-design-sample-size\`
