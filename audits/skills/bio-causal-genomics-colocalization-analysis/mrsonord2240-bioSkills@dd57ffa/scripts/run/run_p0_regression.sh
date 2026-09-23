#!/usr/bin/env bash
set -euo pipefail
root="F:/OpenScience/audits/bio-causal-genomics-colocalization-analysis/run"
bash "$root/skill_snapshot/scripts/test_coloc_susie_eqtl_ld_guard.sh" \
  "F:/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh" \
  "$root/skill_snapshot/scripts/test_coloc_susie_eqtl_ld_guard.R" \
  "$root/skill_snapshot/scripts/coloc_susie.R" \
  > "$root/p0_eqtl_ld_guard_output.txt" 2>&1
grep -Fqx 'PASS: eQTL LD mismatch rejected (lambda=1.000000) before coloc output' "$root/p0_eqtl_ld_guard_output.txt"
