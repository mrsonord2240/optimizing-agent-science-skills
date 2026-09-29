#!/usr/bin/env bash
set -euo pipefail
root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit2-opt10-20260928
python=/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets/conda-env/bin/python
"$python" "$root/scripts/compare_hyb_pairs.py" "$root/work/hyb-pair-a3" "$root/work/hyb-pair-b3" >"$root/evidence/hyb-repeatability.json"
"$python" "$root/scripts/umi_contract_check.py" >"$root/evidence/umi-contract.json"
"$python" "$root/scripts/targetscan_overlap_check.py" >"$root/evidence/targetscan-contract.json"
"$python" "$root/scripts/candidate_identity.py" >"$root/evidence/candidate-identity-end.json"
