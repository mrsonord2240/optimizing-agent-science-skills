#!/bin/bash
# Input 2 (Variant A, post-fix regression 2026-09-15; commands rebuilt from the pre-fix viewer): "Our pipeline annotated
# callerB.vcf against ClinVar and says the homopolymer deletion near chr1:506 is not in ClinVar, so we flagged it as novel.
# Is that right? Fix the pipeline so database matching works." SKILL.md 'Before Database Annotation' (post-fix).
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data; R=$D/ref.fa
for f in callerB clinvar_syn dbsnp_syn; do bgzip -c $D/$f.vcf > $f.vcf.gz; bcftools index -f $f.vcf.gz; done
ann() { bcftools annotate -a clinvar_syn.vcf.gz -c INFO/CLNSIG,INFO/CLNREVSTAT $1 -Oz -o t1.vcf.gz && bcftools index -f t1.vcf.gz && \
        bcftools annotate -a dbsnp_syn.vcf.gz -c ID t1.vcf.gz -Oz -o $2 && bcftools index -f $2; }
echo "== RAW =="
ann callerB.vcf.gz raw_ann.vcf.gz
bcftools query -f '%CHROM:%POS %REF>%ALT\t%ID\t%INFO/CLNSIG\t%INFO/CLNREVSTAT\n' raw_ann.vcf.gz | tr -d '\r'
echo "== SKILL.md 'Before Database Annotation' block, verbatim =="
bcftools norm -m- callerB.vcf.gz | \
    bcftools norm --atomize | \
    bcftools norm -f $R -Oz -o for_annotation.vcf.gz; echo "exit=${PIPESTATUS[*]}"
bcftools index -f for_annotation.vcf.gz; echo "index exit=$?  records written: $(bcftools view -H for_annotation.vcf.gz 2>/dev/null | wc -l) of $(bcftools view -H callerB.vcf.gz | wc -l)"
echo "== same block with the REF mismatch excluded (-c x, after inspecting it) =="
bcftools norm -m- callerB.vcf.gz | bcftools norm --atomize | bcftools norm -f $R -c x -Oz -o for_annotation.vcf.gz; bcftools index -f for_annotation.vcf.gz
ann for_annotation.vcf.gz norm_ann.vcf.gz
bcftools query -f '%CHROM:%POS %REF>%ALT\t%ID\t%INFO/CLNSIG\t%INFO/CLNREVSTAT\n' norm_ann.vcf.gz | tr -d '\r'
