#!/usr/bin/env bash
set -euo pipefail
root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit2-opt10-20260928
python=/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets/conda-env/bin/python
"$python" "$root/scripts/secondary_routes_check.py" >"$root/evidence/secondary-routes.json" 2>"$root/evidence/secondary-routes.stderr"
