#!/usr/bin/env bash
set -euo pipefail

root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit3-opt10-20260928
tooling=/mnt/openscience/audit-envs/bio-clip-seq-ago-clip-mirna-targets
candidate=/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets
env_bin="$tooling/conda-env/bin"
runtime="$tooling/runtime/hyb"
fix_root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/fix-ago009-opt10-20260928
delta_root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/tooling-delta-ago009-opt10-20260928
reaudit2_root=/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit2-opt10-20260928

export PATH="$env_bin:$runtime/bin:/usr/bin:/bin"
export HYB_HOME="$runtime"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p -- "$root/evidence" "$root/work"

"$env_bin/python" "$fix_root/scripts/candidate_identity.py" "$candidate" "$root/candidate-manifest-before.tsv" >"$root/evidence/candidate-identity-before.json"
"$env_bin/python" -c 'import ast,pathlib,sys; [ast.parse(pathlib.Path(p).read_text(encoding="utf-8"),filename=p) for p in sys.argv[1:]]' "$candidate/scripts/consensus_hyb.py" "$candidate/scripts/extract_targeted_umi.py" "$candidate/scripts/targetscan_sites_to_bed12.py" "$candidate/tests/test_scripts.py" >"$root/evidence/syntax-check.stdout" 2>"$root/evidence/syntax-check.stderr"
"$env_bin/python" "$candidate/tests/test_scripts.py" >"$root/evidence/shipped-tests.stdout" 2>"$root/evidence/shipped-tests.stderr"
"$env_bin/python" "$delta_root/scripts/verify_consensus_delta.py" >"$root/evidence/consensus-parser-independent.json" 2>"$root/evidence/consensus-parser-independent.stderr"
"$env_bin/python" "$reaudit2_root/scripts/umi_contract_check.py" >"$root/evidence/umi-contract-independent.json" 2>"$root/evidence/umi-contract-independent.stderr"

bash "$candidate/scripts/run_chimeric_eclip.sh" --reads "$runtime/data/fastq/testdata.txt" --hyb-db hOH7 --run-id reaudit3 --replicates 2 --output-dir "$root/work/workflow-a" --hyb-bin "$runtime/bin/hyb" >"$root/evidence/hyb-pair-a.stdout" 2>"$root/evidence/hyb-pair-a.stderr"
bash "$candidate/scripts/run_chimeric_eclip.sh" --reads "$runtime/data/fastq/testdata.txt" --hyb-db hOH7 --run-id reaudit3 --replicates 2 --output-dir "$root/work/workflow-b" --hyb-bin "$runtime/bin/hyb" >"$root/evidence/hyb-pair-b.stdout" 2>"$root/evidence/hyb-pair-b.stderr"
"$env_bin/python" "$reaudit2_root/scripts/compare_hyb_pairs.py" "$root/work/workflow-a" "$root/work/workflow-b" >"$root/evidence/hyb-repeatability.json"
"$env_bin/python" -c 'import json,pathlib,sys; a,b=[json.loads((pathlib.Path(p)/"manifest.json").read_text()) for p in sys.argv[1:]]; assert a==b and a["hyb"]["commit"]=="028ab6371ce793ca5e86f475fce1f2cc6ad3c677" and a["accepted_rows"]==111 and a["replicates"]==2; print(json.dumps({"pinned_commit":a["hyb"]["commit"],"manifest_equal":a==b,"accepted_rows":a["accepted_rows"],"excluded_rows":a["excluded_rows"],"replicates":a["replicates"],"target_rows":a["target_rows"]},indent=2,sort_keys=True))' "$root/work/workflow-a" "$root/work/workflow-b" >"$root/evidence/hyb-pinned-manifest-check.json"

"$env_bin/python" "$fix_root/scripts/candidate_identity.py" "$candidate" "$root/candidate-manifest-after.tsv" >"$root/evidence/candidate-identity-after.json"
{
  python --version
  bash --version | head -n 1
  bowtie2 --version | head -n 1
  samtools --version | head -n 1
  bedtools --version
  umi_tools --version
  cutadapt --version
  perl -e 'print "Perl $^V\n"'
  make --version | head -n 1
  python -c 'import pysam; print("pysam " + pysam.__version__)'
  printf 'WSL_INTEROP=%s\n' "${WSL_INTEROP-unset}"
  printf 'mnt/f mounted: '; if mountpoint -q /mnt/f; then echo yes; else echo no; fi
  printf 'mnt/openscience mounted: '; if mountpoint -q /mnt/openscience; then echo yes; else echo no; fi
} >"$root/evidence/environment-live.txt" 2>&1
sha256sum "$root/candidate-manifest-before.tsv" "$root/candidate-manifest-after.tsv" "$root/evidence/candidate-identity-before.json" "$root/evidence/candidate-identity-after.json" "$root/evidence/syntax-check.stdout" "$root/evidence/syntax-check.stderr" "$root/evidence/shipped-tests.stdout" "$root/evidence/shipped-tests.stderr" "$root/evidence/consensus-parser-independent.json" "$root/evidence/consensus-parser-independent.stderr" "$root/evidence/umi-contract-independent.json" "$root/evidence/umi-contract-independent.stderr" "$root/evidence/hyb-pair-a.stdout" "$root/evidence/hyb-pair-a.stderr" "$root/evidence/hyb-pair-b.stdout" "$root/evidence/hyb-pair-b.stderr" "$root/evidence/hyb-repeatability.json" "$root/evidence/hyb-pinned-manifest-check.json" "$root/evidence/environment-live.txt" >"$root/evidence/evidence.sha256"
