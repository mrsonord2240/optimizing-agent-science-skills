> **Audit record for `bio-population-genetics-rare-variant-association`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/population-genetics/rare-variant-association) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-population-genetics-rare-variant-association
Generated: 2026-09-15 · Auditor: variant-annotation-curation-analyst round-2 audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:population-genetics/rare-variant-association`  
Category: Data Analysis · Mode A · Complexity: Moderate → N = 5. Three engines (regenie, SAIGE-GENE+, SKAT) with test and mask selection; 3 files.

Environment and data: Mode A. WSL agents distro via tar hand-over: plink2 v2.0.0-a.6.9, regenie 4.1.3 and r-saige 1.3.1 (bioconda; tbb<2021 pinned so SAIGE.so loads); Windows R 4.4.3 with SKAT 2.2.5 in the candidate R library. Data SYNTHETIC (data/make_rv_data.py, seed 20260915): 2,000 unrelated samples, 180 cases, covariates age/sex/PC1/PC2, 1,200 common array SNPs on 3 chromosomes, 30 genes with 462 rare variants (LoF/missense/synonymous); planted G01 burden (LoF+missense risk), G11 mixed-direction missense, G21 LoF-only; 27 null genes. STAAR was not run (text only).

## Step 1 — Skill Veto
T1 stability PASS (instruction Skill, deterministic tools), T2 contract PASS (frontmatter name/description present), T3 determinism PASS (no stochastic steps without seeds), T4 security PASS (no eval/exec of user strings, no credentials).

## Step 2 — Static score: 84/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | Test-selection logic (burden vs SKAT vs SKAT-O, mask as hypothesis, SPA/Firth, per-gene-per-mask burden) is correct, and the SKAT R block ran verbatim. Defects found by running it: the SKILL.md regenie step-1 block has no --bt and stops on a binary trait ("very few unique values"); regenie adds an "all" mask, not the "implicit singleton mask" the version block describes; the SAIGE-GENE+ --annotation_in_groupTest string has its separators reversed (SAIGE: comma separates tests, semicolon joins annotations), so "lof;lof,missense;lof,missense,synonymous" runs lof, missense+lof, missense-only and synonymous-only instead of the three nested masks; the printed step-2 command uses --bgenFile without the --bgenFileIndex/--sampleFile it needs. |
| Reliability | 9/12 | Common Errors covers skat-o spelling (confirmed: "unrecognized VC test: 'skat-o'"), missing burden files and Firth/SPA; it misses the step-1 --bt omission and the reversed SAIGE separators. |
| Performance context | 7/8 | 197-line SKILL.md; decision tables compact. |
| Agent usability | 13/16 | Clear mechanism-first framing; the in-code comment describing SAIGE group syntax contradicts the tool and would mislead an agent. |
| Human usability | 7/8 | Usage-guide prompts map to the decision tree. |
| Security | 11/12 | Local files; no credentials. |
| Maintainability | 8/12 | Shipped example reuses one genotype prefix for step 1 and step 2 and fails on a rare-variant-only set; no test data. |
| Agent specific | 19/20 | Precise scope with explicit routing to association-testing, variant-annotation and clinical-databases/variant-prioritization. |

Shipped-means-present (gate 8): SKILL.md cross-references other Skills only; usage-guide.md and examples/rare_variant_test.sh exist. PASS (the example fails at step 1 on a rare-variant-only genotype set, see P1).

Research scope (gate 7): Cohort-level gene tests; no individual-level content. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 32 | 47 | 79 | 2/4 | yes | ✅ |
| 2 | Variant A | 38 | 55 | 93 | 4/4 | yes | ✅ |
| 3 | Edge | 38 | 55 | 93 | 4/4 | yes | ✅ |
| 4 | Variant B | 30 | 44 | 74 | 2/4 | yes | ⚠️ |
| 5 | Stress | 35 | 51 | 86 | 3/4 | yes | ✅ |

**Execution Average: 85.0 / 100** · **Assertion Pass Rate: 15/20 (75 %)** · Layer 1 avg 34.6 · Layer 2 avg 50.4

Research Veto: scientific integrity PASS; practice boundaries PASS; methodological ground PASS; code usability PASS.  
**Final: 84 × 0.4 + 85.0 × 0.6 = 33.6 + 51.0 = 85 → ✅ Limited Release** (Production Ready floor not met (assertions): downgraded one tier)

## Detailed Outputs

### Input 1 — Canonical: regenie masks with SKAT-O and ACAT-O
**Prompt:** "Run gene-based rare-variant tests on our exome cohort (2,000 samples, ~9 % cases): LoF and LoF+missense masks at AAF 0.001 and 0.01, burden plus SKAT-O and ACAT-O, with Firth for the imbalanced binary trait."

**Executed:** yes — runs/in1/run.sh in WSL (plink2, regenie 4.1.3); shipped example run from an upstream byte copy.

Code (`runs/in1/run.sh`):
```bash
#!/bin/bash
# Input 1 (Canonical): "Run gene-based rare-variant tests on our exome cohort (2000 samples, ~9% cases):
# LoF and LoF+missense masks at AAF 0.001 and 0.01, burden plus SKAT-O and ACAT-O, Firth for the imbalanced
# binary trait." SYNTHETIC data (data/make_rv_data.py): planted G01 burden, G11 mixed-direction, G21 LoF-only.
# Runs in WSL: plink2 v2.0.0-a.6.9, regenie 4.1.3 (bioconda).
set -uo pipefail
export PATH=/tmp/vaca/env/bin:$PATH
D=../../data
regenie --version 2>&1 | head -1
plink2 --vcf $D/array.vcf --double-id --make-bed --out geno_array --silent; plink2 --vcf $D/wes.vcf --double-id --make-bed --out geno_wes --silent
echo "array SNPs $(wc -l < geno_array.bim); WES variants $(wc -l < geno_wes.bim); samples $(wc -l < geno_wes.fam)"
cp $D/pheno.txt $D/covar.txt $D/annot.txt $D/sets.txt $D/masks.txt .
echo "== check-burden-files (SKILL.md) =="
regenie --step 2 --bed geno_wes --phenoFile pheno.txt --covarFile covar.txt --anno-file annot.txt --set-list sets.txt \
    --mask-def masks.txt --aaf-bins 0.001,0.01 --build-mask max --check-burden-files --ignore-pred --bt --out check > check.log 2>&1
echo "exit=$?"; ls check* ; head -5 check_masks_report.txt 2>/dev/null
echo "== step 1 (SKILL.md: geno_array) =="
regenie --step 1 --bed geno_array --phenoFile pheno.txt --covarFile covar.txt --bsize 1000 --lowmem --out fit_null > step1_nobt.log 2>&1
echo "SKILL.md step-1 block as printed (no --bt): exit=$?"; grep -iE "error|binary|quantitative" step1_nobt.log | head -3
regenie --step 1 --bed geno_array --phenoFile pheno.txt --covarFile covar.txt --bsize 1000 --bt --lowmem --lowmem-prefix tmp_rg --out fit_null_bt > step1.log 2>&1
echo "step 1 with --bt exit=$?"
echo "== step 2 (SKILL.md block, --pred from the --bt null) =="
regenie --step 2 --bed geno_wes --phenoFile pheno.txt --covarFile covar.txt \
    --pred fit_null_bt_pred.list --anno-file annot.txt --set-list sets.txt --mask-def masks.txt \
    --aaf-bins 0.001,0.01 --vc-tests skato,acato --build-mask max \
    --bt --firth --approx --pThresh 0.05 --out gene_tests > step2.log 2>&1
echo "exit=$?"; ls gene_tests*
F=$(ls gene_tests_*.regenie | head -1)
echo "tests present: $(awk 'NR>1 && $1!~/^#/{print $8}' $F | sort | uniq -c | tr '\n' ' ')"
echo "masks x bins per gene: $(awk 'NR>1 && $1!~/^#/ && $3~/^G01\./{print $3}' $F | sort -u | tr '\n' ' ')"
echo "== top 12 tests by LOG10P =="
awk 'NR>1 && $1!~/^#/ {print $3, $8, $12}' $F | sort -k3,3gr | head -12
echo "== best LOG10P per planted gene =="
for g in G01 G11 G21; do awk -v g=$g 'NR>1 && $3~"^"g"\\." {print $3, $8, $12}' $F | sort -k3,3gr | head -3; done
echo "== null genes: tests with LOG10P > 2.0 / total =="
awk 'NR>1 && $1!~/^#/ && $3!~/^G01\.|^G11\.|^G21\./ {n++; if($12>2) k++} END{print k+0" / "n}' $F
echo "== shipped examples/rare_variant_test.sh (verbatim, same genotype prefix for step 1 and 2 as the script requires) =="
bash rare_variant_test.upstream_copy.sh geno_wes pheno.txt covar.txt annot.txt sets.txt masks.txt ex_out > example.log 2>&1
echo "example exit=$?"; tail -3 example.log; ls ex_out 2>/dev/null
```
Printed (`runs/in1/out.txt`, trimmed):
```
v4.1.3.gz
array SNPs 1200; WES variants 462; samples 2000
== check-burden-files (SKILL.md) ==
exit=0
check.log
check_Y.regenie
check_masks_report.txt
## mask file: [masks.txt]
## list of unknown annnotations in mask file
->Detected 0 masks with unknown annotations.
->Detected 0 masks with only unknown annotations.
== step 1 (SKILL.md: geno_array) ==
SKILL.md step-1 block as printed (no --bt): exit=1
ERROR: phenotype 'Y' has very few unique values (=2). If you really want to analyze it as a QT, use `--force-qt`.
step 1 with --bt exit=0
== step 2 (SKILL.md block, --pred from the --bt null) ==
exit=0
gene_tests.log
gene_tests_Y.regenie
tests present:     139 ADD      58 ADD-ACATO      58 ADD-ACATV      58 ADD-SKAT      58 ADD-SKATO       1 TEST 
masks x bins per gene: G01.Mask_LoF.0.01 G01.Mask_LoF.all G01.Mask_LoF_mis.0.001 G01.Mask_LoF_mis.0.01 G01.Mask_LoF_mis.all 
== top 12 tests by LOG10P ==
G21.Mask_LoF.all ADD-SKATO 7.93299
G21.Mask_LoF.all ADD-ACATO 7.61034
G21.Mask_LoF.0.01 ADD 7.56361
G21.Mask_LoF.all ADD 7.56361
G21.Mask_LoF.all ADD-SKAT 6.40461
G21.Mask_LoF_mis.all ADD-SKAT 5.69569
G21.Mask_LoF_mis.all ADD-ACATO 5.30393
G21.Mask_LoF_mis.all ADD-SKATO 5.19522
G21.Mask_LoF.all ADD-ACATV 4.13486
G01.Mask_LoF_mis.all ADD-ACATO 4.00725
G01.Mask_LoF_mis.0.01 ADD 3.97368
G01.Mask_LoF_mis.all ADD 3.97368
== best LOG10P per planted gene ==
G01.Mask_LoF_mis.all ADD-ACATO 4.00725
G01.Mask_LoF_mis.0.01 ADD 3.97368
G01.Mask_LoF_mis.all ADD 3.97368
G11.Mask_LoF_mis.all ADD-SKAT 2.30316
G11.Mask_LoF_mis.all ADD-ACATV 2.22512
G11.Mask_LoF_mis.all ADD-ACATO 2.10812
G21.Mask_LoF.all ADD-SKATO 7.93299
G21.Mask_LoF.all ADD-ACATO 7.61034
G21.Mask_LoF.0.01 ADD 7.56361
== null genes: tests with LOG10P > 2.0 / total ==
3 / 334
== shipped examples/rare_variant_test.sh (verbatim, same genotype prefix for step 1 and 2 as the script requires) ==
example exit=1
Chromosome 1
 block [1] : 153 snps  (16ms) 
   -residualizing and scaling genotypes...ERROR: !! Uh-oh, SNP 1:5000247:G:T has low variance (=0.000000).
check.log
check_Y.regenie
check_masks_report.txt
fit_null.log
... (2 more lines in out.txt)
```

**Output (agent answer, Mode A):** Ran --check-burden-files, then step 1 on the array SNPs with --bt added (the Skill's step-1 block omits it and regenie refuses a binary phenotype without it), then step 2 with both masks, AAF bins 0.001/0.01, SKAT-O and ACAT-O and Firth. G21 is significant under the LoF-only mask (ACAT-O 2.5e-8), G01 under LoF+missense (ACAT-O 9.8e-5), and G11 shows a SKAT-only signal (5e-3) suggesting mixed effect directions. Reported the mask with every p-value and noted regenie's extra mask is "all", not a singleton mask. The shipped script needs a common-variant genotype set for step 1.

**Scores:** Basic 32/40 | Specialized 47/60 | Total 79/100 · **Assertions 2/4**
- [PASS] Mask inputs validated before testing — --check-burden-files, 0 unknown annotations
- [FAIL] SKILL.md step-1 block runs for the binary trait — needs --bt
- [PASS] Planted genes recovered with calibrated nulls — G21/G01 top; null 3/334 above LOG10P 2
- [FAIL] Shipped example script runs — step 1 on rare variants: low variance error

### Input 2 — Variant A: SKAT, burden and SKAT-O in R
**Prompt:** "Small case-control cohort: fit a SKAT null model on covariates and report burden, SKAT and SKAT-O p-values per gene with Beta(1,25) MAF weighting."

**Executed:** yes — runs/in2/run.sh (Windows R 4.4.3, SKAT 2.2.5); SKILL.md block verbatim inside a per-gene loop.

Code (`runs/in2/skat.R`):
```r
# Input 2 (Variant A): "Small case-control cohort: fit a SKAT null model on covariates and report burden, SKAT
# and SKAT-O p-values per gene with Beta(1,25) MAF weighting." SYNTHETIC data (data/make_rv_data.py).
# SKILL.md block verbatim inside the loop; only data loading is added.
suppressMessages(library(SKAT))
cat("SKAT", as.character(packageVersion("SKAT")), "\n")
covar_df <- read.delim("../../data/covar_skat.tsv")
covar_df$phenotype <- covar_df$Y
cat("n =", nrow(covar_df), " cases =", sum(covar_df$phenotype), "\n")

# Null model on covariates only (out_type='D' binary, 'C' continuous). Refit once, reuse per gene.
obj <- SKAT_Null_Model(phenotype ~ age + sex + PC1 + PC2, out_type = 'D', data = covar_df)

genes <- sprintf("G%02d", 1:30)
res <- data.frame()
for (g in genes) {
  Z <- as.matrix(read.delim(sprintf("../../data/gene_%s.tsv", g), check.names = FALSE))
  skato <- SKAT(Z, obj, method = 'SKATO', weights.beta = c(1, 25))
  burden <- SKAT(Z, obj, r.corr = 1, weights.beta = c(1, 25))
  skat <- SKAT(Z, obj, weights.beta = c(1, 25))
  p <- c(skato = skato$p.value, burden = burden$p.value, skat = skat$p.value)
  res <- rbind(res, data.frame(gene = g, n_var = ncol(Z), skato = p[["skato"]], burden = p[["burden"]], skat = p[["skat"]]))
}
res$min_p <- pmin(res$skato, res$burden, res$skat)
print(format(res[order(res$min_p), ], digits = 3), row.names = FALSE)
cat("\nBonferroni over 30 genes x 3 tests: 0.05/90 =", signif(0.05 / 90, 3), "\n")
cat("null genes with any p < 0.05:", sum(res$min_p[!res$gene %in% c("G01", "G11", "G21")] < 0.05), "of 27\n")
write.table(res, "skat_results.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
```
Printed (`runs/in2/out.txt`, trimmed):
```
SKAT 2.2.5 
n = 2000  cases = 180 
There were 21 warnings (use warnings() to see them)
 gene n_var    skato   burden     skat    min_p
  G21    16 1.74e-06 0.024898 4.58e-07 4.58e-07
  G01    14 9.47e-06 0.000146 9.93e-06 9.47e-06
  G11    14 6.15e-03 0.044321 3.35e-03 3.35e-03
  G03    11 2.13e-02 0.315864 1.09e-02 1.09e-02
  G19    18 2.44e-02 0.445015 1.24e-02 1.24e-02
  G06    22 1.36e-01 0.074312 8.58e-01 7.43e-02
  G30    10 2.22e-01 0.215504 1.32e-01 1.32e-01
  G25    21 2.51e-01 0.144209 8.90e-01 1.44e-01
  G10    18 3.14e-01 0.537047 1.86e-01 1.86e-01
  G29    22 3.40e-01 0.200929 5.83e-01 2.01e-01
  G08    13 3.64e-01 0.940972 2.21e-01 2.21e-01
  G14    13 3.75e-01 0.973115 2.29e-01 2.29e-01
  G09    19 5.07e-01 0.738806 3.20e-01 3.20e-01
  G22    15 5.14e-01 0.329119 5.70e-01 3.29e-01
  G28    20 5.92e-01 0.654764 3.90e-01 3.90e-01
  G04    11 6.15e-01 0.407707 9.73e-01 4.08e-01
  G15    19 6.47e-01 0.793223 4.33e-01 4.33e-01
  G16    11 6.67e-01 0.548906 4.59e-01 4.59e-01
  G05    11 6.87e-01 0.768587 4.78e-01 4.78e-01
  G20    11 7.39e-01 0.525380 8.82e-01 5.25e-01
  G23    21 7.62e-01 0.723059 5.42e-01 5.42e-01
  G18    11 7.59e-01 0.553241 8.16e-01 5.53e-01
  G27    14 8.04e-01 0.890890 5.92e-01 5.92e-01
  G07    17 8.28e-01 0.964640 6.24e-01 6.24e-01
  G02    17 8.42e-01 0.778143 6.38e-01 6.38e-01
  G17    16 8.66e-01 0.675180 7.91e-01 6.75e-01
  G24    12 1.00e+00 0.787268 9.88e-01 7.87e-01
  G26    13 1.00e+00 0.799278 7.95e-01 7.95e-01
  G12    21 1.00e+00 0.962038 8.05e-01 8.05e-01
  G13    11 1.00e+00 0.846130 8.30e-01 8.30e-01
Bonferroni over 30 genes x 3 tests: 0.05/90 = 0.000556 
null genes with any p < 0.05: 2 of 27
```

**Output (agent answer, Mode A):** Fitted SKAT_Null_Model on age, sex, PC1, PC2 once and ran burden (r.corr=1), SKAT and SKAT-O with Beta(1,25) weights for all 30 genes. G21 and G01 pass the 30-gene x 3-test Bonferroni threshold; G11 is nominal with SKAT much stronger than burden, the pattern expected for mixed directions. Suggested reporting SKAT-O as the primary test and the burden/SKAT contrast as architecture evidence.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100 · **Assertions 4/4**
- [PASS] SKILL.md SKAT block runs as written — SKAT 2.2.5
- [PASS] SKAT-O selected via method="SKATO"; burden via r.corr=1 — three distinct p-values per gene
- [PASS] Planted genes rank first — G21, G01, G11
- [PASS] Multiple-testing threshold stated for genes x tests — 5.6e-4

### Input 3 — Edge: Mixed directions and LoF-only architecture
**Prompt:** "In G11 we expect both gain- and loss-of-function missense variants, and in G21 only the truncating variants should matter. Burden or SKAT? And which mask?"

**Executed:** yes — runs/in3/run.sh (Windows R, SKAT 2.2.5) over LoF, LoF+missense and LoF+missense+synonymous masks.

Code (`runs/in3/skat_masks.R`):
```r
# Input 3 (Edge): "In G11 we expect both gain- and loss-of-function missense variants, and in G21 only the
# truncating variants should matter. Burden or SKAT? And which mask?" SYNTHETIC data.
suppressMessages(library(SKAT))
covar_df <- read.delim("../../data/covar_skat.tsv"); covar_df$phenotype <- covar_df$Y
obj <- SKAT_Null_Model(phenotype ~ age + sex + PC1 + PC2, out_type = 'D', data = covar_df)
run3 <- function(Z) {
  c(burden = SKAT(Z, obj, r.corr = 1, weights.beta = c(1, 25))$p.value,
    skat = SKAT(Z, obj, weights.beta = c(1, 25))$p.value,
    skato = SKAT(Z, obj, method = 'SKATO', weights.beta = c(1, 25))$p.value)
}
masked <- function(g, keep) {
  Z <- as.matrix(read.delim(sprintf("../../data/gene_%s.tsv", g), check.names = FALSE))
  anno <- sub(".*\\|", "", colnames(Z))
  Z[, anno %in% keep, drop = FALSE]
}
for (g in c("G11", "G21", "G01")) {
  for (m in list(c("LoF"), c("LoF", "missense"), c("LoF", "missense", "synonymous"))) {
    Z <- masked(g, m)
    p <- run3(Z)
    cat(sprintf("%s mask=%-26s nvar=%2d burden=%.2e skat=%.2e skato=%.2e\n", g, paste(m, collapse = "+"), ncol(Z), p[1], p[2], p[3]))
  }
}
# per-variant direction in G11 missense (marginal log-OR sign from carrier case fraction)
Z <- masked("G11", "missense")
y <- covar_df$phenotype
cat("\nG11 missense carriers: case fraction per variant (overall", round(mean(y), 3), ")\n")
print(round(apply(Z, 2, function(z) if (sum(z > 0) > 0) mean(y[z > 0]) else NA), 3))
```
Printed (`runs/in3/out.txt`, trimmed):
```
G11 mask=LoF                        nvar= 3 burden=5.71e-01 skat=6.49e-01 skato=7.10e-01
G11 mask=LoF+missense               nvar=12 burden=5.38e-02 skat=2.52e-03 skato=4.94e-03
G11 mask=LoF+missense+synonymous    nvar=14 burden=4.43e-02 skat=3.35e-03 skato=6.15e-03
G21 mask=LoF                        nvar= 3 burden=3.19e-14 skat=2.40e-11 skato=2.24e-13
G21 mask=LoF+missense               nvar=14 burden=2.51e-03 skat=2.71e-07 skato=1.43e-06
G21 mask=LoF+missense+synonymous    nvar=16 burden=2.49e-02 skat=4.58e-07 skato=1.74e-06
G01 mask=LoF                        nvar= 4 burden=1.07e-01 skat=2.51e-01 skato=1.73e-01
G01 mask=LoF+missense               nvar=11 burden=5.56e-06 skat=1.21e-07 skato=4.38e-08
G01 mask=LoF+missense+synonymous    nvar=14 burden=1.46e-04 skat=9.93e-06 skato=9.47e-06
Warning messages:
1: 2 SNPs with either high missing rates or no-variation are excluded! 
2: 2 SNPs with either high missing rates or no-variation are excluded! 
3: 2 SNPs with either high missing rates or no-variation are excluded! 
4: 2 SNPs with either high missing rates or no-variation are excluded! 
5: 2 SNPs with either high missing rates or no-variation are excluded! 
6: 2 SNPs with either high missing rates or no-variation are excluded! 
G11 missense carriers: case fraction per variant (overall 0.09 )
2:5000019:T:G|missense 2:5000041:G:C|missense 2:5000072:G:A|missense 
                 0.214                  0.038                  0.167 
2:5000097:C:T|missense 2:5000140:A:T|missense 2:5000155:G:C|missense 
                 0.000                  0.308                  0.000 
2:5000195:T:G|missense 2:5000230:A:C|missense 2:5000244:A:T|missense 
                 0.333                  0.000                  0.417 
```

**Output (agent answer, Mode A):** For G11 use SKAT or SKAT-O: the carriers of different missense variants sit both above and below the baseline case rate, so a burden score cancels (0.054 vs SKAT 0.0025). For G21 use a LoF-only burden mask: adding missense variants dilutes the signal by 11 orders of magnitude. Recommended testing a small mask grid and combining with ACAT-O, counting masks in the multiple-testing burden.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100 · **Assertions 4/4**
- [PASS] Burden cancels under mixed directions, as the Skill states — G11 burden 0.054 vs SKAT 0.0025
- [PASS] Mask choice changes the answer, as the Skill states — G21 LoF 3e-14 vs LoF+mis 2.5e-3
- [PASS] Recommends SKAT/SKAT-O for mixed directions and burden for a single-direction mask — decision tree applied
- [PASS] Masks counted in the multiple-testing burden — stated

### Input 4 — Variant B: SAIGE-GENE+ for an imbalanced trait
**Prompt:** "Case:control is ~1:10 and we suspect cryptic relatedness. Set up SAIGE-GENE+ across MAF cutoffs 0.0001, 0.001 and 0.01 with lof / lof+missense / lof+missense+synonymous groups."

**Executed:** yes — runs/in4/run.sh in WSL (r-saige 1.3.1): step 1 with SAIGE-documented flags (the Skill gives none for GENE+), the SKILL.md step-2 command as printed, then the same flags with PLINK input.

Code (`runs/in4/run.sh`):
```bash
#!/bin/bash
# Input 4 (Variant B): "Case:control is ~1:10 and we suspect cryptic relatedness. Set up SAIGE-GENE+ across MAF
# cutoffs 0.0001, 0.001 and 0.01 with lof / lof+missense / lof+missense+synonymous groups."
# WSL: r-saige 1.3.1 (bioconda, tbb<2021 pinned so SAIGE.so loads) in /tmp/vaca/saige. SYNTHETIC data
# (unrelated by construction, so no sparse GRM is fitted; step 1 uses all array + WES markers).
set -uo pipefail
export PATH=/tmp/vaca/saige/bin:/tmp/vaca/env/bin:$PATH
D=../../data
plink2 --vcf $D/wes.vcf --double-id --make-bed --out geno_wes --silent
bgzip -c $D/array.vcf > a.vcf.gz; bgzip -c $D/wes.vcf > w.vcf.gz; bcftools index -f a.vcf.gz; bcftools index -f w.vcf.gz
bcftools concat -a a.vcf.gz w.vcf.gz -Oz -o all.vcf.gz 2>/dev/null
plink2 --vcf all.vcf.gz --double-id --make-bed --out geno_all --silent
echo "geno_all markers: $(wc -l < geno_all.bim); geno_wes markers: $(wc -l < geno_wes.bim)"
printf 'IID\tY\tage\tsex\tPC1\tPC2\n' > pheno_saige.txt
paste <(awk 'NR>1{print $2"\t"$3}' $D/pheno.txt) <(awk 'NR>1{print $3"\t"$4"\t"$5"\t"$6}' $D/covar.txt) >> pheno_saige.txt
head -2 pheno_saige.txt
# group file (SAIGE >=1.0 format): '<gene> var <ids...>' then '<gene> anno <labels...>', lowercase labels as in SKILL.md
awk '{lab=($3=="LoF")?"lof":$3; v[$2]=v[$2]" "$1; a[$2]=a[$2]" "lab; if(!($2 in seen)){order[++n]=$2; seen[$2]=1}} END{for(i=1;i<=n;i++){g=order[i]; print g" var"v[g]; print g" anno"a[g]}}' $D/annot.txt > groups.txt
head -2 groups.txt | cut -c1-110
Rscript -e 'suppressMessages(library(SAIGE)); cat("SAIGE", as.character(packageVersion("SAIGE")), "\n")'
echo "== step 1: null GLMM with categorical variance ratios (SAIGE docs; the Skill gives only the step-2 command) =="
step1_fitNULLGLMM.R --plinkFile=geno_all --phenoFile=pheno_saige.txt --phenoCol=Y --covarColList=age,sex,PC1,PC2 \
    --sampleIDColinphenoFile=IID --traitType=binary --isCateVarianceRatio=TRUE --outputPrefix=null \
    --nThreads=2 --IsOverwriteVarianceRatioFile=TRUE > step1.log 2>&1
echo "step1 exit=$?"; grep -iE "error|warning" step1.log | head -3; ls -la null.rda null.varianceRatio.txt 2>/dev/null | awk '{print $5, $9}'
echo "== step 2, SKILL.md command verbatim (bgen input as printed; only .bed exists) =="
step2_SPAtests.R --bgenFile geno_wes.bgen --groupFile groups.txt \
    --GMMATmodelFile null.rda --varianceRatioFile null.varianceRatio.txt \
    --annotation_in_groupTest "lof;lof,missense;lof,missense,synonymous" \
    --maxMAF_in_groupTest 0.0001,0.001,0.01 --is_output_moreDetails TRUE \
    --SAIGEOutputFile gene_tests_bgen.txt > step2_bgen.log 2>&1
echo "step2 as printed exit=$?"; grep -iE "error|bgenFileIndex|sampleFile" step2_bgen.log | head -3
echo "== step 2 with the Skill's flags, PLINK input =="
step2_SPAtests.R --bedFile=geno_wes.bed --bimFile=geno_wes.bim --famFile=geno_wes.fam --AlleleOrder=alt-first \
    --groupFile=groups.txt --GMMATmodelFile=null.rda --varianceRatioFile=null.varianceRatio.txt \
    --annotation_in_groupTest="lof;lof,missense;lof,missense,synonymous" \
    --maxMAF_in_groupTest=0.0001,0.001,0.01 --is_output_moreDetails=TRUE --LOCO=FALSE \
    --SAIGEOutputFile=gene_tests.txt > step2.log 2>&1
echo "step2 exit=$?"; grep -iE "error" step2.log | head -3
if [ -s gene_tests.txt ]; then
  echo "columns: $(head -1 gene_tests.txt | tr '\t' ' ')"
  echo "== Cauchy-combined rows, smallest p =="
  awk -F'\t' 'NR==1{for(i=1;i<=NF;i++) h[$i]=i; next} $h["Group"]=="Cauchy" {print $h["Region"], $h["max_MAF"], $h["Pvalue"]}' gene_tests.txt | sort -k3,3g | head -8
  echo "== planted genes, best rows =="
  for g in G01 G11 G21; do awk -F'\t' -v g=$g 'NR==1{for(i=1;i<=NF;i++) h[$i]=i; next} $h["Region"]==g {print $h["Region"], $h["Group"], $h["max_MAF"], $h["Pvalue"], $h["Pvalue_Burden"], $h["Pvalue_SKAT"]}' gene_tests...
  echo "null genes Cauchy p<0.05: $(awk -F'\t' 'NR==1{for(i=1;i<=NF;i++) h[$i]=i; next} $h["Group"]=="Cauchy" && $h["Region"]!~/^G(01|11|21)$/ && $h["Pvalue"]<0.05' gene_tests.txt | wc -l) of $(awk -F'\t' 'NR==1{for(i...
fi
```
Printed (`runs/in4/out.txt`, trimmed):
```
geno_all markers: 1662; geno_wes markers: 462
IID	Y	age	sex	PC1	PC2
SYN0001	0	45.19	1	-0.1292	0.3826
G01 var 1:5000017:C:T 1:5000050:G:A 1:5000071:A:C 1:5000107:T:A 1:5000137:G:C 1:5000153:G:C 1:5000181:G:T 1:50
G01 anno synonymous lof lof missense synonymous missense missense synonymous missense missense missense lof lo
SAIGE 1.3.1 
== step 1: null GLMM with categorical variance ratios (SAIGE docs; the Skill gives only the step-2 command) ==
step1 exit=0
WARNING: Genetic variants needs to be ordered by chromosome and position in the Plink file
WARNING: Genetic variants needs to be ordered by chromosome and position in the Plink file
WARNING: Genetic variants needs to be ordered by chromosome and position in the Plink file
1343206 null.rda
49 null.varianceRatio.txt
== step 2, SKILL.md command verbatim (bgen input as printed; only .bed exists) ==
step2 as printed exit=1
$bgenFileIndex
$sampleFile
$sampleFile_male
== step 2 with the Skill's flags, PLINK input ==
step2 exit=0
columns: Region Group max_MAF Pvalue Pvalue_Burden Pvalue_SKAT BETA_Burden SE_Burden MAC MAC_case MAC_control Number_rare Number_ultra_rare
== Cauchy-combined rows, smallest p ==
G21 NA 5.12646802786065e-08
G01 NA 7.18575911418107e-05
G19 NA 0.0187562024496324
G11 NA 0.0188195430845194
G15 NA 0.148676740668717
G10 NA 0.194147425253275
G14 NA 0.265099639010707
G09 NA 0.303405427005999
== planted genes, best rows ==
G01 missense 0.01 1.54557759090013e-05 4.98546044092052e-05 1.2386157019928e-05
G01 missense;lof 0.01 3.05714591324335e-05 1.99172443197115e-05 9.38150105584956e-05
G11 missense 0.01 0.00401410711624373 0.059342625650442 0.00195454509984094
G11 missense;lof 0.01 0.0127244466224411 0.058755278649802 0.00678734596047725
G21 lof;lof 0.01 7.89289433811291e-09 2.04265655501246e-08 2.35907554824166e-07
G21 Cauchy NA 5.12646802786065e-08 1.42980635331469e-07 3.36331008599089e-07
null genes Cauchy p<0.05: 1 of 27
rc=0
```

**Output (agent answer, Mode A):** Fitted the SAIGE null GLMM with categorical variance ratios, then ran step 2. Gave the group string in SAIGE's documented form, `--annotation_in_groupTest=lof,missense;lof,missense;lof;synonymous`, after the Skill's version produced a missense-only and a synonymous-only test instead of the nested masks, and added --bgenFileIndex/--sampleFile for bgen input. G21 and G01 are the associated genes; noted that relatedness would need a sparse GRM in step 1, which this unrelated synthetic cohort does not require.

**Scores:** Basic 30/40 | Specialized 44/60 | Total 74/100 · **Assertions 2/4**
- [FAIL] SKILL.md step-2 command runs as printed — bgen needs --bgenFileIndex/--sampleFile
- [FAIL] Annotation groups match the intended nested masks — separators reversed vs SAIGE help
- [PASS] Multiple MAF cutoffs parsed in one run — 0.0001/0.001/0.01 rows
- [PASS] Planted genes recovered with calibrated nulls — G21 5e-8, G01 7e-5; null 1/27

### Input 5 — Stress: Full scan, thresholds and flag checks
**Prompt:** "Scan all 30 genes with both masks and three MAF bins, combine with ACAT-O, and give me the exome-wide threshold that accounts for the masks. Also confirm the regenie flag spellings and defaults the Skill states before I put this in a pipeline."

**Executed:** yes — runs/in5/run.sh in WSL (regenie 4.1.3).

Code (`runs/in5/run.sh`):
```bash
#!/bin/bash
# Input 5 (Stress): "Scan all 30 genes with both masks and three MAF bins, combine with ACAT-O, and give me the
# exome-wide threshold that accounts for the masks. Also confirm the regenie flag spellings and defaults the
# Skill states before I put this in a pipeline." Runs in WSL (regenie 4.1.3). SYNTHETIC data.
set -uo pipefail
export PATH=/tmp/vaca/env/bin:$PATH
D=../../data
plink2 --vcf $D/array.vcf --double-id --make-bed --out geno_array --silent; plink2 --vcf $D/wes.vcf --double-id --make-bed --out geno_wes --silent
cp $D/pheno.txt $D/covar.txt $D/annot.txt $D/sets.txt $D/masks.txt .
echo "== flag claims in the Skill's version block =="
regenie --help 2>&1 | grep -E -- "--vc-tests|--build-mask|--vc-MACthr|--aaf-bins|--check-burden-files|--joint" | sed 's/^ *//' | cut -c1-140
regenie --step 1 --bed geno_array --phenoFile pheno.txt --covarFile covar.txt --bsize 1000 --bt --lowmem --lowmem-prefix tmp --out n > s1.log 2>&1
echo "step1 exit=$?"
regenie --step 2 --bed geno_wes --phenoFile pheno.txt --covarFile covar.txt --pred n_pred.list --anno-file annot.txt \
  --set-list sets.txt --mask-def masks.txt --aaf-bins 0.001,0.01 --vc-tests skat-o --bt --firth --approx --out bad > bad.log 2>&1
echo "--vc-tests skat-o exit=$?"; grep -iE "error|invalid|unrecogn" bad.log | head -2
regenie --step 2 --bed geno_wes --phenoFile pheno.txt --covarFile covar.txt --pred n_pred.list --anno-file annot.txt \
  --set-list sets.txt --mask-def masks.txt --aaf-bins 0.0001,0.001,0.01 --vc-tests skato,acato,acatv --bt --firth --approx --out scan > scan.log 2>&1
echo "scan exit=$?"
F=$(ls scan_*.regenie | head -1)
echo "total gene-level rows: $(awk 'NR>1 && $1!~/^#/' $F | wc -l); distinct masks: $(awk 'NR>1 && $1!~/^#/{split($3,a,"."); print a[2]"."a[3]"."a[4]}' $F | sort -u | tr '\n' ' ')"
echo "== rows per test =="; awk 'NR>1 && $1!~/^#/{print $8}' $F | sort | uniq -c
echo "== genes x masks Bonferroni: 30 genes x (2 masks x (3 bins + singleton)) burden tests =="
awk 'NR>1 && $1!~/^#/ && $8=="ADD" {n++} END{printf "burden tests=%d -> alpha=%.2e (-log10 %.2f)\n", n, 0.05/n, -log(0.05/n)/log(10)}' $F
awk 'NR>1 && $1!~/^#/ {n++} END{printf "all tests=%d -> alpha=%.2e (-log10 %.2f)\n", n, 0.05/n, -log(0.05/n)/log(10)}' $F
echo "== genes passing 30-gene ACAT-O-style threshold (0.05/30, -log10 2.78) on any ADD-ACATO row =="
awk 'NR>1 && $8=="ADD-ACATO" && $12>2.78 {print $3, $12}' $F
echo "== best row per planted gene =="
for g in G01 G11 G21; do awk -v g=$g 'NR>1 && $3~"^"g"\\." {print $3, $8, $12}' $F | sort -k3,3gr | head -2; done
echo "== genomic-control style check on null genes (median chi2 / 0.456) =="
awk 'NR>1 && $1!~/^#/ && $8=="ADD" && $3!~/^G01\.|^G11\.|^G21\./ && $11!="NA" {print $11}' $F | sort -g | awk '{a[NR]=$1} END{m=(NR%2)?a[(NR+1)/2]:(a[NR/2]+a[NR/2+1])/2; printf "n=%d median chi2=%.3f lambda=%.2f\n", N...
```
Printed (`runs/in5/out.txt`, trimmed):
```
== flag claims in the Skill's version block ==
--aaf-bins FLOAT,..,FLOAT
--build-mask STRING       rule to construct masks, can be 'max', 
--vc-tests STRING,..,STRING
--joint STRING            comma spearated list of joint tests to 
--check-burden-files      check annotation file, set list file and 
step1 exit=0
--vc-tests skat-o exit=1
ERROR: unrecognized VC test: 'skat-o' (accepted=skat/skato/skato-acat/acatv/acato)
scan exit=0
total gene-level rows: 372; distinct masks: .. Mask_LoF.0.001 Mask_LoF.0.01 Mask_LoF.all. Mask_LoF_mis.0.001 Mask_LoF_mis.0.01 Mask_LoF_mis.all. 
== rows per test ==
    139 ADD
     58 ADD-ACATO
     58 ADD-ACATV
     58 ADD-SKAT
     58 ADD-SKATO
      1 TEST
== genes x masks Bonferroni: 30 genes x (2 masks x (3 bins + singleton)) burden tests ==
burden tests=139 -> alpha=3.60e-04 (-log10 3.44)
all tests=372 -> alpha=1.34e-04 (-log10 3.87)
== genes passing 30-gene ACAT-O-style threshold (0.05/30, -log10 2.78) on any ADD-ACATO row ==
G01.Mask_LoF_mis.all 4.00725
G21.Mask_LoF.all 7.61034
G21.Mask_LoF_mis.all 5.30393
== best row per planted gene ==
G01.Mask_LoF_mis.all ADD-ACATO 4.00725
G01.Mask_LoF_mis.0.01 ADD 3.97368
G11.Mask_LoF_mis.all ADD-SKAT 2.30316
G11.Mask_LoF_mis.all ADD-ACATV 2.22512
G21.Mask_LoF.all ADD-SKATO 7.93299
G21.Mask_LoF.all ADD-ACATO 7.61034
== genomic-control style check on null genes (median chi2 / 0.456) ==
n=125 median chi2=0.472 lambda=1.04
rc=0
```

**Output (agent answer, Mode A):** Confirmed skato/acato spellings; corrected the Skill on masks: regenie adds an "all" mask, and a singleton mask needs --singleton-carrier. Recommended combining masks per gene with ACAT-O and using 0.05/30 = 1.7e-3 for 30 genes here (about 2.5e-6 exome-wide), or a Bonferroni over genes x masks (1.3e-4 for all 372 tests) if masks are reported separately. G21 and G01 pass either; null calibration is fine (lambda 1.04).

**Scores:** Basic 35/40 | Specialized 51/60 | Total 86/100 · **Assertions 3/4**
- [PASS] regenie token spelling claim is correct — skat-o rejected, skato accepted
- [FAIL] Mask construction described correctly (implicit singleton) — regenie builds "all", not singleton
- [PASS] Per-gene-per-mask threshold computed and explained — 1.3e-4 / 3.6e-4 / 1.7e-3
- [PASS] ACAT-O omnibus combines masks as described — ADD-ACATO rows per mask set

## Key strengths
- Mechanism-first test selection is correct and was borne out: burden cancelled for the mixed-direction gene and a LoF-only mask beat LoF+missense by 11 orders of magnitude
- SKAT R block runs verbatim and the regenie step-2 recipe recovers the planted genes with calibrated nulls
- Version traps that change results (skato token, SPA/Firth under imbalance, LOCO null) are called out

## Recommendations
- **[P1] SAIGE-GENE+ group syntax is reversed** (inputs [4]) — "lof;lof,missense;lof,missense,synonymous" makes SAIGE test lof, missense+lof, missense-only and synonymous-only, not the three nested masks; the comment describing the syntax is backwards. *Root cause:* Separator semantics not checked against step2_SPAtests.R --help (comma = tests, semicolon = annotations within a test). *Fix:* Use `--annotation_in_groupTest=lof,missense;lof,missense;lof;synonymous` and fix the comment.
- **[P1] regenie step-1 block omits --bt** (inputs [1]) — The SKILL.md step-1 command fails on a binary phenotype ("very few unique values"), while step 2 uses --bt. *Root cause:* Trait-type flag missing from step 1. *Fix:* Add --bt to step 1 whenever step 2 uses --bt, as the shipped example already does.
- **[P1] Shipped example runs step 1 on the rare-variant genotypes** (inputs [1]) — rare_variant_test.sh passes one genotype prefix to both steps; step 1 on a rare-variant set stops with a low-variance SNP error. *Root cause:* Step-1 and step-2 inputs conflated. *Fix:* Take separate array and exome prefixes (or filter step 1 to MAC/MAF-QC'd common variants).
- **[P2] regenie adds an "all" mask, not a singleton mask** (inputs [1, 5]) — The version block says --aaf-bins always adds an implicit singleton mask; regenie 4.1.3 emitted ".all" masks and no singleton mask. *Root cause:* Behaviour described from memory. *Fix:* Say that an all-variant mask is added and that singleton masks need --singleton-carrier.
- **[P2] SAIGE step-2 bgen command incomplete** (inputs [4]) — --bgenFile is shown without --bgenFileIndex and --sampleFile, which the tool requires. *Root cause:* Abbreviated command. *Fix:* Add both flags, or show the --bedFile/--bimFile/--famFile form.
