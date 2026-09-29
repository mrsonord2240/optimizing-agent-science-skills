#!/usr/bin/env bash
set -euo pipefail
root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit3-opt10-20260928
old=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit2-opt10-20260928/scripts
tooling=/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets
export PATH="$tooling/conda-env/bin:$PATH"
export PYTHONDONTWRITEBYTECODE=1
python "$old/targetscan_overlap_check.py" >"$root/evidence/targetscan-contract-independent.json" 2>"$root/evidence/targetscan-contract-independent.stderr"
python "$old/secondary_routes_check.py" >"$root/evidence/secondary-routes-independent.json" 2>"$root/evidence/secondary-routes-independent.stderr"
sha256sum "$root/evidence/targetscan-contract-independent.json" "$root/evidence/targetscan-contract-independent.stderr" "$root/evidence/secondary-routes-independent.json" "$root/evidence/secondary-routes-independent.stderr" >>"$root/evidence/evidence.sha256"
