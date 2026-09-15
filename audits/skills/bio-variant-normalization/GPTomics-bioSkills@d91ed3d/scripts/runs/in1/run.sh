#!/bin/bash
# Input 1 (canonical): normalize GATK-like and FreeBayes-like VCFs, then compare with isec.
# Commands follow SKILL.md "Full Normalization for Caller Comparison" + "Check for Normalization Issues".
set -uo pipefail
DATA=../../data
for v in callerA callerB; do bgzip -c $DATA/$v.vcf > $v.vcf.gz; bcftools index -f $v.vcf.gz; done
echo "== REF check (-c w) =="
for v in callerA callerB; do echo "[$v]"; bcftools norm -f $DATA/ref.fa -c w $v.vcf.gz 2>&1 >/dev/null | tail -3; done
echo "== Skill pipeline as written (atomize | split | left-align) =="
for vcf in callerA.vcf.gz callerB.vcf.gz; do
  base=$(basename "$vcf" .vcf.gz)
  bcftools norm --atomize "$vcf" | bcftools norm -m- | bcftools norm -f $DATA/ref.fa -Oz -o "${base}.norm.vcf.gz"
  echo "$base exit=${PIPESTATUS[*]}"
done
echo "== callerB REF mismatch: exclude (-c x) after inspection, as the Skill advises =="
bcftools norm --atomize callerB.vcf.gz | bcftools norm -m- | bcftools norm -f $DATA/ref.fa -c x -Oz -o callerB.norm.vcf.gz
bcftools norm --atomize callerA.vcf.gz | bcftools norm -m- | bcftools norm -f $DATA/ref.fa -Oz -o callerA.norm.vcf.gz
for b in callerA callerB; do bcftools index -f $b.norm.vcf.gz; done
echo "== normalized callerB records =="
bcftools view -H callerB.norm.vcf.gz | cut -f1-5,10
echo "== isec on normalized =="
rm -rf comparison; bcftools isec -p comparison callerA.norm.vcf.gz callerB.norm.vcf.gz
for f in 0000 0001 0002; do echo "[$f] $(grep -vc '^#' comparison/$f.vcf)"; grep -v '^#' comparison/$f.vcf | cut -f1-5; done
echo "== isec on RAW (un-normalized) for contrast =="
rm -rf raw_cmp; bcftools isec -p raw_cmp callerA.vcf.gz callerB.vcf.gz
for f in 0000 0001 0002; do echo "[$f] $(grep -vc '^#' raw_cmp/$f.vcf)"; done
echo "== idempotence check: normalize normalized A again =="
bcftools norm -f $DATA/ref.fa -m- callerA.norm.vcf.gz 2>&1 >/dev/null | tail -1
