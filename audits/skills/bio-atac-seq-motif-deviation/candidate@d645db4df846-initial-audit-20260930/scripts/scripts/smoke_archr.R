# Skill references/single-cell.md ArchR chain (verbatim calls) on real 10x PBMC 5k chr1:1-30Mb slice
suppressPackageStartupMessages({library(ArchR);library(GenomicRanges)})
D <- Sys.getenv("ATACDATA"); W <- file.path(Sys.getenv("MD"),"work/archr"); dir.create(W,recursive=TRUE,showWarnings=FALSE); setwd(W)
cat("ArchR",as.character(packageVersion("ArchR")),"\n")
addArchRThreads(threads=4); addArchRGenome("hg38")
ar <- createArrowFiles(inputFiles=file.path(D,"scatac/outs/fragments.tsv.gz"), sampleNames="pbmc5k", minTSS=0, minFrags=800, addTileMat=TRUE, addGeneScoreMat=FALSE, force=TRUE)
proj <- ArchRProject(ArrowFiles=ar, outputDirectory="ArchROut", copyArrows=FALSE)
cat("cells",nrow(getCellColData(proj)),"\n")
proj <- addIterativeLSI(proj, useMatrix="TileMatrix", name="IterativeLSI", iterations=2, varFeatures=5000, dimsToUse=1:20, force=TRUE)
proj <- addClusters(proj, reducedDims="IterativeLSI", name="Clusters", resolution=0.5, force=TRUE)
print(table(proj$Clusters))
# --- exactly as Skill ---
proj <- addGroupCoverages(proj, groupBy="Clusters", minCells=40, maxCells=500, force=TRUE)
proj <- addReproduciblePeakSet(proj, groupBy='Clusters', pathToMacs2=Sys.getenv("MACS2"))
cat("peaks",length(getPeakSet(proj)),"\n")
proj <- addPeakMatrix(proj)
proj <- addMotifAnnotations(proj, motifSet='cisbp', name='Motif')
proj <- addBgdPeaks(proj)
proj <- addDeviationsMatrix(proj, peakAnnotation='Motif')
proj <- saveArchRProject(proj)
z0 <- getMatrixFromProject(proj, useMatrix="MotifMatrix"); zz0 <- assays(z0)$z
cat("DIAG z dim",dim(zz0),"NA",sum(is.na(zz0)),"motif rows with NA",sum(rowSums(is.na(zz0))>0),"presto",as.character(packageVersion("presto")),"
")
markersMotifs <- try(getMarkerFeatures(proj, useMatrix='MotifMatrix', groupBy='Clusters', useSeqnames='z'))
if (inherits(markersMotifs,"try-error")) {
  cat("GETMARKERFEATURES FAILED (verbatim Skill call)
")
  cl <- proj$Clusters[match(colnames(zz0), rownames(getCellColData(proj)))]
  zc <- zz0[rowSums(is.na(zz0))==0,]
  for (g in sort(unique(cl))) { a <- rowMeans(zc[,cl==g,drop=FALSE]); b <- rowMeans(zc[,cl!=g,drop=FALSE]); o <- order(a-b,decreasing=TRUE)[1:8]
    cat("SUBSTITUTE mean-diff (NA rows dropped)", g, ":", paste(sub("_[0-9]+$","",rownames(zc)[o]),collapse=" "), "
") }
  quit(status=0)
}
print(markersMotifs)
mk <- getMarkers(markersMotifs, cutOff="FDR <= 0.05 & MeanDiff >= 0.5")
for (n in names(mk)) cat(n, nrow(mk[[n]]), ":", paste(head(mk[[n]]$name,8),collapse=" "), "\n")
z <- getMatrixFromProject(proj, useMatrix="MotifMatrix"); cat("MotifMatrix assays:",paste(assayNames(z),collapse=","),"dim",dim(z),"\n")
zz <- assays(z)$z; cat("z NA",sum(is.na(zz)),"range",range(zz),"\n")
