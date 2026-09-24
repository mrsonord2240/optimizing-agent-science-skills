#!/bin/bash
# Run t4_example.sh (shipped example from the clean copy in run/skill_copy) for the 3 platforms and the 3 platforms + SR_JUNCTIONS in parallel
R=/mnt/openscience/audits/bio-long-read-splicing/run; cd $R
for p in hifi ont drna; do bash t4_example.sh $p > logs/t4_example_$p.log 2>&1 & done
wait
for p in hifi ont drna; do bash t4_example.sh $p sj > logs/t4_example_${p}sj.log 2>&1 & done
wait
echo done
