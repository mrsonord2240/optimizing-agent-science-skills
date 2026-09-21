#!/bin/bash
cd /mnt/openscience/audits/bio-outlier-splicing-detection/run
micromamba run -n as-drop Rscript scripts/23_ae_seed_fixer_script.R /mnt/openscience/audits/bio-outlier-splicing-detection/run/ex_drop/fraser_workdir > logs/24_ae_seed_fixer_script.log 2>&1
tail -n 4 logs/24_ae_seed_fixer_script.log
