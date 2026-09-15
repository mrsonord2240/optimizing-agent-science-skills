#!/bin/bash
# Input 1 (canonical, post-fix regression 2026-09-15; pre-fix commands rebuilt from the viewer): "callerA.vcf is from GATK,
# callerB.vcf from FreeBayes, same sample, both against ref.fa. Normalize them so I can compare them, and tell me what is
# shared and what is private." SKILL.md 'Check for Normalization Issues' + 'Full Normalization for Caller Comparison' (post-fix).
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data; R=$D/ref.fa
echo "### $(bcftools --version | head -1)"
for f in callerA callerB; do bgzip -c $D/$f.vcf > $f.vcf.gz; bcftools index -f $f.vcf.gz; done
echo "== REF check (SKILL.md: -c w) =="
bcftools norm -f $R -c w callerB.vcf.gz 2>&1 > /dev/null | grep -iE "mismatch|REF_MISMATCH" | tr -d '\r'
echo "== Full Normalization for Caller Comparison (post-fix, verbatim; reference.fa -> ref.fa path) =="
for vcf in callerA.vcf.gz callerB.vcf.gz; do
    base=$(basename "$vcf" .vcf.gz)
    bcftools norm -m- "$vcf" | \
        bcftools norm --atomize | \
        bcftools norm -f $R -Oz -o "${base}.norm.vcf.gz"; echo "$base exit=${PIPESTATUS[*]}"
    bcftools index -f "${base}.norm.vcf.gz"
done
echo "== callerB after inspecting the mismatch: same pipeline, -c x on the last step =="
bcftools norm -m- callerB.vcf.gz | bcftools norm --atomize | bcftools norm -f $R -c x -Oz -o callerB.norm.vcf.gz; echo "exit=${PIPESTATUS[*]}"
bcftools index -f callerB.norm.vcf.gz
for b in callerA callerB; do
  echo "[$b.norm] $(bcftools query -f '%POS %REF>%ALT %GT; ' -s SYN_S1 $b.norm.vcf.gz 2>/dev/null | tr -d '\r')"
  echo "  ALT=* records: $(bcftools view -H -i 'ALT="*"' $b.norm.vcf.gz | wc -l)"
done
rm -rf comparison; bcftools isec -p comparison callerA.norm.vcf.gz callerB.norm.vcf.gz
for k in 0 1 2; do echo "comparison/000$k.vcf ($(grep -vc '^#' comparison/000$k.vcf)): $(grep -v '^#' comparison/000$k.vcf | cut -f2,4,5 | tr -d '\r' | tr '\t\n' ' ;')"; done
rm -rf rawcmp; bcftools isec -p rawcmp callerA.vcf.gz callerB.vcf.gz
echo "RAW isec: private A $(grep -vc '^#' rawcmp/0000.vcf), private B $(grep -vc '^#' rawcmp/0001.vcf), shared $(grep -vc '^#' rawcmp/0002.vcf)"
echo "== idempotence: re-normalize callerA.norm =="
bcftools norm -m- callerA.norm.vcf.gz | bcftools norm --atomize | bcftools norm -f $R -Ov 2>/dev/null | grep -v '^#' | cut -f1-5 > renorm.tsv
bcftools view -H callerA.norm.vcf.gz | cut -f1-5 > norm.tsv
echo "changed records: $(diff norm.tsv renorm.tsv | grep -c '^[<>]')"
