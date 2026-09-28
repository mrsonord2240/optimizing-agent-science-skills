#!/usr/bin/env bash
set -euo pipefail

root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit-opt10-20260928
tooling=/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets
candidate=/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets
env_bin="$tooling/conda-env/bin"
runtime="$tooling/runtime/hyb"
work="$root/work"
evidence="$root/evidence"

export PATH="$env_bin:$runtime/bin:/usr/bin:/bin"
export HYB_HOME="$runtime"
export PYTHONDONTWRITEBYTECODE=1

mkdir -p -- "$work" "$evidence"

"$env_bin/python" "$candidate/tests/test_scripts.py" \
  >"$evidence/shipped-tests.stdout" 2>"$evidence/shipped-tests.stderr"

"$env_bin/python" "$root/scripts/reaudit_contracts.py" \
  >"$evidence/contract-tests.stdout" 2>"$evidence/contract-tests.stderr"

rm -rf -- "$work/hyb-pair-a" "$work/hyb-pair-b"
bash "$candidate/scripts/run_chimeric_eclip.sh" \
  --reads "$runtime/data/fastq/testdata.txt" \
  --hyb-db hOH7 --run-id reaudit_a --replicates 2 \
  --output-dir "$work/hyb-pair-a" --hyb-bin "$runtime/bin/hyb" \
  >"$evidence/hyb-pair-a.stdout" 2>"$evidence/hyb-pair-a.stderr"
bash "$candidate/scripts/run_chimeric_eclip.sh" \
  --reads "$runtime/data/fastq/testdata.txt" \
  --hyb-db hOH7 --run-id reaudit_b --replicates 2 \
  --output-dir "$work/hyb-pair-b" --hyb-bin "$runtime/bin/hyb" \
  >"$evidence/hyb-pair-b.stdout" 2>"$evidence/hyb-pair-b.stderr"

"$env_bin/python" "$root/scripts/compare_hyb_pairs.py" \
  "$work/hyb-pair-a" "$work/hyb-pair-b" \
  >"$evidence/hyb-repeatability.json"

"$env_bin/python" "$root/scripts/yeo_targeted_check.py" \
  >"$evidence/yeo-targeted-contract.json"

"$env_bin/python" "$root/scripts/targetscan_overlap_check.py" \
  >"$evidence/targetscan-contract.json"

