# INPUT 8 (NEW, auditor's own data): 4 v 7 UNBALANCED design, batch column, shuffled SRR IDs and metadata rows, new gene set/effect sizes (data/new1, seed 8801).
# 8A SKILL block r_01 verbatim (max replicates 7 -> satuRn branch), without and with the batch line the block itself offers (uncommented);
# 8B same data, DEXSeq branch forced, for comparison; 8C treatment-only 3 v 4 null split (batch column); 8D truth scoring incl. batch-artefact genes.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
NEW <- "F:/OpenScience/audits/bio-isoform-switching/run/data/new1"; tt <- read.delim(file.path(NEW, "truth_genes.tsv"), stringsAsFactors = FALSE)
stage <- function(wd, ids = NULL, cond = NULL) { unlink(wd, recursive = TRUE); dir.create(file.path(wd, "salmon_quant"), recursive = TRUE)
  m <- read.delim(file.path(NEW, "sample_metadata.tsv"), stringsAsFactors = FALSE); if (!is.null(ids)) m <- m[m$sample_id %in% ids, ]
  for (s in m$sample_id) { dir.create(file.path(wd, "salmon_quant", s)); file.copy(file.path(NEW, "salmon_quant", s, "quant.sf"), file.path(wd, "salmon_quant", s, "quant.sf")) }
  if (!is.null(cond)) m$condition <- cond[match(m$sample_id, names(cond))]
  write.table(m, file.path(wd, "sample_metadata.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
  file.copy(file.path(NEW, "annotation.gtf"), file.path(wd, "annotation.gtf")); file.copy(file.path(NEW, "transcripts.fa"), file.path(wd, "transcripts.fa")); m }
score <- function(sl, label) {
  f <- sl$isoformFeatures; f <- f[!is.na(f$isoform_switch_q_value), ]; sig <- f[f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1, ]; g <- unique(sig$gene_id)
  pl <- tt$gene_id[tt$true_switch]; nul <- tt$gene_id[tt$type == "null" & !tt$is_batch_gene]; bg <- tt$gene_id[tt$is_batch_gene]
  dm <- dir_mag(f, tt, intersect(g, pl))
  cat(sprintf("[%s] tested %d genes | planted %d/20 | batch-artefact genes %d/20 | other null FP %d/%d | dge_only %d | small(0.04) %d | dir %d/%d mag(<0.1) %d/%d\n", label, length(unique(f$gene_id)), length(intersect(g, pl)), length(intersect(g, bg)), length(intersect(g, nul)), length(nul), length(intersect(g, tt$gene_id[tt$type == "dge_only"])), length(intersect(g, tt$gene_id[tt$type == "small_switch"])), dm["dir"], dm["n"], dm["mag"], dm["n"]))
  invisible(list(pl = length(intersect(g, pl)), bg = length(intersect(g, bg)), nul = length(intersect(g, nul)), dm = dm, sig = sig)) }
# ---- 8A without batch
m <- stage("w8a"); setwd("w8a"); cat("metadata (rows shuffled):\n"); print(m)
run_block("r_01.R"); cat("test branch:", if (max(table(design$condition)) > 5) "satuRn" else "DEXSeq", "| design:\n"); print(design)
chk("8A design joined by name: condition of each sample equals metadata", all(design$condition == m$condition[match(design$sampleID, m$sample_id)]))
sA <- score(aSwitchList, "4v7 satuRn, no batch column")
chk("8A >=19/20 planted (effect 0.30-0.45) recovered", sA$pl >= 19, sA$pl)
chk("8A dir and magnitude right for all recovered planted", sA$dm["dir"] == sA$dm["n"] && sA$dm["mag"] == sA$dm["n"])
# ---- 8A' with batch line uncommented (the Skill's own instruction)
txt <- readLines(file.path("F:/OpenScience/audits/bio-isoform-switching/run/blocks", "r_01.R")); i <- grep("^# design\\$batch", txt); stopifnot(length(i) == 1)
txt[i] <- sub("^# ", "", txt[i]); writeLines(txt, "block_batch.R"); cat("uncommented line:", txt[i], "\n")
source("block_batch.R"); cat("design with batch:\n"); print(design)
sB <- score(aSwitchList, "4v7 satuRn, batch column")
chk("8A' batch column removes >=75% of batch-artefact calls and keeps >=19/20 planted", sB$bg <= 0.25 * max(sA$bg, 1) && sB$pl >= 19, sprintf("artefacts %d -> %d ; planted %d -> %d", sA$bg, sB$bg, sA$pl, sB$pl))
setwd("..")
# ---- 8B DEXSeq branch forced (compare with the Skill's satuRn choice at n=7)
setwd("w8a"); txt <- readLines("block_batch.R"); j <- grep("isoformSwitchTestSatuRn", txt); k <- grep("isoformSwitchTestDEXSeq", txt)
txt2 <- txt; txt2[grep("max\\(table\\(design\\$condition\\)\\) > 5", txt2)] <- sub("> 5", "> 50", txt2[grep("max\\(table\\(design\\$condition\\)\\) > 5", txt2)]); writeLines(txt2, "block_dex.R")
source("block_dex.R"); sD <- score(aSwitchList, "4v7 DEXSeq forced, batch column")
setwd("..")
# ---- 8C null split among the 7 treatment samples (3 v 4), batch column kept
mm <- read.delim(file.path(NEW, "sample_metadata.tsv"), stringsAsFactors = FALSE); trt <- mm$sample_id[mm$condition == "treatment"]
cnd <- setNames(c(rep("nullA", 3), rep("nullB", 4)), trt)
m0 <- stage("w8c", trt, cnd); setwd("w8c"); txt <- readLines("../w8a/block_batch.R"); writeLines(txt, "block_batch.R"); source("block_batch.R")
f <- aSwitchList$isoformFeatures; f <- f[!is.na(f$isoform_switch_q_value), ]; g0 <- unique(f$gene_id[f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])
cat(sprintf("[null split 3v4 among treatment samples, DEXSeq, batch] tested %d genes, %d called (%s)\n", length(unique(f$gene_id)), length(g0), paste(head(g0, 8), collapse = ",")))
chk("8C null split: gene calls <= 5% of tested genes", length(g0) <= 0.05 * length(unique(f$gene_id)), sprintf("%d/%d", length(g0), length(unique(f$gene_id))))
setwd("..")
cat("DONE 8A-8C\n")
