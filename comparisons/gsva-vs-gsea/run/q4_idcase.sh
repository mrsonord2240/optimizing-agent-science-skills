#!/bin/bash
# Failure-mode probe: expression matrix with lower-case gene symbols (namespace mismatch).
R=F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/r.sh; D=F:/OpenScience/comparisons/gsva-vs-gsea/data; S=F:/OpenScience/comparisons/gsva-vs-gsea/shim
cd $S/gsva-analysis-and-visualization && bash $R scripts/main.R --mode analyze --input_file $D/expr_lowercase_genes.csv --group_file $D/group.csv --case_group Case --control_group Control --category C2 --subcategory CP:KEGG_LEGACY --output_dir out_q4 2>&1 | tail -2
cd $S/immune-pathway-analysis && bash $R scripts/main.R --mode analyze --input_file $D/expr_lowercase_genes.csv --group_file $D/group.csv --geneset_file $D/kegg_table.csv --case_group Case --control_group Control --output_dir out_q4 2>&1 | tail -2
cd $S/ssgsea-immune-infiltration-analysis && bash $R scripts/main.R --input_file $D/expr_lowercase_genes.csv --group_file $D/group.csv --gene_set $D/kegg_as_celltype.csv --case_group Case --control_group Control --output_dir out_q4 --make_plots false 2>&1 | tail -2
ls $S/ssgsea-immune-infiltration-analysis/out_q4/table 2>/dev/null | head -3
