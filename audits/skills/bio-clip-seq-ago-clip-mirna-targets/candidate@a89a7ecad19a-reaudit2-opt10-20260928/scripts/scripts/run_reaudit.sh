#!/usr/bin/env bash
set -euo pipefail

root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit2-opt10-20260928
tooling=/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets
candidate=/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets
env_bin="$tooling/conda-env/bin"
runtime="$tooling/runtime/hyb"

export PATH="$env_bin:$runtime/bin:/usr/bin:/bin"
export HYB_HOME="$runtime"
export PYTHONDONTWRITEBYTECODE=1

mkdir -p -- "$root/evidence" "$root/inputs"

"$env_bin/python" "$root/scripts/candidate_identity.py" >"$root/evidence/candidate-identity-start.json"

"$env_bin/python" "$candidate/tests/test_scripts.py" \
  >"$root/evidence/shipped-tests.stdout" 2>"$root/evidence/shipped-tests.stderr"

"$env_bin/python" "$root/scripts/reaudit_contracts.py" \
  >"$root/evidence/contract-tests.stdout" 2>"$root/evidence/contract-tests.stderr"

bash "$candidate/scripts/run_chimeric_eclip.sh" \
  --reads "$runtime/data/fastq/testdata.txt" \
  --hyb-db hOH7 --run-id reaudit2 --replicates 2 \
  --output-dir "$root/work/hyb-pair-a3" --hyb-bin "$runtime/bin/hyb" \
  >"$root/evidence/hyb-pair-a.stdout" 2>"$root/evidence/hyb-pair-a.stderr"
bash "$candidate/scripts/run_chimeric_eclip.sh" \
  --reads "$runtime/data/fastq/testdata.txt" \
  --hyb-db hOH7 --run-id reaudit2 --replicates 2 \
  --output-dir "$root/work/hyb-pair-b3" --hyb-bin "$runtime/bin/hyb" \
  >"$root/evidence/hyb-pair-b.stdout" 2>"$root/evidence/hyb-pair-b.stderr"

"$env_bin/python" "$root/scripts/compare_hyb_pairs.py" \
  "$root/work/hyb-pair-a3" "$root/work/hyb-pair-b3" \
  >"$root/evidence/hyb-repeatability.json"

"$env_bin/python" "$root/scripts/umi_contract_check.py" \
  >"$root/evidence/umi-contract.json"
"$env_bin/python" "$root/scripts/targetscan_overlap_check.py" \
  >"$root/evidence/targetscan-contract.json"

