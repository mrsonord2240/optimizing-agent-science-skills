#!/bin/bash
# Re-run with the biom-export comment line stripped from the ASV table (see
# picrust2_real_run.log from run 03: the raw `biom convert --to-tsv` output's leading
# "# Constructed from biom file" line breaks picrust2's metagenome_pipeline.py table
# parser -- AFTER placement/HSP had already run for 9m25s. This is a real, reproducible
# finding: the Skill's Common Errors table does not warn about this.
set -uo pipefail

WORK=/mnt/openscience/audits/bio-microbiome-functional-prediction/work
cd "$WORK"

eval "$(micromamba shell hook --shell bash)"
micromamba activate picrust2

time picrust2_pipeline.py \
    -s exported-rep-seqs/dna-sequences.fasta \
    -i asv_table_fixed.tsv \
    -o picrust2_out_real \
    -p 4 \
    --hsp_method mp \
    --max_nsti 2 \
    --verbose > picrust2_real_run_fixed.log 2>&1
echo "EXIT_CODE=$?" >> picrust2_real_run_fixed.log
tail -60 picrust2_real_run_fixed.log

add_descriptions.py \
    -i picrust2_out_real/pathways_out/path_abun_unstrat.tsv.gz \
    -m METACYC \
    -o picrust2_out_real/pathways_out/path_abun_described.tsv.gz
echo "add_descriptions EXIT_CODE=$?"

ls -la picrust2_out_real/ picrust2_out_real/pathways_out/ picrust2_out_real/KO_metagenome_out/ 2>&1
