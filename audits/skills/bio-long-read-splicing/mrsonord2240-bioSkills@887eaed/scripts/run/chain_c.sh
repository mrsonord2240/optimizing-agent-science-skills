#!/bin/bash
R=/mnt/openscience/audits/bio-long-read-splicing/run; cd $R
bash t1_uf.sh > logs/t1_uf.log 2>&1
bash t16_unoriented_hifi.sh > logs/t16_unoriented_hifi.log 2>&1
bash t20_junction_bed.sh > logs/t20_junction_bed.log 2>&1
