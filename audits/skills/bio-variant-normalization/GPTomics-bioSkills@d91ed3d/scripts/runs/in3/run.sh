#!/bin/bash
# Input 3 (edge): split a multiallelic keeping AD/PL/per-ALT INFO correct; test -m+ rejoin.
set -uo pipefail
DATA=../../data
for f in edge_multiallelic edge_multiallelic_fixedhdr; do
  echo "== $f : bcftools norm -m-any =="
  bcftools norm -m-any $DATA/$f.vcf 2>/dev/null | grep -v '^##' | cut -f2,4,5,8-
done
echo "== rejoin (-m+any) of the correctly-declared split file =="
bcftools norm -m-any $DATA/edge_multiallelic_fixedhdr.vcf -Oz -o split.vcf.gz 2>/dev/null
bcftools norm -m+any split.vcf.gz 2>/dev/null | grep -v '^##' | cut -f2,4,5,8-
echo "== original =="; grep -v '^##' $DATA/edge_multiallelic_fixedhdr.vcf | cut -f2,4,5,8-
echo "== --keep-sum AD on split =="
bcftools norm -m-any --keep-sum AD $DATA/edge_multiallelic_fixedhdr.vcf 2>/dev/null | grep -v '^#' | cut -f2,4,5,10-
