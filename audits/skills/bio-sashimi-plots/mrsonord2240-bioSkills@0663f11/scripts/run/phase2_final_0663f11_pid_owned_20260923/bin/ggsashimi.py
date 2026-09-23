#!/usr/bin/env bash
set -euo pipefail
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
exec asenv as-viz-gg34 python /mnt/openscience/audit-envs/alternative-splicing/tools/src/ggsashimi/ggsashimi.py "$@"
