# The Skill's permutation block (blocks/r_02.R) verbatim on the UNBALANCED odd-ID 3 v 5 planted set (no heterogeneity): does it produce valid, distinct,
# size-preserving alternative splits, and do the permuted counts stay near zero while the observed list is the planted one?
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
D <- "../data/odd_3v5"; wd <- "w92b"; unlink(wd, recursive = TRUE); dir.create(wd); file.copy(file.path(D, c("salmon_quant", "annotation.gtf", "transcripts.fa", "sample_metadata.tsv")), wd, recursive = TRUE); setwd(wd)
invisible(capture.output(suppressMessages(suppressWarnings(run_block("r_01.R")))))
t0 <- Sys.time(); invisible(capture.output(suppressMessages(suppressWarnings(run_block("r_02.R")))))
cat(sprintf("observed %d; permuted: %s; %d splits; %.0f s\n", observed, paste(permuted, collapse = " "), length(perms), as.numeric(difftime(Sys.time(), t0, units = "secs"))))
sizes <- sapply(perms, function(p) sum(p == design$condition[1])); k <- sum(design$condition == design$condition[1])
chk("all permuted labelings keep the group sizes", all(sizes == k), paste("group of sample 1:", k, "sizes", paste(unique(sizes), collapse = ",")))
keys <- sapply(perms, function(p) paste(p, collapse = "")); chk("permuted labelings are distinct and differ from the true labels", !anyDuplicated(keys) && !any(keys == paste(design$condition, collapse = "")))
ov <- sapply(perms, function(p) sum(p == design$condition[1] & design$condition == design$condition[1])); cat("overlap with the true group of sample 1 (k*k/n =", k * k / nrow(design), "):", paste(ov, collapse = " "), "\n")
chk("observed >> permuted (planted list 20+ vs permuted max <= 3)", observed >= 20 && max(permuted, na.rm = TRUE) <= 3, paste(observed, "vs", max(permuted, na.rm = TRUE)))
cat("DONE 92b\n")
