#!/usr/bin/env bash
# Re-auditor's independent LEfSe execution attempt, run inside the shared WSL
# `science` distro's `lefse` env (LEfSe 1.1.1), against a freshly-built input
# file (lefse_input.txt / lefse_input.in), NOT reusing the fixer's files.
# Invoked from Windows via:
#   MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc '<this script's body>'
cd /mnt/openscience/audits/bio-microbiome-differential-abundance/run
echo "=== lefse-format_input.py ==="
micromamba run -n lefse lefse-format_input.py lefse_input.txt lefse_input.in -c 1 -u -1 -o 1000000
echo "exit=$?"
echo "=== run_lefse.py (default -r lda) ==="
micromamba run -n lefse run_lefse.py lefse_input.in lefse_output.res
echo "exit=$?"
echo "=== run_lefse.py -r svm ==="
micromamba run -n lefse run_lefse.py lefse_input.in lefse_output_svm.res -r svm
echo "exit=$?"
