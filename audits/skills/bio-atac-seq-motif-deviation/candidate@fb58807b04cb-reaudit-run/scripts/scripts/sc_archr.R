suppressPackageStartupMessages({library(ArchR);library(GenomicRanges)}); setwd(file.path(Sys.getenv("MD"),"work/archr")); addArchRGenome("hg38"); addArchRThreads(2)
proj <- loadArchRProject("ArchROut"); print(table(proj$Clusters))
# Sparse cells x rare motifs can give 0/0 (NaN) z-scores, and getMarkerFeatures (presto) refuses NA.
mm <- getMatrixFromProject(proj, useMatrix='MotifMatrix')
na_cells <- colnames(mm)[colSums(is.na(assays(mm)$z)) > 0]
length(na_cells)
if (length(na_cells) > 0) proj <- subsetCells(proj, cellNames=setdiff(proj$cellNames, na_cells))

# Per-cluster deviation summary
markersMotifs <- getMarkerFeatures(proj, useMatrix='MotifMatrix',
                                   groupBy='Clusters', useSeqnames='z')

cat("dropped cells:", length(na_cells), " remaining:", length(proj$cellNames), "
")
mk <- getMarkers(markersMotifs, cutOff="FDR <= 0.05 & MeanDiff >= 0.5")
for (n in names(mk)) cat(n, nrow(mk[[n]]), ":", paste(head(mk[[n]]$name,8),collapse=" "), "
")
mm2 <- getMatrixFromProject(proj, useMatrix='MotifMatrix'); cat("post-guard NA in z:", sum(is.na(assays(mm2)$z)), " dim", dim(mm2), "
")
