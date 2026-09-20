# Skill's exact library() order: library(tximeta); library(DRIMSeq); library(DEXSeq); library(stageR)
suppressPackageStartupMessages({library(tximeta); library(DRIMSeq); library(DEXSeq); library(stageR)})
cat("find('samples') ->", paste(find("samples"), collapse=", "), "\n")
cat("find('counts')  ->", paste(find("counts"), collapse=", "), "\n")
d <- dmDSdata(counts = data.frame(gene_id=c("g","g"), feature_id=c("a","b"), s1=c(10,20), s2=c(12,18)), samples = data.frame(sample_id=c("s1","s2"), condition=c("x","y")))
r <- try(samples(d), silent = TRUE); cat("samples(d) unqualified:", if (inherits(r,"try-error")) paste("ERROR:", conditionMessage(attr(r,"condition"))) else "ok", "\n")
r <- try(DRIMSeq::samples(d), silent = TRUE); cat("DRIMSeq::samples(d):", if (inherits(r,"try-error")) "ERROR" else "ok", "\n")
r <- try(counts(d), silent = TRUE); cat("counts(d) unqualified:", if (inherits(r,"try-error")) paste("ERROR:", conditionMessage(attr(r,"condition"))) else "ok", "\n")
cat("DRIMSeq exports samples:", "samples" %in% getNamespaceExports("DRIMSeq"), "; DEXSeq exports samples:", "samples" %in% getNamespaceExports("DEXSeq"), "\n")
# order reversed
detach("package:DEXSeq", unload=FALSE); library(DEXSeq); 
