#!/usr/bin/env bash
set -euo pipefail
OUT=/mnt/openscience/audits/bio-vcf-statistics/reaudit-ffa74e9-20260927/outputs
grep '^SN' "$OUT/input1_cohort.stats.txt"
echo '--- independent per-sample het count via bcftools query (SNP+indel, all GT forms) ---'
bcftools query -f '[%SAMPLE\t%GT\n]' "$OUT/cohort.vcf.gz" \
  | awk -F'\t' '$2 ~ /^(0[\/|]1|1[\/|]0)$/ {c[$1]++} END {for (k in c) print k, c[k]}' \
  | sort > "$OUT/input8_query_het_by_sample.txt"
cat "$OUT/input8_query_het_by_sample.txt"
echo '--- diff vs cyvcf2 snippet ---'
if diff "$OUT/input8_query_het_by_sample.txt" "$OUT/input8_snippet_het_by_sample.txt"; then
  echo IDENTICAL
else
  echo DIFFERS
fi
echo '--- diff vs bcftools PSC nHets (expected to differ: PSC excludes het indels) ---'
diff "$OUT/input8_psc_het_by_sample.txt" "$OUT/input8_query_het_by_sample.txt" || true
