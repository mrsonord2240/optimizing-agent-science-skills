#!/bin/bash
# Input 6 (NEW, re-audit 2026-09-15, Variant C): "Scan every gene from PLINK files with the SKAT SSD route
# (Generate_SSD_SetID / Open_SSD / SKAT.SSD.All) instead of loading matrices, and check it agrees with the
# per-gene matrix run." Runs in WSL: plink2 a6.9, SKAT 2.2.5 (installed with r-saige 1.3.1). SYNTHETIC data.
set -uo pipefail
export PATH=/tmp/vaca/saige/bin:/tmp/vaca/env/bin:$PATH
D=../../data
plink2 --vcf $D/wes.vcf --double-id --make-bed --out wes --silent
awk '{print $2"\t"$1}' $D/annot.txt > setid.txt
echo "sets: $(cut -f1 setid.txt | sort -u | wc -l); variants: $(wc -l < setid.txt)"
Rscript skat_ssd.R; echo "Rscript exit=$?"
