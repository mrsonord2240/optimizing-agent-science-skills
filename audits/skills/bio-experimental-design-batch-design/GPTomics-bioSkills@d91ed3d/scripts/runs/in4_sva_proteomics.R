# Batch-design Input 4 (variant): "Do I have hidden batches?" on a MaxQuant log2 LFQ matrix (NA = missing). SKILL.md SVA block
# run verbatim with expr_normalized = the matrix as a proteomics user has it, then with complete cases. SYNTHETIC data
# (shared set: a real, unannotated day effect exists: B1 vs B2).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(sva))
BB <- 'F:/OpenScience/audits/bio-experimental-design-batch-design'
pg <- read.delim(file.path(BB, 'data', 'proteinGroups.txt'), quote = '', check.names = FALSE)
pg <- pg[pg$Reverse != '+' & pg$`Potential contaminant` != '+' & pg$`Only identified by site` != '+', ]
M <- as.matrix(pg[, grep('^LFQ intensity ', names(pg))]); M[M == 0] <- NA; M <- log2(M); colnames(M) <- sub('LFQ intensity ', '', colnames(M))
colData <- read.csv(file.path(BB, 'data', 'sample_annotation.csv')); M <- M[, colData$sample]
blk <- list.files(file.path(BB, 'runs', 'blocks'), pattern = '^b03', full.names = TRUE)
for (case in c('as imported (NA present)', 'complete cases')) {
  expr_normalized <- if (case == 'complete cases') M[complete.cases(M), ] else M
  cat(sprintf('--- %s: %d x %d, NA %d\n', case, nrow(expr_normalized), ncol(expr_normalized), sum(is.na(expr_normalized))))
  res <- tryCatch({ invisible(capture.output(sys.source(blk, envir = globalenv()))); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
  cat('[SVA block verbatim]', res, '\n')
  if (res == 'OK') { cat('n_sv:', n_sv, '\n'); if (n_sv > 0) cat('cor(SV1, day B2):', round(cor(svobj$sv[, 1], as.numeric(colData$batch == 'B2')), 2), '\n') }
}
