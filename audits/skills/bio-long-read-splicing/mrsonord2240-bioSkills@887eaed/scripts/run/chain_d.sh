#!/bin/bash
# regression: the first re-auditor's microexon sets (4242: 7/12/24 nt; 4343 scan: 4-21 nt) with the SKILL's current recipes and bonus 20 for contrast
R=/mnt/openscience/audits/bio-long-read-splicing/run; cd $R
bash t3_microscan.sh > logs/t3_microscan.log 2>&1 &
bash t2_micro.sh > logs/t2_micro.log 2>&1 &
wait
