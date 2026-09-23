#!/usr/bin/env bash
set -euo pipefail
root="F:/OpenScience/audits/bio-causal-genomics-colocalization-analysis/run"
"F:/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh" "$root/parse_all_r_sources.R" "$root/skill_snapshot" > "$root/parse_all_r_sources_output.txt" 2>&1
