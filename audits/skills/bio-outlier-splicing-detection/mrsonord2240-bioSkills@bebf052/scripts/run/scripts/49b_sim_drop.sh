#!/bin/bash
cd /mnt/openscience/audits/bio-outlier-splicing-detection/run
micromamba run -n as-drop Rscript scripts/45_block_outrider.R /mnt/openscience/audits/bio-outlier-splicing-detection/run/in5_drop100 /mnt/openscience/audits/bio-outlier-splicing-detection/run/blocks/02_r.R > logs/49_sim_drop_m100.log 2>&1
tail -n 3 logs/49_sim_drop_m100.log
