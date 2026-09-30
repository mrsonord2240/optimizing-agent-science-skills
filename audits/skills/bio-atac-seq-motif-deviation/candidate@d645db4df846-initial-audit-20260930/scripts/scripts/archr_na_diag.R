suppressPackageStartupMessages(library(ArchR)); setwd(file.path(Sys.getenv("MD"),"work/archr")); addArchRGenome("hg38"); addArchRThreads(2)
proj <- loadArchRProject("ArchROut")
z <- getMatrixFromProject(proj, useMatrix="MotifMatrix"); zz <- assays(z)$z; dd <- assays(z)$deviations
cd <- as.data.frame(getCellColData(proj))[colnames(zz),]
cat("cellColData cols:", colnames(cd), "
")
na_cells <- colnames(zz)[colSums(is.na(zz))>0]
na_motifs <- rownames(zz)[rowSums(is.na(zz))>0]
cat("NA cells:", length(na_cells), "\n")
print(cd[na_cells, "nFrags"])
cat("nFrags quantiles all cells:\n"); print(quantile(cd$nFrags, c(0,.05,.25,.5,.75,1)))
cat("NA cells nFrags rank (percentile among cells):", round(sapply(cd[na_cells,"nFrags"], function(x) mean(cd$nFrags<=x)),3), "\n")
# motif peak counts
pa <- getPeakAnnotation(proj, "Motif"); mm <- readRDS(pa$Matches); mmat <- assay(mm)
npk <- Matrix::colSums(mmat); names(npk) <- colnames(mmat)
cat("peaks total", nrow(mmat), "; matched peaks per NA motif:\n"); print(npk[na_motifs])
cat("median matched peaks all motifs:", median(npk), " min:", min(npk), "\n")
# which cells x motifs are NA: dev value
idx <- which(is.na(zz), arr.ind=TRUE); print(head(data.frame(motif=rownames(zz)[idx[,1]], cell=colnames(zz)[idx[,2]], dev=dd[idx]),25))
# does NA relate to cell PeakMatrix counts?
pm <- getMatrixFromProject(proj, useMatrix="PeakMatrix")
cnt <- Matrix::colSums(assay(pm)); cat("PeakMatrix total counts in NA cells:", cnt[na_cells], "; median all:", median(cnt), "\n")
# for NA motifs x NA cells: count of motif-peak reads in those cells
for (i in seq_len(min(6,nrow(idx)))) { m <- rownames(zz)[idx[i,1]]; cl <- colnames(zz)[idx[i,2]]
  pk <- which(mmat[, m]); cat(m, cl, "motif peaks", length(pk), "reads in motif peaks in this cell", sum(assay(pm)[pk, cl]), "\n") }
# Does the failure reproduce when NA cells are removed?
keep <- setdiff(colnames(zz), na_cells)
if(!"Clusters" %in% colnames(getCellColData(proj))) { cl <- ClusterMap <- NULL; proj <- addClusters(addIterativeLSI(proj, useMatrix="TileMatrix", name="IterativeLSI", iterations=2, varFeatures=5000, dimsToUse=1:20, force=TRUE), reducedDims="IterativeLSI", name="Clusters", resolution=0.5, force=TRUE) }
p2 <- proj[keep]
mk <- try(getMarkerFeatures(p2, useMatrix="MotifMatrix", groupBy="Clusters", useSeqnames="z"), silent=TRUE)
cat("getMarkerFeatures after dropping", length(na_cells), "NA cells:", if(inherits(mk,"try-error")) paste("FAILED", conditionMessage(attr(mk,"condition"))) else "OK", "\n")
if(!inherits(mk,"try-error")) { m <- getMarkers(mk, cutOff="FDR <= 0.05 & MeanDiff >= 0.5"); for(n in names(m)) cat(n, nrow(m[[n]]), ":", paste(head(sub("_[0-9]+$","",m[[n]]$name),6),collapse=" "), "\n") }
