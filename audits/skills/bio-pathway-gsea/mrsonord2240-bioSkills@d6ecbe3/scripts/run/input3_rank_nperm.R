library(clusterProfiler)
library(msigdbr)
set.seed(321)
h <- msigdbr(species = "Homo sapiens", collection = "H")
t2g <- unique(h[, c("gs_name", "ncbi_gene")])
ids <- unique(as.character(t2g$ncbi_gene))
ids <- ids[seq_len(min(5000, length(ids)))]
stats <- rnorm(length(ids)); names(stats) <- ids
signal <- intersect(ids, as.character(t2g$ncbi_gene[t2g$gs_name == "HALLMARK_TNFA_SIGNALING_VIA_NFKB"]))
stats[signal] <- stats[signal] + 2
gl <- sort(stats, decreasing = TRUE)
stopifnot(isTRUE(all.equal(gl, sort(gl, decreasing = TRUE))), !anyDuplicated(names(gl)))
oldwarn <- character(); g <- withCallingHandlers(
  GSEA(gl, TERM2GENE=t2g, minGSSize=10, maxGSSize=500, pvalueCutoff=1, nPerm=1000, seed=TRUE, verbose=FALSE),
  warning=function(w) { oldwarn <<- c(oldwarn, conditionMessage(w)); invokeRestart("muffleWarning") })
stopifnot("nPerm" %in% names(g@params), any(grepl("fgseaSimple", oldwarn, fixed=TRUE)))
guarded <- tryCatch({if ("nPerm" %in% names(g@params)) stop("nPerm forced a fgseaSimple fallback - remove it"); FALSE}, error=function(e) grepl("fgseaSimple", conditionMessage(e), fixed=TRUE))
stopifnot(guarded)
unsorted <- tryCatch({GSEA(rev(gl), TERM2GENE=t2g, minGSSize=10, maxGSSize=500, verbose=FALSE); FALSE}, error=function(e) grepl("decreasing sorted", conditionMessage(e), fixed=TRUE))
dup <- c(gl, gl[1]); names(dup)[length(dup)] <- names(gl)[1]
duplicate <- tryCatch({GSEA(sort(dup, decreasing=TRUE), TERM2GENE=t2g, minGSSize=10, maxGSSize=500, verbose=FALSE); FALSE}, error=function(e) grepl("Duplicate values", conditionMessage(e), fixed=TRUE))
stopifnot(unsorted, duplicate)
res <- as.data.frame(g)
stopifnot(nrow(res)>0)
cat(sprintf("ASSERT input3 terms=%d warnings=%d guard=%s unsorted=%s duplicate=%s\n", nrow(res), length(oldwarn), guarded, unsorted, duplicate))
