# Purpose: execute the shipped SCEVAN example unchanged on its genome-wide audit panel.
# Usage: micromamba run -n cnv-audit Rscript input8_scevan_shipped_fresh.R
root <- '/mnt/openscience/audits/bio-single-cell-cnv-inference'
out <- paste0(root, '/2026-09-23-final-pass/run/scevan_input8')
unlink(out, recursive = TRUE); dir.create(out, recursive = TRUE)
source_data <- paste0(root, '/run/reaudit/scevan_genomewide')
file.copy(paste0(source_data, '/counts.matrix'), paste0(out, '/counts.matrix'))
file.copy(paste0(source_data, '/cell_annotations.txt'), paste0(out, '/cell_annotations.txt'))
setwd(out)
source('/mnt/openscience/wt/single-cell-cnv-inference/single-cell/cnv-inference/examples/scevan_calling.R')
stopifnot(file.exists('output/tumor1_CNAmtx.RData'))
cat('PASS: shipped SCEVAN example completed and wrote its CNA matrix.\n')
