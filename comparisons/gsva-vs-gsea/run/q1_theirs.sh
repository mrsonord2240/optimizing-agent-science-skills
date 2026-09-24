#!/bin/bash
# Q1: KEGG pathway-level Case vs Control, three Open Science skills (shimmed copies; GSVA 2.0.7)
R=F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/r.sh; D=F:/OpenScience/comparisons/gsva-vs-gsea/data; S=F:/OpenScience/comparisons/gsva-vs-gsea/shim
cd $S/gsva-analysis-and-visualization && bash $R scripts/main.R --mode full --input_file $D/expr.csv --group_file $D/group.csv --case_group Case --control_group Control --category C2 --subcategory CP:KEGG_LEGACY --output_dir out_q1 --seed 1 2>&1 | tail -6
cd $S/immune-pathway-analysis && bash $R scripts/main.R --mode full --input_file $D/expr.csv --group_file $D/group.csv --geneset_file $D/kegg_table.csv --case_group Case --control_group Control --max_sz 500 --output_dir out_q1 --seed 1 2>&1 | tail -6
cd $S/ssgsea-immune-infiltration-analysis && bash $R scripts/main.R --input_file $D/expr.csv --group_file $D/group.csv --gene_set $D/kegg_as_celltype.csv --case_group Case --control_group Control --output_dir out_q1 --method ssgsea --seed 1 2>&1 | tail -6
