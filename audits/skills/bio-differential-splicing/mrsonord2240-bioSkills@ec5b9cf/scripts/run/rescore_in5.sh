#!/bin/bash
# re-run only the scoring step of in5 (first scoring attempt failed: pandas parsed the truth class 'null' as NaN; fixed with keep_default_na=False)
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
$CORE python $R/eval_sim2.py $R/data/sim2/truth.tsv $R/out/in5 1 2 3 4 6 > $R/out/in5/eval.txt 2>&1; cat $R/out/in5/eval.txt
