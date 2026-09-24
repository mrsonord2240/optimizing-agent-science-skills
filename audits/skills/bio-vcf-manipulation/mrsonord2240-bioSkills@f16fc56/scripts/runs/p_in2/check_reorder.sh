#!/bin/bash
# Second-method check of the post-fix advice "reorder samples with bcftools view -s <order> first" before --naive.
set -uo pipefail
O=$(bcftools query -l chr1.bcf | tr -d '\r' | paste -sd,)
echo "header INFO lines chr1.bcf: $(bcftools view -h chr1.bcf | grep -c '^##INFO')  chr2_fixed.bcf (view -s): $(bcftools view -h chr2_fixed.bcf | grep -c '^##INFO')"
bcftools view -h chr2_fixed.bcf | grep -E 'ID=(AC|AN),' | tr -d '\r'
bcftools view -I -s $O chr2_reordered.bcf -Ob -o chr2_fixedI.bcf
bcftools concat --naive chr1.bcf chr2_fixedI.bcf -Ob -o naive_I.bcf 2>&1 | tail -1; echo "view -I -s then --naive: exit=${PIPESTATUS[0]} md5 $(bcftools view -H naive_I.bcf 2>/dev/null | md5sum | cut -c1-8) vs joint $(bcftools view -H joint.vcf.gz | md5sum | cut -c1-8)"
bcftools concat chr1.bcf chr2_fixed.bcf -Ob -o plain_fixed.bcf 2>&1 | tail -1; echo "view -s then plain concat: exit=${PIPESTATUS[0]} records $(bcftools view -H plain_fixed.bcf | wc -l)"
