#!/bin/bash
# Input 3 (Edge, post-fix regression 2026-09-15; commands rebuilt from the pre-fix output): "Split the multiallelic sites so
# each ALT is its own record. Our in-house INFO/XAF (one value per ALT) and per-sample AD and PL must stay correct. Can I
# rejoin later with -m+ and get the original back?" Hand-written SYNTHETIC edge files.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data
show() { bcftools query -f '%POS\t%REF\t%ALT\t%INFO/AC;XAF=%INFO/XAF\t[%GT:%AD:%PL\t]\n' "$1" | tr -d '\r'; }
for f in edge_multiallelic edge_multiallelic_fixedhdr; do
  echo "== $f: header XAF $(grep -o 'ID=XAF,Number=[^,]*' $D/$f.vcf) ; bcftools norm -m-any =="
  bcftools norm -m-any $D/$f.vcf -Oz -o $f.split.vcf.gz; bcftools index -f $f.split.vcf.gz; show $f.split.vcf.gz
done
echo "== rejoin (-m+any) of the correctly declared split file =="
bcftools norm -m+any edge_multiallelic_fixedhdr.split.vcf.gz -Oz -o rejoined.vcf.gz; show rejoined.vcf.gz
echo "== original =="; show $D/edge_multiallelic_fixedhdr.vcf
echo "== --keep-sum AD on split =="
bcftools norm -m-any --keep-sum AD $D/edge_multiallelic_fixedhdr.vcf | bcftools query -f '%POS\t%REF\t%ALT\t[%GT:%AD\t]\n' | tr -d '\r'
