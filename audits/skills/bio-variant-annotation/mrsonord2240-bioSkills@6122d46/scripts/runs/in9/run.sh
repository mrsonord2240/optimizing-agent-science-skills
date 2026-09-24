#!/bin/bash
# Input 9 (NEW, re-audit 2026-09-15, Edge): "SYN_S1 has the frameshift at chr1:1420 and the stop at chr1:1466, both unphased.
# Long reads put them on different haplotypes. Which bcftools csq --phase mode should I use, and what consequence does each
# variant get?" Tests the post-fix -p a/m/s explanation against real csq output. SYNTHETIC data.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH; export BCFTOOLS_PLUGINS=$(cygpath -w $E/msys/mingw64/libexec/bcftools)
DATA=../../data
bgzip -c $DATA/callerA.vcf > in.vcf.gz; bcftools index -f in.vcf.gz
bcftools norm -f $DATA/ref.fa -m-any in.vcf.gz -Oz -o norm.vcf.gz 2>/dev/null; bcftools index -f norm.vcf.gz
echo "samples: $(bcftools query -l norm.vcf.gz | tr -d '\r' | tr '\n' ' ')"
bcftools query -r chr1:1400-1500 -f '%POS %REF>%ALT [%SAMPLE=%GT ]\n' norm.vcf.gz | tr -d '\r'
for p in a s; do
  echo "== csq -p $p (unphased input) =="
  bcftools csq -p $p -f $DATA/ref.fa -g $DATA/genes.gff3 norm.vcf.gz -Oz -o p_$p.vcf.gz 2> p_$p.err; echo "exit=$?"; grep -iE "error|unphased" p_$p.err | head -2
  bcftools query -i 'POS>=1400 && POS<=1500' -f '%POS\t%INFO/BCSQ\t[%SAMPLE:%BCSQ ]\n' p_$p.vcf.gz | tr -d '\r' | cut -c1-200
done
echo "== phase the two SYN_S1 hets in TRANS (1420 0|1, 1466 1|0), others unchanged, then -p m and default -p r =="
bcftools view norm.vcf.gz | awk 'BEGIN{OFS="\t"} /^#/{print;next} $2==1420{sub(/^0\/1/,"0|1",$10)} $2==1466{sub(/^0\/1/,"1|0",$10)} {print}' | bgzip -c > trans.vcf.gz; bcftools index -f trans.vcf.gz
bcftools query -r chr1:1400-1500 -f '%POS [%SAMPLE=%GT ]\n' trans.vcf.gz | tr -d '\r'
for p in m r; do
  echo "== csq -p $p (SYN_S1 phased in trans) =="
  bcftools csq -p $p -f $DATA/ref.fa -g $DATA/genes.gff3 trans.vcf.gz -Oz -o t_$p.vcf.gz 2> t_$p.err; echo "exit=$?"; grep -iE "error|unphased" t_$p.err | head -2
  bcftools query -i 'POS>=1400 && POS<=1500' -f '%POS\t%INFO/BCSQ\t[%SAMPLE:%BCSQ ]\n' t_$p.vcf.gz 2>/dev/null | tr -d '\r' | cut -c1-200
done
