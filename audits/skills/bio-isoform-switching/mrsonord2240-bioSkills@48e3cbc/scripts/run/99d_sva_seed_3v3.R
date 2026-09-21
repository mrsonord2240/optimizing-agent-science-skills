# Same seed-sensitivity test as 99c on planted 3 v 3 data (het_3v3) and on the 9A pure-null design at n=3 (het_null, first 6 samples): workflow block r_01 verbatim under set.seed(1..6).
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR)); D <- "../data"
stage <- function(wd, src, ids = NULL, cond = NULL) { unlink(wd, recursive = TRUE); dir.create(wd); dir.create(file.path(wd, "salmon_quant")); m <- read.delim(file.path(src, "sample_metadata.tsv"), stringsAsFactors = FALSE)
  if (!is.null(ids)) { m <- data.frame(sample_id = ids, condition = cond) }
  for (s in m$sample_id) { dir.create(file.path(wd, "salmon_quant", s)); file.copy(file.path(src, "salmon_quant", s, "quant.sf"), file.path(wd, "salmon_quant", s, "quant.sf")) }
  write.table(m, file.path(wd, "sample_metadata.tsv"), sep = "\t", quote = FALSE, row.names = FALSE); file.copy(file.path(src, c("annotation.gtf", "transcripts.fa")), wd) }
sets <- list(planted_3v3 = function() stage("w99d1", file.path(D, "het_3v3")),
             null_3v3 = function() { ids <- sort(list.files(file.path(D, "het_null/salmon_quant")))[1:6]; stage("w99d2", file.path(D, "het_null"), ids, rep(c("A", "B"), 3)) })
for (nm in names(sets)) { sets[[nm]](); setwd(if (nm == "planted_3v3") "w99d1" else "w99d2")
  for (sd in 1:6) { set.seed(sd); invisible(capture.output(suppressWarnings(run_block("r_01.R")))); f <- aSwitchList$isoformFeatures
    g <- unique(f$gene_id[!is.na(f$isoform_switch_q_value) & f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])
    cat(sprintf("%-11s seed %d: covariates: %-6s | genes called %2d\n", nm, sd, paste(colnames(aSwitchList$designMatrix)[-(1:2)], collapse = ","), length(g))) }
  setwd("..") }
cat("DONE 99d\n")
