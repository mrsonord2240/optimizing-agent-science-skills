# INPUT 5 (Stress + adversarial; regression of pre-fix inputs 5 and 7): batch-confounded SYNTHETIC set (regression dataset "synthB": 40% of isoform A moves to C in batch b2
# in 30 null genes GENE100-129; ctrl 5 b1 + 1 b2, trt 1 b1 + 5 b2), sample IDs shuffled. SKILL block r_01 verbatim (+ its own optional batch line), then error-table rows.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR)); set.seed(505)
tt <- truth(); bgenes <- sprintf("GENE%03d", 100:129); oid <- c(sprintf("ctrl_%d", 1:6), sprintf("trt_%d", 1:6))
batch <- c(rep("b1", 5), "b2", "b1", rep("b2", 5)); names(batch) <- oid
outB <- "../data/synthB/salmon_quant"; unlink("../data/synthB", recursive = TRUE); dir.create(outB, recursive = TRUE)
for (s in oid) { q <- read.delim(file.path(SYN, "salmon_quant", s, "quant.sf"), stringsAsFactors = FALSE)
  if (batch[s] == "b2") for (g in bgenes) { a <- which(q$Name == paste0(g, "_A")); cI <- which(q$Name == paste0(g, "_C")); mv <- rbinom(1, round(q$NumReads[a]), 0.4); q$NumReads[a] <- q$NumReads[a] - mv; q$NumReads[cI] <- q$NumReads[cI] + mv }
  rpk <- q$NumReads / q$EffectiveLength; q$TPM <- rpk / sum(rpk) * 1e6; dir.create(file.path(outB, s)); write.table(q, file.path(outB, s, "quant.sf"), sep = "\t", quote = FALSE, row.names = FALSE) }
newid <- sprintf("SRR74%05d", sample(10000:99999, 12)); names(newid) <- oid
stg <- function(wd, cond, bat, srcdir = outB, gtf = file.path(SYN, "annotation.gtf"), fa = file.path(SYN, "transcripts.fa")) {
  unlink(wd, recursive = TRUE); dir.create(file.path(wd, "salmon_quant"), recursive = TRUE)
  for (s in oid) { dir.create(file.path(wd, "salmon_quant", newid[s])); file.copy(file.path(srcdir, s, "quant.sf"), file.path(wd, "salmon_quant", newid[s], "quant.sf")) }
  m <- data.frame(sample_id = newid[oid], condition = cond, batch = bat); m <- m[sample(nrow(m)), ]; write.table(m, file.path(wd, "sample_metadata.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
  file.copy(gtf, file.path(wd, "annotation.gtf")); file.copy(fa, file.path(wd, "transcripts.fa")); m }
cond <- rep(c("control", "treatment"), each = 6)
sc <- function(sl, label) { f <- sl$isoformFeatures; f <- f[!is.na(f$isoform_switch_q_value), ]; g <- unique(f$gene_id[f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])
  cat(sprintf("%-30s planted %2d/20 | batch-artefact genes %2d/30 | other null FP %d | genes called %d\n", label, length(intersect(g, tt$gene_id[tt$true_switch])), length(intersect(g, bgenes)), length(setdiff(intersect(g, tt$gene_id[tt$type == "null"]), bgenes)), length(g)))
  c(pl = length(intersect(g, tt$gene_id[tt$true_switch])), bg = length(intersect(g, bgenes))) }
blk <- readLines("../blocks/r_01.R")
cat("### 5a Skill block verbatim, condition-only (no batch line)\n"); stg("w5a", cond, unname(batch[oid])); setwd("w5a"); source("../../blocks/r_01.R"); ra <- sc(aSwitchList, "no batch column"); setwd("..")
cat("\n### 5b Skill block with its own commented batch line enabled\n"); stg("w5b", cond, unname(batch[oid])); setwd("w5b")
i <- grep("^# design\\$batch", blk); b2 <- blk; b2[i] <- sub("^# ", "", b2[i]); writeLines(b2, "block_batch.R"); source("block_batch.R"); rb <- sc(aSwitchList, "batch column"); setwd("..")
chk("5a ignoring batch produces batch-artefact calls (hazard real)", ra["bg"] >= 5, sprintf("%d/30", ra["bg"]))
chk("5b batch column removes >=80% of artefact calls, keeps >=19/20 planted", rb["bg"] <= 0.2 * ra["bg"] && rb["pl"] >= 19, sprintf("artefacts %d -> %d, planted %d -> %d", ra["bg"], rb["bg"], ra["pl"], rb["pl"]))
tryblk <- function(wd, cond, bat, edit = NULL) { stg(wd, cond, bat); owd <- setwd(wd); on.exit(setwd(owd)); txt <- b2; if (!is.null(edit)) txt <- edit(txt); writeLines(txt, "blk.R")
  tryCatch({ source("blk.R"); "no error" }, error = function(e) conditionMessage(e)) }
cat("\n### 5c batch identical to condition\n"); r5c <- tryblk("w5c", cond, cond); cat("->", gsub("\n", " ", r5c), "\n")
chk("5c perfectly confounded covariate stops with 'not full rank' (Skill Common Errors row)", grepl("not full rank", r5c), substr(r5c, 1, 100))
cat("\n### 5d constant covariate\n"); r5d <- tryblk("w5d", cond, rep("b1", 12)); cat("->", gsub("\n", " ", r5d), "\n")
chk("5d constant covariate stops with 'Contain constant information' (Skill row)", grepl("Contain constant information", r5d), substr(r5d, 1, 100))
cat("\n### 5e metadata missing one sample -> the Skill block's stopifnot\n"); stg("w5e", cond, unname(batch[oid])); setwd("w5e"); m <- read.delim("sample_metadata.tsv"); write.table(m[-1, ], "sample_metadata.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
r5e <- tryCatch({ source("../../blocks/r_01.R"); "no error" }, error = function(e) conditionMessage(e)); cat("->", gsub("\n", " ", r5e), "\n"); setwd("..")
chk("5e a missing metadata row stops the Skill block (not a silent mislabel)", r5e != "no error", substr(r5e, 1, 100))
cat("\n### 5f 1 v 1 (replicates)\n"); stg("w5f", cond, unname(batch[oid])); setwd("w5f"); m <- read.delim("sample_metadata.tsv")
keep <- c(newid["ctrl_1"], newid["trt_1"]); for (s in setdiff(list.files("salmon_quant"), keep)) unlink(file.path("salmon_quant", s), recursive = TRUE); write.table(m[m$sample_id %in% keep, c("sample_id", "condition")], "sample_metadata.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
r5f <- tryCatch({ source("../../blocks/r_01.R"); "no error" }, error = function(e) conditionMessage(e)); cat("->", gsub("\n", " ", r5f), "\n"); setwd("..")
chk("5f 1v1 stops with 'A statistical test cannot be performed without replicates'", grepl("cannot be performed without replicates", r5f))
cat("\n### 5g version-suffixed quant IDs (X.1) vs unversioned GTF\n"); stg("w5g", cond, unname(batch[oid])); setwd("w5g")
for (s in list.files("salmon_quant")) { p <- file.path("salmon_quant", s, "quant.sf"); q <- read.delim(p, stringsAsFactors = FALSE); q$Name <- paste0(q$Name, ".1"); write.table(q, p, sep = "\t", quote = FALSE, row.names = FALSE) }
r5g <- tryCatch({ source("../../blocks/r_01.R"); "no error" }, error = function(e) conditionMessage(e)); cat("->", substr(gsub("\n", " ", r5g), 1, 200), "\n")
chk("5g suffix mismatch errors with the Jaccard message", grepl("Jaccard", r5g))
b3 <- blk; b3 <- sub("addIsofomIdAsColumn = TRUE", "addIsofomIdAsColumn = TRUE, ignoreAfterPeriod = TRUE", b3, fixed = TRUE); b3 <- sub("showProgress = FALSE\n", "showProgress = FALSE\n", b3)
b3 <- sub("    addAnnotatedORFs = TRUE,", "    addAnnotatedORFs = TRUE, ignoreAfterPeriod = TRUE,", b3, fixed = TRUE); writeLines(b3, "blk_ignore.R"); cat("edited lines:", paste(grep("ignoreAfterPeriod", b3, value = TRUE), collapse = " || "), "\n")
r5g2 <- tryCatch({ source("blk_ignore.R"); paste("imported", nrow(aSwitchList$isoformFeatures), "isoform rows") }, error = function(e) conditionMessage(e)); cat("with ignoreAfterPeriod=TRUE in both calls ->", substr(gsub("\n", " ", r5g2), 1, 200), "\n")
chk("5g the Skill's remedy (ignoreAfterPeriod = TRUE in BOTH calls) imports the versioned IDs", grepl("^imported", r5g2), substr(r5g2, 1, 100)); setwd("..")
cat("\n### 5h default reduceToSwitchingGenes = TRUE on a null comparison (the 'No genes were considered switching' row)\n"); ids0 <- sprintf("ctrl_%d", 1:6); stage_salmon("w5h", ids0, sprintf("SRR75%05d", 1:6), rep(c("nA", "nB"), each = 3)); setwd("w5h")
b4 <- blk; writeLines(b4, "blk.R"); source("blk.R")
r5h <- tryCatch({ isoformSwitchTestDEXSeq(aSwitchList, alpha = 1e-30, dIFcutoff = 0.9, quiet = TRUE); "no error" }, error = function(e) conditionMessage(e)); cat("->", gsub("\n", " ", r5h), "\n")
chk("5h reduceToSwitchingGenes=TRUE with nothing significant errors with the Skill-quoted text", grepl("No genes were considered switching", r5h)); setwd("..")
cat("DONE input5\n")
