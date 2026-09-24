# INPUT 10 (NEW, Edge): unbalanced 3 v 5 design whose sample IDs are not R-syntactic ("1-ctrl", "trt.1-b": leading digit, dash, dot), no batch.
# Realistic for hand-named Salmon directories. (10A) SKILL.md workflow block verbatim (blocks/r_01.R); (10B) manual DTU block verbatim (blocks/r_04.R) + the
# confirm snippet (blocks/r_05.R); (10C) shipped example in real-data mode; all scored against planted truth. Synthetic data (05_gen_het.R, planted, no het genes).
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR)); set.seed(1010)
D <- "F:/OpenScience/audits/bio-isoform-switching/run/data/odd_3v5"
tt <- read.delim(file.path(D, "truth_genes.tsv"), stringsAsFactors = FALSE); planted <- tt$gene_id[tt$true_switch]
wd <- "w10"; unlink(wd, recursive = TRUE); dir.create(wd); file.copy(file.path(D, c("salmon_quant", "annotation.gtf", "transcripts.fa", "sample_metadata.tsv")), wd, recursive = TRUE)
setwd(wd)
cat("sample dirs:", paste(list.files("salmon_quant"), collapse = ", "), "\n"); print(read.delim("sample_metadata.tsv"))
cat("### 10A SKILL workflow block verbatim\n")
r10a <- tryCatch({ run_block("r_01.R"); "no error" }, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("10A result:", r10a, "\n")
if (r10a == "no error") {
  f <- aSwitchList$isoformFeatures; s <- f[!is.na(f$isoform_switch_q_value) & f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1, ]; g <- unique(s$gene_id)
  cat(sprintf("test branch: %s | design sample IDs in list: %s\n", if (max(table(design$condition)) > 5) "satuRn" else "DEXSeq", paste(aSwitchList$designMatrix$sampleID, collapse = ",")))
  cat(sprintf("10A: %d genes called | planted %d/20 | other genes %d\n", length(g), length(intersect(g, planted)), length(setdiff(g, planted))))
  chk("10A odd IDs: planted recovered >= 19/20", length(intersect(g, planted)) >= 19, length(intersect(g, planted)))
  chk("10A odd IDs: <= 2 non-planted genes", length(setdiff(g, planted)) <= 2)
  ff <- f[f$isoform_id %in% c(paste0(planted[1:10], "_B"), paste0(planted[11:20], "_C")) & !duplicated(f$isoform_id), ]
  dr <- sapply(planted, function(p) { i <- if (tt$type[tt$gene_id == p] == "poison_switch") paste0(p, "_B") else paste0(p, "_C"); ff$dIF[ff$isoform_id == i] })
  chk("10A dIF of the switching isoform > 0 in 20/20 planted", sum(unlist(dr) > 0) == 20, sum(unlist(dr) > 0))
}
cat("\n### 10B manual DTU block verbatim (r_04) then confirm snippet (r_05)\n")
meta <- read.delim("sample_metadata.tsv", stringsAsFactors = FALSE)
files <- setNames(file.path("salmon_quant", meta$sample_id, "quant.sf"), meta$sample_id)
suppressPackageStartupMessages({ library(tximport); library(DRIMSeq); library(DEXSeq); library(stageR) })
tx <- read.delim(files[1])$Name; tx2gene <- data.frame(tx = tx, gene = sub("_[ABC]$", "", tx))
r10b <- tryCatch({ run_block("r_04.R"); "no error" }, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("10B result:", r10b, "\n")
if (r10b == "no error") {
  sg <- names(qval)[!is.na(qval) & qval < 0.05]
  cat(sprintf("10B manual: gene q<0.05 %d | planted %d/20 | other %d | dmFilter kept genes %d (n=%d, n_small=%d)\n", length(sg), length(intersect(sg, planted)), length(setdiff(sg, planted)), length(unique(dxr$groupID)), n, n_small))
  chk("10B manual pipeline recovers >= 18/20 planted at 3 v 5", length(intersect(sg, planted)) >= 18, length(intersect(sg, planted)))
  if (r10a == "no error") { run_block("r_05.R"); cat(sprintf("10B confirm snippet: ISAR called %d genes, %d DEXSeq-confirmed, planted among confirmed %d\n", length(called), length(confirmed), length(intersect(confirmed, planted)))) }
  rs <- getAdjustedPValues(stageRObj, order = FALSE, onlySignificantGenes = FALSE)
  cat("stageR result columns:", paste(colnames(rs), collapse = ","), "| rows", nrow(rs), "\n")
}
cat("DONE 92\n")
