#!/bin/bash
source /mnt/openscience/audit-envs/bio-atac-seq-co-accessibility/tools/env.sh
micromamba run -n bio-atac-seq-co-accessibility Rscript /mnt/openscience/audits/bio-atac-seq-co-accessibility/runs/${1:-audit_checks.R} 2>&1 | grep -v -E "lme4|Matrix ABI|check_dep|Please re-install"
