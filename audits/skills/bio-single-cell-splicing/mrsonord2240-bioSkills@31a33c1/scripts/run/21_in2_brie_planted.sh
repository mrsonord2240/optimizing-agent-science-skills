#!/bin/bash
# INPUT 2 (planted) + null comparison: generate own SYNTHETIC v2 data, then run SKILL.md block S05 LITERALLY (brie-count + brie-quant) and score the readout.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run
for mode in planted null; do
  D=$R/data/v2_$mode; W=$R/out/in2_$mode; rm -rf $W; mkdir -p $W
  if [ $mode = planted ]; then asenv as-core python $R/20_gen_planted_v2.py $D 41; else asenv as-core python $R/20_gen_planted_v2.py $D 77 null; fi
  cd $W; cp $D/cell_table.tsv sample_list.tsv; cp $D/events.gff3 splicing_events.gff3; cp $D/cell_metadata.tsv .
  bash $R/blocks/S05_bash.sh > s05.log 2>&1
  tr '\r' '\n' < s05.log | grep -E 'Filtered|Traceback|Error|genes done' | tail -4
  asenv as-sc python $R/22_in2_eval.py $mode
done
