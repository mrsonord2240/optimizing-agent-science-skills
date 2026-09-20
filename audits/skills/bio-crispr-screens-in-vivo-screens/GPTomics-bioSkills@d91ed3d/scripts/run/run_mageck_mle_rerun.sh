#!/bin/bash
set -e
export PATH="/f/OpenScience/audit-envs/crispr-screen-analyst/bin:/f/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/mageck-0.5.9.5/bin:$PATH"
cd "F:\OpenScience\audits\bio-crispr-screens-in-vivo-screens\run"
PY="F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe"
MAGECK="F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\mageck"
mkdir -p mle_rerun
timeout 90 "$PY" "$MAGECK" mle --count-table in_vivo_counts.txt --design-matrix in_vivo_design.txt --output-prefix mle_rerun/in_vivo_mle > mle_rerun/mle_run2.log 2>&1
echo "exit: $?"
diff in_vivo_mle.gene_summary.txt mle_rerun/in_vivo_mle.gene_summary.txt && echo "IDENTICAL" || echo "DIFFERS (see diff above)"
