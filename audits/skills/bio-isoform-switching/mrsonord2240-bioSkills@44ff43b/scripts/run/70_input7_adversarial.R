# INPUT 7 (Adversarial): unreplicated 1v1 request, mismatched / version-suffixed annotation, and the Skill's "Common Errors" table checked against the real messages.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages({ library(IsoformSwitchAnalyzeR); library(DRIMSeq); library(fishpond); library(SummarizedExperiment) })
tr <- truth(); ids <- c(sprintf("ctrl_%d", 1:6), sprintf("trt_%d", 1:6))
file.copy(file.path(SYN, "annotation.gtf"), "annotation.gtf", overwrite = TRUE); file.copy(file.path(SYN, "transcripts.fa"), "transcripts.fa", overwrite = TRUE)
rq <- function(s) read.delim(file.path(SYN, "salmon_quant", s, "quant.sf"), stringsAsFactors = FALSE)
q <- lapply(ids, rq); tx <- q[[1]]$Name
cnt <- sapply(q, function(x) x$NumReads); tpm <- sapply(q, function(x) x$TPM); colnames(cnt) <- colnames(tpm) <- ids
mk <- function(m, rn = tx) data.frame(isoform_id = rn, m, check.names = FALSE)
try_run <- function(expr) { w <- character(); r <- tryCatch(withCallingHandlers(expr, warning = function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") }), error = function(e) paste("ERROR:", conditionMessage(e)))
  if (length(w)) r <- paste0(r, " [warnings: ", paste(substr(gsub("[[:space:]]+", " ", w), 1, 160), collapse = " || "), "]"); r }

cat("\n### (a) 1 v 1, no replicates: 'which isoform switches are significant?'\n")
ra <- try_run({ sl <- importRdata(mk(cnt[, c(1, 7)]), mk(tpm[, c(1, 7)]), data.frame(sampleID = ids[c(1, 7)], condition = c("control", "treatment")), "annotation.gtf", "transcripts.fa", showProgress = FALSE, quiet = TRUE)
  sl <- preFilter(sl, quiet = TRUE); sl <- isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, quiet = TRUE); s <- sum(sl$isoformFeatures$isoform_switch_q_value < 0.05, na.rm = TRUE); paste("returned q-values;", s, "isoforms q<0.05") })
cat("1v1 pipeline ->", ra, "\n")
chk("1 v 1 request is refused or clearly flagged (no silent 'significant' calls)", grepl("ERROR|very low complexity", ra) || grepl(" 0 isoforms", ra), ra)
cat("Skill text mentions unreplicated designs / minimum replicates? ", any(grepl("replicate", readLines("../skill/SKILL.md"), ignore.case = TRUE) & grepl("minimum|at least|unreplicated|no replicate|without replicate", readLines("../skill/SKILL.md"), ignore.case = TRUE)), "\n")

cat("\n### (b) annotation mismatch\n")
# b1: quant IDs carry Ensembl-style version suffix (.1) but GTF/FASTA do not
rb1 <- try_run({ sl <- importRdata(mk(cnt[, c(1:3, 7:9)], paste0(tx, ".1")), mk(tpm[, c(1:3, 7:9)], paste0(tx, ".1")), data.frame(sampleID = ids[c(1:3, 7:9)], condition = rep(c("control", "treatment"), each = 3)), "annotation.gtf", "transcripts.fa", showProgress = FALSE, quiet = TRUE); paste("imported", nrow(sl$isoformFeatures), "isoform rows") })
cat("versioned quant IDs vs unversioned GTF ->", substr(rb1, 1, 400), "\n")
# b2: wrong annotation entirely (real chrX GTF/FASTA against synthetic quant)
PD <- "F:/OpenScience/audit-envs/alternative-splicing/public-data"
rb2 <- try_run({ sl <- importRdata(mk(cnt[, c(1:3, 7:9)]), mk(tpm[, c(1:3, 7:9)]), data.frame(sampleID = ids[c(1:3, 7:9)], condition = rep(c("control", "treatment"), each = 3)), file.path(PD, "rnasplice/reference/genes_chrX.gtf"), file.path(PD, "derived/chrX_tx.fa"), showProgress = FALSE, quiet = TRUE); paste("imported", nrow(sl$isoformFeatures), "isoform rows") })
cat("wrong annotation entirely ->", substr(rb2, 1, 500), "\n")
chk("Wrong annotation entirely is rejected with an error mentioning missing/mismatched isoform ids (Skill Common Errors row 1)", grepl("ERROR", rb2), substr(rb2, 1, 200))
cat("Skill quotes the error as: `Error in importRdata: ... transcript_ids do not match`. Real text above.\n")

cat("\n### (c) Skill 'Common Errors' table rows vs real messages\n")
# c1: analyzeSwitchConsequences with no switching genes (null comparison)
sq0 <- lapply(1:6, function(i) NULL)
sl0 <- importRdata(mk(cnt[, 1:6]), mk(tpm[, 1:6]), data.frame(sampleID = ids[1:6], condition = rep(c("a", "b"), each = 3)), "annotation.gtf", "transcripts.fa", showProgress = FALSE, quiet = TRUE)
sl0 <- preFilter(sl0, quiet = TRUE)
c1 <- try_run({ x <- isoformSwitchTestDEXSeq(sl0, reduceToSwitchingGenes = TRUE, alpha = 1e-12, dIFcutoff = 0.9, quiet = TRUE); x <- analyzeORF(x, quiet = TRUE); analyzeSwitchConsequences(x, consequencesToAnalyze = "NMD_status", quiet = TRUE) })
cat("analyzeSwitchConsequences on a list with no significant switches ->", substr(if (is.character(c1)) c1 else "returned object", 1, 300), "\n")
# c2: analyzeIUPred2A with a missing file
sl1 <- readRDS("in4_after_orf.rds")
c2 <- try_run(analyzeIUPred2A(sl1, pathToIUPred2AresultFile = "iupred2_results.txt", quiet = TRUE))
cat("analyzeIUPred2A(missing file) ->", substr(c2, 1, 300), "\n")
c3 <- try_run(analyzeSignalP(sl1, pathToSignalPresultFile = "signalp_results.txt", quiet = TRUE))
cat("analyzeSignalP(missing file) ->", substr(c3, 1, 300), "\n")
# c4: swish on an SE without inferential replicates
se <- SummarizedExperiment(assays = list(counts = cnt, abundance = tpm, length = matrix(1000, nrow(cnt), ncol(cnt), dimnames = dimnames(cnt))), colData = DataFrame(condition = factor(rep(c("a", "b"), each = 6)), row.names = ids))
c4 <- try_run(scaleInfReps(se, quiet = TRUE))
cat("scaleInfReps(no infReps) ->", substr(if (is.character(c4)) c4 else "returned without error", 1, 300), "\n")
c5 <- try_run({ y <- labelKeep(se); swish(y, x = "condition", quiet = TRUE) })
cat("swish(no infReps) ->", substr(if (is.character(c5)) c5 else "returned without error", 1, 300), "\n")
# c6: dmFilter strict thresholds -> empty
d <- dmDSdata(counts = data.frame(gene_id = sub("_[ABC]$", "", tx), feature_id = tx, round(cnt)), samples = data.frame(sample_id = ids, condition = rep(c("a", "b"), each = 6)))
c6 <- try_run(length(names(dmFilter(d, min_samps_gene_expr = 12, min_gene_expr = 1e9))))
cat("dmFilter impossible thresholds ->", c6, "\n")
cat("DONE input7\n")
