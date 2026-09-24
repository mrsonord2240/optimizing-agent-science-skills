> **Audit record for `bio-causal-genomics-genomic-sem`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5475243](https://github.com/mrsonord2240/bioSkills/tree/547524301ce5ee3cedf6cae70d5204e9c0d013f2/causal-genomics/genomic-sem) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-genomic-sem

## Canonical final summary

**Final:** 94/100 — ⭐ Production Ready; deployable: true.

Source: `mrsonord2240/bioSkills@547524301ce5ee3cedf6cae70d5204e9c0d013f2:causal-genomics/genomic-sem`
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

Generated: 2026-09-23. Source: `mrsonord2240/bioSkills@547524301ce5ee3cedf6cae70d5204e9c0d013f2:causal-genomics/genomic-sem` on `fix/causal-genomics-genomic-sem`.

This is the final-pass exception: `auditor_independent: false`; see `F:\OpenScience\audits\_final_pass\bio-causal-genomics-genomic-sem\CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed | Status |
|---|---:|---:|---:|---:|---:|---|---|
| 1 | Canonical CFA regression | 38 | 56 | 94 | 3/3 | true | ✅ |
| 2 | Q_SNP regression | 37 | 55 | 92 | 3/3 | true | ✅ |
| 3 | Heywood edge regression | 36 | 54 | 90 | 3/3 | true | ✅ |
| 4 | Two-factor regression | 38 | 56 | 94 | 3/3 | true | ✅ |
| 5 | userGWAS regression | 37 | 55 | 92 | 3/3 | true | ✅ |
| 6 | Scope boundary | 38 | 56 | 94 | 3/3 | true | ✅ |
| 7 | Two-trait adversarial case | 38 | 56 | 94 | 3/3 | true | ✅ |
| 8 | MAF/N Q_SNP regression | 37 | 55 | 92 | 3/3 | true | ✅ |
| 9 | p-factor stress regression | 35 | 53 | 88 | 3/3 | true | ✅ |
| 10 | Fresh extracted-helper run | 39 | 56 | 95 | 3/3 | true | ✅ |
| 11 | Fresh version-guard run | 38 | 56 | 94 | 3/3 | true | ✅ |

Execution average: **92.6/100**. Assertions: **33/33**. Static: **97/100**. Final: **94/100, Production Ready, deployable**. Both structural and research vetoes pass.

## What ran

`run/phase2_runner.sh` is the complete command record. It replayed all nine prior inputs with `r_gsem.sh`, then ran two fresh inputs. The R wrapper uses GenomicSEM 0.0.5 + lavaan 0.6.19. Inputs 1–5 and 7–10 printed their asserted results and then the local Windows R process returned 139; they are counted executed because the evidence output was checked, not because the exit code was trusted. The clean fixture, assertion, guard, and parse scripts exited 0.

`run/parse_all_shipped_code.py` fresh-checked all seven R fences, `examples/genomic_sem_commonfactor.R`, `scripts/commonfactor_gwas_qsnp.R`, and `examples/mtag_pipeline.sh`:

```text
PARSE_ALL_PASS r_fences=7 r_files=2 bash_files=1
```

## Detailed outputs

### Inputs 1–5 — prior executable regressions

Input 1 recovered planted common-factor loadings `0.75, 0.65, 0.70, 0.55` exactly under DWLS and ML, with CFI 1. Input 2 returned 20 Q_SNP rows: DWLS Q values were 0.9146–0.9308 for both factor and heterogeneous SNPs, while ML marked all five planted heterogeneous SNPs below `1e-4` and kept factor SNPs clean. This matches the shipped rule: DWLS is provisional and ML must cross-check it.

Input 3 detected two Heywood flags and a BMI standardized loading around 1.06. Input 4 exactly recovered six two-factor loadings and `rF=0.4000`. Input 5 recovered the planted `rs3` direct path as 0.1000 under DWLS; its ML attempt stopped with the distinct small-fixture singular-matrix error, not the old `ReorderModel` compatibility failure.

### Inputs 6–9 — boundaries and advanced-model regressions

Input 6 directly applied the Scope Boundary: decline individual PGS diagnosis, state population-summary-statistic scope, and redirect to a qualified clinician/genetic counselor. Input 7 rejected a two-trait factor with the documented `df=-1` message and supplied both remedies.

Input 8 supplied MAF/N-driven SEs (0.00637–0.01069). DWLS again did not discriminate heterogeneous SNPs, while ML did; the Skill now says exactly how to handle this. Input 9 showed the expected singular-information warning for a two-first-order-factor p model; the three-factor p model completed under DWLS and ML with CFI 1.

### Input 10 — fresh helper execution

`input10_prepare_helper_fixture.R` wrote a 20-SNP synthetic fixture. The shipped command was executed as documented:

```text
r_gsem.sh scripts/commonfactor_gwas_qsnp.R input10_covstruc.rds input10_snps.csv input10_helper_output.tsv 1
SNPs 20 | factor-significant 5 | factor-only (DWLS) 5 | factor-only (DWLS + ML) 4
```

`input10_assert_helper_output.R` exited 0 and asserted 20 unique rows, the six required result columns, finite DWLS/ML Q values, and logical factor-only columns.

### Input 11 — fresh version-guard execution

The exact bundled-example predicate was executed under both libraries:

```text
INPUT11 lavaan=0.6.19 should_warn=FALSE observed_warnings=0
INPUT11 lavaan=0.7.2 should_warn=TRUE observed_warnings=1
```

## Remaining issue

P1: LDSC, sumstats, stratified LDSC and enrich remain unexecuted because aligned multi-trait inputs, `eur_w_ld_chr`, 1000G MAF and baselineLD_v2.2 are not available locally. This does not invalidate the executable core paths or deployment floor, but the branches need a positive-control rerun when those resources are provisioned.

## Artifact map

- Report: `eval_report_bio-causal-genomics-genomic-sem_result.json`
- Fresh code and logs: `run/`
- Preserved previous report: `F:\OpenScience\audits\_pre-fix-20260923\bio-causal-genomics-genomic-sem\`
