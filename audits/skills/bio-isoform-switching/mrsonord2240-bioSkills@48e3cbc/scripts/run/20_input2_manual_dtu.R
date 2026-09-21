# INPUT 2 (Variant A): SKILL.md "Manual DTU Pipeline" block (blocks/r_04.R) executed VERBATIM on SYNTHETIC 6 v 6 (shuffled IDs), planted truth.
# Also: masking claim (unqualified samples(d)/counts(d) after library(DEXSeq)), DRIMSeq dmTest comparison, stageR check, null split.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
set.seed(202); tt <- truth()
shuf <- function(k) sprintf("SRR70%05d", sample(10000:99999, k))
ids6 <- c(sprintf("ctrl_%d", 1:6), sprintf("trt_%d", 1:6)); o <- sample(12); ids6 <- ids6[o]; cond6 <- rep(c("control", "treatment"), each = 6)[o]
new6 <- shuf(12)
stage_salmon("w2", ids6, new6, cond6); setwd("w2")
meta <- read.delim("sample_metadata.tsv", stringsAsFactors = FALSE)                       # preamble the Skill's block comments ask for
files <- setNames(file.path("salmon_quant", new6, "quant.sf"), new6)
tx2gene <- local({ tx <- unique(vapply(strsplit(readLines(file.path(SYN, "annotation.gtf")), "\t", fixed = TRUE), function(x) sub('.*transcript_id "([^"]+)".*', "\\1", x[9]), ""))
                   data.frame(tx = tx, gene = sub("_[ABC]$", "", tx)) })   # (read.delim would mangle the GTF quotes)
run_block("r_04.R")                                                                        # <- the Skill's block, verbatim
cat("block finished; result columns:", paste(colnames(results), collapse = ","), "| rows", nrow(results), "\n")
# masking claim
cat("find('samples'):", paste(find("samples"), collapse = ","), "| find('counts'):", paste(find("counts"), collapse = ","), "\n")
r <- try(samples(d), silent = TRUE); chk("Skill's masking warning is real: unqualified samples(d) fails after library(DEXSeq)", inherits(r, "try-error"), if (inherits(r, "try-error")) substr(conditionMessage(attr(r, "condition")), 1, 110) else "worked?")
# gene-level q from perGeneQValue
sig_g <- names(qval)[!is.na(qval) & qval < 0.05]
pl <- tt$gene_id[tt$true_switch]
cat(sprintf("DEXSeq gene q<0.05: %d genes | planted %d/20 | null %d | dge_only %d | small(0.06) %d | dte_like(0.15) %d\n", length(sig_g), length(intersect(sig_g, pl)),
  length(intersect(sig_g, tt$gene_id[tt$type == "null"])), length(intersect(sig_g, tt$gene_id[tt$type == "dge_only"])), length(intersect(sig_g, tt$gene_id[tt$type == "small_switch"])), length(intersect(sig_g, tt$gene_id[tt$type == "dte_like"]))))
chk("manual DEXSeq recovers >=19/20 planted", length(intersect(sig_g, pl)) >= 19)
chk("manual DEXSeq null-gene FP <= 5% of null genes", length(intersect(sig_g, tt$gene_id[tt$type == "null"])) <= 13, sprintf("%d/260", length(intersect(sig_g, tt$gene_id[tt$type == "null"]))))
chk("DGE-only decoys not called", length(intersect(sig_g, tt$gene_id[tt$type == "dge_only"])) == 0)
# stageR transcript confirmation: the truly switching transcript (B poison / C skip) confirmed
conf <- results[!is.na(results$transcript) & results$transcript < 0.05, ]
okc <- 0; for (g in pl) { iso <- if (tt$type[tt$gene_id == g] == "poison_switch") paste0(g, "_B") else paste0(g, "_C"); okc <- okc + as.integer(iso %in% conf$txID) }
chk("stageR confirms the truly switching transcript in >=19/20 planted genes", okc >= 19, sprintf("%d/20", okc))
# independent implementation: DRIMSeq dmPrecision/dmFit/dmTest on the filtered object d
suppressPackageStartupMessages(library(BiocParallel))
design_full <- model.matrix(~ condition, data = DRIMSeq::samples(d)); d2 <- dmPrecision(d, design = design_full, BPPARAM = SerialParam()); d2 <- dmFit(d2, design = design_full, verbose = 0, BPPARAM = SerialParam()); d2 <- dmTest(d2, coef = "conditiontreatment", verbose = 0)
dr <- DRIMSeq::results(d2); dri_g <- dr$gene_id[!is.na(dr$adj_pvalue) & dr$adj_pvalue < 0.05]
jac <- length(intersect(sig_g, dri_g)) / length(union(sig_g, dri_g))
cat(sprintf("DRIMSeq: %d genes, planted %d/20, Jaccard with DEXSeq %.2f\n", length(dri_g), length(intersect(dri_g, pl)), jac))
chk("DRIMSeq (independent test) recovers >=19/20 planted and Jaccard >= 0.8 with DEXSeq", length(intersect(dri_g, pl)) >= 19 && jac >= 0.8)
# Skill claims 'Checked ... 27 genes = 20 + 1 null + 5 dte_like + 1 small' : compare numbers
cat("Skill-stated check: perGeneQValue<0.05 in 27 genes (20 planted + 1 null + 5 +1). Mine:", length(sig_g), "\n")
# null split of the same pipeline (ctrl 1-3 vs ctrl 4-6)
ids0 <- sprintf("ctrl_%d", 1:6); stage_salmon("../w2n", ids0, shuf(6), rep(c("nA", "nB"), each = 3)); setwd("../w2n")
meta <- read.delim("sample_metadata.tsv", stringsAsFactors = FALSE); nid <- meta$sample_id; files <- setNames(file.path("salmon_quant", nid, "quant.sf"), nid)
run_block("r_04.R"); sg0 <- names(qval)[!is.na(qval) & qval < 0.05]
cat("null split gene calls:", length(sg0), "| stageR confirmed transcripts:", sum(!is.na(results$transcript) & results$transcript < 0.05), "\n")
chk("null split: <=5 gene calls of ~290", length(sg0) <= 5, sprintf("%d", length(sg0)))
# 3 v 3 through the same block (dmFilter scaled: n=6, n_small=3)
setwd(".."); ids3 <- c(sprintf("ctrl_%d", 1:3), sprintf("trt_%d", 1:3)); new3 <- shuf(6)
stage_salmon("w2_3", ids3, new3, rep(c("control", "treatment"), each = 3)); setwd("w2_3"); meta <- read.delim("sample_metadata.tsv", stringsAsFactors = FALSE)
files <- setNames(file.path("salmon_quant", new3, "quant.sf"), new3); run_block("r_04.R"); sg3 <- names(qval)[!is.na(qval) & qval < 0.05]
cat(sprintf("3v3 manual DEXSeq: %d genes, planted %d/20\n", length(sg3), length(intersect(sg3, pl))))
chk("3v3 manual pipeline recovers >=18/20 planted", length(intersect(sg3, pl)) >= 18)
cat("DONE input2\n")
