# Re-audit: ArchR snippet from references/method-reference.md executed verbatim on the existing public PBMC 5k chr1 ArchR project
# (arrow built by the tooling phase from the 10x PBMC 5k fragments; reused as an input; project, peak set, LSI rebuilt here).
suppressPackageStartupMessages({library(ArchR); library(GenomicRanges)})
CO <- Sys.getenv("CO"); setwd(file.path(CO, "work/archr")); addArchRThreads(threads=4); addArchRGenome("hg38")
chk <- function(n, ok, d="") cat(if (isTRUE(ok)) "PASS" else "FAIL", n, d, "\n")
library(rtracklayer)
proj <- ArchRProject(ArrowFiles="pbmc5k.arrow", outputDirectory="ArchROutRA", copyArrows=FALSE)
pk <- import(file.path(Sys.getenv("ATACDATA"), "scatac/outs/peaks.bed")); pk <- pk[seqnames(pk)=="chr1" & end(pk) <= 30e6]; mcols(pk) <- NULL
proj <- addPeakSet(proj, peakSet=pk, force=TRUE); proj <- addPeakMatrix(proj, force=TRUE)
proj <- addIterativeLSI(proj, useMatrix="PeakMatrix", name="IterativeLSI", iterations=2, varFeatures=1000, dimsToUse=1:20, force=TRUE)
cat("cells:", nrow(getCellColData(proj)), " peaks:", length(getPeakSet(proj)), "
")
proj <- addCoAccessibility(proj, reducedDims='IterativeLSI',
                          k=100, knnIteration=500,
                          maxDist=250000)
co_acc <- getCoAccessibility(proj, corCutOff=0.5, returnLoops=TRUE)
loops <- co_acc[[1]]
cat("class(co_acc):", paste(class(co_acc), collapse=","), " class(loops):", paste(class(loops), collapse=","), " n loops:", length(loops), "\n")
chk("returnLoops=TRUE is a SimpleList, element 1 is GRanges (COACC-010 wording)", is(co_acc, "SimpleList") && is(loops, "GRanges") && !is(co_acc, "GRanges"))
df <- getCoAccessibility(proj, corCutOff=0.5, returnLoops=FALSE)
cc <- as.data.frame(df)
chk("returnLoops=FALSE is a DataFrame of peak-pair correlations", is(df, "DataFrame") && all(c("queryHits","subjectHits","correlation") %in% colnames(cc)), paste(colnames(cc), collapse=","))
chk("correlations in [0.5, 1]", all(cc$correlation >= 0.5 & cc$correlation <= 1.0001), sprintf("%.2f..%.2f, n=%d", min(cc$correlation), max(cc$correlation), nrow(cc)))
ps <- getPeakSet(proj); mid <- start(resize(ps, 1, "center")); d <- abs(mid[cc$queryHits] - mid[cc$subjectHits])
chk("maxDist=250000 respected", max(d) <= 250500, sprintf("max %d bp", max(d)))
