# The shipped example on the mixed chrX split (35c) called 0 genes while the workflow block on the same split called 11 (71, 96). 35c's log shows
# "Added 1 batch/covariates to the design matrix" (a sva surrogate variable). Test: is the switch list reproducible run to run? Workflow block (r_01) verbatim,
# real chrX mixed1 split (ERR188383+ERR188454 v ERR188428+ERR204916) and the true GBR v YRI split, different set.seed() values; record whether sv was added and the call count.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
PD <- "F:/OpenScience/audit-envs/alternative-splicing/public-data"; sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916")
lab <- list(mixed1 = c("A", "B", "A", "B"), true = c("GBR", "GBR", "YRI", "YRI"))
for (sp in names(lab)) {
  wd <- paste0("w99c_", sp); unlink(wd, recursive = TRUE); dir.create(file.path(wd, "salmon_quant"), recursive = TRUE)
  for (s in sm) { dir.create(file.path(wd, "salmon_quant", s)); file.copy(file.path(PD, "rnasplice/salmon", s, "quant.sf"), file.path(wd, "salmon_quant", s, "quant.sf")) }
  file.copy(file.path(PD, "rnasplice/reference/genes_chrX.gtf"), file.path(wd, "annotation.gtf")); file.copy(file.path(PD, "derived/chrX_tx.fa"), file.path(wd, "transcripts.fa"))
  write.table(data.frame(sample_id = sm, condition = lab[[sp]]), file.path(wd, "sample_metadata.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
  setwd(wd)
  for (sd in c(1, 2, 3, 4, 5, 6)) {
    set.seed(sd); log <- capture.output(suppressWarnings(run_block("r_01.R")))
    f <- aSwitchList$isoformFeatures; g <- unique(f$gene_id[!is.na(f$isoform_switch_q_value) & f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])
    cat(sprintf("%-7s seed %d: covariates in design: %-22s | genes called %2d\n", sp, sd, paste(colnames(aSwitchList$designMatrix)[-(1:2)], collapse = ",") , length(g)))
  }
  setwd("..")
}
cat("DONE 99c\n")
