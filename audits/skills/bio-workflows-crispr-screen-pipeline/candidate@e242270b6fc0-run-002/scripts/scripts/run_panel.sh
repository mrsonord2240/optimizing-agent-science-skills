#!/bin/bash
set -u
export PATH=/f/OpenScience/audit-envs/crispr-screen-analyst/Scripts:$PATH
SK=/f/OpenScience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline
D=/f/OpenScience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline
T=/f/OpenScience/audit-envs/crispr-screen-analyst/tools
R=$(pwd)/work
# jacks: literal command from JACKS clone root (route says run_JACKS.py)
mkdir -p $R/jacks_literal; cd $R/jacks_literal
cp $D/jacks/* .
(cd $T/dl/JACKS && ls run_JACKS.py 2>&1 | head -1)
python run_JACKS.py panel.count.txt replicatemap.txt guidemap.txt --rep_hdr Replicate --sample_hdr Sample --ctrl_sample_hdr Control --sgrna_hdr sgRNA --gene_hdr Gene --outprefix jacks_out --apply_w_hp > log 2>&1; echo "jacks literal exit $?"
mkdir -p $R/jacks; cd $R/jacks; cp $D/jacks/* .
python $T/dl/JACKS/jacks/run_JACKS.py panel.count.txt replicatemap.txt guidemap.txt --rep_hdr Replicate --sample_hdr Sample --ctrl_sample_hdr Control --sgrna_hdr sgRNA --gene_hdr Gene --outprefix jacks_out --apply_w_hp > log 2>&1; echo "jacks exit $?"
# chronos literal snippet
mkdir -p $R/chronos_literal; cd $R/chronos_literal; cp $D/chronos/* .
cat > literal.py <<'PY'
import chronos, pandas as pd
c = pd.read_csv('panel.count.txt', sep='\t')
cols=list(c.columns[2:])
counts=c.set_index('sgRNA')[cols].T; counts.index.name='sequence_ID'
sequence_map=pd.DataFrame({'sequence_ID':cols,'cell_line':[x.split('_')[0] for x in cols],'days':14})
guide_gene_map=c[['sgRNA','Gene']].rename(columns={'sgRNA':'sgrna','Gene':'gene'})
counts_df=counts
model = chronos.Chronos(sequence_map={'screen': sequence_map},
                        guide_gene_map={'screen': guide_gene_map},
                        readcounts={'screen': counts_df})
model.train(nepochs=301)
gene_effects = model.gene_effect
PY
$T/chronos-venv/Scripts/python.exe literal.py > log 2>&1; echo "chronos literal exit $?"; tail -3 log
# chronos working (tooling script, copied to scripts/)
mkdir -p $R/chronos; cd $R/chronos; cp $D/chronos/* .; cp /f/OpenScience/fix-evidence/recut-crispr-pipeline/tooling/chronos/run_chronos.py .
$T/chronos-venv/Scripts/python.exe run_chronos.py > log 2>&1; echo "chronos exit $?"; tail -4 log
# consensus
mkdir -p $R/consensus; cd $R/consensus
python $SK/scripts/consensus.py tier_consensus.csv mageck=$D/consensus/essentiality_rra.gene_summary.txt bagel=$D/consensus/bayes_factor.txt drugz=$D/consensus/drugz_output.txt > log 2>&1; echo "consensus exit $?"; tail -5 log
# consensus on this-run outputs (two methods; 
mkdir -p $R/consensus_run; cd $R/consensus_run
python $SK/scripts/consensus.py tier_consensus.csv mageck=$R/rra/essentiality_rra.gene_summary.txt bagel=$R/bagel2/bayes_factor.txt > log 2>&1; echo "consensus2 exit $?"; tail -5 log
