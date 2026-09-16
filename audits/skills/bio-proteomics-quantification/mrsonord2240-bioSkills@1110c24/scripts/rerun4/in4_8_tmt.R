# Input 4 regression (TMT10 reporter extraction + impurity correction, block verbatim)
# and Input 8 regression (TMTpro 16plex: does the pass-3 comment tell the truth?).
suppressPackageStartupMessages({library(MSnbase)})
cat('MSnbase:', as.character(packageVersion('MSnbase')), '\n')

QD <- 'F:/OpenScience/audits/bio-proteomics-quantification/data'
QW <- 'F:/OpenScience/audits/bio-proteomics-quantification/rerun4'

cat('\n=== Input 4: block verbatim on the synthetic TMT10 mzML ===\n')
blk <- readLines(file.path(QW, 'blocks', 'tmt_reporters.R'))
blk <- sub("readMSData\\('experiment.mzML'", sprintf("readMSData('%s'", file.path(QD, 'tmt10_synthetic.mzML')), blk)
tf <- tempfile(fileext = '.R'); writeLines(blk, tf)
t0 <- Sys.time()
source(tf, echo = FALSE)
cat('[block verbatim] OK | elapsed s:', round(as.numeric(Sys.time() - t0, units = 'secs'), 1), '\n')
m <- exprs(quant)
cat('corrected matrix:', dim(m), '| negative values:', sum(m < 0, na.rm = TRUE), '\n')

truth <- read.csv(file.path(QD, 'tmt_truth.csv'), stringsAsFactors = FALSE)
cat('truth columns:', paste(colnames(truth), collapse = ','), '\n')

cat('\n=== Input 8: the TMTpro claims in the block comment ===\n')
cat('TMT16 reporter set exists:', exists('TMT16'), '\n')
cat('TMT18 reporter set exists:', exists('TMT18'), '\n')
if (exists('TMT16')) cat('  TMT16 channels:', length(TMT16), '\n')
for (x in c(4, 6, 8, 10, 11, 16)) {
  r <- tryCatch({d <- dim(makeImpuritiesMatrix(x = x, edit = FALSE)); paste(d, collapse = 'x')},
                error = function(e) paste('ERROR:', conditionMessage(e)))
  cat(sprintf('  makeImpuritiesMatrix(x = %2d, edit = FALSE) -> %s\n', x, r))
}

# the block's documented CoA escape hatch, built for 16 channels
cat('\n  CoA route (filename=), built as the comment describes: 16 offset columns\n')
n <- 16
offs <- c(seq(-n / 2, -1), seq(1, n / 2))
coa <- as.data.frame(matrix(0, nrow = n, ncol = length(offs)))
colnames(coa) <- as.character(offs)
coa[[as.character(-1)]] <- 0.6
coa[[as.character(1)]] <- 0.8
f <- file.path(QW, 'tmtpro16_coa.csv')
write.csv(coa, f, row.names = FALSE)
r <- tryCatch({
  imp16 <- makeImpuritiesMatrix(filename = f, edit = FALSE)
  paste(paste(dim(imp16), collapse = 'x'), '| row sums all 1:',
        all(abs(rowSums(imp16) - 1) < 1e-9))
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('  makeImpuritiesMatrix(filename = <16ch CoA>, edit = FALSE) ->', r, '\n')

# does that matrix actually work on a 16-channel MSnSet?
if (exists('imp16')) {
  set.seed(1)
  e <- matrix(runif(300 * 16, 1e4, 1e6), nrow = 300,
              dimnames = list(paste0('P', 1:300), colnames(imp16)))
  ms <- new('MSnSet', exprs = e)
  r <- tryCatch({
    pc <- purityCorrect(ms, imp16)
    paste('corrected', paste(dim(exprs(pc)), collapse = 'x'),
          '| negatives:', sum(exprs(pc) < 0))
  }, error = function(e) paste('ERROR:', conditionMessage(e)))
  cat('  purityCorrect on a 16-channel MSnSet ->', r, '\n')
}
