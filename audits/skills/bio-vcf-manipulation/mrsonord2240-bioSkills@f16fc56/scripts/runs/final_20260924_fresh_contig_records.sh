#!/usr/bin/env bash
set -euo pipefail
src=/mnt/f/OpenScience/audits/bio-vcf-manipulation/runs/p_in5
out=/mnt/f/OpenScience/audits/bio-vcf-manipulation/runs/final_20260924_fresh_contig_records
mkdir -p "$out"
bcftools reheader -f /mnt/f/OpenScience/audits/bio-vcf-manipulation/data/ref.fa.fai "$src/b2_names.vcf.gz" -o "$out/header_only.vcf.gz"
header_only_chroms=$(bcftools view -H "$out/header_only.vcf.gz" | cut -f1 | sort -u | paste -sd, -)
bcftools annotate --rename-chrs "$src/to_ucsc.txt" "$src/b2_names.vcf.gz" -Oz -o "$out/records_renamed.vcf.gz"
bcftools index -f "$out/records_renamed.vcf.gz"
bcftools merge "$src/batch1.vcf.gz" "$out/records_renamed.vcf.gz" -Oz -o "$out/merged.vcf.gz"
merged_sites=$(bcftools view -H "$out/merged.vcf.gz" | wc -l)
merged_samples=$(bcftools query -l "$out/merged.vcf.gz" | wc -l)
truth=$(bcftools view -H "$src/joint.vcf.gz" | cut -f1-5 | md5sum | cut -d' ' -f1)
merged=$(bcftools view -H "$out/merged.vcf.gz" | cut -f1-5 | md5sum | cut -d' ' -f1)
printf 'header_only_record_chroms=%s\\nmerged_sites=%s merged_samples=%s\\ntruth=%s merged=%s\\n' "$header_only_chroms" "$merged_sites" "$merged_samples" "$truth" "$merged"
test "$header_only_chroms" = '1,2'
test "$merged_sites" = 361
test "$merged_samples" = 8
test "$truth" = "$merged"
