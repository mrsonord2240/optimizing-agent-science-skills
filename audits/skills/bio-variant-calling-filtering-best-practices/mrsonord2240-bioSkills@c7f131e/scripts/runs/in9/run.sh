#!/bin/bash
# Input 9 (NEW, re-audit 2026-09-15, Variant C): "For the rare-variant analysis, soft-label low QUAL and low depth,
# keep PASS, drop samples with too many no-calls, drop sites >5% missing, and remove hets with skewed allele
# balance. Use the usage-guide recipes and tell me how many sites and genotypes each step removed."
# Runs the usage-guide recipes (post-fix) on the SYNTHETIC cohort. Genotype nulling first, per SKILL.md order.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
echo "== Multi-step soft-filter pipeline (usage guide, verbatim) =="
bcftools filter -s 'LowQual' -e 'QUAL<30' cohort.vcf.gz | \
    bcftools filter -s 'LowDepth' -e 'INFO/DP<10' -Oz -o marked.vcf.gz; echo "exit=$?"
bcftools query -f '%FILTER\n' marked.vcf.gz | tr -d '\r' | sort | uniq -c
bcftools view -f PASS marked.vcf.gz -Oz -o pass_only.vcf.gz
echo "PASS records: $(bcftools view -H pass_only.vcf.gz | wc -l)"
echo "== genotype nulling (SKILL.md) =="
bcftools filter -S . -e 'FMT/GQ<20 | FMT/DP<8' pass_only.vcf.gz -Oz -o gt.vcf.gz; bcftools index -f gt.vcf.gz
echo "== per-sample missingness (usage guide: bcftools stats -s - | grep ^PSC | cut -f3,14) =="
bcftools stats -s - gt.vcf.gz | grep '^# PSC' | tr '\t' '\n' | sed -n '3p;14p' | tr '\n' '|'; echo
bcftools stats -s - gt.vcf.gz | grep ^PSC | cut -f3,14 | tr -d '\r'
bcftools stats -s - gt.vcf.gz | grep ^PSC | cut -f3,14 | tr -d '\r' | awk '$2<30{print $1}' > good_samples.txt
echo "kept samples: $(tr '\n' ' ' < good_samples.txt)"
bcftools view -S good_samples.txt gt.vcf.gz -Oz -o sample_filtered.vcf.gz; echo "view -S exit=$?"
echo "== site missingness (usage guide) =="
bcftools filter -i 'F_MISSING<0.05' sample_filtered.vcf.gz -Oz -o site_filtered.vcf.gz; echo "exit=$?"
echo "sites: $(bcftools view -H sample_filtered.vcf.gz | wc -l) -> $(bcftools view -H site_filtered.vcf.gz | wc -l)"
echo "== allele balance (usage guide, post-fix) =="
bcftools filter -i 'GT="het" & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) > 0.2 & FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) < 0.8' \
    site_filtered.vcf.gz -o ab_filtered.vcf; echo "exit=$?"
echo "records: $(bcftools view -H site_filtered.vcf.gz | wc -l) -> $(grep -vc '^#' ab_filtered.vcf)"
echo "records with NO het genotype at all (dropped by GT=\"het\" in -i): $(bcftools view -H -e 'GT="het"' site_filtered.vcf.gz | wc -l)"
echo "hom-alt-only true sites surviving AB step:"
bcftools query -f '%CHROM\t%POS\n' ab_filtered.vcf | tr -d '\r' > ab_kept.tsv; $PY $S/score_truth.py ab_kept.tsv "after AB include:"
echo "== genotype-level alternative: null skewed het genotypes instead of dropping sites =="
bcftools filter -S . -e 'GT="het" & (FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) <= 0.2 | FMT/AD[:1]/(FMT/AD[:0]+FMT/AD[:1]) >= 0.8)' site_filtered.vcf.gz -Oz -o ab_gt.vcf.gz; echo "exit=$?"
bcftools query -f '%CHROM\t%POS\n' ab_gt.vcf.gz | tr -d '\r' > abgt_kept.tsv; $PY $S/score_truth.py abgt_kept.tsv "genotype-level AB null:"
