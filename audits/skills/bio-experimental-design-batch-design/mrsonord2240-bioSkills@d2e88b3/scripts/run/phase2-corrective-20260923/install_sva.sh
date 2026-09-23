#!/usr/bin/env bash
# Provision SVA in the already-isolated Linux designit runtime, never in Windows R-lib.
set -euo pipefail
root="/mnt/openscience/audit-envs/crispr-screen-analyst/tools/designit-linux-runtime"
"$root/r-designit-linux.sh" "$root/install_sva.R"
