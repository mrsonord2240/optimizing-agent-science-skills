# INPUT 5 (Stress): batch-confounded SYNTHETIC design + sample-order hazard in the Skill's hard-coded design vector.
# synthB = synth with a batch effect (b2: 40% of isoform A counts move to C in 30 otherwise-null genes GENE100-GENE129),
# batch imbalanced with condition (ctrl: 5 b1 + 1 b2; trt: 1 b1 + 5 b2).  All SYNTHETIC.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
set.seed(5)
ids <- c(sprintf("ctrl_%d", 1:6), sprintf("trt_%d", 1:6))
batch <- c(rep("b1", 5), "b2", "b1", rep("b2", 5)); names(batch) <- ids
bgenes <- sprintf("GENE%03d", 100:129); tr <- truth()
stopifnot(all(tr$type[match(bgenes, tr$gene_id)] == "null"))
outB <- file.path(dirname(SYN), "synthB", "salmon_quant"); unlink(dirname(outB), recursive = TRUE); dir.create(outB, recursive = TRUE)
for (s in ids) {
  q <- read.delim(file.path(SYN, "salmon_quant", s, "quant.sf"), stringsAsFactors = FALSE)
  if (batch[s] == "b2") for (g in bgenes) {
    a <- which(q$Name == paste0(g, "_A")); cI <- which(q$Name == paste0(g, "_C"))
    mv <- rbinom(1, round(q$NumReads[a]), 0.4); q$NumReads[a] <- q$NumReads[a] - mv; q$NumReads[cI] <- q$NumReads[cI] + mv
  }
  rpk <- q$NumReads / q$EffectiveLength; q$TPM <- rpk / sum(rpk) * 1e6
  dir.create(file.path(outB, s)); write.table(q, file.path(outB, s, "quant.sf"), sep = "\t", quote = FALSE, row.names = FALSE)
}
cat("SYNTHETIC batch dataset written:", outB, "\n")
file.copy(file.path(SYN, "annotation.gtf"), "annotation.gtf", overwrite = TRUE); file.copy(file.path(SYN, "transcripts.fa"), "transcripts.fa", overwrite = TRUE)
sq <- importIsoformExpression(parentDir = paste0(outB, "/"), addIsofomIdAsColumn = TRUE, showProgress = FALSE, quiet = TRUE)
run <- function(design, label) {
  sl <- importRdata(sq$counts, sq$abundance, design, "annotation.gtf", "transcripts.fa", showProgress = FALSE, quiet = TRUE)
  sl <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, IFcutoff = 0.01, removeSingleIsoformGenes = TRUE, quiet = TRUE)
  sl <- isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, quiet = TRUE)
  s <- score_sl(sl); called <- s$sig_genes
  cat(sprintf("%-32s planted %2d/20 | batch-artefact genes called %2d/30 | other null FP %d | total genes called %d\n", label, length(s$tp_planted), length(intersect(called, bgenes)), length(setdiff(intersect(called, tr$gene_id[tr$type == "null"]), bgenes)), length(called)))
  list(sl = sl, s = s, called = called)
}
cond <- rep(c("control", "treatment"), each = 6)
cat("\n### (a) condition-only design (what the Skill shows) on batch-confounded data\n")
ra <- run(data.frame(sampleID = colnames(sq$counts)[-1], condition = cond), "no batch column")
cat("\n### (b) design with a batch column (ISAR feature, not mentioned in the Skill)\n")
rb <- run(data.frame(sampleID = colnames(sq$counts)[-1], condition = cond, batch = unname(batch[colnames(sq$counts)[-1]])), "batch column in designMatrix")
chk("Ignoring the batch produces batch-artefact false positives (design hazard is real)", length(intersect(ra$called, bgenes)) >= 5, sprintf("%d/30 artefact genes called", length(intersect(ra$called, bgenes))))
chk("Adding batch to the designMatrix removes >=80% of the artefact calls and keeps >=18/20 planted switches", length(intersect(rb$called, bgenes)) <= 0.2 * length(intersect(ra$called, bgenes)) && length(rb$s$tp_planted) >= 18,
    sprintf("artefacts %d -> %d ; planted %d/20", length(intersect(ra$called, bgenes)), length(intersect(rb$called, bgenes)), length(rb$s$tp_planted)))

cat("\n### (c) perfectly confounded covariate (batch == condition): Skill 'Common Errors' says rank-deficient design errors\n")
rc <- tryCatch({ x <- importRdata(sq$counts, sq$abundance, data.frame(sampleID = colnames(sq$counts)[-1], condition = cond, batch = cond), "annotation.gtf", "transcripts.fa", showProgress = FALSE, quiet = TRUE)
  x <- preFilter(x, quiet = TRUE); x <- isoformSwitchTestDEXSeq(x, reduceToSwitchingGenes = FALSE, quiet = TRUE); paste("no error; isoform_switch_q_value non-NA:", sum(!is.na(x$isoformFeatures$isoform_switch_q_value))) },
  error = function(e) paste("ERROR:", conditionMessage(e)))
cat("confounded design ->", rc, "\n")
chk("Perfect confounding is caught with an explicit error (not silently analysed)", grepl("ERROR", rc), rc)

cat("\n### (d) sample-order hazard: Skill hard-codes condition = c(control x3, treatment x3) positionally against colnames(counts)[-1]\n")
# rename dirs so alphabetical order interleaves the conditions (SRR-style IDs): odd = treatment, even = control
map <- data.frame(old = ids, new = sprintf("SRR%06d", c(2,4,6,8,10,12, 1,3,5,7,9,11)), cond = cond, stringsAsFactors = FALSE)
dO <- "salmon_srr"; unlink(dO, recursive = TRUE); dir.create(dO)
for (i in seq_len(nrow(map))) { dir.create(file.path(dO, map$new[i])); file.copy(file.path(SYN, "salmon_quant", map$old[i], "quant.sf"), file.path(dO, map$new[i], "quant.sf")) }
sq2 <- importIsoformExpression(parentDir = paste0(dO, "/"), addIsofomIdAsColumn = TRUE, showProgress = FALSE, quiet = TRUE)
cat("column order from importIsoformExpression:", paste(colnames(sq2$counts)[-1], collapse = " "), "\n")
truth_cond <- map$cond[match(colnames(sq2$counts)[-1], map$new)]
skill_cond <- rep(c("control", "treatment"), each = 6)   # positional vector, as a user copying the Skill would write for 6+6 samples
cat("fraction of samples whose positional label is correct:", mean(truth_cond == skill_cond), "\n")
runs <- function(cvec, label) { sl <- importRdata(sq2$counts, sq2$abundance, data.frame(sampleID = colnames(sq2$counts)[-1], condition = cvec), "annotation.gtf", "transcripts.fa", showProgress = FALSE, quiet = TRUE)
  sl <- preFilter(sl, quiet = TRUE); sl <- isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, quiet = TRUE); s <- score_sl(sl)
  cat(sprintf("%-40s planted recovered %2d/20, null FP %d\n", label, length(s$tp_planted), length(s$fp_null))); s }
s_bad <- runs(skill_cond, "positional vector (Skill pattern)"); s_ok <- runs(truth_cond, "condition joined by sample ID")
chk("Skill's positional design vector silently mislabels samples when IDs do not sort by condition (recovery collapses)", length(s_bad$tp_planted) < 10 && length(s_ok$tp_planted) >= 18, sprintf("%d/20 vs %d/20 planted recovered", length(s_bad$tp_planted), length(s_ok$tp_planted)))
cat("DONE input5\n")
