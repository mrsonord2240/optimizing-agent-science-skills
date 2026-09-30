#!/bin/bash
# Audit run: T1 follow-up - is CLI failure specific to a pattern-format .mtx, or general for any readMM output?
source /mnt/openscience/audit-envs/bio-atac-seq-co-accessibility/tools/env.sh
micromamba run -n bio-atac-seq-co-accessibility Rscript /mnt/openscience/audits/bio-atac-seq-co-accessibility/runs/audit_cli2.R 2>&1 | grep -v -E "lme4|Matrix ABI|check_dep|Please re-install"
