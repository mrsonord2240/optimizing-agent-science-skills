suppressPackageStartupMessages({library(DiffBind)})
setwd("/mnt/openscience/audits/bio-atac-seq-differential-accessibility/reaudit-run/work")
d <- dba(sampleSheet="samples.csv"); d <- dba.count(d, summits=250, minOverlap=2, bParallel=FALSE)
se <- dba(d, bSummarizedExperiment=TRUE); counts <- round(SummarizedExperiment::assay(se,"Reads"))
coldata <- data.frame(condition=factor(c("control","control","treated","treated")), row.names=colnames(counts))
library(DESeq2); library(sva)

dds <- DESeqDataSetFromMatrix(countData=counts, colData=coldata, design=~condition)
dds <- estimateSizeFactors(dds)
dat <- counts(dds, normalized=TRUE)
dat <- dat[rowMeans(dat) > 1, ]

mod  <- model.matrix(~condition, colData(dds))
mod0 <- model.matrix(~1, colData(dds))
nsv <- min(2, ncol(dat) - ncol(mod) - 1)
svobj <- svaseq(dat, mod, mod0, n.sv=nsv)

colData(dds) <- cbind(colData(dds), setNames(as.data.frame(svobj$sv), paste0('SV', seq_len(nsv))))
design(dds) <- as.formula(paste('~', paste0('SV', seq_len(nsv), collapse=' + '), '+ condition'))
dds <- DESeq(dds)
res <- results(dds, contrast=c('condition', 'treated', 'control'))

cat("RECIPE nsv", nsv, "design", deparse(design(dds)), "padj<0.05:", sum(res$padj<0.05,na.rm=TRUE), "anyNA sv", anyNA(svobj$sv), "
")
