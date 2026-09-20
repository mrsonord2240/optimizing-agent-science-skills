# INPUT 6 (Scope boundary): fishpond/swish "inferential-uncertainty-aware" branch of the Skill + long-read style count-only import.
# (a) real Salmon Gibbs (20 reps) chrX 2v2 through the Skill code incl. tximeta(coldata) with an offline linkedTxome
# (b) SYNTHETIC 6v6 with planted DTE truth + Poisson-resampled inferential replicates (assay names infRep1..20)
# (c) count-only importRdata (long-read style; no abundance matrix)
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages({ library(tximeta); library(fishpond); library(SummarizedExperiment); library(IsoformSwitchAnalyzeR) })
PD <- "F:/OpenScience/audit-envs/alternative-splicing/public-data"
sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916"); cnd <- c("GBR", "GBR", "YRI", "YRI")

cat("\n### (a) Skill code: se <- tximeta(coldata); scaleInfReps; labelKeep; swish(y, x='condition')  [real Gibbs, 2v2]\n")
coldata <- data.frame(names = sm, files = file.path(PD, "derived/salmon_gibbs", sm, "quant.sf"), condition = cnd)
r0 <- tryCatch(tximeta(coldata), error = function(e) paste("ERROR:", substr(conditionMessage(e), 1, 300)), warning = function(w) paste("WARNING:", substr(conditionMessage(w), 1, 300)))
cat("tximeta(coldata) with no linked transcriptome ->", if (is.character(r0)) r0 else "returned SE", "\n")
# offline linkedTxome (no network): local Ensembl GTF/FASTA + the Salmon index used for the Gibbs runs
lt <- tryCatch({ makeLinkedTxome(indexDir = file.path(PD, "derived/salmon_idx"), source = "LocalEnsembl", organism = "Homo sapiens", release = "75", genome = "GRCh37",
                                 fasta = file.path(PD, "derived/chrX_tx.fa"), gtf = file.path(PD, "rnasplice/reference/genes_chrX.gtf"), write = FALSE); "linkedTxome ok" },
               error = function(e) paste("ERROR:", substr(conditionMessage(e), 1, 300)))
cat("makeLinkedTxome:", lt, "\n")
se <- tryCatch(tximeta(coldata), error = function(e) paste("ERROR:", substr(conditionMessage(e), 1, 400)))
if (is.character(se)) { cat("tximeta(coldata) after linkedTxome ->", se, "\n"); quit(status = 1) }
cat("tximeta SE:", nrow(se), "x", ncol(se), "| assays:", paste(head(assayNames(se), 4), collapse = ","), "...", length(grep("infRep", assayNames(se))), "infReps\n")
cat("rowData columns:", paste(colnames(rowData(se)), collapse = ","), "; class(rowData(se)$gene_id) =", class(rowData(se)$gene_id)[1], "\n")
# The tximeta -> linkedTxome match FAILED here (Salmon 2.7 index metadata; "Unknown or uninitialised column: sha256"), so rowData(se) is empty and the
# Skill's `rowData(se)$gene_id` / `rowData(se)$tx_id` lines could not be executed on real tximeta output. Simulate the documented tximeta layout
# (gene_id is a CharacterList in transcript-level tximeta output) to test the Skill's data.frame(...) line:
cnt_demo <- assays(se)$counts[1:5, ]
rd_demo <- DataFrame(tx_id = rownames(cnt_demo), gene_id = IRanges::CharacterList(as.list(paste0("G", 1:5))))   # SIMULATED tximeta rowData
txdf <- tryCatch(data.frame(gene_id = rd_demo$gene_id, feature_id = rd_demo$tx_id, cnt_demo), error = function(e) paste("ERROR:", conditionMessage(e)))
cat("SIMULATED tximeta rowData: Skill txdf <- data.frame(gene_id = rowData(se)$gene_id, feature_id = rowData(se)$tx_id, counts) ->", if (is.character(txdf)) txdf else paste0("ok; dim ", nrow(txdf), "x", ncol(txdf), "; colnames ", paste(colnames(txdf), collapse = ",")), "
")
chk("Skill's txdf line yields a 1-row-per-transcript table with character gene_id when gene_id is a CharacterList (SIMULATED)", !is.character(txdf) && nrow(txdf) == 5 && is.character(txdf$gene_id),
    if (is.character(txdf)) txdf else sprintf("%d rows, cols %s", nrow(txdf), paste(colnames(txdf), collapse = ",")))
y <- scaleInfReps(se, quiet = TRUE); y <- labelKeep(y); y <- y[mcols(y)$keep, ]
set.seed(1)
chk("colData(se)$condition from Skill-style coldata (data.frame default) is a factor as swish requires", is.factor(colData(y)$condition), class(colData(y)$condition)[1])
y2 <- tryCatch(swish(y, x = 'condition'), error = function(e) paste("ERROR:", conditionMessage(e)), warning = function(w) paste("WARNING:", conditionMessage(w)))
cat("Skill call swish(y, x='condition') on 2v2 (default nperms=100) ->", if (is.character(y2)) y2 else "returned", "\n")
if (is.character(y2)) { colData(y)$condition <- factor(colData(y)$condition); y2 <- suppressWarnings(swish(y, x = 'condition')) }
cat("mcols columns:", paste(colnames(mcols(y2)), collapse = ","), "\n")
dte_results <- as.data.frame(mcols(y2)); sig <- subset(dte_results, qvalue < 0.05)
cat(sprintf("real 2v2 swish: %d transcripts tested; %d with qvalue<0.05 (Skill threshold); %d with qvalue<0.1; min p %.3g; distinct p-values %d\n", nrow(dte_results), nrow(sig), sum(dte_results$qvalue < 0.1, na.rm = TRUE), min(dte_results$pvalue, na.rm = TRUE), length(unique(round(dte_results$pvalue, 6)))))
chk("Skill's swish(qvalue<0.05) call yields interpretable output on 2v2 real data", nrow(sig) > 0 || nrow(dte_results) > 0, sprintf("%d sig at 0.05", nrow(sig)))
# infRV diagnostic mentioned by the Skill
cat("infRV column present after scaleInfReps/labelKeep:", "meanInfRV" %in% colnames(mcols(y)) || "infRV" %in% colnames(mcols(y)), "(columns:", paste(colnames(mcols(y)), collapse = ","), ")\n")

cat("\n### (b) SYNTHETIC planted DTE: true up-regulated transcripts = B of poison genes (x5.5), C of skip genes (x3), all isoforms of dge_only genes (x3)\n")
tr <- truth(); ids <- c(sprintf("ctrl_%d", 1:6), sprintf("trt_%d", 1:6))
q <- lapply(ids, function(s) read.delim(file.path(SYN, "salmon_quant", s, "quant.sf"), stringsAsFactors = FALSE)); tx <- q[[1]]$Name
cnt <- sapply(q, function(x) x$NumReads); tpm <- sapply(q, function(x) x$TPM); len <- sapply(q, function(x) x$EffectiveLength)
colnames(cnt) <- colnames(tpm) <- colnames(len) <- ids; rownames(cnt) <- rownames(tpm) <- rownames(len) <- tx
set.seed(3); K <- 20
assays <- list(counts = cnt, abundance = tpm, length = len)
for (k in 1:K) assays[[paste0("infRep", k)]] <- matrix(rpois(length(cnt), cnt), nrow(cnt), ncol(cnt), dimnames = dimnames(cnt))  # Poisson-resampled 'inferential replicates' (synthetic)
sy <- SummarizedExperiment(assays = assays, colData = DataFrame(condition = factor(rep(c("control", "treatment"), each = 6)), row.names = ids))
sy <- scaleInfReps(sy, quiet = TRUE); sy <- labelKeep(sy); sy <- sy[mcols(sy)$keep, ]
set.seed(1); sy <- swish(sy, x = "condition", quiet = TRUE)
res <- as.data.frame(mcols(sy)); res$tx <- rownames(sy); res$gene <- sub("_[ABC]$", "", res$tx); res$iso <- sub(".*_", "", res$tx)
tg <- tr[match(res$gene, tr$gene_id), ]
true_up <- (tg$type == "poison_switch" & res$iso == "B") | (tg$type == "skip_switch" & res$iso == "C") | (tg$type == "dge_only")
called <- !is.na(res$qvalue) & res$qvalue < 0.05
cat(sprintf("swish 6v6: %d tested | true-up %d | called %d | TP %d | FP %d (of %d non-true)\n", nrow(res), sum(true_up), sum(called), sum(called & true_up), sum(called & !true_up), sum(!true_up)))
cat("log2FC sign of called true-up transcripts (should be >0):", paste(names(table(sign(res$log2FC[called & true_up]))), table(sign(res$log2FC[called & true_up])), collapse = " "), "\n")
chk("swish recovers >=80% of planted DTE-up transcripts, in the right direction", sum(called & true_up) >= 0.8 * sum(true_up) && all(res$log2FC[called & true_up] > 0), sprintf("%d/%d", sum(called & true_up), sum(true_up)))
chk("swish false positives <= 5% of non-DTE transcripts", sum(called & !true_up) <= 0.05 * sum(!true_up), sprintf("%d", sum(called & !true_up)))
# DTU-side contrast the Skill draws: gene-level DGE decoy genes are DTE but NOT DTU -> swish flags them (that is the DTE vs DTU distinction); fishpond has isoformProportions() for DTU
cat("fishpond::isoformProportions available for DTU-style swish:", exists("isoformProportions"), "\n")
# (c) count-only importRdata (the Skill: 'for long-read input, use importRdata with long-read transcript counts directly')
cat("\n### (c) importRdata with counts only (no isoformRepExpression), as long-read counts would be supplied\n")
file.copy(file.path(SYN, "annotation.gtf"), "annotation.gtf", overwrite = TRUE); file.copy(file.path(SYN, "transcripts.fa"), "transcripts.fa", overwrite = TRUE)
ic <- data.frame(isoform_id = tx, cnt[, c(1:3, 7:9)], check.names = FALSE)
r <- tryCatch({ x <- importRdata(isoformCountMatrix = ic, designMatrix = data.frame(sampleID = colnames(ic)[-1], condition = rep(c("control", "treatment"), each = 3)), isoformExonAnnoation = "annotation.gtf", isoformNtFasta = "transcripts.fa", showProgress = FALSE, quiet = TRUE)
  x <- preFilter(x, quiet = TRUE); x <- isoformSwitchTestDEXSeq(x, reduceToSwitchingGenes = FALSE, quiet = TRUE); s <- score_sl(x); sprintf("planted %d/20, null FP %d", length(s$tp_planted), length(s$fp_null)) }, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("count-only import + DEXSeq ->", r, "\n")
chk("Count-only importRdata (long-read style) recovers >=18/20 planted switches", grepl("^planted (1[89]|20)/20", r), r)
cat("ISAR importRdata formals mentioning long-read/single-cell:", paste(grep("long|single|cell", names(formals(importRdata)), value = TRUE, ignore.case = TRUE), collapse = ",") , "(none => 'v2 long-read input mode' is not a separate mode in installed 2.6.0)\n")
cat("DONE input6\n")
