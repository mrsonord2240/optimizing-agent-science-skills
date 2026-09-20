#!/bin/bash
set -e
export PATH="/f/OpenScience/audit-envs/crispr-screen-analyst/bin:/f/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/mageck-0.5.9.5/bin:$PATH"
cd "F:\OpenScience\audits\bio-crispr-screens-in-vivo-screens\run"
PY="F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe"
MAGECK="F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\mageck"
timeout 90 "$PY" "$MAGECK" mle --count-table in_vivo_counts.txt --design-matrix in_vivo_design.txt --output-prefix in_vivo_mle > mle_run1.log 2>&1
echo "exit: $?"
tail -20 mle_run1.log
ls in_vivo_mle* 2>&1
