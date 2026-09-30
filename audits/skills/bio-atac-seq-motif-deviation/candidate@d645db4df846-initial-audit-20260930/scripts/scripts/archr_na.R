suppressPackageStartupMessages(library(ArchR)); setwd(file.path(Sys.getenv("MD"),"work/archr")); addArchRGenome("hg38"); addArchRThreads(2)
proj <- ArchRProject(ArrowFiles="pbmc5k.arrow", outputDirectory="ArchROut2", copyArrows=TRUE)
print(getAvailableMatrices(proj))
z <- getMatrixFromProject(proj, useMatrix="MotifMatrix"); print(assayNames(z)); zz <- assays(z)$z
cat("dim",dim(zz),"NA total",sum(is.na(zz)),"rows w NA",sum(rowSums(is.na(zz))>0),"cols w NA",sum(colSums(is.na(zz))>0),"\n")
d <- assays(z)$deviations; cat("dev NA",sum(is.na(d)),"\n")
rn <- rownames(zz)[rowSums(is.na(zz))>0]; cat("NA motif rows (first 10):",head(rn,10),"\n")
cat("presto", as.character(packageVersion("presto")),"\n")
zc <- zz[rowSums(is.na(zz))==0,]; cat("clean rows",nrow(zc),"\n")
