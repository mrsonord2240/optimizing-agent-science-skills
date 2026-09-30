# Independent probe: do SVs enter the model, and do results change appropriately? (real ENCODE 2v2, chr1:1-30Mb)
suppressPackageStartupMessages({library(DiffBind);library(DESeq2);library(sva);library(GenomicRanges);library(rtracklayer)})
SK <- "/mnt/openscience/wt/atac-differential-accessibility/skills/bio-atac-seq-differential-accessibility/scripts/diff_accessibility.R"
R0 <- "/mnt/openscience/audits/bio-atac-seq-differential-accessibility/reaudit-run"
setwd(file.path(R0,"work")); source(SK)   # sourced: must not auto-run
cat("sourced without auto-run: OK\n")
d <- dba(sampleSheet="samples.csv"); meta <- dba.show(d)
d <- dba.count(d, summits=250, minOverlap=2, bParallel=FALSE)
d <- dba.normalize(d, normalize=DBA_NORM_LIB, library=DBA_LIBSIZE_FULL); nrm <- dba.normalize(d,bRetrieve=TRUE)
cat("consensus sites:", nrow(dba.peakset(d,bRetrieve=TRUE)), " lib.sizes:", nrm$lib.sizes, "\n")
# skill path
res <- fit_sva(d, nrm, meta, 2, NULL, "treated", "control", 0.05, 1)
tab_skill <- res$table
# independent re-implementation
se <- dba(d, bSummarizedExperiment=TRUE); cnt <- round(SummarizedExperiment::assay(se,"Reads")); colnames(cnt) <- meta$ID
mod <- model.matrix(~Condition, meta); mod0 <- model.matrix(~1, meta)
set.seed(1); sv <- svaseq(cnt[rowMeans(cnt)>1,], mod, mod0, n.sv=1)$sv
cat("SV1 values:", round(sv[,1],4), "\n")
cat("cor(SV1, Condition):", cor(sv[,1], as.numeric(meta$Condition=="treated")), "  cor(SV1, log lib size):", cor(sv[,1], log(nrm$lib.sizes)), "\n")
cd <- data.frame(Condition=factor(meta$Condition,levels=c("control","treated")), SV1=sv[,1], row.names=meta$ID)
sf <- nrm$lib.sizes/min(nrm$lib.sizes)
mk <- function(des){ x <- DESeqDataSetFromMatrix(cnt, cd, des); sizeFactors(x) <- sf; DESeq(x,quiet=TRUE) }
dds_sv <- mk(~SV1+Condition); dds_no <- mk(~Condition)
cat("design in independent SV dds:", deparse(design(dds_sv)), " coef:", paste(resultsNames(dds_sv),collapse=","), "\n")
t_sv <- as.data.frame(results(dds_sv, contrast=c("Condition","treated","control")))
t_no <- as.data.frame(results(dds_no, contrast=c("Condition","treated","control")))
cat(sprintf("skill vs independent SV fit: max|dLFC|=%.2e  max|d(-log10 padj)| on finite=%.2e  identical sig calls=%s\n",
  max(abs(tab_skill$log2FoldChange-t_sv$log2FoldChange),na.rm=TRUE),
  {i<-is.finite(tab_skill$padj)&is.finite(t_sv$padj); max(abs(-log10(tab_skill$padj[i])+log10(t_sv$padj[i])))},
  identical(!is.na(tab_skill$padj)&tab_skill$padj<.05&abs(tab_skill$log2FoldChange)>=1, !is.na(t_sv$padj)&t_sv$padj<.05&abs(t_sv$log2FoldChange)>=1)))
cat(sprintf("SV vs no-SV: cor(LFC)=%.4f  max|dLFC|=%.3f  cor(-log10 p)=%.3f  n.sig SV=%d noSV=%d\n",
  cor(t_sv$log2FoldChange,t_no$log2FoldChange,use="c"), max(abs(t_sv$log2FoldChange-t_no$log2FoldChange),na.rm=TRUE),
  cor(-log10(t_sv$pvalue),-log10(t_no$pvalue),use="c"),
  sum(t_sv$padj<.05&abs(t_sv$log2FoldChange)>=1,na.rm=TRUE), sum(t_no$padj<.05&abs(t_no$log2FoldChange)>=1,na.rm=TRUE)))
cat("SV term p-value distribution (Wald not fitted for SV; LRT for SV1):\n")
dl <- DESeq(dds_sv, test="LRT", reduced=~Condition, quiet=TRUE); r <- results(dl); cat("  sites with SV1 LRT padj<0.05:", sum(r$padj<.05,na.rm=TRUE), "of", nrow(r), "\n")
cat("dds_sv coefficient SV1 nonzero:", any(abs(coef(dds_sv)[, "SV1"])>1e-6), "\n")
# planted truth: K562-only peaks
D <- "/mnt/openscience/audits/bio-atac-seq-differential-accessibility/initial-20260930/work/"
gm <- c(import(paste0(D,"gm1.narrowPeak"),format="narrowPeak"), import(paste0(D,"gm2.narrowPeak"),format="narrowPeak")); kp <- import(paste0(D,"k.narrowPeak"),format="narrowPeak")
ko <- kp[!overlapsAny(kp,gm)]; cat("planted K562-only:", length(ko), "\n")
gr <- SummarizedExperiment::rowRanges(se)
for (nm in c("SV","noSV")) { t <- if(nm=="SV") t_sv else t_no; sig <- !is.na(t$padj)&t$padj<.05&abs(t$log2FoldChange)>=1
  h <- overlapsAny(gr[sig],ko); cat(sprintf("%s: sig=%d, K562-only hits=%d, frac opened among them=%.3f, frac of sig hits that are K562-only=%.3f\n", nm, sum(sig), sum(h), mean(t$log2FoldChange[sig][h]>0), mean(h))) }
# blacklist impact
bl <- tryCatch({ x <- DiffBind::dba.blacklist(d, blacklist=DBA_BLACKLIST_HG38, greylist=FALSE); nrow(dba.peakset(x,bRetrieve=TRUE)) }, error=function(e) conditionMessage(e))
cat("consensus sites before/after DiffBind hg38 blacklist:", nrow(dba.peakset(d,bRetrieve=TRUE)), bl, "\n")
# oversized request capped, guard for too-few samples
r2 <- fit_sva(d, nrm, meta, 9, NULL, "treated","control",.05,1); cat("n_sv=9 request did not error (capped)\n")
