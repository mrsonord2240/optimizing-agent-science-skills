# 10B workaround check: same odd-ID 3v5 set, but sample_id/names passed through make.names() (paths unchanged); manual block r_04 verbatim, scored vs truth.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work/w10"); source("../../helpers.R"); source("../../helpers2.R")
suppressPackageStartupMessages({ library(tximport); library(DRIMSeq); library(DEXSeq); library(stageR) })
tt <- read.delim("../../data/odd_3v5/truth_genes.tsv", stringsAsFactors = FALSE); planted <- tt$gene_id[tt$true_switch]
meta <- read.delim("sample_metadata.tsv", stringsAsFactors = FALSE); paths <- file.path("salmon_quant", meta$sample_id, "quant.sf")
meta$sample_id <- make.names(meta$sample_id); files <- setNames(paths, meta$sample_id); cat("renamed IDs:", paste(meta$sample_id, collapse = ","), "\n")
tx <- read.delim(files[1])$Name; tx2gene <- data.frame(tx = tx, gene = sub("_[ABC]$", "", tx))
run_block("r_04.R"); sg <- names(qval)[!is.na(qval) & qval < 0.05]
cat(sprintf("manual pipeline with syntactic IDs: gene q<0.05 %d | planted %d/20 | other %d\n", length(sg), length(intersect(sg, planted)), length(setdiff(sg, planted))))
chk("10B-fix manual block runs once IDs are syntactic and recovers >= 18/20 planted", length(intersect(sg, planted)) >= 18, length(intersect(sg, planted)))
rs <- getAdjustedPValues(stageRObj, order = FALSE, onlySignificantGenes = FALSE); cat("stageR rows", nrow(rs), "columns", paste(colnames(rs), collapse = ","), "\n")
