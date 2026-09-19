#!/usr/bin/env bash
cd /home/sci/audit_bio_microbiome_diversity_analysis_20260919/exported
for d in wu_permanova_viz uwu_permanova_viz bc_permanova_viz wu_permdisp_viz uwu_permdisp_viz bc_permdisp_viz; do
  echo "=== $d ==="
  grep -A2 -i 'method name\|test statistic name\|sample size\|test statistic\|p-value\|number of groups' $d/index.html | sed -e 's/<[^>]*>//g' | grep -v '^[[:space:]]*$'
  echo
done
