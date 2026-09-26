#!/usr/bin/env bash
set -euo pipefail

export R_LIBS_USER=/tmp/qfeatures-wsl-lib
audit_root=/mnt/openscience/audits/bio-proteomics-data-import/reaudit-optimized-scientific-skills@2dee47f-20260925

Rscript --vanilla -e 'suppressPackageStartupMessages(library(QFeatures)); cat(sprintf("R %s | QFeatures %s | cli %s\n", getRversion(), packageVersion("QFeatures"), packageVersion("cli")))'
Rscript --vanilla "$audit_root/run/source_examples/load_maxquant_qfeatures.R" "$audit_root/data/proteinGroups.txt"
Rscript --vanilla "$audit_root/run/input4_qfeatures_assert.R" "$audit_root/data/proteinGroups.txt"
