# Input 6/7 (part 2): SKILL.md "DTU on Long-Read Counts" R block on the FLAIR quantify output of the SYNTHETIC 3 v 3 data.
# Leg A: SKILL code verbatim (file name, read.table, dmDSdata(counts = counts, samples = samples)).
# Leg B: minimal repair (split FLAIR 'ids' into feature_id/gene_id, match sample names), then dmFilter as in SKILL, then DRIMSeq test (SKILL says "then proceed").
D <- "F:/OpenScience/audits/bio-long-read-splicing/run"
setwd(paste0(D, "/out/flair"))
suppressMessages({library(DRIMSeq); library(DEXSeq); library(stageR)})
cat("DRIMSeq", as.character(packageVersion("DRIMSeq")), " DEXSeq", as.character(packageVersion("DEXSeq")), " stageR", as.character(packageVersion("stageR")), "\n")

cat("\n### Leg A: SKILL verbatim\n")
r <- try(counts <- read.table("flair_quantified_counts.tsv", header = TRUE, sep = "\t"), silent = TRUE)
cat("read.table('flair_quantified_counts.tsv'):", if (inherits(r, "try-error")) paste("ERROR:", conditionMessage(attr(r, "condition"))) else "ok", "\n")
counts <- read.table("quantifiedSR.counts.tsv", header = TRUE, sep = "\t")  # the file FLAIR really writes (SKILL's diffSplice call uses flair_quantified.counts.tsv)
samples <- data.frame(
  sample_id = c("s1", "s2", "s3", "s4", "s5", "s6"),
  condition = c("ctrl", "ctrl", "ctrl", "trt", "trt", "trt")
)
r <- try(d <- dmDSdata(counts = counts, samples = samples), silent = TRUE)
cat("dmDSdata(counts=<FLAIR counts>, samples=<SKILL data.frame>):", if (inherits(r, "try-error")) paste("ERROR:", conditionMessage(attr(r, "condition"))) else "ok", "\n")
cat("FLAIR counts columns:", paste(colnames(counts), collapse = ", "), "\n")

cat("\n### Leg B: minimal repair\n")
cnt <- counts
cnt$gene_id <- sub("^.*_", "", cnt$ids)          # FLAIR id = <isoform>_<gene>
cnt$feature_id <- cnt$ids
scols <- setdiff(colnames(counts), "ids")
samples2 <- data.frame(sample_id = scols, condition = sub("^[^_]+_([^_]+)_.*$", "\\1", scols))
cnt2 <- cnt[, c("gene_id", "feature_id", scols)]
d <- dmDSdata(counts = cnt2, samples = samples2)
d <- dmFilter(d, min_samps_feature_expr = 3, min_feature_expr = 5, min_samps_feature_prop = 3, min_feature_prop = 0.1, min_samps_gene_expr = 6, min_gene_expr = 10)
cat("after SKILL dmFilter: genes", length(unique(counts(d)$gene_id)), " features", nrow(counts(d)), "\n")
design <- model.matrix(~ condition, data = DRIMSeq::samples(d))
set.seed(1)
d <- try(dmPrecision(d, design = design), silent = TRUE)
if (inherits(d, "try-error")) { cat("dmPrecision ERROR:", conditionMessage(attr(d, "condition")), "\n") } else {
  d <- dmFit(d, design = design)
  d <- dmTest(d, coef = "conditiontrt")
  res <- DRIMSeq::results(d)
  print(res)
  rf <- DRIMSeq::results(d, level = "feature"); print(rf); print(round(DRIMSeq::proportions(d)[, 3:8], 3))
}
