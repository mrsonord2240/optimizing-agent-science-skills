> **Audit record for `bio-causal-genomics-pleiotropy-detection`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5c1c030](https://github.com/mrsonord2240/bioSkills/tree/5c1c030c4152f90b8a1457853c927e8568a710fd/causal-genomics/pleiotropy-detection) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-pleiotropy-detection

## Canonical final summary

**Final:** 94/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23
Exact source: `mrsonord2240/bioSkills@5c1c030c4152f90b8a1457853c927e8568a710fd:causal-genomics/pleiotropy-detection`
Final-pass metadata: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.

## Verdict

**94/100 — Production Ready — deployable: true.** Both veto gates passed. The preceding audit was preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-causal-genomics-pleiotropy-detection` before this canonical report was written.

| Input | Type | What was executed | Basic | Specialized | Total | Assertions |
|---|---|---|---:|---:|---:|---:|
| 1 | Canonical | Cached real BMI15→MDD18 battery + PRESSO | 36 | 56 | 92 | 4/4 |
| 2 | Variant A | Planted CHP false-negative regression | 37 | 58 | 95 | 4/4 |
| 3 | Edge | Three-SNP PRESSO precondition | 38 | 55 | 93 | 3/3 |
| 4 | Variant B | Extreme weak-IV RAPS | 36 | 54 | 90 | 4/4 |
| 5 | Stress | Exact SIMEX source + conmix | 37 | 55 | 92 | 4/4 |
| 6 | Scope Boundary | Personal statin request | 39 | 57 | 96 | 3/3 |
| 7 | Adversarial | Eighteen-SNP mixture methods | 37 | 55 | 92 | 4/4 |
| 8 | Variant B | LCV return-field contract | 38 | 57 | 95 | 4/4 |
| 9 | Stress | TwoSampleMR RAPS signature | 38 | 56 | 94 | 4/4 |
| 10 | Scope Boundary | Documentation/reference integrity | 39 | 57 | 96 | 3/3 |
| 11 | Canonical | Exact shipped CAUSE example | 38 | 58 | 96 | 4/4 |
| 12 | Stress | Exact shipped 5,000-draw MR-PRESSO example | 38 | 58 | 96 | 4/4 |

**Execution average:** 93.9/100. **Assertions:** 45/45.

## Fresh runtime evidence

All scripts and captured output are in `run/2026-09-23-final-pass/`. The successful R runner was the environment's Git-Bash `r.sh`/`r_cause.sh`; an initial PowerShell direct invocation produced empty output and was discarded before scoring.

- Real BMI15→MDD18: IVW 0.1422; corrected PRESSO IVW 0.1561; mean F 58.7; 95 instruments; PRESSO completed in 160.8 seconds at the audit's reduced 1,000-draw check.
- Planted CHP: true effect 0; IVW 0.869 with p < 2.22e-16; PRESSO global p 0.9995 and 0/40 outliers. This is the documented reason to escalate to CAUSE/LHC-MR rather than accept the UHP battery.
- Exact CAUSE source: 150 signature SNPs; gamma 0.2884 (95% CI 0.2476–0.3286) for planted 0.3; delta ELPD -8.586, z -7.115, one-sided p 5.61e-13.
- Exact MR-PRESSO source: raw IVW 0.3372; no outliers, corrected IVW NA; the zero-length distortion-test case did not crash.
- LCV: `gcp.pm` is numeric; legacy `gcp` is NULL. RAPS: top-level loss arguments error, while the documented nested `parameters=list(...)` form succeeds.

## Veto review

- **Skill Veto:** PASS. Frontmatter and linked artifacts exist; all five shipped R examples parse; no raw evaluation or destructive instruction was found.
- **Research Veto M1:** PASS. Every reported figure above comes from captured output or a shipped source file.
- **Research Veto M2:** PASS. Input 6 declines a personal recommendation and names the population-to-individual gap.
- **Research Veto M3:** PASS. Input 2 prevents the primary methodological error: mistaking a CHP-biased IVW/PRESSO result for causal confirmation.
- **Research Veto M4:** PASS. The exact CAUSE and MR-PRESSO examples and the SIMEX/LCV/RAPS routes executed with the current environment.

## Static score: 94/100

The UHP/CHP split, explicit thresholded decision flow, practice boundary, reporting requirements, and reference-file split are strong. Small deductions reflect the unseeded standalone SIMEX example, version-sensitive GitHub dependencies, and validation delegated to packages.

## Open recommendations

- **P2:** seed the standalone SIMEX script (or print an accepted seed).
- **P2:** label the CAUSE demo's expected warning that 50,000 nuisance variants is below its preferred 100,000-variant scale.

No P0 or P1 findings are open.
auditor_independent: false
