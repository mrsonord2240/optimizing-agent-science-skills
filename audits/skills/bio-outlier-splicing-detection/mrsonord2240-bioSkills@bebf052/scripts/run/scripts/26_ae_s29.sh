#!/bin/bash
cd /mnt/openscience/audits/bio-outlier-splicing-detection/run
micromamba run -n as-drop Rscript scripts/25_ae_s29.R /mnt/openscience/audits/bio-outlier-splicing-detection/run/ex_drop/fraser_workdir > logs/26_ae_s29.log 2>&1
grep -A7 "^== " logs/26_ae_s29.log | cut -c1-200
