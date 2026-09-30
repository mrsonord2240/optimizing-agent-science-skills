suppressPackageStartupMessages({library(ArchR);library(GenomicRanges)}); setwd(file.path(Sys.getenv("MD"),"work/archr")); addArchRGenome("hg38"); addArchRThreads(2)
proj <- loadArchRProject("ArchROut"); print(table(proj$Clusters))
# Per-cluster deviation summary
markersMotifs <- getMarkerFeatures(proj, useMatrix='MotifMatrix',
                                   groupBy='Clusters', useSeqnames='z')
