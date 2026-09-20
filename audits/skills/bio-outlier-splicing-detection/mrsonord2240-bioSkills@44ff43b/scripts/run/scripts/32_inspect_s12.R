suppressPackageStartupMessages({library(FRASER); library(GenomicRanges)})
a <- commandArgs(TRUE); wd <- a[1]; nm <- a[2]; synth <- a[3]
genes <- read.delim(file.path(synth, "genes.tsv")); g <- genes[genes$gene == "g030", ]; print(g)
ex <- do.call(rbind, strsplit(strsplit(g$exons, ",")[[1]], "-")); e1end <- as.integer(ex[1, 2]); e2start <- as.integer(ex[2, 1])
cat("expected cryptic junction: donor", e1end + 45, "-> acceptor", e2start, " canonical:", e1end, "->", e2start, "\n")
fds <- loadFraserDataSet(dir = wd, name = nm)
rr <- rowRanges(fds); cat("kept junctions:", length(rr), "\n")
idx <- which(start(rr) %in% c(e1end + 1, e1end + 46, e1end, e1end+45) & end(rr) %in% c(e2start, e2start - 1, e2start+1))
print(as.data.frame(rr[idx])[, 1:5])
if (length(idx)) { cm <- counts(fds, type = "j")[idx, , drop = FALSE]; print(cm[, c("S11", "S12", "S13")]) }
# raw junction table (before filter) from the counts saved on disk
sc <- readRDS(file.path(wd, "savedObjects", "rare_disease_cohort", "g_ranges_split_counts.RDS"))
cat("raw junctions total:", length(sc), "\n")
i2 <- which(start(sc) > e1end - 5 & start(sc) < e1end + 60 & end(sc) > e2start - 5 & end(sc) < e2start + 5); print(as.data.frame(sc[i2])[, 1:5])
