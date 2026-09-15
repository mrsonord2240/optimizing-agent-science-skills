#!/bin/bash
# Input 3 (Edge): "About 20 sites fail HWE in my cohort. Should I drop every HWE failure? Some might be real."
# SYNTHETIC: 6 planted excess_het sites (collapsed-paralog-like, every sample het), SYN_S6 low coverage,
# no case/control labels in this cohort (PED phenotype -9), single simulated population.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
echo "== SKILL.md: ExcessHet > 54.69 (GATK default cutoff) =="
bcftools query -f '%CHROM\t%POS\t%INFO/ExcessHet\n' cohort.vcf.gz | tr -d '\r' | awk '$3>54.69' > exhet_flag.tsv
cat exhet_flag.tsv
awk -F'\t' 'NR>1 && $3=="excess_het"{print $1"\t"$2}' $S/cohort_truth_classes.tsv > truth_exhet.tsv
echo "flagged=$(wc -l < exhet_flag.tsv) truth excess_het=$(wc -l < truth_exhet.tsv) overlap=$(cut -f1,2 exhet_flag.tsv | grep -cFf truth_exhet.tsv)"
echo "== genotype filter first (GQ<20 | DP<8 -> ./.), then two-sided vs excess-het HWE with +fill-tags =="
bcftools filter -S . -e 'FMT/GQ<20 | FMT/DP<8' cohort.vcf.gz -Oz -o gtf.vcf.gz; bcftools index -f gtf.vcf.gz
for f in cohort gtf; do
  bcftools +fill-tags $f.vcf.gz -Oz -o $f.tags.vcf.gz -- -t HWE,ExcHet 2>/dev/null; bcftools index -f $f.tags.vcf.gz
  echo "$f: HWE p<1e-3 (two-sided) = $(bcftools view -H -i 'INFO/HWE<1e-3' $f.tags.vcf.gz | wc -l); ExcHet p<1e-3 (excess only) = $(bcftools view -H -i 'INFO/ExcHet<1e-3' $f.tags.vcf.gz | wc -l)"
done
echo "HWE / ExcHet p-values at the 6 ExcessHet-flagged sites (n=8 samples limits the attainable p):"
cut -f1,2 exhet_flag.tsv > exhet_regions.tsv
bcftools query -R exhet_regions.tsv -f '%CHROM\t%POS\t%INFO/HWE\t%INFO/ExcHet\t[%GT ]\n' gtf.tags.vcf.gz | tr -d '\r'
echo "sites HWE p<0.05: cohort=$(bcftools view -H -i 'INFO/HWE<0.05' cohort.tags.vcf.gz | wc -l) gtf=$(bcftools view -H -i 'INFO/HWE<0.05' gtf.tags.vcf.gz | wc -l)"
bcftools query -i 'INFO/HWE<0.05' -f '%CHROM\t%POS\n' cohort.tags.vcf.gz | tr -d '\r' > hwe_fail.tsv
echo "two-sided HWE failures by truth class:"; awk -F'\t' 'NR==FNR{c[$1"\t"$2]=$3;next} {print c[$1"\t"$2]}' $S/cohort_truth_classes.tsv hwe_fail.tsv | sort | uniq -c
echo "== exact test: vcftools --hardy in WSL (see out_wsl.txt) =="
