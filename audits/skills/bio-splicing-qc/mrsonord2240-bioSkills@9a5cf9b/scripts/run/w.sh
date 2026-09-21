#!/bin/bash
# Windows-side launcher: w.sh <script.sh in this run dir> ; runs it inside WSL `science`
export MSYS2_ARG_CONV_EXCL='*'
s=$1; shift
wsl.exe -d science -- bash -l "/mnt/openscience/audits/bio-splicing-qc/run/$s" "$@" 2>&1 | grep -av 'Failed to start the systemd'
