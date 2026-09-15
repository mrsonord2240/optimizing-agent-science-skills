#!/bin/bash
# Input 3 (edge): usage-guide "Rare Variant Analysis" recipe on a VCF that already carries its own INFO/AF.
set -uo pipefail
DATA=../../data
bgzip -c ../../data/gnomad_syn.vcf > gnomad_syn.vcf.gz; bcftools index -f gnomad_syn.vcf.gz
bgzip -c $DATA/callerA.vcf > in.vcf.gz; bcftools index -f in.vcf.gz
bcftools norm -f $DATA/ref.fa -m-any in.vcf.gz 2>/dev/null | bcftools +fill-tags -Oz -o cohort.vcf.gz -- -t AF; bcftools index -f cohort.vcf.gz
echo "== recipe as written (annotate | filter | csq) =="
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/AF cohort.vcf.gz | bcftools filter -i 'INFO/AF<0.01 || INFO/AF="."' | \
  bcftools csq -f $DATA/ref.fa -g $DATA/genes.gff3 -Oz -o rare_consequences.vcf.gz; echo "exit=${PIPESTATUS[*]}"
echo "== recipe steps on files (so the pipe is not the failure) =="
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/AF cohort.vcf.gz -Oz -o s1.vcf.gz; bcftools index -f s1.vcf.gz
bcftools query -f '%POS %REF>%ALT\tAF_after_annotate=%INFO/AF\n' s1.vcf.gz
echo "-- kept by INFO/AF<0.01 || INFO/AF=\".\" --"
bcftools filter -i 'INFO/AF<0.01 || INFO/AF="."' s1.vcf.gz | bcftools query -f '%POS %REF>%ALT\t%INFO/AF\n'
echo "== SKILL.md-consistent alternative: rename the source tag, filter on grpmax FAF, keep absent =="
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max cohort.vcf.gz -Oz -o s2.vcf.gz; bcftools index -f s2.vcf.gz
bcftools view -i 'INFO/gnomAD_FAF<0.0001 || INFO/gnomAD_FAF="."' s2.vcf.gz | bcftools query -f '%POS %REF>%ALT\tcohortAF=%INFO/AF\tFAF=%INFO/gnomAD_FAF\n'
