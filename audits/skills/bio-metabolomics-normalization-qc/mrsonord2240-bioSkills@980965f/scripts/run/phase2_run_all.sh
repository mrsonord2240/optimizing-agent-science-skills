#!/bin/bash
# Fresh Phase 2 evidence run: all nine inherited regressions and both newly authored inputs.
set -euo pipefail
root=/f/OpenScience/audits/bio-metabolomics-normalization-qc/run
rs=/f/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh
{
  echo '=== Phase 2 fresh execution: 2026-09-23 ==='
  "$rs" "$root/input1_canonical.R"
  "$rs" "$root/input2_variantA.R"
  "$rs" "$root/input3_variantB.R"
  "$rs" "$root/input4_edge.R"
  "$rs" "$root/input5_stress.R"
  "$rs" "$root/input6_scope_boundary.R"
  "$rs" "$root/input7_adversarial.R"
  "$rs" "$root/input8_new_guard_stress.R"
  "$rs" "$root/input9_new_pqn_se_path.R"
  "$rs" "$root/input10_robust_dratio_prepare.R"
  "$root/input10_robust_dratio_cli.sh"
  "$root/input11_example_regression.sh"
} 2>&1 | tee "$root/phase2_execution.log"
