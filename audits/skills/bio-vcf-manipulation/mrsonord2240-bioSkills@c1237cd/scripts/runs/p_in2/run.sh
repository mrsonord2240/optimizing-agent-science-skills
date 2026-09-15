#!/bin/bash
# Input 2: stitch per-chromosome files (same samples) with concat; --naive; overlapping windows with -a -d.
set -uo pipefail
bgzip -c ../../data/cohort.vcf > joint.vcf.gz; bcftools index -f joint.vcf.gz
for c in chr1 chr2; do bcftools view -r $c joint.vcf.gz -Ob -o $c.bcf; bcftools index -f $c.bcf; bcftools view -r $c joint.vcf.gz -Oz -o $c.vcf.gz; bcftools index -f $c.vcf.gz; done
bcftools concat chr1.vcf.gz chr2.vcf.gz -Oz -o genome.vcf.gz 2>/dev/null
echo "concat == original records: $(bcftools view -H genome.vcf.gz | md5sum | cut -c1-8) vs $(bcftools view -H joint.vcf.gz | md5sum | cut -c1-8)"
bcftools concat --naive chr1.bcf chr2.bcf -Ob -o naive.bcf; echo "naive exit=$?  records=$(bcftools view -H naive.bcf | wc -l)"
echo "== --naive with a different sample order =="
bcftools view -s SYN_S2,SYN_S1,SYN_S3,SYN_S4,SYN_S5,SYN_S6,SYN_S7,SYN_S8 chr2.bcf -Ob -o chr2_reordered.bcf
bcftools concat --naive chr1.bcf chr2_reordered.bcf -Ob -o naive_bad.bcf 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"
echo "== plain concat with a different sample order =="
bcftools concat chr1.bcf chr2_reordered.bcf -Ob -o plain_reorder.bcf 2>&1 | tail -1; echo "exit=${PIPESTATUS[0]}"
echo "== overlapping windows (same samples): chr1:1-12000 and chr1:10001-20000 =="
bcftools view -r chr1:1-12000 joint.vcf.gz -Oz -o w1.vcf.gz; bcftools view -r chr1:10001-20000 joint.vcf.gz -Oz -o w2.vcf.gz; bcftools index -f w1.vcf.gz; bcftools index -f w2.vcf.gz
echo "chr1 truth=$(bcftools view -H -r chr1 joint.vcf.gz | wc -l)"
bcftools concat w1.vcf.gz w2.vcf.gz -Oz -o nov.vcf.gz 2>&1 | tail -1; echo "no -a: exit=${PIPESTATUS[0]} records=$(bcftools view -H nov.vcf.gz 2>/dev/null | wc -l)"
bcftools concat -a -d exact w1.vcf.gz w2.vcf.gz -Oz -o ov.vcf.gz; echo "-a -d exact: records=$(bcftools view -H ov.vcf.gz | wc -l)"
echo "== concat given DIFFERENT samples (the inverted-operation error) =="
bcftools view -s SYN_S1 chr1.vcf.gz -Oz -o s1.vcf.gz; bcftools view -s SYN_S2 chr1.vcf.gz -Oz -o s2.vcf.gz
bcftools concat s1.vcf.gz s2.vcf.gz -Oz -o wrong.vcf.gz 2>&1 | tail -1
echo "== post-fix Common Errors advice: reorder samples with bcftools view -s <order> first, then --naive =="
bcftools view -s $(bcftools query -l chr1.bcf | tr -d '\r' | paste -sd,) chr2_reordered.bcf -Ob -o chr2_fixed.bcf; bcftools index -f chr2_fixed.bcf
bcftools concat --naive chr1.bcf chr2_fixed.bcf -Ob -o naive_fixed.bcf; echo "naive after reorder exit=$? records=$(bcftools view -H naive_fixed.bcf | wc -l) md5 $(bcftools view -H naive_fixed.bcf | md5sum | cut -c1-8) vs joint $(bcftools view -H joint.vcf.gz | md5sum | cut -c1-8)"
