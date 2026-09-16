suppressPackageStartupMessages(library(MSnbase))
QD <- 'F:/OpenScience/audits/bio-proteomics-quantification/data'
QW <- 'F:/OpenScience/audits/bio-proteomics-quantification/rerun4'
blk <- readLines(file.path(QW, 'blocks', 'tmt_reporters.R'))
blk <- sub("experiment.mzML", file.path(QD, 'tmt10_synthetic.mzML'), blk, fixed = TRUE)
tf <- tempfile(fileext = '.R'); writeLines(blk, tf); source(tf)
m <- exprs(quant)
cat('corrected:', dim(m), '| NA cells:', sum(is.na(m)),
    '| negatives:', sum(m < 0, na.rm = TRUE), '\n')

raw2 <- quantify(readMSData(file.path(QD, 'tmt10_synthetic.mzML'), mode = 'onDisk'),
                 reporters = TMT10, method = 'max')
mu <- exprs(raw2)
tr <- read.csv(file.path(QD, 'tmt_truth.csv'), stringsAsFactors = FALSE)
cols <- grep('^X1', colnames(tr), value = TRUE)
T <- as.matrix(tr[, cols])
k <- min(nrow(T), nrow(m))
relerr <- function(A) {
  A <- A[1:k, , drop = FALSE]; Tt <- T[1:k, , drop = FALSE]
  median(abs(A / rowSums(A, na.rm = TRUE) - Tt / rowSums(Tt)), na.rm = TRUE)
}
cat('median |relative error| vs truth: before', round(relerr(mu), 5),
    '| after purityCorrect', round(relerr(m), 5), '\n')
