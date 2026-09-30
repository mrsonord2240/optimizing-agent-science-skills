#!/bin/bash
source /mnt/openscience/audit-envs/bio-atac-seq-co-accessibility/tools/env.sh
RA=/mnt/openscience/audits/bio-atac-seq-co-accessibility/reaudit-run
for m in "$@"; do echo "=== MODE $m $(date -Is)"; time micromamba run -n bio-atac-seq-co-accessibility Rscript $RA/scripts/ra_fn.R $m; echo "EXIT $?"; done
