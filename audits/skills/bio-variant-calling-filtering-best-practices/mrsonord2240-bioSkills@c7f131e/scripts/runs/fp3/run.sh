#!/bin/bash
# Input 3 (Edge): "We only have 8 jointly-called samples on a small targeted panel. Set up VQSR like the
# GATK best practices." The Skill says VQSR is non-identifiable here; we run the SKILL.md command anyway
# to observe what happens, using a SYNTHETIC truth resource (the simulation's true sites: a best case).
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
awk -F'\t' 'NR>1 && ($3=="true_snp"||$3=="true_homalt") {print $1"\t"$2}' $S/cohort_truth_classes.tsv > truth_pos.tsv
bcftools view -T truth_pos.tsv -v snps cohort.vcf.gz | bcftools view -G -Oz -o truth_resource.vcf.gz; bcftools index -t -f truth_resource.vcf.gz
bcftools view -G -v snps cohort.vcf.gz -i 'ID!="."' -Oz -o known_resource.vcf.gz; bcftools index -t -f known_resource.vcf.gz
echo "variants: $(bcftools view -H -v snps cohort.vcf.gz | wc -l) SNPs; resource sites: truth=$(bcftools view -H truth_resource.vcf.gz | wc -l) known=$(bcftools view -H known_resource.vcf.gz | wc -l)"
echo "== SKILL.md VariantRecalibrator (-an QD MQ MQRankSum ReadPosRankSum FS SOR, -mode SNP) =="
$GATK VariantRecalibrator -R $(cygpath -w $S/ref.fa) -V cohort.vcf.gz \
    --resource:hapmap,known=false,training=true,truth=true,prior=15.0 truth_resource.vcf.gz \
    --resource:dbsnp,known=true,training=false,truth=false,prior=2.0 known_resource.vcf.gz \
    -an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR \
    -mode SNP -O snp.recal --tranches-file snp.tranches 2> vqsr.log; echo "VariantRecalibrator exit=$?"
grep -E "USER ERROR|Bad input" vqsr.log | head -3
echo "== retry without MQ (constant 60 at simulated true sites: synthetic-data artifact) =="
$GATK VariantRecalibrator -R $(cygpath -w $S/ref.fa) -V cohort.vcf.gz \
    --resource:hapmap,known=false,training=true,truth=true,prior=15.0 truth_resource.vcf.gz \
    --resource:dbsnp,known=true,training=false,truth=false,prior=2.0 known_resource.vcf.gz \
    -an QD -an MQRankSum -an ReadPosRankSum -an FS -an SOR \
    -mode SNP -O snp2.recal --tranches-file snp2.tranches 2> vqsr2.log; echo "VariantRecalibrator exit=$?"
grep -E "Convergence|Training with|very few|worst" vqsr2.log | head -6
grep -v '^#' snp2.tranches
$GATK ApplyVQSR -R $(cygpath -w $S/ref.fa) -V cohort.vcf.gz -mode SNP --recal-file snp2.recal --tranches-file snp2.tranches \
    --truth-sensitivity-filter-level 99.7 -O snp_vqsr.vcf.gz --QUIET true 2>/dev/null; echo "ApplyVQSR 99.7 exit=$?"
bcftools view -v snps -f PASS snp_vqsr.vcf.gz | bcftools query -f '%CHROM\t%POS\n' | tr -d '\r' > vqsr_kept.tsv
$PY ../../data/score_truth.py vqsr_kept.tsv "VQSR 99.7 PASS (circular best-case truth):"
echo "== what the Skill recommends instead: hard filters (guarded bcftools SNP expression) =="
bcftools view -v snps cohort.vcf.gz | bcftools filter -i 'QUAL >= 30 && (INFO/QD >= 2.0 || INFO/QD = ".") && (INFO/FS <= 60.0 || INFO/FS = ".") && (INFO/MQ >= 40.0 || INFO/MQ = ".") && (INFO/MQRankSum >= -12.5 || INFO/MQRankSum = ".") && (INFO/ReadPosRankSum >= -8.0 || INFO/ReadPosRankSum = ".") && (INFO/SOR <= 3.0 || INFO/SOR = ".")' | bcftools query -f '%CHROM\t%POS\n' | tr -d '\r' > hard_kept.tsv
$PY ../../data/score_truth.py hard_kept.tsv "hard filter PASS:"
