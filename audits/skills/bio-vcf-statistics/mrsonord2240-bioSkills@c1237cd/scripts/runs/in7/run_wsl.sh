#!/bin/bash
# WSL part of input 7: shipped examples/vcf_stats.py (fork commit copy) with cyvcf2 0.34.0 on the raw and soft-filtered files.
set -uo pipefail
cd "$(dirname "$0")"
export PATH=/tmp/vaca/env/bin:$PATH
for f in cohort marked; do
  echo "== examples/vcf_stats.py $f.vcf.gz =="; python vcf_stats.fork_copy.py $f.vcf.gz | grep -E "Total|PASS|Filtered"; echo "exit=${PIPESTATUS[0]}"
done
