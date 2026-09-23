#!/usr/bin/env bash
# Purpose: record the independently installed CNV runtime and copyKAT selector.
# Usage: bash check_cnv_runtime.sh
set -euo pipefail
/home/sci/.local/bin/micromamba run -n cnv-audit Rscript - <<'RS'
pkgs <- c('infercnv', 'copykat', 'SCEVAN', 'numbat')
for (p in pkgs) {
  suppressPackageStartupMessages(library(p, character.only = TRUE))
  cat(p, as.character(packageVersion(p)), '\n')
}
ck <- get('copykat', envir = asNamespace('copykat'))
cat('copykat_formals:', paste(capture.output(formals(ck)), collapse = ' '), '\n')
RS
