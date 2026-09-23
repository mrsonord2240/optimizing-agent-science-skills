# Input 15 (new, fresh) -- run the exact source copy of simex_egger.R on a deterministic
# NOME-violated harmonised fixture and require both naive and SIMEX slopes.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) stop("usage: input15_fresh_simex_script.R <rscript> <simex-script> <outdir>")
rscript <- args[[1]]; simex_script <- args[[2]]; outdir <- args[[3]]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
set.seed(515); n <- 40L
bx <- rnorm(n, 0.03, 0.003); sx <- rnorm(n, 0.025, 0.003)
dat <- data.frame(SNP=paste0("rs",seq_len(n)), beta.exposure=bx, se.exposure=sx,
  beta.outcome=0.40*bx+rnorm(n,0,0.01), se.outcome=runif(n,0.01,0.02), mr_keep=TRUE)
infile <- file.path(outdir, "simex_harmonised.tsv"); write.table(dat, infile, sep="\t", row.names=FALSE, quote=FALSE)
result <- system2(rscript, c(simex_script, "--dat", infile, "--B", "200", "--seed", "42"), stdout=TRUE, stderr=TRUE)
cat(paste(result, collapse="\n"), "\n")
if (!any(grepl("SIMEX-corrected slope", result, fixed=TRUE)) || !any(grepl("Naive Egger slope", result, fixed=TRUE))) stop("source SIMEX script did not print both slopes")
cat("INPUT15 PASS: exact source SIMEX script completed with both slopes.\n")
