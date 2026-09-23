#!/usr/bin/env bash
set -euo pipefail
cd /mnt/openscience/audits/bio-experimental-design-batch-design/run/phase2-corrective-20260923
/mnt/openscience/audit-envs/crispr-screen-analyst/tools/designit-linux-runtime/r-designit-sva-linux.sh install_sva_overlay.R
