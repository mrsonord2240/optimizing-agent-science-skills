# Reproduce the round-2 "Null check" table on real chrX (2 GBR + 2 YRI, Salmon 2.7.0, GRCh37) with the Skill's own blocks verbatim:
# per split: workflow block (r_01, raw counts, DEXSeq branch), manual block (r_04), confirm snippet (r_05), plus DRIMSeq dmTest (my code, same as 70). Then the permutation
# block (r_02) on the true split. Assertions compare against the numbers printed in SKILL.md (20/11/15; default route 0; manual 13/0/4; DRIMSeq 11/4/3; both 7/0/1; confirmed 12/0/4).
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages({ library(IsoformSwitchAnalyzeR); library(tximport); library(DRIMSeq); library(DEXSeq); library(stageR); library(BiocParallel) })
PD <- "F:/OpenScience/audit-envs/alternative-splicing/public-data"; sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916")
t2g <- read.delim(file.path(PD, "rnasplice/salmon/genes_chrX.tx2gene.tsv"), header = FALSE); tx2gene <- data.frame(tx = t2g$V1, gene = t2g$V2)
splits <- list(true = c("GBR", "GBR", "YRI", "YRI"), mixed1 = c("A", "B", "A", "B"), mixed2 = c("A", "B", "B", "A")); out <- list()
for (sp in names(splits)) {
  wd <- paste0("w96_", sp); unlink(wd, recursive = TRUE); dir.create(file.path(wd, "salmon_quant"), recursive = TRUE)
  for (s in sm) { dir.create(file.path(wd, "salmon_quant", s)); file.copy(file.path(PD, "rnasplice/salmon", s, "quant.sf"), file.path(wd, "salmon_quant", s, "quant.sf")) }
  file.copy(file.path(PD, "rnasplice/reference/genes_chrX.gtf"), file.path(wd, "annotation.gtf")); file.copy(file.path(PD, "derived/chrX_tx.fa"), file.path(wd, "transcripts.fa"))
  write.table(data.frame(sample_id = sm, condition = splits[[sp]]), file.path(wd, "sample_metadata.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
  setwd(wd); invisible(capture.output(suppressMessages(suppressWarnings(run_block("r_01.R")))))
  f <- aSwitchList$isoformFeatures; isar_genes <- unique(f$gene_id[!is.na(f$isoform_switch_q_value) & f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])
  meta <- data.frame(sample_id = sm, condition = splits[[sp]]); files <- setNames(file.path("salmon_quant", sm, "quant.sf"), sm)
  invisible(capture.output(suppressMessages(suppressWarnings(run_block("r_04.R"))))); sg <- names(qval)[!is.na(qval) & qval < 0.05]
  invisible(capture.output(run_block("r_05.R")))
  dd <- model.matrix(~ condition, data = DRIMSeq::samples(d)); d2 <- dmPrecision(d, design = dd, BPPARAM = SerialParam()); d2 <- dmFit(d2, design = dd, verbose = 0, BPPARAM = SerialParam()); d2 <- dmTest(d2, coef = colnames(dd)[2], verbose = 0)
  dr <- DRIMSeq::results(d2); dg <- dr$gene_id[!is.na(dr$adj_pvalue) & dr$adj_pvalue < 0.05]
  out[[sp]] <- c(isar_raw = length(isar_genes), manual_dexseq = length(sg), manual_drimseq = length(dg), both = length(intersect(sg, dg)), isar_confirmed = length(confirmed))
  cat(sprintf("%-7s ISAR raw %2d | manual DEXSeq %2d | DRIMSeq %2d | both %d | ISAR calls DEXSeq-confirmed %d\n", sp, out[[sp]][1], out[[sp]][2], out[[sp]][3], out[[sp]][4], out[[sp]][5]))
  if (sp == "true") { true_genes <- isar_genes; wdt <- wd }
  setwd("..")
}
skill <- list(true = c(20, 13, 11, 7, 12), mixed1 = c(11, 0, 4, 0, 0), mixed2 = c(15, 4, 3, 1, 4))
for (sp in names(skill)) chk(paste("Null-check table row", sp, "(ISAR raw, manual DEXSeq, DRIMSeq, both, confirmed) equals SKILL.md"), all(out[[sp]] == skill[[sp]]), paste(out[[sp]], collapse = "/"))
cat("### the Skill's permutation block (r_02) verbatim on the true chrX split\n")
setwd(wdt); invisible(capture.output(suppressMessages(suppressWarnings(run_block("r_01.R"))))); t0 <- Sys.time(); invisible(capture.output(suppressMessages(suppressWarnings(run_block("r_02.R")))))
cat(sprintf("SKILL BLOCK OUTPUT -> observed %d genes; label-permuted: %s | splits produced %d | %.0f s\n", observed, paste(permuted, collapse = " "), length(perms), as.numeric(difftime(Sys.time(), t0, units = "secs"))))
chk("permutation block on chrX: observed 20; every permuted count within 10-16 (Skill: 15 and 11); only 2 alternative splits exist", observed == 20 && length(perms) == 2 && all(permuted >= 10 & permuted <= 16), paste(permuted, collapse = "/"))
setwd(".."); cat("DONE 96\n")
