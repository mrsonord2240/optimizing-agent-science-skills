> **Audit record for `bio-causal-genomics-colocalization-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@9266ded](https://github.com/mrsonord2240/bioSkills/tree/9266dedec974cb14afb9dfddb6c0b36753d150ad/causal-genomics/colocalization-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-22 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-colocalization-analysis

Generated: 2026-09-22  
Source: `mrsonord2240/bioSkills@9266dedec974cb14afb9dfddb6c0b36753d150ad:causal-genomics/colocalization-analysis`  
Mode: D (Hybrid) | Category: Data Analysis | Complexity: Complex

`eval_report_*` and every prior `run/` artifact were moved before this audit to [the pre-fix archive](F:/OpenScience/audits/_pre-fix-20260922/bio-causal-genomics-colocalization-analysis/). This audit executed only a snapshot of the requested exact tip. `meta.auditor_independent` is deliberately `false`: final pass, as directed; see `F:\OpenScience\audits\_final_pass\bio-causal-genomics-colocalization-analysis\CHECKPOINT.md`.

## Result

**❌ Reject; 92/100 numeric score; deployable: false.** The Research Veto M3 fails on Input 10: `scripts/coloc_susie.R` does not test eQTL-to-LD consistency, so a measured eQTL `lambda=1.000000` still produces a PP.H4=1 output.

| Input | Purpose | Total | Assertions | Status |
|---|---|---:|---:|---|
| 1 | Legacy coloc.abf shared-causal regression | 97 | 5/5 | ✅ |
| 2 | Shipped single-signal SuSiE example | 98 | 5/5 | ✅ |
| 3 | Shipped multi-causal SuSiE example | 98 | 5/5 | ✅ |
| 4 | MHC/chr8 exclusion boundaries | 98 | 5/5 | ✅ |
| 5 | Real SMR + HEIDI controls | 95 | 4/5 | ✅ |
| 6 | Revised low-power PP.H3 condition | 96 | 5/5 | ✅ |
| 7 | Current strand-complement harmonisation | 98 | 5/5 | ✅ |
| 8 | New current coloc.abf CLI positive control | 98 | 5/5 | ✅ |
| 9 | New current coloc.susie CLI positive control | 98 | 5/5 | ✅ |
| 10 | New eQTL-only LD mismatch control | 31 | 2/5 | ❌ |

Execution average: **90.7/100**. Assertion rate: **46/50 (92.0%)**. Static score: **93/100**. Every score and assertion is recorded in the JSON report.

## Executed evidence

All runner and generator code is under [`run/`](F:/OpenScience/audits/bio-causal-genomics-colocalization-analysis/run/). `assert_phase2.py` checked output content, TSV parsing, and nonempty PDFs; it printed `ALL_ASSERTIONS_PASS` for the audit observations. `parse_all_r_sources.R` parsed all nine shipped R sources successfully.

### Inputs 1–4

```
Input 1: top PP.H4 SNP rs501; PP.H4 > 0.75 at 100/100 p12 points.
Input 2: GWAS/eQTL credible sets = 1/1; rs149 x rs149; PP.H4=1.000.
Input 3: GWAS/eQTL credible sets = 2/1; rs79 x rs79 PP.H4=1; rs198 x rs79 PP.H3=1.
Input 4: 9/9 MHC/chr8 boundary cases pass; hg19 and MHC pipeline cases stop.
```

### Inputs 5–7

```
SMR shared:  topSNP rs9025; p_SMR=4.58e-45; p_HEIDI=0.993; nsnp_HEIDI=9.
SMR linkage: topSNP rs9027; p_SMR=1.36e-08; p_HEIDI=9.08e-12; nsnp_HEIDI=9.
Low power: r2=0.505; N=150 PP.H1=0.943, PP.H3=0.0275; N=400 PP.H1=0.861.
Harmonise: rs1, rs2, rs3, rs4, rs6 retained; complement flip/same assertions all TRUE.
```

The SMR result exercises the actual SMR 1.3.1 and plink2 binaries. It correctly distinguishes the two planted scenarios, but `nsnp_HEIDI=9` falls one SNP below the Skill’s documented `>=10` reliability floor, so that assertion is marked fail rather than silently treated as high-confidence HEIDI evidence.

### Inputs 8–9 and supplementary examples

```
Input 8 current script: PP.H4=1; summary TSV, SNP TSV, and sensitivity PDF exist.
Input 9 current script: rs90 x rs90; PP.H4=1; summary TSV exists.
Supplementary coloc_analysis.R: PP.H4=0.9997 and top SNP rs508.
Supplementary regional_plots.R: regional_association.pdf, locuscompare.pdf, regional_ld.pdf all nonempty.
```

### Input 10 — failed scientific safeguard

The generator built eQTL statistics from an independent identity-LD genotype panel, then paired them with the Input 9 AR(1) LD matrix. The independent diagnostic measured `EQTL_LAMBDA_WITH_WRONG_LD=1.000000`, far over the documented `--lambda-max 0.05` stop threshold. The current wrapper did not compute this eQTL diagnostic:

```
running max iterations: 100
  converged: FALSE
Warning: IBSS algorithm did not converge ... check consistency between summary statistics and LD matrix
     hit1 hit2 PP.H3.abf PP.H4.abf
1:   rs90 rs90         0          1
```

The underlying library warned, but the shipped wrapper continued and emitted a decisive shared-causal result. This directly contradicts its documented LD-mismatch safety contract and fires M3.

## Gates and recommendations

- Skill Veto: PASS (stability, contract, determinism, security).
- Research Veto: M1 PASS, M2 PASS, **M3 FAIL**, M4 PASS.
- P0: add an eQTL `estimate_s_rss()`/`lambda-max` stop in `scripts/coloc_susie.R` and a shipped regression test.
- P1: independently execute moloc, eCAVIAR, PWCoCo, and HyPrColoc in a reproducible isolated environment.
- P1: investigate the recurring Windows wrapper exit 139 after fully materialized `coloc` output.

The source worktree remains unchanged at the requested commit.
