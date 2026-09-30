# Is the direct-DESeq2 no-SV fit (basis of --sva mode) equivalent to DiffBind's DESeq2 path? Explains 1372 vs 1181.
suppressPackageStartupMessages({library(DiffBind);library(DESeq2)})
setwd("/mnt/openscience/audits/bio-atac-seq-differential-accessibility/reaudit-run/work")
d <- dba(sampleSheet="samples.csv"); meta <- dba.show(d)
d <- dba.count(d, summits=250, minOverlap=2, bParallel=FALSE)
d <- dba.normalize(d, normalize=DBA_NORM_LIB, library=DBA_LIBSIZE_FULL); nrm <- dba.normalize(d,bRetrieve=TRUE)
d <- dba.contrast(d, design=TRUE, contrast=c("Condition","treated","control"), minMembers=2); d <- dba.analyze(d, method=DBA_DESEQ2)
rep <- dba.report(d, method=DBA_DESEQ2, th=1, fold=0, bCounts=FALSE)   # all sites
se <- dba(d, bSummarizedExperiment=TRUE); cnt <- round(SummarizedExperiment::assay(se,"Reads")); colnames(cnt) <- meta$ID
cd <- data.frame(Condition=factor(meta$Condition,levels=c("control","treated")),row.names=meta$ID)
x <- DESeqDataSetFromMatrix(cnt,cd,~Condition); sizeFactors(x) <- nrm$lib.sizes/min(nrm$lib.sizes); x <- DESeq(x,quiet=TRUE)
t <- as.data.frame(results(x,contrast=c("Condition","treated","control"))); gr <- SummarizedExperiment::rowRanges(se)
o <- findOverlaps(rep, gr, type="equal"); cat("matched", length(o), "of", length(rep), "sites\n")
cat(sprintf("LFC cor DiffBind vs direct: %.5f; max|d|=%.4f; DiffBind sig=%d; direct sig(same thr)=%d; direct sig among matched=%d\n",
 cor(rep$Fold[queryHits(o)], t$log2FoldChange[subjectHits(o)]), max(abs(rep$Fold[queryHits(o)]-t$log2FoldChange[subjectHits(o)])),
 sum(rep$FDR<.05&abs(rep$Fold)>=1), sum(t$padj<.05&abs(t$log2FoldChange)>=1,na.rm=T),
 sum(t$padj[subjectHits(o)]<.05&abs(t$log2FoldChange[subjectHits(o)])>=1,na.rm=T)))
cat("padj NA in DiffBind report:", sum(is.na(rep$FDR)), " direct NA:", sum(is.na(t$padj)),"\n")
