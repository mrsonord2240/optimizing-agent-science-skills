#!/bin/bash
# Input 3: three-caller set operations; normalize first (SKILL.md), -n+2 -w1, -C, shipped compare_vcfs.sh.
set -uo pipefail
F=../../data/ref.fa
bgzip -c ../../data/callerA.vcf > A.vcf.gz; bgzip -c ../../data/callerB.vcf | bcftools view -e 'POS==4000' -Oz -o B.vcf.gz
# caller C: A minus the frameshift, plus one private SNV, written right-shifted for the homopolymer deletion
bcftools view -e 'POS==1420 || POS==500' A.vcf.gz -Oz -o C0.vcf.gz
( bcftools view -h C0.vcf.gz; bcftools view -H C0.vcf.gz; printf 'chr1\t506\t.\tAA\tA\t200\tPASS\tDP=30\tGT:AD:DP:GQ\t0/1:14,12:26:99\n' ) | bcftools sort -Oz -o C.vcf.gz 2>/dev/null
for v in A B C; do bcftools index -f $v.vcf.gz; bcftools norm -m-any -f $F $v.vcf.gz -Oz -o $v.norm.vcf.gz 2>/dev/null; bcftools index -f $v.norm.vcf.gz; done
echo "raw   -n+2 (in >=2 callers): $(bcftools isec -n+2 -w1 A.vcf.gz B.vcf.gz C.vcf.gz 2>/dev/null | grep -vc '^#')"
echo "norm  -n+2 (in >=2 callers): $(bcftools isec -n+2 -w1 A.norm.vcf.gz B.norm.vcf.gz C.norm.vcf.gz | grep -vc '^#')"
echo "norm  -n=3 (all three):      $(bcftools isec -n=3 -w1 A.norm.vcf.gz B.norm.vcf.gz C.norm.vcf.gz | grep -vc '^#')"
echo "norm  -C  (A only):";  bcftools isec -C -w1 A.norm.vcf.gz B.norm.vcf.gz C.norm.vcf.gz | grep -v '^#' | cut -f1-5
echo "norm  -n~100 (A only, mask):"; bcftools isec -n~100 -w1 A.norm.vcf.gz B.norm.vcf.gz C.norm.vcf.gz | grep -v '^#' | cut -f1-5
echo "== shipped examples/compare_vcfs.sh on normalized A vs B =="
bash compare_vcfs.upstream_copy.sh A.norm.vcf.gz B.norm.vcf.gz cmp_out 2>&1 | sed -n '/Comparison Results/,$p'; echo "exit=$?"
