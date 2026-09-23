# Purpose: fresh copyKAT reference-free regression with the documented selector.
# Usage: micromamba run -n cnv-audit Rscript input2_copykat_fresh.R
suppressMessages(library(copykat))
root <- '/mnt/openscience/audits/bio-single-cell-cnv-inference'
data_dir <- paste0(root, '/data_realgenes')
out <- paste0(root, '/2026-09-23-final-pass/run/copykat_input2')
unlink(out, recursive = TRUE)
dir.create(out, recursive = TRUE); setwd(out)
counts <- read.table(paste0(data_dir, '/counts.matrix'), header = TRUE, row.names = 1,
  sep = '\t', check.names = FALSE)
res <- copykat(rawmat = as.matrix(counts), id.type = 'S', ngene.chr = 5,
  min.gene.per.cell = 50, win.size = 25, KS.cut = 0.1, sam.name = 'tumor1',
  distance = 'euclidean', norm.cell.names = '', genome = 'hg20', n.cores = 4)
pred <- res$prediction
print(table(pred$copykat.pred))
stopifnot(nrow(pred) > 0, all(pred$copykat.pred %in% c('aneuploid', 'diploid', 'not.defined')))
write.csv(pred, 'prediction.csv', row.names = FALSE)
cat('PASS: copyKAT accepted hg20 and emitted a prediction table\n')
