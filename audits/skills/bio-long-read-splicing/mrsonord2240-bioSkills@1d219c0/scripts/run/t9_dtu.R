# SKILL "DTU on Long-Read Counts" R block, sourced VERBATIM (out/blocks/dtu-on-long-read-counts_1.R) in the FLAIR run directory, then scored against the planted truth.
args <- commandArgs(trailingOnly = TRUE)
wd <- args[1]; truthf <- args[2]
setwd(wd)
cat("working dir:", getwd(), "\n")
source("F:/OpenScience/audits/bio-long-read-splicing/run/out/blocks/dtu-on-long-read-counts_1.R", echo = FALSE)
cat("block finished; class(dtu) =", class(dtu)[1], "\n")
if (is.null(dtu)) { cat("dtu is NULL (no significant gene)\n"); quit(status = 0) }
print(head(dtu, 4))
gcol <- intersect(c("gene", "geneID"), colnames(dtu))
cat("columns:", paste(colnames(dtu), collapse = ", "), "\n")
called <- unique(as.character(dtu[[grep("^gene", colnames(dtu))[1]]]))
if (length(called) > 0 && "gene" %in% colnames(dtu)) called <- unique(as.character(dtu$geneID))
t <- read.table(truthf, header = TRUE, sep = "\t")
plant <- t$gene[t$planted_dtu == 1]
tested <- unique(res_gene$gene_id)
cat(sprintf("genes tested by DRIMSeq: %d ; planted DTU genes tested: %d/%d\n", length(tested), sum(plant %in% tested), length(plant)))
cat(sprintf("stage-wise significant genes: %d ; planted recovered: %d/%d ; other genes called: %d\n", length(called), sum(plant %in% called), length(plant), sum(!(called %in% plant))))
cat("other genes called:", paste(setdiff(called, plant), collapse = ","), "\n")
