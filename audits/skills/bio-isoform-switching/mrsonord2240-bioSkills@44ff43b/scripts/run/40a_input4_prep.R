# INPUT 4 (Variant B) part A: functional-consequence workflow on SYNTHETIC 6 v 6 with planted poison-exon (NMD) and ubiquitin-domain-loss switches.
# Follows SKILL.md order: importRdata -> preFilter -> isoformSwitchTestSatuRn (6 v 6 => ">5 reps => satuRn") -> extractSequence -> (external tools) -> analyzeORF ...
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
d6 <- "salmon6v6"; unlink(d6, recursive = TRUE); dir.create(d6)
ids <- c(sprintf("ctrl_%d", 1:6), sprintf("trt_%d", 1:6))
for (s in ids) { dir.create(file.path(d6, s)); file.copy(file.path(SYN, "salmon_quant", s, "quant.sf"), file.path(d6, s, "quant.sf")) }
file.copy(file.path(SYN, "annotation.gtf"), "annotation.gtf", overwrite = TRUE); file.copy(file.path(SYN, "transcripts.fa"), "transcripts.fa", overwrite = TRUE)
salmonQuant <- importIsoformExpression(parentDir = 'salmon6v6/', addIsofomIdAsColumn = TRUE, showProgress = FALSE, quiet = TRUE)
design <- data.frame(sampleID = colnames(salmonQuant$counts)[-1], condition = rep(c('control', 'treatment'), each = 6))
aSwitchList <- importRdata(isoformCountMatrix = salmonQuant$counts, isoformRepExpression = salmonQuant$abundance, designMatrix = design,
                           isoformExonAnnoation = 'annotation.gtf', isoformNtFasta = 'transcripts.fa', showProgress = FALSE, quiet = TRUE)
aSwitchList <- preFilter(aSwitchList, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, IFcutoff = 0.01, removeSingleIsoformGenes = TRUE, keepIsoformInAllConditions = TRUE, quiet = TRUE)
aSwitchList <- isoformSwitchTestSatuRn(aSwitchList, reduceToSwitchingGenes = TRUE, alpha = 0.05, dIFcutoff = 0.1, diagplots = FALSE, quiet = TRUE)
cat("genes kept after reduceToSwitchingGenes:", length(unique(aSwitchList$isoformFeatures$gene_id)), "\n")
s <- score_sl(aSwitchList); cat(sprintf("satuRn 6v6: planted recovered %d/20, null FP %d, dge decoys %d\n", length(s$tp_planted), length(s$fp_null), length(s$fp_dge)))
chk("satuRn (6v6, Skill call with reduceToSwitchingGenes=TRUE) keeps all 20 planted switch genes", length(s$tp_planted) == 20, sprintf("%d/20", length(s$tp_planted)))

# --- SKILL order: extractSequence BEFORE analyzeORF
dir.create("sequences", showWarnings = FALSE)
r1 <- tryCatch({ x <- extractSequence(aSwitchList, pathToOutput = 'sequences/', writeToFile = TRUE); "ok" },
               error = function(e) paste("ERROR:", conditionMessage(e)))
cat("Skill order extractSequence() before analyzeORF():", r1, "\n")
chk("SKILL order (extractSequence -> analyzeORF) works as documented", identical(r1, "ok"), r1)
# ORF prediction first (ISAR requirement when the GTF has no CDS)
aSwitchList <- analyzeORF(aSwitchList, orfMethod = 'longest', genomeObject = NULL, quiet = TRUE)
cat("ORF table rows:", nrow(aSwitchList$orfAnalysis), "\n")
r2 <- tryCatch({ aSwitchList <- extractSequence(aSwitchList, pathToOutput = 'sequences/', writeToFile = TRUE, quiet = TRUE); "ok" }, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("extractSequence() AFTER analyzeORF():", r2, "\n")
print(list.files("sequences"))
# ORF-level ground truth: predicted ORF of every canonical isoform A must start at nt 31 (5'UTR 30 nt) ; poison isoform B ORF must end inside exon P
o <- aSwitchList$orfAnalysis
oa <- o[grepl("_A$", o$isoform_id), ]
stopifnot(nrow(oa) > 0)
chk("analyzeORF finds the planted CDS start (ATG at transcript position 31) in all canonical isoforms", all(oa$orfTransciptStart == 31), sprintf("%d isoforms, starts: %s", nrow(oa), paste(unique(oa$orfTransciptStart), collapse = ",")))
tr <- truth()
gene <- sub("_[ABC]$", "", o$isoform_id); is_poisonB <- grepl("_B$", o$isoform_id) & gene %in% tr$gene_id[tr$type == "poison_switch"]
chk("analyzeORF PTC flag == planted poison isoform (B of poison genes) for every isoform", all(o$PTC == is_poisonB), sprintf("PTC TRUE: %d, planted poison isoforms present: %d, mismatches: %d", sum(o$PTC), sum(is_poisonB), sum(o$PTC != is_poisonB)))
# hand-computed PTC distance to last exon-exon junction from GTF exon lengths
gtf <- read.delim("annotation.gtf", header = FALSE, stringsAsFactors = FALSE, quote = ""); tid <- sub('.*transcript_id "([^"]+)".*', "\\1", gtf$V9); ln <- gtf$V5 - gtf$V4 + 1
strand <- gtf$V7; tlen <- tapply(ln, tid, sum)
# last exon in transcript order = highest coord for '+', lowest for '-'
lastlen <- sapply(split(seq_along(tid), tid), function(ix) { g <- gtf[ix, ]; if (g$V7[1] == "+") ln[ix][which.max(g$V4)] else ln[ix][which.min(g$V4)] })
hand_dist <- (tlen[o$isoform_id] - lastlen[o$isoform_id]) - o$orfTransciptEnd   # nt from stop-codon end to last junction
poi <- o[is_poisonB, ]
cat("PTC distance (nt, ISAR stopDistanceToLastJunction vs hand) for poison isoforms:
"); print(data.frame(isoform_id = poi$isoform_id, ISAR = poi$stopDistanceToLastJunction, hand = as.numeric(hand_dist[poi$isoform_id]))[1:5, ])
chk("ISAR stopDistanceToLastJunction == hand-computed for all poison isoforms", all(poi$stopDistanceToLastJunction == hand_dist[poi$isoform_id]), sprintf("%d isoforms", nrow(poi)))
saveRDS(aSwitchList, "in4_after_orf.rds")
cat("DONE 40a\n")
