# Skill calls analyzeORF(orfMethod='longest') unconditionally. On a GTF that already carries CDS, does that overwrite annotated ORFs, and how good is de novo 'longest' PTC/NMD vs Ensembl NMD biotype?
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages({ library(IsoformSwitchAnalyzeR); library(tximport) })
sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916"); design <- data.frame(sampleID = sm, condition = c("GBR", "GBR", "YRI", "YRI"))
txi <- suppressMessages(tximport(setNames(file.path("real_salmon", sm, "quant.sf"), sm), type = "salmon", txOut = TRUE, countsFromAbundance = "no"))
sl <- suppressWarnings(importRdata(data.frame(isoform_id = rownames(txi$counts), txi$counts, check.names = FALSE), data.frame(isoform_id = rownames(txi$abundance), txi$abundance, check.names = FALSE), design, "annotation.gtf", "transcripts.fa", showProgress = FALSE, quiet = TRUE))
a <- sl$orfAnalysis[, c("isoform_id", "orfTransciptStart", "orfTransciptEnd", "PTC")]; names(a)[2:4] <- c("s0", "e0", "ptc0")
sl2 <- suppressWarnings(analyzeORF(sl, orfMethod = "longest", quiet = TRUE)); b <- sl2$orfAnalysis
cat("orf_origin before:", paste(names(table(sl$orfAnalysis$orf_origin)), table(sl$orfAnalysis$orf_origin), collapse = " "), "| after analyzeORF(longest):", paste(names(table(b$orf_origin)), table(b$orf_origin), collapse = " "), "\n")
m <- merge(a, b[, c("isoform_id", "orfTransciptStart", "orfTransciptEnd", "PTC")], by = "isoform_id")
same <- mean(m$s0 == m$orfTransciptStart & m$e0 == m$orfTransciptEnd); cat(sprintf("annotated vs longest-predicted ORF identical for %.1f%% of %d isoforms\n", 100 * same, nrow(m)))
tid_of <- function(x) vapply(regmatches(x, regexec('transcript_id "([^"]+)"', x)), function(z) z[2], "")
g <- read.delim("annotation.gtf", header = FALSE, stringsAsFactors = FALSE, quote = "", comment.char = ""); tl <- g[g$V3 == "transcript", ]; bt <- setNames(tl$V2, tid_of(tl$V9))
m$nmd <- bt[m$isoform_id] == "nonsense_mediated_decay"
for (v in c("ptc0", "PTC")) { tb <- table(factor(m[[v]], c(FALSE, TRUE)), factor(m$nmd, c(FALSE, TRUE))); cat(sprintf("%-5s vs Ensembl NMD biotype: sens %.2f (%d/%d) spec %.2f (%d/%d) | %s\n", v, tb[2,2]/sum(tb[,2]), tb[2,2], sum(tb[,2]), tb[1,1]/sum(tb[,1]), tb[1,1], sum(tb[,1]), if (v == "ptc0") "GTF-annotated ORFs" else "analyzeORF(longest)")) }
chk("analyzeORF(orfMethod='longest') preserves annotated CDS ORFs when the GTF has them", same > 0.9, sprintf("%.0f%% identical; all origins now '%s'", 100 * same, paste(unique(b$orf_origin), collapse = "/")))
