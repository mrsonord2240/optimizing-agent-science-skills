# INPUT 10C evaluation: shipped example (real-data mode) output on the odd-ID unbalanced 3 v 5 set vs planted truth.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
tt <- read.delim("../data/odd_3v5/truth_genes.tsv", stringsAsFactors = FALSE); pl <- tt$gene_id[tt$true_switch]; poison <- tt$gene_id[tt$type == "poison_switch"]
sig <- read.csv("ex_odd/out/significant_switches.csv"); g <- unique(sig$gene_id)
cat(sprintf("example output: %d isoforms in %d genes | planted recovered %d/20 | other genes called %d (%s)\n", nrow(sig), length(g), length(intersect(g, pl)), length(setdiff(g, pl)), paste(setdiff(g, pl), collapse = ",")))
chk("10C shipped example, odd IDs, 3v5: >=19/20 planted recovered", length(intersect(g, pl)) >= 19)
chk("10C shipped example: <=2 non-planted genes", length(setdiff(g, pl)) <= 2, length(setdiff(g, pl)))
sl <- readRDS("ex_odd/out/switchAnalyzeRlist.rds"); cat("designMatrix sampleIDs:", paste(sl$designMatrix$sampleID, collapse = ","), "| conditions:", paste(sl$designMatrix$condition, collapse = ","), "\n")
chk("10C sample IDs kept verbatim in the switchAnalyzeRlist", setequal(sl$designMatrix$sampleID, c("1-ctrl", "2-ctrl", "3-ctrl", paste0("trt.", 1:5, "-b"))))
sc <- sl$switchConsequence; nm <- sc[which(sc$featureCompared == "NMD_status" & sc$switchConsequence == "NMD sensitive"), ]
ng <- unique(sub("_[ABC]$", "", nm$isoformUpregulated)); cat(sprintf("NMD sensitive isoform UP in %d genes, planted poison among them %d/10\n", length(ng), length(intersect(ng, poison))))
chk("10C NMD_status: poison isoform up in >= 9/10 poison genes", length(intersect(ng, poison)) >= 9)
chk("10C plot PDF non-trivial", file.exists("ex_odd/out/switchPlot_HET010.pdf") && file.size("ex_odd/out/switchPlot_HET010.pdf") > 5000)
cat("DONE 93b\n")
