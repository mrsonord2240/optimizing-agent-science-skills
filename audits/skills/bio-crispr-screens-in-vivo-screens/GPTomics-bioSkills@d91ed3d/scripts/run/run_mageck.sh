#!/bin/bash
set -e
export PATH="/f/OpenScience/audit-envs/crispr-screen-analyst/bin:/f/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/mageck-0.5.9.5/bin:$PATH"
cd "F:\OpenScience\audits\bio-crispr-screens-in-vivo-screens\run"
PY="F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe"
MAGECK="F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\mageck"
rm -rf mageck_out mageck_out_rerun
mkdir -p mageck_out mageck_out_rerun
for a in 1 2 3 4 5 6; do
  "$PY" "$MAGECK" test -k in_vivo_counts.txt -t Animal$a -c Plasmid -n mageck_out/animal_$a > mageck_out/animal_${a}_run1.log 2>&1
done
echo "RUN1 done"
ls mageck_out/*.gene_summary.txt
