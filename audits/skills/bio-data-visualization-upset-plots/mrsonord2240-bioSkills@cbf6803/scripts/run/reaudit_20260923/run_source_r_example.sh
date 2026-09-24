#!/usr/bin/env bash
# Run the exact committed R example directly, from an isolated writable output directory.
set -euo pipefail
source_file='F:/OpenScience/wt/data-visualization-upset-plots/data-visualization/upset-plots/examples/upset_gene_sets.R'
out_dir='F:/OpenScience/audits/bio-data-visualization-upset-plots/run/reaudit_20260923/out/r_example'
cd "$out_dir"
exec 'F:/OpenScience/audit-envs/data-visualization/r.sh' "$source_file"
