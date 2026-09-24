#!/bin/bash
# Input 1 (Canonical): "Apply GATK best-practice hard filters to our 8-sample joint callset (cohort.vcf),
# SNPs and indels separately, and tell me what was removed." SYNTHETIC data (data/make_data.py).
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
git -C F:/OpenScience/external/mrsonord2240__bioSkills show c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/filtering-best-practices/examples/filter_variants.sh > filter_variants.fork_copy.sh
echo "### bcftools $(bcftools --version | head -1)"
echo "### shipped examples/filter_variants.sh (Windows bcftools 1.24)"
bash filter_variants.fork_copy.sh cohort.vcf.gz ex > ex.log 2>&1; echo "script exit=$?"
grep -E "Merging|not contiguous|Could not read|Failed" ex.log
ls ex_all_filtered.vcf.gz 2>&1
echo "### GATK $($GATK --version 2>/dev/null | grep -m1 'The Genome Analysis Toolkit')"
$GATK SelectVariants -V cohort.vcf.gz -select-type SNP -O raw_snps.vcf.gz --QUIET true 2>/dev/null; echo "SelectVariants SNP exit=$?"
$GATK SelectVariants -V cohort.vcf.gz -select-type INDEL -O raw_indels.vcf.gz --QUIET true 2>/dev/null; echo "SelectVariants INDEL exit=$?"
# SKILL.md commands verbatim (reference/paths substituted)
$GATK VariantFiltration -R $(cygpath -w $S/ref.fa) -V raw_snps.vcf.gz -O filtered_snps.vcf.gz --QUIET true \
    --filter-expression "QD < 2.0" --filter-name "QD2" \
    --filter-expression "FS > 60.0" --filter-name "FS60" \
    --filter-expression "MQ < 40.0" --filter-name "MQ40" \
    --filter-expression "MQRankSum < -12.5" --filter-name "MQRankSum-12.5" \
    --filter-expression "ReadPosRankSum < -8.0" --filter-name "ReadPosRankSum-8" \
    --filter-expression "SOR > 3.0" --filter-name "SOR3" 2>gatk_snps.log; echo "VariantFiltration SNP exit=$?"
$GATK VariantFiltration -R $(cygpath -w $S/ref.fa) -V raw_indels.vcf.gz -O filtered_indels.vcf.gz --QUIET true \
    --filter-expression "QD < 2.0" --filter-name "QD2" \
    --filter-expression "FS > 200.0" --filter-name "FS200" \
    --filter-expression "ReadPosRankSum < -20.0" --filter-name "ReadPosRankSum-20" \
    --filter-expression "SOR > 10.0" --filter-name "SOR10" 2>gatk_indels.log; echo "VariantFiltration INDEL exit=$?"
echo "SNP FILTER labels (top):"; bcftools query -f '%FILTER\n' filtered_snps.vcf.gz | tr -d '\r' | tr ';' '\n' | sort | uniq -c | sort -rn
echo "INDEL FILTER labels:"; bcftools query -f '%FILTER\n' filtered_indels.vcf.gz | tr -d '\r' | tr ';' '\n' | sort | uniq -c | sort -rn
bcftools concat -a filtered_snps.vcf.gz filtered_indels.vcf.gz 2>/dev/null | bcftools view -f PASS | bcftools query -f '%CHROM\t%POS\n' | tr -d '\r' > gatk_kept.tsv
$PY ../../data/score_truth.py gatk_kept.tsv "GATK VariantFiltration PASS:"
echo "hom-alt-only sites (RankSum missing) that PASS: $(bcftools concat -a filtered_snps.vcf.gz filtered_indels.vcf.gz 2>/dev/null | bcftools view -f PASS -i 'INFO/MQRankSum="."' -H | wc -l) of $(bcftools view -H -i 'INFO/MQRankSum="."' cohort.vcf.gz | wc -l)"
echo "### Fixed example (concat -a) to confirm the only defect is the concat step"
sed -e 's/bcftools concat "\${OUTPUT_PREFIX}_snps_filtered.vcf.gz"/bcftools concat -a "${OUTPUT_PREFIX}_snps_filtered.vcf.gz"/' \
    -e '/=== Merging filtered variants ===/a bcftools index -f "${OUTPUT_PREFIX}_snps_filtered.vcf.gz"; bcftools index -f "${OUTPUT_PREFIX}_indels_filtered.vcf.gz"' \
    filter_variants.fork_copy.sh > filter_variants.concat_a.sh
diff filter_variants.fork_copy.sh filter_variants.concat_a.sh
bash filter_variants.concat_a.sh cohort.vcf.gz fx > fx.log 2>&1; echo "fixed script exit=$?"
grep -E "Ti/Tv ratio" fx.log
bcftools query -f '%CHROM\t%POS\n' fx_all_filtered.vcf.gz | tr -d '\r' > fx_kept.tsv; $PY ../../data/score_truth.py fx_kept.tsv "example (concat -a) kept:"
