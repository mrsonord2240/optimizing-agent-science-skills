# INPUT 7 (NEW): does the Skill's count-route guidance hold on data I generated? (7A synthetic 5v5 with isoform lengths 0.5-5 kb, planted truth; DEXSeq route table;
# 7B 4v7 satuRn across routes (never compared by the fixer); 7C real chrX satuRn across routes; 7D manual DRIMSeq/DEXSeq block across routes on real chrX.)
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages({ library(IsoformSwitchAnalyzeR); library(tximport) }); set.seed(707)
PD <- "F:/OpenScience/audit-envs/alternative-splicing/public-data"
RD <- "F:/OpenScience/audits/bio-isoform-switching/run/data"
prep <- function(src, wd) { unlink(wd, recursive = TRUE); dir.create(wd, recursive = TRUE)
  file.copy(file.path(src, "salmon_quant"), wd, recursive = TRUE); file.copy(file.path(src, c("annotation.gtf", "transcripts.fa", "sample_metadata.tsv")), wd)
  read.delim(file.path(wd, "sample_metadata.tsv"), stringsAsFactors = FALSE) }
route_run <- function(cnt, ab, design, test, tt, label, wd) {
  sl <- suppressWarnings(importRdata(cnt, ab, design, file.path(wd, "annotation.gtf"), file.path(wd, "transcripts.fa"), showProgress = FALSE, quiet = TRUE))
  sl <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, IFcutoff = 0.01, removeSingleIsoformGenes = TRUE, keepIsoformInAllConditions = TRUE, quiet = TRUE)
  sl <- suppressWarnings(if (test == "sat") isoformSwitchTestSatuRn(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, diagplots = FALSE, quiet = TRUE) else isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, quiet = TRUE))
  f <- sl$isoformFeatures; f <- f[!is.na(f$isoform_switch_q_value), ]; g <- unique(f$gene_id[f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])
  pl <- tt$gene_id[tt$true_switch]; nul <- tt$gene_id[tt$type == "null" & !tt$is_batch_gene]
  cat(sprintf("%-58s planted %2d/20 | null FP %d/%d | genes called %d\n", label, length(intersect(g, pl)), length(intersect(g, nul)), length(nul), length(g))); invisible(c(pl = length(intersect(g, pl)), fp = length(intersect(g, nul)))) }
routes <- function(wd, tt, meta, test, do_tx = TRUE) {
  ids <- sort(meta$sample_id); design <- meta[match(ids, meta$sample_id), c("sample_id", "condition")]; colnames(design)[1] <- "sampleID"; rownames(design) <- NULL
  out <- list()
  a <- suppressMessages(importIsoformExpression(file.path(wd, "salmon_quant"), addIsofomIdAsColumn = TRUE, calculateCountsFromAbundance = FALSE, showProgress = FALSE, quiet = TRUE))
  d <- suppressMessages(importIsoformExpression(file.path(wd, "salmon_quant"), addIsofomIdAsColumn = TRUE, calculateCountsFromAbundance = TRUE, showProgress = FALSE, quiet = TRUE))
  out$raw <- route_run(a$counts, a$abundance, design, test, tt, paste0(test, ": raw NumReads (calculateCountsFromAbundance=FALSE)"), wd)
  out$def <- route_run(d$counts, d$abundance, design, test, tt, paste0(test, ": ISAR default (calculateCountsFromAbundance=TRUE)"), wd)
  if (do_tx) {
    fl <- setNames(file.path(wd, "salmon_quant", ids, "quant.sf"), ids); t2g <- data.frame(tx = tt$gene_id, gene = tt$gene_id)[0, ]
    t2g <- data.frame(tx = unlist(lapply(tt$gene_id, function(g) paste0(g, "_", c("A", "B", "C")))), gene = rep(tt$gene_id, each = 3))
    for (m in c("lengthScaledTPM", "scaledTPM", "dtuScaledTPM")) { tx <- tximport(fl, type = "salmon", txOut = TRUE, countsFromAbundance = m, tx2gene = t2g)
      out[[m]] <- route_run(data.frame(isoform_id = rownames(tx$counts), tx$counts, check.names = FALSE), data.frame(isoform_id = rownames(tx$abundance), tx$abundance, check.names = FALSE), design, test, tt, paste0(test, ": tximport ", m), wd) } }
  len <- read.delim(file.path(wd, "salmon_quant", ids[1], "quant.sf"), stringsAsFactors = FALSE); fac <- median(len$Length) / len$Length[match(a$counts$isoform_id, len$Name)]
  cat(sprintf("  (median(len)/len factor range on this set: %.2f - %.2f)\n", min(fac), max(fac)))
  e <- a$counts; e[, ids] <- e[, ids] * fac; out$emu <- route_run(e, a$abundance, design, test, tt, paste0(test, ": raw x median(len)/len (emulated scaledTPM)"), wd)
  out }
# ---- 7A synthetic 5v5 (data/new2), DEXSeq
tt2 <- read.delim(file.path(RD, "new2/truth_genes.tsv"), stringsAsFactors = FALSE); wd2 <- "w7a"; m2 <- prep(file.path(RD, "new2"), wd2)
cat("### 7A synthetic 5v5 (transcript lengths 0.5-5.4 kb), DEXSeq\n"); r7a <- routes(wd2, tt2, m2, "dex")
chk("7A raw counts recover >=19/20 planted", r7a$raw["pl"] >= 19, r7a$raw["pl"])
cat("route table verdict on synthetic: default(TRUE)", r7a$def["pl"], "| lengthScaledTPM", r7a$lengthScaledTPM["pl"], "| scaledTPM", r7a$scaledTPM["pl"], "| dtuScaledTPM", r7a$dtuScaledTPM["pl"], "| emulated", r7a$emu["pl"], "of 20 planted\n")
# ---- 7B synthetic 4v7 (data/new1), satuRn (max replicates 7 > 5)
tt1 <- read.delim(file.path(RD, "new1/truth_genes.tsv"), stringsAsFactors = FALSE); wd1 <- "w7b"; m1 <- prep(file.path(RD, "new1"), wd1)
cat("\n### 7B synthetic 4v7, satuRn (the Skill's branch for >5 replicates)\n"); r7b <- routes(wd1, tt1, m1, "sat", do_tx = FALSE)
# ---- 7C real chrX 2v2, ISAR satuRn wrapper across routes
cat("\n### 7C real chrX 2v2: ISAR satuRn wrapper vs DEXSeq wrapper, raw vs default counts\n")
sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916"); wd3 <- "w7c"; unlink(wd3, recursive = TRUE); dir.create(file.path(wd3, "salmon_quant"), recursive = TRUE)
for (s in sm) { dir.create(file.path(wd3, "salmon_quant", s)); file.copy(file.path(PD, "rnasplice/salmon", s, "quant.sf"), file.path(wd3, "salmon_quant", s, "quant.sf")) }
file.copy(file.path(PD, "rnasplice/reference/genes_chrX.gtf"), file.path(wd3, "annotation.gtf")); file.copy(file.path(PD, "derived/chrX_tx.fa"), file.path(wd3, "transcripts.fa"))
des <- data.frame(sampleID = sm, condition = c("GBR", "GBR", "YRI", "YRI"))
real_run <- function(cnt, ab, test, label) {
  r <- tryCatch({ sl <- suppressWarnings(importRdata(cnt, ab, des, file.path(wd3, "annotation.gtf"), file.path(wd3, "transcripts.fa"), showProgress = FALSE, quiet = TRUE))
    sl <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, IFcutoff = 0.01, removeSingleIsoformGenes = TRUE, keepIsoformInAllConditions = TRUE, quiet = TRUE)
    sl <- suppressWarnings(if (test == "sat") isoformSwitchTestSatuRn(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, diagplots = FALSE, quiet = TRUE) else isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, quiet = TRUE))
    f <- sl$isoformFeatures; s <- f[!is.na(f$isoform_switch_q_value) & f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1, ]; rr <- f[f$isoform_id == "ENST00000406022", ]
    sprintf("%d isoforms / %d genes | RPL10 q %.3g", nrow(s), length(unique(s$gene_id)), rr$isoform_switch_q_value[1]) }, error = function(e) paste("ERROR:", conditionMessage(e)))
  cat(sprintf("%-50s %s\n", label, r)) }
a <- suppressMessages(importIsoformExpression(file.path(wd3, "salmon_quant"), addIsofomIdAsColumn = TRUE, calculateCountsFromAbundance = FALSE, showProgress = FALSE, quiet = TRUE))
d <- suppressMessages(importIsoformExpression(file.path(wd3, "salmon_quant"), addIsofomIdAsColumn = TRUE, calculateCountsFromAbundance = TRUE, showProgress = FALSE, quiet = TRUE))
real_run(a$counts, a$abundance, "sat", "satuRn wrapper, raw counts"); real_run(d$counts, d$abundance, "sat", "satuRn wrapper, ISAR default counts")
real_run(a$counts, a$abundance, "dex", "DEXSeq wrapper, raw counts (reference)"); real_run(d$counts, d$abundance, "dex", "DEXSeq wrapper, ISAR default counts (reference)")
# ---- 7D manual block r_03 across routes on real chrX
cat("\n### 7D manual DRIMSeq/DEXSeq block (r_03) on real chrX 2v2 across countsFromAbundance\n")
t2g <- read.delim(file.path(PD, "rnasplice/salmon/genes_chrX.tx2gene.tsv"), header = FALSE); tx2gene <- data.frame(tx = t2g$V1, gene = t2g$V2)
meta <- data.frame(sample_id = sm, condition = c("GBR", "GBR", "YRI", "YRI")); files <- setNames(file.path(wd3, "salmon_quant", sm, "quant.sf"), sm)
base_txt <- readLines("../blocks/r_04.R")
for (m in c("no", "lengthScaledTPM", "scaledTPM")) {
  txt <- sub("countsFromAbundance = 'no'", sprintf("countsFromAbundance = '%s', tx2gene = tx2gene", m), base_txt, fixed = TRUE); stopifnot(!identical(txt, base_txt) || m == "no")
  if (m == "no") txt <- base_txt
  writeLines(txt, "blk_route.R"); source("blk_route.R", echo = FALSE)
  sg <- names(qval)[!is.na(qval) & qval < 0.05]
  suppressPackageStartupMessages(library(BiocParallel)); design_full <- model.matrix(~ condition, data = DRIMSeq::samples(d)); d2 <- dmPrecision(d, design = design_full, BPPARAM = SerialParam()); d2 <- dmFit(d2, design = design_full, verbose = 0, BPPARAM = SerialParam()); d2 <- dmTest(d2, coef = "conditionYRI", verbose = 0)
  dr <- DRIMSeq::results(d2); dg <- dr$gene_id[!is.na(dr$adj_pvalue) & dr$adj_pvalue < 0.05]
  cat(sprintf("manual pipeline countsFromAbundance=%-16s genes kept %d | DEXSeq q<0.05: %d | DRIMSeq adj p<0.05: %d | overlap %d\n", m, length(unique(DRIMSeq::counts(d)$gene_id)), length(sg), length(dg), length(intersect(sg, dg)))) }
cat("DONE 7\n")
