#!/bin/bash
# wsl -d science -- bash /mnt/openscience/audits/bio-atac-seq-differential-accessibility/initial-20260930/scripts/run.sh <mode>
export PATH=/home/sci/.local/bin:$PATH MAMBA_ROOT_PREFIX=/home/sci/micromamba
micromamba run -n bio-atac-seq-differential-accessibility Rscript /mnt/openscience/audits/bio-atac-seq-differential-accessibility/initial-20260930/scripts/audit_tests.R "$1"
