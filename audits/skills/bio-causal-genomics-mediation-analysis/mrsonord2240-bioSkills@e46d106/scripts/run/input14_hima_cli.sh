#!/bin/bash
# Phase 2 fresh input: invoke scripts/hima_ewas.R exactly through the documented CLI form.
set -euo pipefail
RSH=/f/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh
AUDIT=/f/OpenScience/audits/bio-causal-genomics-mediation-analysis
SKILL=/f/OpenScience/wt/causal-genomics-mediation-analysis/causal-genomics/mediation-analysis
"$RSH" "$AUDIT/run/input14_make_hima_cli_data.R"
"$RSH" "$SKILL/scripts/hima_ewas.R" "$AUDIT/data/input14_pheno.csv" "$AUDIT/data/input14_mediators.csv" "outcome ~ exposure + age + sex + batch" "$AUDIT/data/input14_hima_output.csv" gaussian DBlasso 0.05 1
test -f "$AUDIT/data/input14_hima_output.csv"
"$RSH" -e 'x <- read.csv("F:/OpenScience/audits/bio-causal-genomics-mediation-analysis/data/input14_hima_output.csv"); cat("output_rows=", nrow(x), "\n"); stopifnot(all(c("ID") %in% names(x)))'
echo "ASSERT PASS: CLI wrote a parseable result table after NA alignment and batch dummy coding."
