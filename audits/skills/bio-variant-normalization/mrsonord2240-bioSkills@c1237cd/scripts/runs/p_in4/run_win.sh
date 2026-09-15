#!/bin/bash
# Input 4, second part (Windows bcftools 1.24): shipped examples/normalize_vcf.sh from the fork commit, verbatim.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data
git -C F:/OpenScience/external/mrsonord2240__bioSkills show c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/variant-normalization/examples/normalize_vcf.sh > normalize_vcf.fork_copy.sh
bash -n normalize_vcf.fork_copy.sh && echo "bash -n ok"
for f in callerA callerB; do bgzip -c $D/$f.vcf > $f.vcf.gz; bcftools index -f $f.vcf.gz; done
bgzip -c $D/edge_multiallelic_fixedhdr.vcf > edge.vcf.gz; bcftools index -f edge.vcf.gz
for f in callerA callerB edge; do
  echo "== example on $f =="
  bash normalize_vcf.fork_copy.sh $D/ref.fa $f.vcf.gz $f.ex.vcf.gz 2>&1 | grep -E "Error|Inspect|Records|Extra"; echo "exit=${PIPESTATUS[0]}"
  [ -f $f.ex.vcf.gz ] && echo "ALT=* in output: $(bcftools view -H -i 'ALT="*"' $f.ex.vcf.gz | wc -l); output: $(bcftools query -f '%POS %REF>%ALT; ' $f.ex.vcf.gz | tr -d '\r')"
done
