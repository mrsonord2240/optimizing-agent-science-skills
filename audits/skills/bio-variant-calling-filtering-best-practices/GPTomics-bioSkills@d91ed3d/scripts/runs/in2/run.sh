#!/bin/bash
# Input 2 (Variant A): "Reproduce the GATK SNP hard filter in bcftools so hom-alt sites don't get dropped,
# and give me a cyvcf2 version for custom logic." SYNTHETIC data.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf | bcftools view -v snps -Oz -o snps.vcf.gz; bcftools index -f snps.vcf.gz
echo "SNP records: $(bcftools view -H snps.vcf.gz | wc -l); records without MQRankSum (hom-alt-only sites): $(bcftools view -H -i 'INFO/MQRankSum="."' snps.vcf.gz | wc -l)"
# SKILL.md block, expression verbatim
bcftools filter -i '
    QUAL >= 30 && (INFO/QD >= 2.0 || INFO/QD = ".") &&
    (INFO/FS <= 60.0 || INFO/FS = ".") && (INFO/MQ >= 40.0 || INFO/MQ = ".") &&
    (INFO/MQRankSum >= -12.5 || INFO/MQRankSum = ".") &&
    (INFO/ReadPosRankSum >= -8.0 || INFO/ReadPosRankSum = ".") &&
    (INFO/SOR <= 3.0 || INFO/SOR = ".")' snps.vcf.gz -Oz -o snps_guarded.vcf.gz; echo "guarded exit=$?"
# The naive translation the Skill warns against
bcftools filter -i 'QUAL >= 30 && INFO/QD >= 2.0 && INFO/FS <= 60.0 && INFO/MQ >= 40.0 && INFO/MQRankSum >= -12.5 && INFO/ReadPosRankSum >= -8.0 && INFO/SOR <= 3.0' snps.vcf.gz -Oz -o snps_naive.vcf.gz
for f in snps_guarded snps_naive; do bcftools query -f '%CHROM\t%POS\n' $f.vcf.gz | tr -d '\r' > $f.tsv; $PY ../../data/score_truth.py $f.tsv "$f:"; done
echo "== Python (cyvcf2) block: run in WSL, see run_py.sh / out_py.txt =="
