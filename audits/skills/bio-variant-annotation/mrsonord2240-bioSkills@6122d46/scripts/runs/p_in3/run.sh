#!/bin/bash
# Input 3 (edge, post-fix regression 2026-09-15): usage-guide "Rare Variant Analysis" recipe (post-fix, verbatim) on a VCF
# that already carries its own cohort INFO/AF.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH; export BCFTOOLS_PLUGINS=$(cygpath -w $E/msys/mingw64/libexec/bcftools)
DATA=../../data
bgzip -c $DATA/gnomad_syn.vcf > gnomad_syn.vcf.gz; bcftools index -f gnomad_syn.vcf.gz
bgzip -c $DATA/callerA.vcf > in.vcf.gz; bcftools index -f in.vcf.gz
bcftools norm -f $DATA/ref.fa -m-any in.vcf.gz 2>/dev/null | bcftools +fill-tags -Oz -o cohort.vcf.gz -- -t AF; bcftools index -f cohort.vcf.gz
echo "== recipe as written (post-fix) =="
bcftools annotate -a gnomad_syn.vcf.gz -c INFO/gnomAD_FAF:=INFO/fafmax_faf95_max cohort.vcf.gz -Oz -o with_gnomad.vcf.gz; echo "annotate exit=$?"
bcftools index -f with_gnomad.vcf.gz
bcftools filter -i 'INFO/gnomAD_FAF<0.01 || INFO/gnomAD_FAF="."' with_gnomad.vcf.gz -Ou | \
bcftools csq -p a -f $DATA/ref.fa -g $DATA/genes.gff3 -Oz -o rare_consequences.vcf.gz; echo "exit=${PIPESTATUS[*]}"
echo "-- all records after annotate --"
bcftools query -f '%POS %REF>%ALT\tcohortAF=%INFO/AF\tFAF=%INFO/gnomAD_FAF\n' with_gnomad.vcf.gz | tr -d '\r'
echo "-- kept (rare or absent) with consequence --"
bcftools query -f '%POS %REF>%ALT\tcohortAF=%INFO/AF\tFAF=%INFO/gnomAD_FAF\t%INFO/BCSQ\n' rare_consequences.vcf.gz | tr -d '\r' | cut -c1-140
