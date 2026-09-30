#!/bin/bash
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
micromamba run -n $P-scprinter python $A/scripts/a8_scprinter.py && micromamba run -n $P-scprinter python $A/scripts/a8b_assert.py
