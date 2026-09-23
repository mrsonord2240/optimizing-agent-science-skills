#!/usr/bin/env bash
# Fresh documented PICRUSt2 2.6.3 run. The drifted shared environment was
# rejected; this isolated exact-version environment confirms the shipped -p flag.
set -euo pipefail
OUT=/mnt/openscience/audits/bio-microbiome-functional-prediction/work/p2-final-20260923
eval "$(micromamba shell hook --shell bash)" 2>/dev/null
micromamba activate picrust2-263-p2
cd "$OUT"
picrust2_pipeline.py --help 2>&1 | grep -F -- '-p PROCESSES, --processes PROCESSES'
picrust2_pipeline.py -s asv_seqs.fna -i asv_table.tsv -o picrust2_out_documented -p 4 --hsp_method mp --max_nsti 2 --verbose > picrust2_documented.log 2>&1
add_descriptions.py -i picrust2_out_documented/pathways_out/path_abun_unstrat.tsv.gz -m METACYC -o picrust2_out_documented/pathways_out/path_abun_described.tsv.gz >> picrust2_documented.log 2>&1
test -s picrust2_out_documented/combined_marker_predicted_and_nsti.tsv.gz
test -s picrust2_out_documented/KO_metagenome_out/pred_metagenome_unstrat.tsv.gz
test -s picrust2_out_documented/EC_metagenome_out/pred_metagenome_unstrat.tsv.gz
test -s picrust2_out_documented/pathways_out/path_abun_unstrat.tsv.gz
gzip -cd picrust2_out_documented/pathways_out/path_abun_unstrat.tsv.gz | awk 'END { if (NR < 2) exit 1; print "pathway_table_rows=" NR-1 }'
tail -n 30 picrust2_documented.log
