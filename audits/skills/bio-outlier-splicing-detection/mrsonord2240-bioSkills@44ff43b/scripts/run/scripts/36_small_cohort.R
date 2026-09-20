# Edge input: FRASER on cohorts BELOW the Skill's stated minimum (n<20). Skill text: "Patient + cohort <20: Insufficient for outlier detection".
# Runs the Skill's workflow verbatim (DataFrame fix) with the Skill's q=10, then with OHT-estimated q. Usage: Rscript 36_small_cohort.R <bamdir_all> <workdir> <synth> <n>
suppressPackageStartupMessages({library(FRASER); library(BiocParallel)})
a <- commandArgs(TRUE); bamdir <- a[1]; wd <- a[2]; synth <- a[3]; n <- as.integer(a[4])
source(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))), "20_eval_lib.R"))
bp <- MulticoreParam(8)
pick <- c("PATIENT_001", sprintf("S%02d", c(1:4, 6:11, 13)))[seq_len(n)]
bam_files <- file.path(bamdir, paste0(pick, ".bam"))
sample_table <- data.frame(sampleID = pick, bamFile = bam_files, pairedEnd = TRUE)
settings <- FraserDataSet(colData = S4Vectors::DataFrame(sample_table), workingDir = wd, name = paste0("cohort_n", n))
settings <- countRNAData(settings, BPPARAM = bp)
fds <- calculatePSIValues(settings)
fds <- filterExpressionAndVariability(fds, minDeltaPsi = 0.0, minExpressionInOneSample = 20, quantile = 0.05, quantileMinExpression = 1)
fitMetrics(fds) <- 'jaccard'; currentType(fds) <- 'jaccard'
r1 <- tryCatch({ f <- suppressWarnings(FRASER(fds, q = c(jaccard = 10), BPPARAM = bp)); eval_fds(f, synth, tag = paste0("n=", n, " q=10 (Skill default)")) }, error = function(e) cat("n=", n, "q=10 FAILED:", conditionMessage(e), "\n"))
fq <- estimateBestQ(fds, type = "jaccard", useOHT = TRUE); qb <- bestQ(fq, "jaccard"); cat("n =", n, "OHT bestQ =", qb, "\n")
r2 <- tryCatch({ f <- suppressWarnings(FRASER(fds, q = c(jaccard = qb), BPPARAM = bp)); eval_fds(f, synth, tag = paste0("n=", n, " q=OHT ", qb)) }, error = function(e) cat("n=", n, "q=", qb, "FAILED:", conditionMessage(e), "\n"))
