.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(limma))
QQ <- 'F:/OpenScience/audits/bio-proteomics-quantification'
R <- as.matrix(read.csv(file.path(QQ, 'rerun', 'in3_silac_log2_norm.csv'), row.names = 1))
truth <- read.csv(file.path(QQ, 'data', 'silac_truth.csv'), row.names = 1)
fit <- tryCatch(eBayes(lmFit(R), trend = TRUE, robust = TRUE), error = function(e) { cat('eBayes ERROR:', conditionMessage(e), '\n'); NULL })
cat('rows into lmFit:', nrow(R), '\n')
if (!is.null(fit)) { tt <- topTable(fit, number = Inf); hit <- rownames(tt)[tt$adj.P.Val < 0.05]
  cat('one-sample limma trend+robust BH<0.05:', length(hit), '| classes:', paste(names(table(truth[hit, 'class'])), table(truth[hit, 'class'])), '\n') }
