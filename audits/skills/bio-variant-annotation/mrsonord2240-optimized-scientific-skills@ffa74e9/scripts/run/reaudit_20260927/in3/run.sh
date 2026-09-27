#!/bin/bash
# Re-audit 2026-09-27 -- Input 3 (Variant B, NEW): usage-guide.md BED/TAB annotation
# and --set-id mechanics. Neither recipe was executed by any prior audit of this Skill
# (prior audits exercised annotate -a <vcf>, csq, and --rename-chrs, not BED/TAB or --set-id).
set -uo pipefail
DATA=/mnt/openscience/audits/bio-variant-annotation/data
cd /mnt/openscience/audits/bio-variant-annotation/run/reaudit_20260927/in3

bgzip -c "$DATA/callerA.vcf" > in.vcf.gz; bcftools index -f in.vcf.gz
bcftools norm -f "$DATA/ref.fa" -m-any in.vcf.gz -Oz -o norm.vcf.gz 2>/dev/null; bcftools index -f norm.vcf.gz

echo "== usage-guide.md: BED File Annotation =="
cat > regions.bed <<'EOF'
chr1	1000	1100	exon1_region
chr1	1400	1500	exon2_region
EOF
bgzip -c regions.bed > regions.bed.gz
tabix -p bed regions.bed.gz
echo '##INFO=<ID=REGION,Number=1,Type=String,Description="Genomic region">' > header.txt
bcftools annotate -a regions.bed.gz -c CHROM,FROM,TO,INFO/REGION -h header.txt norm.vcf.gz -Oz -o with_region.vcf.gz
echo "exit=$?"
bcftools index -f with_region.vcf.gz
bcftools query -f '%CHROM:%POS\t%INFO/REGION\n' with_region.vcf.gz

echo "== usage-guide.md: TAB File Annotation (scores.tab) =="
cat > scores.tab <<'EOF'
chr1	1026	0.87
chr1	1231	0.42
EOF
bgzip -c scores.tab > scores.tab.gz
tabix -s1 -b2 -e2 scores.tab.gz
echo '##INFO=<ID=SCORE,Number=1,Type=Float,Description="Conservation score">' > header2.txt
bcftools annotate -a scores.tab.gz -c CHROM,POS,INFO/SCORE -h header2.txt norm.vcf.gz -Oz -o with_score.vcf.gz
echo "exit=$?"
bcftools query -f '%CHROM:%POS\t%INFO/SCORE\n' with_score.vcf.gz

echo "== usage-guide.md: Setting Variant IDs (--set-id) =="
bcftools annotate --set-id '%CHROM\_%POS\_%REF\_%ALT' norm.vcf.gz -Oz -o with_ids.vcf.gz
echo "exit=$?"
bcftools query -f '%ID\n' with_ids.vcf.gz | head -3

echo "== usage-guide.md: --set-id +'...' only fills missing IDs (first give some variants real IDs) =="
bcftools annotate -a "$DATA/dbsnp_syn.vcf.gz" -c ID norm.vcf.gz -Oz -o with_some_ids.vcf.gz 2>/dev/null || \
  { bgzip -c "$DATA/dbsnp_syn.vcf" > dbsnp_syn.vcf.gz; bcftools index -f dbsnp_syn.vcf.gz; \
    bcftools annotate -a dbsnp_syn.vcf.gz -c ID norm.vcf.gz -Oz -o with_some_ids.vcf.gz; }
bcftools index -f with_some_ids.vcf.gz
bcftools annotate --set-id +'%CHROM\_%POS\_%REF\_%ALT' with_some_ids.vcf.gz -Oz -o with_ids_plus.vcf.gz
echo "exit=$?"
bcftools query -f '%ID\n' with_ids_plus.vcf.gz

echo "== usage-guide.md: Remove All INFO fields (bcftools annotate -x INFO) =="
bcftools annotate -x INFO with_score.vcf.gz -Oz -o minimal.vcf.gz
echo "exit=$?"
bcftools view -H minimal.vcf.gz | head -2
