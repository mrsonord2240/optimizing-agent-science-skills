#!/bin/bash
# Re-audit 2026-09-27 -- Input 5 (Stress/multi-part): bcftools csq --phase (-p) mode
# semantics. Regression of the prior audit's Input 9 (csq phase edge case), re-executed
# fresh, plus a literal cross-check of SKILL.md/usage-guide.md's -p a/m/r/R/s prose
# against `bcftools csq --help` on the currently active bcftools 1.24.
set -uo pipefail
DATA=/mnt/openscience/audits/bio-variant-annotation/data
cd /mnt/openscience/audits/bio-variant-annotation/run/reaudit_20260927/in5

echo "== bcftools csq --help, the --phase section (ground truth for SKILL.md's claims) =="
bcftools csq 2>&1 | grep -A12 -- '-p, --phase'

bgzip -c "$DATA/callerA.vcf" > in.vcf.gz; bcftools index -f in.vcf.gz
bcftools norm -f "$DATA/ref.fa" -m-any in.vcf.gz -Oz -o norm.vcf.gz 2>/dev/null
bcftools index -f norm.vcf.gz

echo "== SYN_S1 genotypes near the frameshift(1420)/stop(1466) pair, unphased =="
bcftools query -r chr1:1400-1500 -f '%POS %REF>%ALT [%SAMPLE=%GT ]\n' norm.vcf.gz

for p in a s; do
  echo "== csq -p $p on UNPHASED input =="
  bcftools csq -p $p -f "$DATA/ref.fa" -g "$DATA/genes.gff3" norm.vcf.gz -Oz -o "p_${p}.vcf.gz" 2> "p_${p}.err"
  echo "exit=$?"
  cat "p_${p}.err"
  bcftools index -f "p_${p}.vcf.gz" 2>/dev/null
  bcftools query -i 'POS>=1400 && POS<=1500' -f '%POS\t%INFO/BCSQ\n' "p_${p}.vcf.gz" 2>/dev/null
done

echo "== default (no -p, i.e. -p r) on UNPHASED input: must error, per SKILL.md =="
bcftools csq -f "$DATA/ref.fa" -g "$DATA/genes.gff3" norm.vcf.gz -Oz -o p_default.vcf.gz 2> p_default.err
echo "exit=$?"
cat p_default.err

echo "== phase SYN_S1's two hets in TRANS (1420=0|1, 1466=1|0) =="
bcftools view norm.vcf.gz | awk 'BEGIN{OFS="\t"} /^#/{print;next} $2==1420{sub(/^0\/1/,"0|1",$10)} $2==1466{sub(/^0\/1/,"1|0",$10)} {print}' | bgzip -c > trans.vcf.gz
bcftools index -f trans.vcf.gz
bcftools query -r chr1:1400-1500 -f '%POS [%SAMPLE=%GT ]\n' trans.vcf.gz

for p in m r a; do
  echo "== csq -p $p on TRANS-phased input =="
  bcftools csq -p $p -f "$DATA/ref.fa" -g "$DATA/genes.gff3" trans.vcf.gz -Oz -o "t_${p}.vcf.gz" 2> "t_${p}.err"
  echo "exit=$?"
  cat "t_${p}.err"
  bcftools index -f "t_${p}.vcf.gz" 2>/dev/null
  bcftools query -i 'POS>=1400 && POS<=1500' -f '%POS\t%INFO/BCSQ\n' "t_${p}.vcf.gz" 2>/dev/null
done
