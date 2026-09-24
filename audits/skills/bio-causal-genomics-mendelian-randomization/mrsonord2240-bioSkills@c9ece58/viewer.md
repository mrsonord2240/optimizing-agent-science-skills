> **Audit record for `bio-causal-genomics-mendelian-randomization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c9ece58](https://github.com/mrsonord2240/bioSkills/tree/c9ece583aa342593b6e2411191636de7f33a1d31/causal-genomics/mendelian-randomization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-mendelian-randomization

## Canonical final summary

**Final:** 93/100 — ⭐ Production Ready; deployable: true.

Source: `mrsonord2240/bioSkills@c9ece583aa342593b6e2411191636de7f33a1d31:causal-genomics/mendelian-randomization`
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@c9ece583aa342593b6e2411191636de7f33a1d31:causal-genomics/mendelian-randomization`
Audit type: final-pass Phase 2; `auditor_independent: false` by the directed final-pass exception.

## Result

**93/100 — Production Ready — deployable: true.** Both veto gates pass. The 2026-09-17 report and its raw evidence were preserved before this audit at `F:\OpenScience\audits\_pre-fix-20260923\bio-causal-genomics-mendelian-randomization\` (31 files).

The exact-tip source copy used for execution has 19 files and SHA-256 matches the worktree for all 19 files (`HASH_DIFFS=0`). All eight shipped R files parse. Dynamic evidence is in `run/phase2_20260923/logs/`; every command harness is retained in that run folder.

| Input | Scenario | Executed | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---|---|
| 1 | Real BMI15→MDD18 two-sample battery | yes, partial PRESSO bootstrap | 36 | 54 | 90 | 3/4 | ❌ Partial |
| 2 | cis-MR plus coloc regression | yes | 38 | 57 | 95 | 4/4 | ✅ |
| 3 | Sparse 3-SNP boundary | yes | 38 | 56 | 94 | 4/4 | ✅ |
| 4 | MVMR conditional-F<1 guard | yes | 39 | 58 | 97 | 4/4 | ✅ |
| 5 | NOME/SIMEX plus Steiger NULL guard | yes | 38 | 57 | 95 | 4/4 | ✅ |
| 6 | Personal-genotype scope boundary | yes, Mode A | 37 | 56 | 93 | 4/4 | ✅ |
| 7 | One-sample overlap mislabeled two-sample | yes | 37 | 56 | 93 | 4/4 | ✅ |
| 8 | CAUSE under compatible loo wrapper | yes | 37 | 57 | 94 | 4/4 | ✅ |
| 9 | LCV gcp execution | yes | 35 | 50 | 85 | 4/4 | ✅ |
| 10 | qhet_mvmr weak-but-not-<1 boundary | yes, partial qhet | 34 | 49 | 83 | 3/4 | ❌ Partial |
| 11 | Steiger forward/reverse success path | yes | 39 | 58 | 97 | 4/4 | ✅ |
| 12 | Exact workflow with real 1000G EUR LD | yes | 39 | 57 | 96 | 4/4 | ✅ |
| 13 | Exact MR-PRESSO outlier script | yes | 39 | 57 | 96 | 4/4 | ✅ |
| 14 | Exact MVMR CLI script | yes | 36 | 54 | 90 | 4/4 | ✅ |
| 15 | Exact SIMEX CLI script | yes | 38 | 56 | 94 | 4/4 | ✅ |

**Execution average: 92.8/100. Assertion pass rate: 58/60 (96.7%).**

## Dynamic evidence

1. `input1_standard_two_sample_regression.R` harmonised 95 real BMI15/MDD18 loci and recovered IVW `b=0.1422`, `p=0.00597`, MR-RAPS `b=0.159`, and Steiger `TRUE` (`p=1.36e-68`). Its 1,000-draw MR-PRESSO substep terminated after materializing the non-PRESSO results, so this isolated execution is partial. The exact shipped 10,000-draw example independently completed later: global MR-PRESSO `p=0.897`, followed by Steiger and STROBE output. The reporting line safely handled the numeric global p-value.
2. `input2_cis_mr_coloc.R` and the exact shipped cis example both yielded IVW `b=0.6132` and coloc `PP.H4=1.00` (the documentation warns that coloc estimated `sdY`; that is not suppressed).
3. `input3_sparse_instruments.R` recovered IVW `b=0.322` against planted `0.35`; MR-PRESSO returned its expected “Not enough intrumental variables” boundary error.
4. `input4_mvmr_guard.R` reproduced conditional F `0.870/0.783`; the exact guard stopped before `qhet_mvmr`, with the documented explanation.
5. `input5_stress_simex_steiger.R` had `I²_GX=0`; SIMEX completed (`1.0202` versus naive `0.339`) and the Steiger NULL path raised the prescribed actionable error.
6. `input6_phase2_scope_boundary_response.md` declined the n=1 diagnostic/treatment request, explained the population-level MR requirement, and redirected personal care to clinicians.
7. `input7_onesample_mislabeled.R` planted zero causal effect but got IVW `b=0.245` and MR-RAPS `b=0.230`, validating the text that MR-RAPS does not resolve overlap/confounding bias.
8. `input8_cause.R`, run through the environment’s compatible-`loo` wrapper, completed `cause()`: 147 eligible variants, causal gamma `0.43 (0.36,0.50)`, sharing-vs-causal delta ELPD `-8.92`, z `-13.79`. This replaces the old environment-only crash evidence.
9. `input9_lcv.R` completed `RunLCV` and returned all documented gcp/rho fields (`gcp.pm=0.0548`, `gcp.pse=0.1182`, `rho=0.2688`). It is an execution test, not validation that the intentionally small synthetic construction estimates its nominal 0.6 exactly.
10. `input10_new_mvmr_guard_boundary.R` recovered F `2.194/2.195` and IVW `0.292/-0.090`, then the 200-iteration `qhet_mvmr` call ended without emitting its result. This remains a partial, transparently scored execution rather than a hidden pass.
11. `input11_new_steiger_success.R` recovered forward IVW `0.5045` for planted `0.5`; directionality was `TRUE` forward and `FALSE` after reversal, both non-NULL.
12. `input12_fresh_real_ld_clump.R` ran the exact `twosample_workflow.R` against the 22,665,064-variant / 503-sample real 1000G EUR bfile. PLINK made two clumps from three instruments, removed the known `r²=0.960` SNP, and retained `rs6728916,rs74048003`; the harmonised two-SNP IVW was exactly `0.35`.
13. `input13_fresh_mr_presso_script.R` ran the exact outlier script with 1,000 draws on 40 synthetic loci. It wrote a parseable 23-SNP list containing all 10 planted invalid SNPs; no second Bonferroni correction occurred.
14. `input14_fresh_mvmr_script.R` ran the exact MVMR CLI script, printing F `8.76/8.53`, IVW `0.290/-0.092`, and Q_A p=`0.962`. The intentionally weak F confirms the script surfaces values for the caller to interpret; it does not clear the Skill’s >10 recommendation.
15. `input15_fresh_simex_script.R` ran the exact SIMEX CLI script with a seed and produced both slopes (`2.1881` corrected, `0.7366` naive).

The shipped visualization example wrote four nonempty PDFs: `mr_scatter.pdf`, `mr_forest.pdf`, `mr_leaveoneout.pdf`, and `mr_funnel.pdf`. The shipped `twosamplemr_analysis.R` completed 20-SNP IVW `b=0.2824`, `p=1.06e-11` and Steiger `TRUE` (`p=9.34e-109`). Several Windows R calls returned a nonzero wrapper status after their asserted output was fully materialized; the evidence above judges parsed, checked artifacts rather than exit status alone.

## Gates and static review

| Gate | Result | Evidence |
|---|---|---|
| T1 Operational stability | PASS | All shipped files parse; current workflow, examples, and all four current CLI scripts materialized checked output. Two isolated platform-wrapper terminations are disclosed and do not correspond to a source crash after the completed shipped example. |
| T2 Contract | PASS | Required frontmatter is present; 19-file source tree, references, scripts, and documented calls resolve. |
| T3 Determinism | PASS | Stochastic demonstrations seed MR-PRESSO and example simulations; current script-level SIMEX test supplied its documented optional seed. |
| T4 Security | PASS | No raw-string evaluation, credentials, destructive action, or patient-data workflow is present. |
| M1 Scientific integrity | PASS | All reported numeric values come from the named fresh runs; synthetic fixtures state their planted truth. |
| M2 Practice boundaries | PASS | Input 6 declined individual diagnosis/treatment and offered only a population-level alternative. |
| M3 Methodological ground | PASS | The overlap, weak-IV, NOME, MVMR, colocalization, and correlated-pleiotropy checks execute or have explicit scope/threshold caveats. |
| M4 Code usability | PASS | All eight shipped R files parse; all executable scripts and examples have fresh checked output. |

Static score: **94/100**. Strong progressive disclosure, runnable scripts, explicit thresholds, escape hatches, and current local-clumping instructions are offset slightly by long Monte-Carlo steps and the CLI MVMR script’s lack of a machine-readable F<10 warning.

## Recommendations

- **P2 — Emit a structured weak-instrument warning from the MVMR CLI.** `input14` prints conditional F below 10 but lets the command finish with no explicit warning. After computing `condF`, emit a clear warning (or structured status) for `1 <= F < 10`, while retaining the current hard stop below 1.

- **P2 — Make SIMEX reproducible by default.** `simex_egger.R` documents `--seed` but leaves it unset by default. Default to a fixed seed or print an explicit reproducibility warning when it is omitted.

## Score calculation

`static 94 × 0.4 = 37.6`; `dynamic 92.8 × 0.6 = 55.7`; total `93.3`, rounded **93**. Production floors all pass: static ≥80, dynamic ≥85, Layer 1 average 37.3/40, Layer 2 average 55.5/60, assertions 96.7%, no veto, no P0.
