#!/bin/bash
# OUTRIDER block verbatim: Windows 1.24.0 (r.sh) and WSL as-drop 1.28.1, n=30 and n=100 synthetic matrices
R=/f/OpenScience/audits/bio-outlier-splicing-detection/run
W=F:/OpenScience/audits/bio-outlier-splicing-detection/run
cd $R
for n in 30 100; do
  bash /f/OpenScience/audit-envs/alternative-splicing/r.sh scripts/45_block_outrider.R $W/in2_win$n $W/blocks/02_r.R > logs/46_outrider_win_n$n.log 2>&1
  MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc "cd /mnt/openscience/audits/bio-outlier-splicing-detection/run; micromamba run -n as-drop Rscript scripts/45_block_outrider.R in2_drop$n /mnt/openscience/audits/bio-outlier-splicing-detection/run/blocks/02_r.R" > logs/46_outrider_drop_n$n.log 2>&1
done
