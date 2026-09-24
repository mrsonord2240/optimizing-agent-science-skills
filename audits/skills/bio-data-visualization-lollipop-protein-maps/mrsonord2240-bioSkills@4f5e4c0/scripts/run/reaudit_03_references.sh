#!/usr/bin/env bash
# Run reference and package-semantics checks under the disposable cleanup guard.
# Usage: bash reaudit_03_references.sh
set -euo pipefail

OUT='/f/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/reaudit_references'
GUARD='/f/OpenScience/external/mrsonord2240__bioSkills/proteomics/ptm-analysis/scripts/cli_windows_cleanup_guard.Rprofile'
mkdir -p "$OUT"
rm -f "$OUT/cli_guard_receipt.txt"
export R_PROFILE_USER="$GUARD"
export CLI_WINDOWS_CLEANUP_GUARD_RECEIPT="$OUT/cli_guard_receipt.txt"
/f/OpenScience/audit-envs/data-visualization/r.sh \
  /f/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/reaudit_03_references.R \
  'F:/OpenScience/wt/data-visualization-lollipop-protein-maps' \
  'F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/reaudit_references' \
  2>&1 | tee "$OUT/references.log"
printf 'REFERENCES_SCRIPT_PASS\n'
