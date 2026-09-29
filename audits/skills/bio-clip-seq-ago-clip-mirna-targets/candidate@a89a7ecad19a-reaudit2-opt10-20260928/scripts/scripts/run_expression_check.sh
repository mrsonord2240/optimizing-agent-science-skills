#!/usr/bin/env bash
set -euo pipefail
root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit2-opt10-20260928
python=/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets/conda-env/bin/python
"$python" "$root/scripts/expression_finite_check.py" >"$root/evidence/expression-nan-check.json" 2>"$root/evidence/expression-nan-check.stderr"
