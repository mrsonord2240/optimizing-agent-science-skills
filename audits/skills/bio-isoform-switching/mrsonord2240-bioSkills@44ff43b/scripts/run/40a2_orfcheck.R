setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
sl <- readRDS("in4_after_orf.rds"); o <- sl$orfAnalysis
cat("orfAnalysis columns:", paste(colnames(o), collapse=", "), "\n"); print(head(o, 3))
