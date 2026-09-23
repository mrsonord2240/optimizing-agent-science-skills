# Input 14 (new, fresh) -- exercise the exact source copy of mvmr_conditional_f.R on a
# well-powered two-exposure fixture; it must print per-exposure conditional F, IVW and Q_A.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) stop("usage: input14_fresh_mvmr_script.R <rscript> <mvmr-script> <outdir>")
rscript <- args[[1]]; mvmr_script <- args[[2]]; outdir <- args[[3]]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
set.seed(514); n <- 80L
x1 <- rnorm(n, 0.09, 0.015); x2 <- rnorm(n, 0.07, 0.015)
dat <- data.frame(SNP = paste0("rs", seq_len(n)), beta.x1 = x1, se.x1 = 0.006,
  beta.x2 = x2, se.x2 = 0.006, beta.y = 0.30*x1 - 0.10*x2 + rnorm(n,0,0.008), se.y = 0.01)
infile <- file.path(outdir, "mvmr.tsv"); write.table(dat, infile, sep="\t", row.names=FALSE, quote=FALSE)
result <- system2(rscript, c(mvmr_script, "--dat", infile, "--exposures", "x1,x2", "--gencov", "0"), stdout=TRUE, stderr=TRUE)
cat(paste(result, collapse="\n"), "\n")
if (!any(grepl("Conditional F-statistics", result, fixed=TRUE))) stop("source MVMR script did not print conditional F")
if (!any(grepl("Q-Statistic", result, fixed=TRUE))) stop("source MVMR script did not print heterogeneity result")
cat("INPUT14 PASS: exact source MVMR script completed above the conditional-F guard.\n")
