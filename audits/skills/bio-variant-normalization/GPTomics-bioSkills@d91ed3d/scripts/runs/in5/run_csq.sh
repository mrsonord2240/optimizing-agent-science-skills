#!/bin/bash
# Input 5 (stress) part (c): consequence on un-atomized vs atomized representation with bcftools csq.
set -uo pipefail
DATA=../../data
bgzip -c $DATA/callerB.vcf > callerB.vcf.gz; bcftools index -f callerB.vcf.gz
bgzip -c $DATA/callerA.vcf > callerA.vcf.gz; bcftools index -f callerA.vcf.gz
# matching copy (split -> atomize -> left-align) and annotation copy (split + left-align, NO atomize)
bcftools norm -m- callerB.vcf.gz 2>/dev/null | bcftools norm --atomize 2>/dev/null | bcftools norm -f $DATA/ref.fa -c x -Oz -o B.match.vcf.gz 2>/dev/null
bcftools norm -m- callerB.vcf.gz 2>/dev/null | bcftools norm -f $DATA/ref.fa -c x -Oz -o B.annot.vcf.gz 2>/dev/null
echo "== csq as the Skill writes it (no -p) on the un-atomized copy =="
bcftools csq -f $DATA/ref.fa -g $DATA/genes.gff3 B.annot.vcf.gz -Ov -o B.annot.csq.vcf 2>&1 | tail -3; echo "exit=$?"
echo "== csq -p a (treat unphased as phased) on un-atomized copy =="
bcftools csq -p a -f $DATA/ref.fa -g $DATA/genes.gff3 B.annot.vcf.gz 2>/dev/null | bcftools query -f '%POS %REF>%ALT\t%BCSQ\n' | awk '$1>=1000 && $1<=1500'
echo "== csq -p a on the ATOMIZED matching copy (unphased, per-record) =="
bcftools csq -p a -f $DATA/ref.fa -g $DATA/genes.gff3 B.match.vcf.gz 2>/dev/null | bcftools query -f '%POS %REF>%ALT\t%BCSQ\n' | awk '$1>=1000 && $1<=1500'
echo "== csq on callerA (adjacent SNVs phased 0|1 with PS) default -p =="
bcftools norm -m- callerA.vcf.gz 2>/dev/null | bcftools norm -f $DATA/ref.fa -Oz -o A.annot.vcf.gz 2>/dev/null
bcftools csq -f $DATA/ref.fa -g $DATA/genes.gff3 A.annot.vcf.gz 2>&1 | tail -2
bcftools csq -p a -f $DATA/ref.fa -g $DATA/genes.gff3 A.annot.vcf.gz 2>/dev/null | bcftools query -f '%POS %REF>%ALT\t%BCSQ\n' | awk '$1>=1000 && $1<=1500'
