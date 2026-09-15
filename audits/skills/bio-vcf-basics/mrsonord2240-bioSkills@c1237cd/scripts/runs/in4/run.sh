#!/bin/bash
# Input 4: is sample.g.vcf an analysis-ready callset?
set -uo pipefail
G=../../data/sample.g.vcf
echo "== ALT alleles and END blocks =="; bcftools query -f '%CHROM\t%POS\t%INFO/END\t%REF\t%ALT\t%QUAL[\t%GT\t%DP\t%GQ]\n' $G
echo "== records whose ALT is more than <NON_REF> (candidate variant sites) =="
bcftools view -H -i 'N_ALT>1' $G | cut -f1-6
echo "== bases covered by reference blocks vs sites listed =="
bcftools query -f '%POS\t%INFO/END\n' $G | awk '$2!="." {b+=$2-$1+1; n++} END{print n" blocks cover "b" bp"}'
echo "== naive variant count (the mistake) =="; echo "records: $(bcftools view -H $G | wc -l)"
