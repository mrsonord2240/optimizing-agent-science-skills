# INPUT 1 (canonical): SKILL.md "IsoformSwitchAnalyzeR v2 Workflow" code, verbatim calls, on SYNTHETIC 3 v 3 Salmon quants.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
# --- stage a 3v3 salmon dir (copy; no symlinks)
d3 <- "salmon3v3"; unlink(d3, recursive = TRUE); dir.create(d3)
keep <- c(sprintf("ctrl_%d", 1:3), sprintf("trt_%d", 1:3))
for (s in keep) { dir.create(file.path(d3, s)); file.copy(file.path(SYN, "salmon_quant", s, "quant.sf"), file.path(d3, s, "quant.sf")) }
file.copy(file.path(SYN, "annotation.gtf"), "annotation.gtf", overwrite = TRUE); file.copy(file.path(SYN, "transcripts.fa"), "transcripts.fa", overwrite = TRUE)

# ---- SKILL.md code (Salmon import, design, importRdata, preFilter)  ----
salmonQuant <- importIsoformExpression(parentDir = 'salmon3v3/', addIsofomIdAsColumn = TRUE)
str(lapply(salmonQuant, dim))
design <- data.frame(
    sampleID = colnames(salmonQuant$counts)[-1],
    condition = c('control', 'control', 'control', 'treatment', 'treatment', 'treatment')
)
print(design)
# TRAP: importIsoformExpression orders samples alphabetically -> ctrl_*, trt_* ; the hard-coded condition vector matches only because of naming
chk("design sample order == quant column order", identical(design$sampleID, c(sprintf("ctrl_%d",1:3), sprintf("trt_%d",1:3))), paste(design$sampleID, collapse=","))
aSwitchList <- importRdata(
    isoformCountMatrix = salmonQuant$counts,
    isoformRepExpression = salmonQuant$abundance,
    designMatrix = design,
    isoformExonAnnoation = 'annotation.gtf',
    isoformNtFasta = 'transcripts.fa',
    showProgress = TRUE
)
aSwitchList <- preFilter(
    aSwitchList,
    geneExpressionCutoff = 1,
    isoformExpressionCutoff = 0,
    IFcutoff = 0.01,
    removeSingleIsoformGenes = TRUE,
    keepIsoformInAllConditions = TRUE
)
saveRDS(aSwitchList, "in1_prefiltered.rds")
sl_dex <- aSwitchList
# Skill's own example test = satuRn on a 3v3 design (its rule says satuRn only if >5 reps)
slSat <- isoformSwitchTestSatuRn(aSwitchList, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, diagplots = FALSE)
# rule-consistent test (<=5 reps -> DEXSeq)
slDex <- isoformSwitchTestDEXSeq(sl_dex, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1)
saveRDS(slSat, "in1_satuRn.rds"); saveRDS(slDex, "in1_dexseq.rds")

# ---- independent checks against planted truth and hand-computed dIF ----
hd <- hand_dif(keep[1:3], keep[4:6])
for (nm in c("satuRn", "DEXSeq")) {
  sl <- if (nm == "satuRn") slSat else slDex
  cat("\n=====", nm, "=====\n")
  f <- sl$isoformFeatures
  m <- merge(f[, c("isoform_id","gene_id","IF1","IF2","dIF")], hd, by = "isoform_id", suffixes = c("", ".hand"))
  chk(paste(nm, "ISAR dIF == hand-computed mean-of-sample-IF dIF (from quant.sf TPM)"), max(abs(m$dIF - m$dIF.hand)) < 1e-3, sprintf("max abs diff %.2e over %d isoforms", max(abs(m$dIF - m$dIF.hand)), nrow(m)))
  s <- score_sl(sl)
  t <- truth()
  cat(sprintf("tested genes %d | planted switches recovered %d/20 | false-neg %s\n", s$tested_genes, length(s$tp_planted), paste(s$fn_planted, collapse=",")))
  cat(sprintf("null-gene false positives %d (of %d null) %s | dge_only called %d | small_switch (dIF~0.06) called %d | dte_like called %d\n",
      length(s$fp_null), sum(t$type=="null"), paste(s$fp_null, collapse=","), length(s$fp_dge), length(s$small_called), length(s$dte_called)))
  chk(paste(nm, "recovers >=18/20 planted switches"), length(s$tp_planted) >= 18)
  chk(paste(nm, "null-gene FP <= 5% of null genes"), length(s$fp_null) <= 0.05 * sum(t$type == "null"))
  chk(paste(nm, "gene-level DGE decoys not called"), length(s$fp_dge) == 0)
  # direction + magnitude: for planted genes, isoform B (poison) / C (skip) must have dIF>0 and be within 0.1 of truth
  ok_dir <- 0; ok_mag <- 0; n_ev <- 0
  for (g in s$tp_planted) {
    tt <- t[t$gene_id == g, ]; iso <- if (tt$type == "poison_switch") paste0(g, "_B") else paste0(g, "_C")
    tru <- if (tt$type == "poison_switch") tt$IF_B_trt - tt$IF_B_ctrl else tt$IF_C_trt - tt$IF_C_ctrl
    row <- f[f$isoform_id == iso, ]; n_ev <- n_ev + 1
    ok_dir <- ok_dir + as.integer(row$dIF > 0); ok_mag <- ok_mag + as.integer(abs(row$dIF - tru) < 0.1)
  }
  chk(paste(nm, "direction correct (up-isoform dIF>0)"), ok_dir == n_ev, sprintf("%d/%d", ok_dir, n_ev))
  chk(paste(nm, "dIF within 0.1 of planted truth"), ok_mag == n_ev, sprintf("%d/%d", ok_mag, n_ev))
  # significant table example
  top <- extractTopSwitches(sl, filterForConsequences = FALSE, n = 5, sortByQvals = TRUE)
  print(top[, intersect(c("gene_name","condition_1","condition_2","gene_switch_q_value","switchConsequencesGene","Rank"), colnames(top))])
}

# ---- null comparison: control 1-3 vs control 4-6 (no true difference) through the same code ----
d0 <- "salmon_null"; unlink(d0, recursive = TRUE); dir.create(d0)
for (s in sprintf("ctrl_%d", 1:6)) { dir.create(file.path(d0, s)); file.copy(file.path(SYN, "salmon_quant", s, "quant.sf"), file.path(d0, s, "quant.sf")) }
sq0 <- importIsoformExpression(parentDir = 'salmon_null/', addIsofomIdAsColumn = TRUE, showProgress = FALSE, quiet = TRUE)
des0 <- data.frame(sampleID = colnames(sq0$counts)[-1], condition = rep(c("nullA", "nullB"), each = 3))
sl0 <- importRdata(sq0$counts, sq0$abundance, des0, 'annotation.gtf', 'transcripts.fa', showProgress = FALSE, quiet = TRUE)
sl0 <- preFilter(sl0, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, IFcutoff = 0.01, removeSingleIsoformGenes = TRUE, quiet = TRUE)
sl0d <- isoformSwitchTestDEXSeq(sl0, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, quiet = TRUE)
sl0s <- isoformSwitchTestSatuRn(sl0, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, diagplots = FALSE, quiet = TRUE)
for (nm in c("DEXSeq", "satuRn")) {
  sl <- if (nm == "DEXSeq") sl0d else sl0s
  f <- sl$isoformFeatures; f <- f[!is.na(f$isoform_switch_q_value), ]
  ng <- sum(f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1)
  chk(paste("NULL comparison", nm, "<=3 calls"), length(unique(f$gene_id[f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])) <= 3,
      sprintf("%d isoform calls in %d tested genes (q<0.05 & |dIF|>0.1); min q = %.3g", ng, length(unique(f$gene_id)), min(f$isoform_switch_q_value)))
}
cat("DONE input1\n")
