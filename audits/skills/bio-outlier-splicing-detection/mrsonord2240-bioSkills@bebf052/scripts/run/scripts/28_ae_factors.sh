#!/bin/bash
cd /mnt/openscience/audits/bio-outlier-splicing-detection/run
micromamba run -n as-drop Rscript scripts/27_ae_seed_factors.R /mnt/openscience/audits/bio-outlier-splicing-detection/run/ex_drop/fraser_workdir > logs/28_ae_factors.log 2>&1
grep "FACTOR" logs/28_ae_factors.log
