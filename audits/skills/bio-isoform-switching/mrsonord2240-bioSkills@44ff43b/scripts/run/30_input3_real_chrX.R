# INPUT 3 (Edge): REAL data (nf-core rnasplice chrX, GEUVADIS LCLs, 2 GBR v 2 YRI, Salmon quant, GRCh37 Ensembl GTF).
# Skill code as written on 4 samples (hard-coded 6-sample vectors, min_samps_gene_expr = 6) -> record failures; then adapted run + cross-implementation checks.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages({ library(IsoformSwitchAnalyzeR); library(DRIMSeq); library(DEXSeq); library(stageR); library(satuRn); library(tximport); library(BiocParallel); library(SummarizedExperiment) })
PD <- "F:/OpenScience/audit-envs/alternative-splicing/public-data"
sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916"); cnd <- c("GBR", "GBR", "YRI", "YRI")
qd <- "real_salmon"; unlink(qd, recursive = TRUE); dir.create(qd)
for (s in sm) { dir.create(file.path(qd, s)); file.copy(file.path(PD, "rnasplice/salmon", s, "quant.sf"), file.path(qd, s, "quant.sf")) }
file.copy(file.path(PD, "rnasplice/reference/genes_chrX.gtf"), "real.gtf", overwrite = TRUE); file.copy(file.path(PD, "derived/chrX_tx.fa"), "real_tx.fa", overwrite = TRUE)

cat("\n### A. Skill code as written: 6-sample hard-coded design vector on 4 quant files\n")
sq <- importIsoformExpression(parentDir = paste0(qd, "/"), addIsofomIdAsColumn = TRUE, showProgress = FALSE, quiet = TRUE)
r <- try(data.frame(sampleID = colnames(sq$counts)[-1], condition = c('control','control','control','treatment','treatment','treatment')), silent = TRUE)
cat("design data.frame from Skill's literal vector:", if (inherits(r, "try-error")) paste("ERROR:", conditionMessage(attr(r, "condition"))) else "ok", "\n")
chk("Skill design vector fails LOUDLY (not silently) when n != 6", inherits(r, "try-error"))

cat("\n### B. Skill manual-pipeline dmFilter thresholds (min_samps_gene_expr = 6) on 4 samples\n")
txi <- tximport(setNames(file.path(qd, sm, "quant.sf"), sm), type = "salmon", txOut = TRUE, countsFromAbundance = "no")
t2g <- read.delim(file.path(PD, "rnasplice/salmon/genes_chrX.tx2gene.tsv"), header = FALSE); colnames(t2g) <- c("tx", "gene")
counts <- txi$counts
dat <- data.frame(gene_id = t2g$gene[match(rownames(counts), t2g$tx)], feature_id = rownames(counts), counts, check.names = FALSE); dat <- dat[!is.na(dat$gene_id), ]
dd <- dmDSdata(counts = dat, samples = data.frame(sample_id = sm, condition = factor(cnd)))
d_skill <- tryCatch(dmFilter(dd, min_samps_feature_expr = 3, min_feature_expr = 10, min_samps_feature_prop = 3, min_feature_prop = 0.1, min_samps_gene_expr = 6, min_gene_expr = 10),
                    error = function(e) { cat("dmFilter ERROR:", conditionMessage(e), "\n"); NULL })
ng_skill <- if (is.null(d_skill)) 0 else length(names(d_skill)); cat("genes surviving Skill's dmFilter values on n=4:", ng_skill, "\n")
chk("Skill's dmFilter values are usable as-is for a 2v2 study (>0 genes)", ng_skill > 0, sprintf("%d genes (Skill hard-codes 6-sample thresholds; error table says 'dmFilter: empty result')", ng_skill))
cat("dmFilter defaults (documented claim 'default dmFilter parameters too strict'):\n"); print(unlist(formals(methods::getMethod("dmFilter", "dmDSdata"))[c("min_samps_gene_expr","min_gene_expr","min_samps_feature_expr","min_feature_expr","min_samps_feature_prop","min_feature_prop")]))

cat("\n### C. Adapted runs on the 4 real samples\n")
d <- dmFilter(dd, min_samps_gene_expr = 4, min_samps_feature_expr = 2, min_gene_expr = 10, min_feature_expr = 5, min_samps_feature_prop = 2, min_feature_prop = 0.05)
cat("genes kept (adapted thresholds):", length(names(d)), "\n")
keep <- DRIMSeq::counts(d)
dx <- DEXSeqDataSet(countData = round(as.matrix(keep[, sm])), sampleData = data.frame(condition = factor(cnd), row.names = sm),
                    design = ~ sample + exon + condition:exon, featureID = keep$feature_id, groupID = keep$gene_id)
dx <- estimateSizeFactors(dx); dx <- estimateDispersions(dx, quiet = TRUE); dx <- testForDEU(dx, reducedModel = ~ sample + exon)
dxr <- DEXSeqResults(dx, independentFiltering = FALSE); qv <- perGeneQValue(dxr)
dex_g <- names(qv)[!is.na(qv) & qv < 0.05]
design <- model.matrix(~ condition, data = DRIMSeq::samples(d)); set.seed(1)
d <- dmPrecision(d, design = design, BPPARAM = SerialParam()); d <- dmFit(d, design = design, verbose = 0, BPPARAM = SerialParam()); d <- dmTest(d, coef = "conditionYRI", verbose = 0)
dr <- DRIMSeq::results(d); dri_g <- dr$gene_id[!is.na(dr$adj_pvalue) & dr$adj_pvalue < 0.05]
# ISAR (DEXSeq wrapper) on the same data
iso_cnt <- data.frame(isoform_id = rownames(txi$counts), txi$counts, check.names = FALSE); iso_rep <- data.frame(isoform_id = rownames(txi$abundance), txi$abundance, check.names = FALSE)
sl <- importRdata(iso_cnt, iso_rep, data.frame(sampleID = sm, condition = cnd), "real.gtf", "real_tx.fa", showProgress = FALSE, quiet = TRUE)
sl <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, IFcutoff = 0.01, removeSingleIsoformGenes = TRUE, quiet = TRUE)
sl <- isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, quiet = TRUE)
f <- sl$isoformFeatures; f <- f[!is.na(f$isoform_switch_q_value), ]
isar_iso <- f$isoform_id[f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1]
cat("ISAR gene_id example:", head(f$gene_id, 2), "| gene_name:", head(f$gene_name, 2), "(ISAR gene_id != Ensembl gene id here; map via isoform -> tx2gene)
")
isar_g <- unique(t2g$gene[match(isar_iso, t2g$tx)])
cat(sprintf("gene-level calls: DEXSeq(manual) %d | DRIMSeq %d | ISAR-DEXSeq(q<0.05,|dIF|>0.1) %d\n", length(dex_g), length(dri_g), length(isar_g)))
jac <- function(a, b) length(intersect(a, b)) / length(union(a, b))
cat(sprintf("Jaccard DEXSeq-vs-DRIMSeq %.2f | overlap %d ; ISAR-vs-DEXSeq(manual) %.2f | overlap %d\n", jac(dex_g, dri_g), length(intersect(dex_g, dri_g)), jac(isar_g, dex_g), length(intersect(isar_g, dex_g))))
chk("Independent implementations agree on the top signal: >=50% of DRIMSeq calls are also DEXSeq calls", length(intersect(dex_g, dri_g)) >= 0.5 * length(dri_g), sprintf("%d/%d", length(intersect(dex_g, dri_g)), length(dri_g)))
# hand-computed dIF for the top ISAR switch, from quant.sf directly
top <- f[which.min(f$isoform_switch_q_value), ]
q <- lapply(sm, function(s) read.delim(file.path(qd, s, "quant.sf"), stringsAsFactors = FALSE)); names(q) <- sm
gi <- unique(f$isoform_id[f$gene_id == top$gene_id])
tp <- sapply(sm, function(s) q[[s]]$TPM[match(gi, q[[s]]$Name)]); IFh <- apply(tp, 2, function(v) v / sum(v)); hand <- rowMeans(IFh[, 3:4]) - rowMeans(IFh[, 1:2]); names(hand) <- gi
cat("top switch gene:", top$gene_id, top$gene_name, " ISAR dIF for", top$isoform_id, "=", round(top$dIF, 4), " | hand-computed (renormalised over the same isoforms):", round(hand[top$isoform_id], 4), "\n")
cat("(ISAR gene isoform set used:", paste(gi, collapse = ","), ")\n")
# note: ISAR IF uses only isoforms retained after filtering; report if equal within 0.02
chk("ISAR dIF for top real switch within 0.02 of hand-computed", abs(top$dIF - hand[top$isoform_id]) < 0.02, sprintf("ISAR %.4f vs hand %.4f", top$dIF, hand[top$isoform_id]))
print(head(f[order(f$isoform_switch_q_value), c("gene_name", "isoform_id", "IF1", "IF2", "dIF", "isoform_switch_q_value")], 6))
cat("guess for #genes with DTU printed by importRdata was 18-30 (smoke log); ISAR calls", length(isar_g), "genes\n")
saveRDS(list(dex = dex_g, dri = dri_g, isar = isar_g), "real_calls.rds")
cat("DONE input3\n")
