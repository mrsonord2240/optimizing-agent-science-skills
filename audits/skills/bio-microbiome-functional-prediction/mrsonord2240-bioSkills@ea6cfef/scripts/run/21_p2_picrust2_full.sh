#!/usr/bin/env bash
# Fresh PICRUSt2 2.6.3 execution of the central documented workflow.
set -euo pipefail
OUT=/mnt/openscience/audits/bio-microbiome-functional-prediction/work/p2-final-20260923
eval "$(micromamba shell hook --shell bash)" 2>/dev/null
micromamba activate picrust2
cd "$OUT"
picrust2_pipeline.py -s asv_seqs.fna -i asv_table.tsv -o picrust2_out -p 4 --hsp_method mp --max_nsti 2 --verbose > picrust2.log 2>&1
add_descriptions.py -i picrust2_out/pathways_out/path_abun_unstrat.tsv.gz -m METACYC -o picrust2_out/pathways_out/path_abun_described.tsv.gz >> picrust2.log 2>&1
test -s picrust2_out/combined_marker_predicted_and_nsti.tsv.gz
test -s picrust2_out/KO_metagenome_out/pred_metagenome_unstrat.tsv.gz
test -s picrust2_out/EC_metagenome_out/pred_metagenome_unstrat.tsv.gz
test -s picrust2_out/pathways_out/path_abun_unstrat.tsv.gz
gzip -cd picrust2_out/pathways_out/path_abun_unstrat.tsv.gz | awk 'END { if (NR < 2) exit 1; print "pathway_table_rows=" NR-1 }'
tail -n 30 picrust2.log
