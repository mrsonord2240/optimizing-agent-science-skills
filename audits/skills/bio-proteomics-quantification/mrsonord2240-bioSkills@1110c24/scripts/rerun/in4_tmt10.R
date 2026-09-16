# Quant Input 4 (regression): TMT10 mzML -> reporter extraction + impurity correction under Rscript. Block b04 verbatim. SYNTHETIC data.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
QQ <- 'F:/OpenScience/audits/bio-proteomics-quantification'
setwd(file.path(QQ, 'rerun', 'work4'))
t0 <- Sys.time()
blk <- list.files(file.path(QQ, 'rerun', 'blocks'), pattern = '^b04', full.names = TRUE)
res <- tryCatch({ suppressMessages(sys.source(blk, envir = globalenv())); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[block b04 verbatim]', res, '| elapsed s:', round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1), '\n')
e <- Biobase::exprs(quant); cat('corrected matrix:', dim(e), '| negative values:', sum(e < 0, na.rm = TRUE), '\n')
print(round(imp[1:4, 1:4], 4))
truth <- read.csv(file.path(QQ, 'data', 'tmt_truth.csv'), check.names = FALSE)
raw_q <- Biobase::exprs(suppressMessages(MSnbase::quantify(raw, reporters = MSnbase::TMT10, method = 'max')))
ch <- c('126','127N','127C','128N','128C','129N','129C','130N','130C','131')
tm <- as.matrix(truth[, ch])
rel <- function(m) m / rowSums(m)
n <- min(nrow(tm), nrow(e))
cat('median |relative error| vs truth: before', round(median(abs(rel(raw_q[1:n, ]) - rel(tm[1:n, ])), na.rm = TRUE), 4),
    '| after purityCorrect', round(median(abs(rel(e[1:n, ]) - rel(tm[1:n, ])), na.rm = TRUE), 4), '\n')
# commented CoA route in the block: filename= with MSnbase's shipped template layout
f6 <- system.file('extdata', 'TMT6plexPurityCorrections.csv', package = 'MSnbase')
cat('CoA route (TMT6 template, edit=FALSE):', dim(MSnbase::makeImpuritiesMatrix(filename = f6, edit = FALSE)), '\n')
