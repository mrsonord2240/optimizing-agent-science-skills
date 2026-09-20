setwd("F:/OpenScience/audits/bio-isoform-switching/run/work")
g <- read.delim("annotation.gtf", header = FALSE, stringsAsFactors = FALSE, quote = "", comment.char = "")
cat(nrow(g), ncol(g), "\n"); print(head(g$V3)); tl <- g[g$V3 == "transcript", ]; cat(nrow(tl), "\n"); print(head(tl$V9, 1))
tid <- sub('.*transcript_id "([^"]+)".*', "\1", tl$V9); print(head(tid)); print(table(tl$V2))
