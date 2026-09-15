source('F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/common.R')
# Diagnose the eBayes failure in input1 (Skill limma block on an unfiltered LFQ matrix with NAs)
suppressPackageStartupMessages(library(limma))
sample_info <- read.csv(file.path(DATA, 'sample_annotation.csv'), stringsAsFactors = TRUE)
pg <- read_pg(); pm <- lfq_log2(pg, as.character(sample_info$sample))
design <- model.matrix(~0 + condition + batch, data = sample_info)
colnames(design)[1:2] <- levels(factor(sample_info$condition))
fit2 <- contrasts.fit(lmFit(pm, design), makeContrasts(Treatment - Control, levels = design))
cat('df.residual table:\n'); print(table(fit2$df.residual))
cat('NA sigma:', sum(is.na(fit2$sigma)), '| NA coef:', sum(is.na(fit2$coefficients)), '\n')
for (tr in c(TRUE, FALSE)) for (rb in c(TRUE, FALSE)) {
  r <- tryCatch({ eBayes(fit2, trend = tr, robust = rb); 'OK' }, error = function(e) conditionMessage(e))
  cat(sprintf('eBayes(trend=%s, robust=%s): %s\n', tr, rb, r))
}
# Is it the NA-coefficient rows (on/off: no Treatment obs) whose Amean is fine but df>0?
bad <- is.na(fit2$coefficients[, 1])
cat('rows with NA contrast:', sum(bad), '; their df.residual:', paste(names(table(fit2$df.residual[bad])), table(fit2$df.residual[bad]), collapse = ' '), '\n')
r <- tryCatch({ eBayes(fit2[!bad, ], trend = TRUE, robust = TRUE); 'OK' }, error = function(e) conditionMessage(e))
cat('eBayes(trend,robust) after dropping NA-contrast rows:', r, '\n')
