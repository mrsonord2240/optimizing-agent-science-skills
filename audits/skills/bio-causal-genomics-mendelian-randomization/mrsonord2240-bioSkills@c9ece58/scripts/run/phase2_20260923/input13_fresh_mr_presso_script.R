# Input 13 (new, fresh) -- run the exact source copy of mr_presso_outliers.R on a
# deterministic synthetic harmonised table with planted invalid instruments. The script itself
# decides which adjusted P values pass; this harness checks that it writes a parseable outlier list.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) stop("usage: input13_fresh_mr_presso_script.R <rscript> <presso-script> <outdir>")
rscript <- args[[1]]; presso_script <- args[[2]]; outdir <- args[[3]]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
set.seed(513)
n <- 40L; invalid <- seq_len(10L)
bx <- rnorm(n, 0.08, 0.01); sx <- rep(0.01, n); sy <- rep(0.012, n)
by <- 0.30 * bx + rnorm(n, 0, sy)
by[invalid] <- by[invalid] + 0.18
dat <- data.frame(SNP = paste0("rs", seq_len(n)), beta.exposure = bx, se.exposure = sx,
  beta.outcome = by, se.outcome = sy, mr_keep = TRUE)
dat_file <- file.path(outdir, "presso_harmonised.tsv"); out_file <- file.path(outdir, "presso_outliers.txt")
write.table(dat, dat_file, sep = "\t", row.names = FALSE, quote = FALSE)
result <- system2(rscript, c(presso_script, "--dat", dat_file, "--nb", "1000", "--seed", "42", "--out", out_file), stdout = TRUE, stderr = TRUE)
cat(paste(result, collapse = "\n"), "\n")
if (!file.exists(out_file)) stop("MR-PRESSO script did not write the required outlier file")
outliers <- readLines(out_file, warn = FALSE)
cat("fresh MR-PRESSO outlier count:", length(outliers), " planted overlap:", sum(outliers %in% paste0("rs", invalid)), "\n")
if (length(outliers) == 0L) stop("MR-PRESSO script found no outliers in a strongly planted-invalid fixture")
cat("INPUT13 PASS: exact source script emitted a non-empty, parseable outlier list.\n")
