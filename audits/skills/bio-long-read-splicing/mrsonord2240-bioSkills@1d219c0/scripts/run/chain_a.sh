#!/bin/bash
# sequence: real-read blocks (t5_real) then SQANTI3 block on real+planted FLAIR isoforms (t11)
R=/mnt/openscience/audits/bio-long-read-splicing/run; cd $R
bash t5_real.sh > logs/t5_real.log 2>&1
bash t11_sqanti_real.sh > logs/t11_sqanti_real.log 2>&1
