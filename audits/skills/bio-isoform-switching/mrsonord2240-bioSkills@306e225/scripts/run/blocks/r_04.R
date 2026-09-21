library(fishpond); library(tximeta)

# meta: data.frame(sample_id, condition); salmon_dir/<sample_id>/quant.sf from a run with --numGibbsSamples 20
coldata <- data.frame(names = meta$sample_id,
                      files = file.path(salmon_dir, meta$sample_id, 'quant.sf'),
                      condition = factor(meta$condition))   # swish needs a factor
se <- tximeta(coldata, skipMeta = TRUE)    # drop skipMeta once a linkedTxome matches your index
y <- scaleInfReps(se)
y <- labelKeep(y)
y <- y[mcols(y)$keep, ]

set.seed(1)
y <- swish(y, x = 'condition')
y <- computeInfRV(y)                        # adds mcols(y)$meanInfRV

dte_results <- as.data.frame(mcols(y))     # log2FC, pvalue, qvalue, meanInfRV
sig <- subset(dte_results, qvalue < 0.05)
