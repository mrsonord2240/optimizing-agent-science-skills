#!/bin/bash
set -e
export PATH="/f/OpenScience/audit-envs/crispr-screen-analyst/bin:/f/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/mageck-0.5.9.5/bin:$PATH"
cd "F:\OpenScience\audits\bio-crispr-screens-in-vivo-screens\run"
PY="F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe"
MAGECK="F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\mageck"
"$PY" "$MAGECK" test -k in_vivo_counts.txt -t Animal1 -c Plasmid -n mageck_out_rerun/animal_1 > mageck_out_rerun/animal_1_run2.log 2>&1
diff mageck_out/animal_1.gene_summary.txt mageck_out_rerun/animal_1.gene_summary.txt && echo "IDENTICAL - deterministic" || echo "DIFFERS"
