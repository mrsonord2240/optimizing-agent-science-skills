#!/usr/bin/env bash
set -uo pipefail

export R_LIBS_USER=/home/sci/.local/share/openscience-pathway-enrichment-r-20260923
export R_LIBS="$R_LIBS_USER"
cd /mnt/openscience/audits/bio-pathway-enrichment-visualization/run

scripts=(
  check_treeplot_current_api.R
  shipped_visualization_ora_fixed.R
  shipped_visualization_gsea_fixed.R
)

status=0
for script in "${scripts[@]}"; do
  /usr/bin/Rscript --vanilla "$script" > "${script}.corrective.log" 2>&1
  rc=$?
  printf '%s\n' "$rc" > "${script}.corrective.exit"
  printf '%s exit=%s\n' "$script" "$rc"
  if [[ "$rc" -ne 0 ]]; then status=1; fi
done
exit "$status"
