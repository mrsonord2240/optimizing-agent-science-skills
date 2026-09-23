#!/usr/bin/env bash
# Fresh regression of the documented all-poor-alignment hard-abort distinction.
set -uo pipefail
OUT=/mnt/openscience/audits/bio-microbiome-functional-prediction/work/p2-final-20260923/synthetic-edge
OLD=/mnt/openscience/audits/_pre-fix-20260923/bio-microbiome-functional-prediction/work/synthetic-edge
mkdir -p "$OUT"
cp "$OLD/asv_seqs.fna" "$OUT/asv_seqs.fna"
cp "$OLD/asv_table.tsv" "$OUT/asv_table.tsv"
eval "$(micromamba shell hook --shell bash)" 2>/dev/null
micromamba activate picrust2-263-p2
cd "$OUT"
picrust2_pipeline.py -s asv_seqs.fna -i asv_table.tsv -o picrust2_out -p 4 --hsp_method mp --max_nsti 2 --verbose > run.log 2>&1
code=$?
cat run.log
printf 'pipeline_exit_code=%s\n' "$code"
grep -F 'all 11 input sequences aligned poorly to reference sequences' run.log
test ! -e picrust2_out/combined_marker_predicted_and_nsti.tsv.gz
exit 0
