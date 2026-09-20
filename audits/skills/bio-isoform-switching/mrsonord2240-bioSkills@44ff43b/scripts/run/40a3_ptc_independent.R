# Independent PTC-distance check on SYNTHETIC poison genes: by construction the stop codon (TAA) is the first codon of exon P, so
# stop-to-last-junction measured from the first nt of the stop codon = |P| + |E3| computed from GTF exon lengths (not from ISAR's ORF coordinates).
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
tid_of <- function(x) vapply(regmatches(x, regexec('transcript_id "([^"]+)"', x)), function(m) m[2], "")
g <- read.delim(file.path(SYN, "annotation.gtf"), header = FALSE, stringsAsFactors = FALSE, quote = "", comment.char = ""); g$tid <- tid_of(g$V9); g$len <- g$V5 - g$V4 + 1
sl <- readRDS("in4_after_orf.rds"); o <- sl$orfAnalysis; tr <- truth()
pois <- paste0(tr$gene_id[tr$type == "poison_switch"], "_B")
res <- t(sapply(pois, function(t) { e <- g[g$tid == t, ]; e <- if (e$V7[1] == "+") e[order(e$V4), ] else e[order(-e$V4), ]   # transcript order E1,E2,P,E3,E4
  c(hand = e$len[3] + e$len[4], isar = o$stopDistanceToLastJunction[o$isoform_id == t]) }))
print(res); chk("ISAR stopDistanceToLastJunction == construction-derived (|P|+|E3|, i.e. measured from the first nt of the stop codon) for all 10 poison isoforms incl. minus-strand genes", all(res[, "hand"] == res[, "isar"]), sprintf("strands: %s", paste(table(tr$strand[tr$type == "poison_switch"]), collapse = "+/-")))
