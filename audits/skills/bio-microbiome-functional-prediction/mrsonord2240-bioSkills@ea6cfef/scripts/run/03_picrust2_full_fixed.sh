#!/bin/bash
# Re-audit: independent fresh full PICRUSt2 run (own output dir, not the original audit's
# picrust2_out_real) on the comment-line-stripped table, to produce a genuinely fresh
# combined_marker_predicted_and_nsti.tsv.gz for the corrected SKILL.md NSTI snippet to read.
set -uo pipefail

WORK=/mnt/openscience/audits/bio-microbiome-functional-prediction/work
cd "$WORK"

eval "$(micromamba shell hook --shell bash)" 2>/dev/null
micromamba activate picrust2

tail -n +2 exported-table/feature-table.tsv > asv_table_fixed.tsv
wc -l asv_table_fixed.tsv

time picrust2_pipeline.py \
    -s asv_seqs.fna \
    -i asv_table_fixed.tsv \
    -o picrust2_out_reaudit \
    -p 4 \
    --hsp_method mp \
    --max_nsti 2 \
    --verbose > picrust2_reaudit_run.log 2>&1
echo "EXIT_CODE=$?" >> picrust2_reaudit_run.log
tail -60 picrust2_reaudit_run.log

add_descriptions.py \
    -i picrust2_out_reaudit/pathways_out/path_abun_unstrat.tsv.gz \
    -m METACYC \
    -o picrust2_out_reaudit/pathways_out/path_abun_described.tsv.gz
echo "add_descriptions EXIT_CODE=$?"

ls -la picrust2_out_reaudit/ picrust2_out_reaudit/pathways_out/ 2>&1
