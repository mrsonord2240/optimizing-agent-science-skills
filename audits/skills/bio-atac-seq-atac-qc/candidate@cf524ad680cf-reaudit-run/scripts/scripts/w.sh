#!/bin/bash
# usage: w.sh <script in reaudit-run/scripts>
exec wsl.exe -d science -- bash -l "/mnt/openscience/audits/bio-atac-seq-atac-qc/reaudit-run/scripts/$1" 2>&1 | grep -v setlocale
