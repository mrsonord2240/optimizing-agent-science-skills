# INPUT 8D evaluation: shipped example (real-data mode) output on the NEW 4v7 batch set vs planted truth.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
tt <- read.delim("../data/new1/truth_genes.tsv", stringsAsFactors = FALSE)
sig <- read.csv("ex_new/out/significant_switches.csv"); g <- unique(sig$gene_id)
pl <- tt$gene_id[tt$true_switch]
cat(sprintf("example output: %d isoforms in %d genes | planted recovered %d/20 | other genes called %d (%s)\n", nrow(sig), length(g), length(intersect(g, pl)), length(setdiff(g, pl)), paste(setdiff(g, pl), collapse = ",")))
chk("8D shipped example (real-data mode, unbalanced 4v7 + batch column) recovers >=19/20 planted", length(intersect(g, pl)) >= 19)
chk("8D shipped example: <=2 non-planted genes called", length(setdiff(g, pl)) <= 2, length(setdiff(g, pl)))
sl <- readRDS("ex_new/out/switchAnalyzeRlist.rds"); sc <- sl$switchConsequence; poison <- tt$gene_id[tt$type == "poison_switch"]
nm <- sc[which(sc$featureCompared == "NMD_status" & sc$switchConsequence == "NMD sensitive"), ]
ng <- unique(sub("_[ABC]$", "", nm$isoformUpregulated)); ngd <- unique(sub("_[ABC]$", "", nm$isoformDownregulated))
cat("design used by the example (batch covariate kept):", paste(colnames(sl$designMatrix), collapse = ","), "\n")
cat(sprintf("NMD_status 'NMD sensitive' (isoform UP) genes: %d, planted poison among them %d/10; NMD-sensitive isoform DOWN genes: %d\n", length(ng), length(intersect(ng, poison)), length(ngd)))
chk("8D example NMD_status (ORFs predicted, no CDS in GTF): the poison isoform up in >=9/10 poison genes", length(intersect(ng, poison)) >= 9)
chk("8D example plot PDF written and non-trivial", file.exists("ex_new/out/switchPlot_NEW010.pdf") && file.size("ex_new/out/switchPlot_NEW010.pdf") > 5000)
cat("DONE 82\n")
