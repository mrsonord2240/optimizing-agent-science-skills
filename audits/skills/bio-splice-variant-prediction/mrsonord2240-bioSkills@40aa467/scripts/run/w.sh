#!/bin/bash
# helper: w.sh <script-relative-to-run> : run a bash script in WSL from Git Bash
MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -l /mnt/openscience/audits/bio-splice-variant-prediction/run/"$@"
