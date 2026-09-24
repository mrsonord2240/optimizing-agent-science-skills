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
echo "== shipped examples/rare_variant_test.sh (verbatim, post-fix signature: array prefix for step 1, exome prefix for step 2) =="
bash rare_variant_test.fork_copy.sh geno_array geno_wes pheno.txt covar.txt annot.txt sets.txt masks.txt ex_out > example.log 2>&1
echo "example exit=$?"; tail -3 example.log; ls ex_out 2>/dev/null
