#!/bin/bash
# Input 6 (NEW, re-audit 2026-09-15, Variant C): "Is the single-pass 'bcftools norm -f ref.fa -m-any --atomize' really the same
# as your three-step pipeline? I'd rather run one command in production. And what happens with the 'Before Database
# Annotation' block when a REF allele is wrong - do I get a usable file?" Windows bcftools 1.24. SYNTHETIC data.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data; R=$D/ref.fa
for f in callerA callerB edge_multiallelic_fixedhdr; do bgzip -c $D/$f.vcf > $f.vcf.gz; bcftools index -f $f.vcf.gz; done
for f in callerA callerB edge_multiallelic_fixedhdr; do
  bcftools norm -m- $f.vcf.gz 2>/dev/null | bcftools norm --atomize 2>/dev/null | bcftools norm -f $R -c x 2>/dev/null | grep -v '^#' | cut -f1-5,10 > $f.three.tsv
  bcftools norm -f $R -m-any --atomize -c x $f.vcf.gz 2>/dev/null | grep -v '^#' | cut -f1-5,10 > $f.one.tsv
  echo "$f: three-step $(wc -l < $f.three.tsv) records, single-pass $(wc -l < $f.one.tsv) records, differing lines $(diff $f.three.tsv $f.one.tsv | grep -c '^[<>]'), ALT=* single-pass $(awk '$5=="*"' $f.one.tsv | wc -l)"
done
diff callerB.three.tsv callerB.one.tsv | head -6
echo "== 'Before Database Annotation' block verbatim on callerB (one REF mismatch at chr1:4000) =="
bcftools norm -m- callerB.vcf.gz | \
    bcftools norm --atomize | \
    bcftools norm -f $R -Oz -o for_annotation.vcf.gz; echo "pipeline exit=${PIPESTATUS[*]}"
bcftools index for_annotation.vcf.gz; echo "bcftools index exit=$?"
echo "records in for_annotation.vcf.gz: $(bcftools view -H for_annotation.vcf.gz 2>/dev/null | wc -l) (input $(bcftools view -H callerB.vcf.gz | wc -l))"
