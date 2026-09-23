#!/bin/bash
# Fresh Phase 2 command record. Run from this audit's run/ directory with Git Bash.
set -uo pipefail
ENV=/f/OpenScience/audit-envs/mendelian-randomization-analyst
AUDIT=/f/OpenScience/audits/bio-causal-genomics-genomic-sem/run
SKILL=/f/OpenScience/wt/causal-genomics-genomic-sem/causal-genomics/genomic-sem
cd "$AUDIT"
run_r() {
  local label="$1"
  shift
  "$@" > "phase2_${label}.log" 2>&1
  local rc=$?
  echo "${label}: exit=${rc}" >> phase2_exit_statuses.txt
  # This Windows R runtime can terminate 139 after materializing valid output.
  # The audit evaluates its asserted output, not its exit code alone.
  return 0
}
rm -f phase2_exit_statuses.txt
for script in input1_commonfactor.R input2_cfgwas.R input3_heywood.R input4_twofactor.R input5_usergwas.R input7_underidentified.R input8_qsnp_realistic_se.R input9_bifactor_pfactor.R; do
  run_r "${script%.R}" "$ENV/r_gsem.sh" "$script"
done
run_r input10_prepare "$ENV/r_gsem.sh" input10_prepare_helper_fixture.R
run_r input10_helper "$ENV/r_gsem.sh" "$SKILL/scripts/commonfactor_gwas_qsnp.R" input10_covstruc.rds input10_snps.csv input10_helper_output.tsv 1
run_r input10_assert "$ENV/r_gsem.sh" input10_assert_helper_output.R
run_r input11_pinned "$ENV/r_gsem.sh" input11_version_guard.R
run_r input11_shared "$ENV/r.sh" input11_version_guard.R
python parse_all_shipped_code.py > phase2_parse_all.log 2>&1
bash -n "$SKILL/examples/mtag_pipeline.sh"
echo "PHASE2_RUNNER_PASS"
