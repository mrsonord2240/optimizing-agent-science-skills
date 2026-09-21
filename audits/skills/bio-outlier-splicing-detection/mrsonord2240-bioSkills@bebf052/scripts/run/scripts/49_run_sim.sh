#!/bin/bash
# OUTRIDER simulator spot check, block verbatim: m=100 on 1.24.0 (Windows) and 1.28.1 (as-drop)
R=/f/OpenScience/audits/bio-outlier-splicing-detection/run; W=F:/OpenScience/audits/bio-outlier-splicing-detection/run
cd $R
for m in 100; do
  bash /f/OpenScience/audit-envs/alternative-splicing/r.sh scripts/48_make_sim.R $m $W/in5_win$m > logs/49_make_sim$m.log 2>&1
  mkdir -p in5_drop$m; cp in5_win$m/counts.tsv in5_win$m/outrider_truth.tsv in5_drop$m/
  bash /f/OpenScience/audit-envs/alternative-splicing/r.sh scripts/45_block_outrider.R $W/in5_win$m $W/blocks/02_r.R > logs/49_sim_win_m$m.log 2>&1
  MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc "cd /mnt/openscience/audits/bio-outlier-splicing-detection/run; micromamba run -n as-drop Rscript scripts/45_block_outrider.R /mnt/openscience/audits/bio-outlier-splicing-detection/run/in5_drop$m /mnt/openscience/audits/bio-outlier-splicing-detection/run/blocks/02_r.R" > logs/49_sim_drop_m$m.log 2>&1
done
