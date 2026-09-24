#!/usr/bin/env bash
# Run two independent non-HGVSp/edge-case input checks with the local R wrapper.
# Usage: bash reaudit_02_new_inputs.sh
set -euo pipefail

OUT='/f/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/reaudit_new_inputs'
GUARD='/f/OpenScience/external/mrsonord2240__bioSkills/proteomics/ptm-analysis/scripts/cli_windows_cleanup_guard.Rprofile'
mkdir -p "$OUT"
rm -f "$OUT/cli_guard_receipt.txt"
export R_PROFILE_USER="$GUARD"
export CLI_WINDOWS_CLEANUP_GUARD_RECEIPT="$OUT/cli_guard_receipt.txt"
/f/OpenScience/audit-envs/data-visualization/r.sh \
  /f/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/reaudit_02_new_inputs.R \
  'F:/OpenScience/wt/data-visualization-lollipop-protein-maps' \
  'F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/reaudit_new_inputs' \
  2>&1 | tee "$OUT/new_inputs.log"
test -s "$OUT/cli_guard_receipt.txt"
for f in "$OUT"/protein_change_maftools.pdf "$OUT"/protein_change_trackviewer.pdf; do
  test -s "$f"
  pdftotext "$f" - >/dev/null
done
printf 'NEW_INPUTS_SCRIPT_PASS\n'
