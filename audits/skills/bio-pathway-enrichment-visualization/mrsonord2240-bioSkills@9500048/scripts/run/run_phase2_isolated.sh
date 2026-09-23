#!/usr/bin/env bash
set -uo pipefail

export R_LIBS_USER=/home/sci/.local/share/openscience-pathway-enrichment-r-20260923
export R_LIBS="$R_LIBS_USER"
cd /mnt/openscience/audits/bio-pathway-enrichment-visualization/run

scripts=(
  prep_data.R
  input1_canonical.R
  input2_variantA.R
  input3_edge.R
  input4_variantB.R
  input5_stress.R
  input6_scope.R
  input7_redundancy_check.R
  check_single_term.R
  check_treeplot_current_api.R
  shipped_visualization_ora_phase2.R
  shipped_visualization_gsea_phase2.R
)

status=0
for script in "${scripts[@]}"; do
  /usr/bin/Rscript --vanilla "$script" > "${script}.phase2.log" 2>&1
  rc=$?
  printf '%s\n' "$rc" > "${script}.phase2.exit"
  printf '%s exit=%s\n' "$script" "$rc"
  if [[ "$rc" -ne 0 ]]; then status=1; fi
done
exit "$status"
