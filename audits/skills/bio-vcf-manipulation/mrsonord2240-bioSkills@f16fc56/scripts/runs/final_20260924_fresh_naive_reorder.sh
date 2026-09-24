#!/usr/bin/env bash
set -euo pipefail
src=/mnt/f/OpenScience/audits/bio-vcf-manipulation/runs/p_in2
out=/mnt/f/OpenScience/audits/bio-vcf-manipulation/runs/final_20260924_fresh_naive_reorder
mkdir -p "$out"
order=$(bcftools query -l "$src/chr1.bcf" | paste -sd, -)
bcftools view -s "$order" "$src/chr2_reordered.bcf" -Ob -o "$out/right.bcf"
bcftools concat "$src/chr1.bcf" "$out/right.bcf" -Ob -o "$out/plain.bcf"
plain_records=$(bcftools view -H "$out/plain.bcf" | wc -l)
bcftools view -s "$order" "$src/chr1.bcf" -Ob -o "$out/left.bcf"
bcftools concat --naive "$out/left.bcf" "$out/right.bcf" -Ob -o "$out/naive.bcf"
naive_records=$(bcftools view -H "$out/naive.bcf" | wc -l)
truth=$(bcftools view -H "$src/joint.vcf.gz" | cut -f1-5 | md5sum | cut -d' ' -f1)
plain=$(bcftools view -H "$out/plain.bcf" | cut -f1-5 | md5sum | cut -d' ' -f1)
naive=$(bcftools view -H "$out/naive.bcf" | cut -f1-5 | md5sum | cut -d' ' -f1)
printf 'order=%s\\nplain_records=%s naive_records=%s\\ntruth=%s plain=%s naive=%s\\n' "$order" "$plain_records" "$naive_records" "$truth" "$plain" "$naive"
test "$plain_records" = 361
test "$naive_records" = 361
test "$truth" = "$plain"
test "$truth" = "$naive"
