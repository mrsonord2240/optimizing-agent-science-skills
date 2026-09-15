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
awk 'NR>1 && $1!~/^#/ && $8=="ADD" && $3!~/^G01\.|^G11\.|^G21\./ && $11!="NA" {print $11}' $F | sort -g | awk '{a[NR]=$1} END{m=(NR%2)?a[(NR+1)/2]:(a[NR/2]+a[NR/2+1])/2; printf "n=%d median chi2=%.3f lambda=%.2f\n", NR, m, m/0.4549}'
