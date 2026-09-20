# Input 3/7: SKILL.md Bambu code, verbatim structure, on SYNTHETIC HiFi-like BAMs (6 samples, planted truth). Run via r-bambu.sh (xgboost 1.7.8.1).
D <- "F:/OpenScience/audits/bio-long-read-splicing/run"
setwd(paste0(D, "/out")); dir.create("bambu", showWarnings = FALSE); setwd("bambu")
cat("R:", R.version.string, " bambu:", as.character(packageVersion("bambu")), "\n")
library(bambu)
bam_files <- paste0(D, "/out/flair/", c("ctrl1","ctrl2","ctrl3","trt1","trt2","trt3"), ".bam")
stopifnot(all(file.exists(bam_files)))
genome <- paste0(D, "/data/synth/chrS1.fa")
gtf <- paste0(D, "/data/synth/ref.gtf")

bambuAnnotations <- prepareAnnotations(gtf)
se <- bambu(reads = bam_files, annotations = bambuAnnotations, genome = genome, NDR = 0.1, ncore = 1)
cat("class:", class(se), " dim:", dim(se), "\n")
saveRDS(se, "se_synth.rds")
writeBambuOutput(se, path = "bambu_output/")
cat("files written:", paste(list.files("bambu_output"), collapse = ", "), "\n")

# --- SKILL lines verbatim: assays()/transcriptToGeneExpression() ---
r1 <- try(tx_counts <- as.data.frame(assays(se)$counts), silent = TRUE)
cat("SKILL line `as.data.frame(assays(se)$counts)`:", if (inherits(r1, "try-error")) paste("ERROR:", conditionMessage(attr(r1, "condition"))) else "ok", "\n")
if (inherits(r1, "try-error")) { library(SummarizedExperiment); tx_counts <- as.data.frame(assays(se)$counts); cat("  ...works after library(SummarizedExperiment)\n") }
r2 <- try(gene_counts <- transcriptToGeneExpression(se), silent = TRUE)
cat("SKILL line `transcriptToGeneExpression(se)`:", if (inherits(r2, "try-error")) paste("ERROR:", conditionMessage(attr(r2, "condition"))) else "ok", "\n")

# --- check vs planted truth (exact intron chain) ---
rr <- rowRanges(se)
cat("n transcripts:", length(rr), "\n")
cnt <- assays(se)$counts
ex <- as.list(rr)
chain <- sapply(names(ex), function(n) { e <- ex[[n]]; e <- e[order(start(e))]; if (length(e) < 2) return("mono") ; paste0(end(e)[-length(e)], "-", start(e)[-1] - 1, collapse = ";")})
truth_gtf <- read.table(paste0(D, "/data/synth/read_tx.gtf"), sep = "\t", quote = "", stringsAsFactors = FALSE)
truth_gtf <- truth_gtf[truth_gtf$V3 == "exon", ]
truth_gtf$tid <- sub('.*transcript_id "([^"]+)".*', "\\1", truth_gtf$V9)
tchain <- sapply(split(truth_gtf, truth_gtf$tid), function(d) { d <- d[order(d$V4), ]; n <- nrow(d); paste0(d$V5[-n], "-", d$V4[-1] - 1, collapse = ";") })
print(head(tchain, 8))
tr <- read.table(paste0(D, "/data/synth/hifi/truth_counts.tsv"), header = TRUE, stringsAsFactors = FALSE)
tt <- tapply(tr$n_reads, tr$transcript, sum)
res <- data.frame(truth = names(tchain), truth_n = as.numeric(tt[names(tchain)]), model = NA_character_, observed = NA_real_, stringsAsFactors = FALSE)
for (i in seq_len(nrow(res))) {
  m <- names(chain)[chain == tchain[res$truth[i]]]
  if (length(m)) { res$model[i] <- paste(m, collapse = ","); res$observed[i] <- sum(cnt[m, ]) }
}
res$err_pct <- round(100 * (res$observed - res$truth_n) / res$truth_n, 1)
print(res)
cat("bambu models with intron chain not in truth:", sum(!(chain %in% tchain)), "\n")
print(table(mcols(rr)$newTxClass))
write.table(res, "bambu_vs_truth.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
