# Batch-design Input 4 (Variant B, regression of pre-fix Input 4 -- the P1 finding): "Our MaxQuant
# LFQ matrix clusters oddly on PCA and we don't have processing dates. Check for hidden batches
# with SVA." Pre-fix, sva()/num.sv() stopped with "infinite or missing values in x" on the NA-
# present matrix and the Skill never said why. Post-fix, SKILL.md's SVA block (b04_sva) messages
# the missing fraction, filters to complete features, and proceeds. Reruns the SAME real synthetic
# MaxQuant proteinGroups.txt used pre-fix, verbatim block.
.libPaths(c('F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/R-lib', .libPaths()))
BB <- 'F:/OpenScience/audits/bio-experimental-design-batch-design'
pg <- read.delim(file.path(BB, 'data', 'proteinGroups.txt'), quote = '', check.names = FALSE)
pg <- pg[pg$Reverse != '+' & pg$`Potential contaminant` != '+' & pg$`Only identified by site` != '+', ]
M <- as.matrix(pg[, grep('^LFQ intensity ', names(pg))]); M[M == 0] <- NA; M <- log2(M); colnames(M) <- sub('LFQ intensity ', '', colnames(M))
colData <- read.csv(file.path(BB, 'data', 'sample_annotation.csv')); M <- M[, colData$sample]

cat(sprintf('as imported: %d proteins x %d samples, NA %d (%.0f%%)\n', nrow(M), ncol(M), sum(is.na(M)), 100*mean(is.na(M))))

expr_normalized <- M
res <- tryCatch({
  withCallingHandlers(sys.source(file.path(BB, 'runs', 'blocks', 'b04_sva.R'), envir = globalenv()),
    message = function(m) { cat('  [message]', conditionMessage(m)); invokeRestart('muffleMessage') })
  'OK'
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[b04_sva verbatim on NA-present matrix]', res, '\n')
if (res == 'OK') {
  cat('rows used after filtering:', nrow(expr_normalized), '/', nrow(M), '\n')
  cat('n_sv:', n_sv, '\n')
  if (n_sv > 0) cat('cor(SV1, day B2):', round(cor(svobj$sv[, 1], as.numeric(colData$batch == 'B2')), 2), '\n')
}

# Sanity: did it silently drop rows a user would want back, or does the block tell the user what
# happened and how many features survive? Recompute directly to confirm the message's arithmetic.
complete_idx <- stats::complete.cases(M)
cat(sprintf('independent check: complete.cases(M) = %d/%d features (%.1f%%)\n',
            sum(complete_idx), nrow(M), 100 * mean(complete_idx)))
