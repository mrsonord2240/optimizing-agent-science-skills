#!/bin/bash
# Q2: immune question. Each skill given ITS OWN immune gene-set input (bundled tables), same shared matrix.
R=F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/r.sh; D=F:/OpenScience/comparisons/gsva-vs-gsea/data; T=F:/OpenScience/comparisons/_theirs; S=F:/OpenScience/comparisons/gsva-vs-gsea/shim
cd $S/ssgsea-immune-infiltration-analysis && bash $R scripts/main.R --input_file $D/expr.csv --group_file $D/group.csv --gene_set $T/ssgsea-immune-infiltration-analysis/tests/data/immune_gene_sets.csv --case_group Case --control_group Control --output_dir out_q2 --method ssgsea --seed 1 2>&1 | tail -3
cd $S/immune-pathway-analysis && bash $R scripts/main.R --mode full --input_file $D/expr.csv --group_file $D/group.csv --geneset_file $T/immune-pathway-analysis/tests/data/immune_genesets.csv --case_group Case --control_group Control --output_dir out_q2 --seed 1 2>&1 | tail -3
cd $S/gsva-analysis-and-visualization && bash $R scripts/main.R --mode full --input_file $D/expr.csv --group_file $D/group.csv --case_group Case --control_group Control --category C2 --subcategory CP:REACTOME --output_dir out_q2 --seed 1 2>&1 | tail -3
