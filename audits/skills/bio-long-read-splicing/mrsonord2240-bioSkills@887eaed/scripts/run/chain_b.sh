#!/bin/bash
# real dRNA example, prior-data regression, de novo / novel-site check
R=/mnt/openscience/audits/bio-long-read-splicing/run; cd $R
bash t12_realdrna.sh > logs/t12_realdrna.log 2>&1
bash t19_denovo_novelsite.sh > logs/t19_denovo_novelsite.log 2>&1
bash t10_prior.sh > logs/t10_prior.log 2>&1
