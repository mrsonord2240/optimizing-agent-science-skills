# Audit run: (1) ArchR formals/help vs the Skill's claims (second method for the returnLoops mismatch; class evidence in evidence/logs/archr.log);
#            (2) Cicero output symmetry (each pair in both orientations)
suppressPackageStartupMessages({library(ArchR)})
CO <- Sys.getenv("CO")
f <- formals(ArchR::addCoAccessibility); g <- formals(ArchR::getCoAccessibility)
cat("addCoAccessibility defaults: k=", f$k, " knnIteration=", f$knnIteration, " maxDist=", f$maxDist, " cellsToUse/scaleTo etc. names:", paste(names(f), collapse=","), "\n")
cat("getCoAccessibility defaults: corCutOff=", g$corCutOff, " returnLoops=", g$returnLoops, " resolution=", g$resolution, "\n")
h <- capture.output(tools::Rd2txt(utils:::.getHelpFile(help("getCoAccessibility", package="ArchR")), options=list(underline_titles=FALSE)))
cat(h[grep("returnLoops|GRanges|loops", h)], sep="\n")
res <- readRDS(file.path(CO, "work/chr1/res_chr1.rds")); cn <- res$conns; cn <- cn[!is.na(cn$coaccess), ]
k <- paste(cn$Peak1, cn$Peak2); kr <- paste(cn$Peak2, cn$Peak1)
cat(sprintf("Cicero rows=%d; rows whose reverse (Peak2,Peak1) also present=%d (%.1f%%)\n", nrow(cn), sum(kr %in% k), 100*mean(kr %in% k)))
st <- cn[cn$coaccess > 0.25, ]; ks <- paste(st$Peak1, st$Peak2); krs <- paste(st$Peak2, st$Peak1)
cat(sprintf("strong rows=%d; unique unordered pairs=%d\n", nrow(st), sum(ks < krs | !(krs %in% ks))))
