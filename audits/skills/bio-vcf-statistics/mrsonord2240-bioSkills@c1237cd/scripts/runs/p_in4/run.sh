#!/bin/bash
# Input 4 (Variant B): "One sample may be contaminated. Use the VCF to check allele balance, het/hom and
# missingness per sample, and tell me what to do next." SYNTHETIC: SYN_S7 carries ~15% foreign reads,
# SYN_S6 is low coverage (25% of sites at DP 0-3).
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
echo "== SKILL.md quick het AB check (post-fix), verbatim =="
bcftools query -f '[%SAMPLE\t%GT\t%AD\n]' cohort.vcf.gz | \
    awk -F'\t' '($2=="0/1" || $2=="0|1") {split($3,a,","); d=a[1]+a[2]; if (d>0) {s[$1]+=a[2]/d; n[$1]++}}
        END {for (k in s) printf "%s\tmean het AB: %.3f (n=%d)\n", k, s[k]/n[k], n[k]}'   # expect ~0.5 per sample
echo "== per-sample het AB computed correctly (only het genotypes, per sample) =="
bcftools query -f '[%SAMPLE\t%GT\t%AD\n]' cohort.vcf.gz | tr -d '\r' | awk -F'\t' '$2=="0/1"{split($3,a,","); if(a[1]+a[2]>0){ab=a[2]/(a[1]+a[2]); s[$1]+=ab; n[$1]++; if(ab<0.2||ab>0.8) o[$1]++}} END{for(k in n) printf "%s n_het=%d mean_AB=%.3f frac_outside_0.2-0.8=%.3f\n",k,n[k],s[k]/n[k],o[k]/n[k]}' | sort
echo "== per-sample het/hom-alt and missing from bcftools stats -s - (PSC) =="
bcftools stats -s - cohort.vcf.gz | grep "^PSC" | awk -F'\t' '{printf "%s het/hom=%.2f nHets=%d missing=%d\n",$3,($5>0?$6/$5:0),$6,$14}'
echo "== vcftools --missing-indv in WSL (see out_wsl.txt) =="
