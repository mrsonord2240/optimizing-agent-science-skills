# INPUT 1 (canonical): SKILL.md "IsoformSwitchAnalyzeR Workflow" block (blocks/r_01.R) executed VERBATIM on SYNTHETIC Salmon quants
# with shuffled SRR-style sample IDs; 3 v 3 (DEXSeq branch), 6 v 6 (satuRn branch), and a control-v-control null comparison.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
set.seed(101)
tt <- truth()
evaluate <- function(sl, label, hd) {
  f <- sl$isoformFeatures; s <- score_sl(sl)
  m <- merge(f[, c("isoform_id", "dIF")], hd[, c("isoform_id", "dIF")], by = "isoform_id", suffixes = c("", ".hand"))
  chk(paste(label, "ISAR dIF == hand-computed dIF from quant.sf TPM"), max(abs(m$dIF - m$dIF.hand)) < 1e-3, sprintf("max abs diff %.2e over %d isoforms", max(abs(m$dIF - m$dIF.hand)), nrow(m)))
  cat(sprintf("[%s] tested genes %d | planted recovered %d/20 (missed: %s) | null FP %d %s | dge_only %d | small(0.06) %d | dte_like(0.15) %d\n", label, s$tested_genes, length(s$tp_planted), paste(s$fn_planted, collapse = ","), length(s$fp_null), paste(s$fp_null, collapse = ","), length(s$fp_dge), length(s$small_called), length(s$dte_called)))
  chk(paste(label, ">=19/20 planted recovered"), length(s$tp_planted) >= 19)
  chk(paste(label, "null-gene FP <= 5%"), length(s$fp_null) <= 0.05 * sum(tt$type == "null"), sprintf("%d/260", length(s$fp_null)))
  chk(paste(label, "DGE decoys not called"), length(s$fp_dge) == 0)
  dm <- dir_mag(f, tt, s$tp_planted); chk(paste(label, "direction correct, dIF within 0.1 of truth"), dm["dir"] == dm["n"] && dm["mag"] == dm["n"], sprintf("dir %d/%d mag %d/%d", dm["dir"], dm["n"], dm["mag"], dm["n"]))
  invisible(s)
}
shuf <- function(k) sprintf("SRR70%05d", sample(10000:99999, k))
# ---- 3 v 3
ids3 <- c(sprintf("ctrl_%d", 1:3), sprintf("trt_%d", 1:3)); new3 <- shuf(6); cond3 <- rep(c("control", "treatment"), each = 3)
o <- sample(6); ids3 <- ids3[o]; new3 <- new3; cond3 <- cond3[o]      # random assignment of IDs to samples
stage_salmon("w1_3v3", ids3, new3, cond3); setwd("w1_3v3")
cat("sample IDs (alphabetical) and conditions:\n"); print(read.delim("sample_metadata.tsv")[order(read.delim("sample_metadata.tsv")$sample_id), ])
run_block("r_01.R")
cat("Skill block printed count of switching isoforms (post-run recompute):", sum(aSwitchList$isoformFeatures$isoform_switch_q_value < 0.05 & abs(aSwitchList$isoformFeatures$dIF) > 0.1, na.rm = TRUE), "\n")
cat("test used:", if (max(table(design$condition)) > 5) "satuRn" else "DEXSeq", "; design:\n"); print(design)
cn <- design$condition[match(c("SRR", ""), c("SRR", ""))]  # noop
hd <- hand_dif(ids3[cond3 == "control"], ids3[cond3 == "treatment"]); hd$isoform_id <- hd$isoform_id
# hand_dif reads from SYN by the ORIGINAL ids (ids3): independent of the renamed dir
evaluate(aSwitchList, "3v3 DEXSeq (Skill block, shuffled IDs)", hd)
saveRDS(design, "design3.rds")
setwd("..")
# ---- 6 v 6 (satuRn branch)
ids6 <- c(sprintf("ctrl_%d", 1:6), sprintf("trt_%d", 1:6)); o <- sample(12); ids6 <- ids6[o]; cond6 <- rep(c("control", "treatment"), each = 6)[o]
stage_salmon("w1_6v6", ids6, shuf(12), cond6); setwd("w1_6v6")
run_block("r_01.R")
cat("6v6 test branch used:", if (max(table(design$condition)) > 5) "satuRn" else "DEXSeq", "\n")
hd6 <- hand_dif(ids6[cond6 == "control"], ids6[cond6 == "treatment"])
evaluate(aSwitchList, "6v6 satuRn (Skill block, shuffled IDs)", hd6)
setwd("..")
# ---- null comparison (control v control), through the same block, both branches
ids0 <- sprintf("ctrl_%d", 1:6); cond0 <- rep(c("nullA", "nullB"), each = 3)
stage_salmon("w1_null", ids0, shuf(6), cond0); setwd("w1_null"); run_block("r_01.R")
f <- aSwitchList$isoformFeatures; f <- f[!is.na(f$isoform_switch_q_value), ]
sg <- unique(f$gene_id[f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])
chk("NULL comparison (ctrl v ctrl 3v3, DEXSeq) <=3 genes called", length(sg) <= 3, sprintf("%d genes / %d tested; min q %.3g", length(sg), length(unique(f$gene_id)), min(f$isoform_switch_q_value)))
setwd("..")
cat("DONE input1\n")
