#!/bin/bash
# Input 5 (Stress): "End to end: split by type, apply site filters, merge, null bad genotypes, drop an exclusion
# BED, then validate with Ti/Tv, known%, and FILTER counts before/after." SYNTHETIC data (a 35-kb toy genome,
# so expected WGS/WES Ti/Tv ranges do not apply; the simulation used Ti:Tv 2:1 for true sites, 1:2 for artifacts).
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
bcftools view -v snps cohort.vcf.gz -Oz -o s.vcf.gz; bcftools view -v indels cohort.vcf.gz -Oz -o i.vcf.gz
bcftools filter -i 'QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=60.0||INFO/FS=".") && (INFO/MQ>=40.0||INFO/MQ=".") && (INFO/MQRankSum>=-12.5||INFO/MQRankSum=".") && (INFO/ReadPosRankSum>=-8.0||INFO/ReadPosRankSum=".") && (INFO/SOR<=3.0||INFO/SOR=".")' s.vcf.gz -Oz -o sf.vcf.gz
bcftools filter -i 'QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=200.0||INFO/FS=".") && (INFO/ReadPosRankSum>=-20.0||INFO/ReadPosRankSum=".") && (INFO/SOR<=10.0||INFO/SOR=".")' i.vcf.gz -Oz -o if.vcf.gz
for f in sf if; do bcftools index -f $f.vcf.gz; done
bcftools concat -a sf.vcf.gz if.vcf.gz -Oz -o sites.vcf.gz 2>/dev/null; bcftools index -f sites.vcf.gz
bcftools filter -S . -e 'FMT/GQ<20 | FMT/DP<8' sites.vcf.gz -Oz -o final.vcf.gz; bcftools index -f final.vcf.gz
printf 'chr2\t0\t1000\n' > exclude.bed
bcftools view -T ^exclude.bed final.vcf.gz -Oz -o final_excl.vcf.gz; echo "exclusion view exit=$?"
echo "records in excluded interval before: $(bcftools view -H -r chr2:1-1000 final.vcf.gz | wc -l)"
for f in cohort sites final_excl; do
  tstv=$(bcftools stats $f.vcf.gz | grep '^TSTV' | cut -f5 | tr -d '\r')
  known=$(bcftools view -H $f.vcf.gz | awk '{n++; if($3!=".") k++} END{printf "%.1f", 100*k/n}')
  echo "$f: records=$(bcftools view -H $f.vcf.gz | wc -l) Ti/Tv=$tstv known%=$known"
done
bcftools query -f '%CHROM\t%POS\n' final_excl.vcf.gz | tr -d '\r' > kept.tsv; $PY ../../data/score_truth.py kept.tsv "final:"
echo "== SKILL.md validation idiom: bcftools stats | grep ^TSTV prints: =="; bcftools stats final_excl.vcf.gz | grep '^TSTV'
echo "== usage-guide allele-balance expression (post-fix, verbatim) =="
bcftools filter -i 'GT="het" & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) > 0.2 & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) < 0.8' final.vcf.gz -o ab_filtered.vcf 2> ab.err; echo "AB filter exit=$?"; head -3 ab.err
echo "AB-filtered records: $(grep -vc '^#' ab_filtered.vcf 2>/dev/null)"
