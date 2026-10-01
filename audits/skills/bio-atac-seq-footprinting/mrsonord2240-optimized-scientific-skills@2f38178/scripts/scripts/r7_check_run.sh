#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1 SCPRINTER_DATA=/mnt/openscience/audit-envs/bio-atac-seq-footprinting/scprinter
/home/sci/micromamba/envs/footprint-scprinter/bin/python /mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-final-20260930/scripts/r7_check_model.py 2>&1 | grep -v Warning
