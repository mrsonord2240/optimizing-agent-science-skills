#!/bin/bash
# same as par_example.sh second half: shipped example with SR_JUNCTIONS (SJ.out.tab from make_sj.py) for the 3 platforms
R=/mnt/openscience/audits/bio-long-read-splicing/run; cd $R
for p in hifi ont drna; do bash t4_example.sh $p sj > logs/t4_example_${p}sj.log 2>&1 & done
wait; echo done
