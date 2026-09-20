# INPUT 2 (Variant A): SKILL.md "Manual DTU Pipeline (DRIMSeq + DEXSeq + stageR)" run on SYNTHETIC 6 v 6, plus null split, plus
# independent cross-checks (DRIMSeq dmTest, satuRn, naive BH vs stageR).
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages({ library(tximport); library(DRIMSeq); library(DEXSeq); library(stageR); library(SummarizedExperiment); library(BiocParallel) })
tr <- truth()
run_pipeline <- function(sample_ids, cond, cfa = "no", label = "") {
  files <- setNames(file.path(SYN, "salmon_quant", sample_ids, "quant.sf"), sample_ids)
  tx2gene <- data.frame(tx = paste0(rep(sprintf("GENE%03d", 1:300), each = 3), "_", c("A","B","C")), gene = rep(sprintf("GENE%03d", 1:300), each = 3))
  txi <- tximport(files, type = "salmon", txOut = TRUE, countsFromAbundance = cfa, tx2gene = tx2gene)
  counts <- txi$counts
  # --- SKILL.md code below (tximeta replaced by tximport: synthetic data has no Salmon index / linked txome) ---
  samples <- data.frame(sample_id = colnames(counts), condition = cond)
  txdf <- data.frame(gene_id = tx2gene$gene[match(rownames(counts), tx2gene$tx)], feature_id = rownames(counts), counts)
  d <- dmDSdata(counts = txdf, samples = samples)
  d <- dmFilter(d, min_samps_feature_expr = 3, min_feature_expr = 10,
                min_samps_feature_prop = 3, min_feature_prop = 0.1,
                min_samps_gene_expr = 6, min_gene_expr = 10)
  design_full <- model.matrix(~ condition, data = DRIMSeq::samples(d))  # PATCH: Skill writes samples(d), masked by Biobase::samples after library(DEXSeq) (see 21_samples_mask.R)
  dxd <- DEXSeqDataSet(
    countData = round(as.matrix(counts(d)[, -c(1, 2)])),
    sampleData = DRIMSeq::samples(d),  # PATCH (same masking)
    design = ~ sample + exon + condition:exon,
    featureID = counts(d)$feature_id,
    groupID = counts(d)$gene_id
  )
  dxd <- estimateSizeFactors(dxd)
  dxd <- estimateDispersions(dxd, quiet = TRUE)
  dxd <- testForDEU(dxd, reducedModel = ~ sample + exon)
  qval <- perGeneQValue(DEXSeqResults(dxd))
  dxr <- DEXSeqResults(dxd, independentFiltering = FALSE)
  pConfirmation <- matrix(dxr$pvalue, ncol = 1)
  rownames(pConfirmation) <- dxr$featureID
  tx2gene2 <- as.data.frame(dxr[, c('featureID', 'groupID')])
  cat(label, "NA transcript p-values passed to stageR:", sum(is.na(pConfirmation)), " NA gene q:", sum(is.na(qval)), "\n")
  stageRObj <- stageRTx(pScreen = qval, pConfirmation = pConfirmation, pScreenAdjusted = TRUE, tx2gene = tx2gene2)
  stageRObj <- stageWiseAdjustment(stageRObj, method = 'dtu', alpha = 0.05)
  results <- getAdjustedPValues(stageRObj, order = FALSE, onlySignificantGenes = FALSE)
  list(d = d, dxr = dxr, qval = qval, results = results)
}

ids <- c(sprintf("ctrl_%d", 1:6), sprintf("trt_%d", 1:6)); cond <- factor(rep(c("control", "treatment"), each = 6))
r <- tryCatch(run_pipeline(ids, cond, "no", "[6v6 raw counts]"), error = function(e) { cat("SKILL CODE ERROR:", conditionMessage(e), "\n"); NULL })
if (is.null(r)) quit(status = 1)
res <- r$results; str(res)
cat("stageR result columns:", paste(colnames(res), collapse = ", "), "\n")
genes_tested <- length(r$qval); cat("genes tested after Skill's dmFilter:", genes_tested, "\n")
sig_genes <- names(r$qval)[!is.na(r$qval) & r$qval < 0.05]
sigtx <- res[res$transcript < 0.05 & !is.na(res$transcript), ]   # stage-wise adjusted transcript p (OFDR 0.05)
tp <- intersect(sig_genes, tr$gene_id[tr$true_switch]); fpn <- intersect(sig_genes, tr$gene_id[tr$type == "null"])
cat(sprintf("gene-level q<0.05: %d genes | planted switches recovered %d/20 | null-gene FPs %d | dge_only called %d | small(0.06) called %d | dte_like(0.15) called %d\n",
            length(sig_genes), length(tp), length(fpn), length(intersect(sig_genes, tr$gene_id[tr$type=="dge_only"])),
            length(intersect(sig_genes, tr$gene_id[tr$type=="small_switch"])), length(intersect(sig_genes, tr$gene_id[tr$type=="dte_like"]))))
chk("Manual pipeline recovers all 20 planted switch genes (gene-level q<0.05)", length(tp) == 20, sprintf("%d/20", length(tp)))
chk("Manual pipeline: null-gene FP <= 5%", length(fpn) <= 13, sprintf("%d of %d null genes", length(fpn), sum(tr$type=="null")))
chk("Manual pipeline: DGE-only decoys not called", length(intersect(sig_genes, tr$gene_id[tr$type=="dge_only"])) == 0)

# stageR transcript confirmation should name B (poison) or C (skip) among confirmed transcripts for planted genes
conf_hits <- 0
for (g in tp) { tt <- tr[tr$gene_id == g, ]; want <- if (tt$type == "poison_switch") paste0(g, "_B") else paste0(g, "_C")
  conf_hits <- conf_hits + as.integer(any(sigtx$txID == want)) }
chk("stageR confirms the truly switching transcript (B for poison, C for skip) in planted genes", conf_hits >= 18, sprintf("%d/%d", conf_hits, length(tp)))

# --- second implementation: DRIMSeq's own gene-level test on the same filtered object
d <- r$d
design <- model.matrix(~ condition, data = DRIMSeq::samples(d))  # PATCH: Skill writes samples(d), masked by Biobase::samples after library(DEXSeq) (see 21_samples_mask.R)
set.seed(1); d <- dmPrecision(d, design = design, BPPARAM = SerialParam()); d <- dmFit(d, design = design, verbose = 0, BPPARAM = SerialParam()); d <- dmTest(d, coef = "conditiontreatment", verbose = 0)
dr <- DRIMSeq::results(d); dsig <- dr$gene_id[dr$adj_pvalue < 0.05]
cat(sprintf("DRIMSeq dmTest: %d genes adj p<0.05 | planted recovered %d/20 | null FPs %d\n", length(dsig), length(intersect(dsig, tr$gene_id[tr$true_switch])), length(intersect(dsig, tr$gene_id[tr$type=="null"]))))
jac <- length(intersect(sig_genes, dsig)) / length(union(sig_genes, dsig))
chk("DEXSeq (Skill) vs DRIMSeq gene-level call sets concordant (Jaccard >= 0.7)", jac >= 0.7, sprintf("Jaccard %.2f (DEXSeq %d, DRIMSeq %d)", jac, length(sig_genes), length(dsig)))

# --- Skill claim: naive transcript-level BH overcounts vs stageR. Measure in null genes (no planted effect), using a null split as well
naive_fp <- function(dxr, trg) { p <- dxr$pvalue; names(p) <- dxr$featureID; p[is.na(p)] <- 1; padj <- p.adjust(p, "BH"); tg <- sub("_[ABC]$", "", names(p)); sum(padj < 0.05 & tg %in% trg$gene_id[trg$type == "null"]) }
cat("\n-- null split (ctrl 1-3 vs ctrl 4-6) --\n")
r0 <- run_pipeline(sprintf("ctrl_%d", 1:6), factor(rep(c("A", "B"), each = 3)), "no", "[null 3v3]")
sg0 <- names(r0$qval)[!is.na(r0$qval) & r0$qval < 0.05]
cat(sprintf("null split: genes tested %d | gene-level q<0.05: %d | stageR-confirmed transcripts %d | naive BH transcripts (padj<0.05) %d\n",
            length(r0$qval), length(sg0), sum(r0$results$transcript < 0.05, na.rm = TRUE), { p <- r0$dxr$pvalue; p[is.na(p)] <- 1; sum(p.adjust(p, "BH") < 0.05) }))
chk("null split: gene-level FDR calls <= 3", length(sg0) <= 3, sprintf("%d", length(sg0)))
cat("naive-BH null-gene transcript FPs (6v6 real comparison):", naive_fp(r$dxr, tr), " | stageR-confirmed transcripts in null genes:", sum(sigtx$geneID %in% tr$gene_id[tr$type == "null"]), "\n")

# --- scaling: raw counts (Skill) vs dtuScaledTPM (Love 2018 recommendation) -> same calls?
r2 <- run_pipeline(ids, cond, "dtuScaledTPM", "[6v6 dtuScaledTPM]")
sg2 <- names(r2$qval)[!is.na(r2$qval) & r2$qval < 0.05]
cat(sprintf("dtuScaledTPM: %d genes q<0.05; planted %d/20; overlap with raw-count calls %d\n", length(sg2), length(intersect(sg2, tr$gene_id[tr$true_switch])), length(intersect(sg2, sig_genes))))
cat("DONE input2\n")
