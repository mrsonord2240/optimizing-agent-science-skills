#!/usr/bin/env bash
set -uo pipefail

base_lib=/home/sci/.local/share/openscience-pathway-enrichment-r-20260923
overlay=/home/sci/.local/share/openscience-pathway-enrichment-phase2-overlay-20260923
export R_LIBS_USER="$overlay:$base_lib"
export R_LIBS="$R_LIBS_USER"
cd /mnt/openscience/audits/bio-pathway-enrichment-visualization/run

/usr/bin/Rscript --vanilla install_phase2_ggupset.R > install_phase2_ggupset.log 2>&1
install_rc=$?
printf '%s\n' "$install_rc" > install_phase2_ggupset.exit
printf 'install_phase2_ggupset.R exit=%s\n' "$install_rc"

/usr/bin/Rscript --vanilla input5_stress.R > input5_stress.R.phase2_overlay.log 2>&1
run_rc=$?
printf '%s\n' "$run_rc" > input5_stress.R.phase2_overlay.exit
printf 'input5_stress.R overlay exit=%s\n' "$run_rc"

if [[ "$install_rc" -ne 0 || "$run_rc" -ne 0 ]]; then
  exit 1
fi
