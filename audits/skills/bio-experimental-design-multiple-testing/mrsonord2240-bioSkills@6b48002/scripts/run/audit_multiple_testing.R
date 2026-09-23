# Phase 2 dynamic audit runner for bio-experimental-design-multiple-testing.
# Inputs: source skill directory supplied as the first command-line argument.
# Usage: r.sh run/audit_multiple_testing.R <skill-dir> <audit-data-dir> <output-dir>

args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 3L)
skill_dir <- normalizePath(args[[1]], winslash = "/", mustWork = TRUE)
data_dir <- normalizePath(args[[2]], winslash = "/", mustWork = FALSE)
out_dir <- normalizePath(args[[3]], winslash = "/", mustWork = FALSE)
dir.create(data_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

library(qvalue)

write_result <- function(name, fields) {
  writeLines(unlist(sprintf("%s=%s", names(fields), fields)),
             file.path(out_dir, paste0(name, ".txt")))
}

# Input 1: canonical genome-wide discovery. BH/BY and q-value receive a seeded
# family with known null status, so the realized FDP can be checked.
set.seed(20260923)
m <- 5000L
n_alt <- 500L
p <- c(rbeta(n_alt, 0.25, 7), runif(m - n_alt))
is_alt <- c(rep(TRUE, n_alt), rep(FALSE, m - n_alt))
bh <- p.adjust(p, method = "BH")
by <- p.adjust(p, method = "BY")
qobj <- qvalue(p)
bh_rej <- bh < 0.05
by_rej <- by < 0.05
bh_fdp <- sum(bh_rej & !is_alt) / max(1L, sum(bh_rej))
stopifnot(length(bh) == m, all(is.finite(bh)), all(bh >= 0 & bh <= 1),
          all(by >= 0 & by <= 1), qobj$pi0 >= 0 && qobj$pi0 <= 1,
          all(qobj$qvalues >= 0 & qobj$qvalues <= 1))
write_result("input1_canonical", list(
  bh_discoveries = sum(bh_rej), by_discoveries = sum(by_rej),
  bh_fdp = sprintf("%.4f", bh_fdp), pi0 = sprintf("%.4f", qobj$pi0),
  qvalue_discoveries = sum(qobj$qvalues < 0.05), status = "PASS"))
write.csv(data.frame(pvalue = p, mean_expression = rgamma(m, 2, 0.4), is_alt = is_alt),
          file.path(data_dir, "canonical_de.csv"), row.names = FALSE)

# Input 2: local-FDR decision and false-coverage-rate interval calculation on
# the same selected large family. This follows the inline FCR block's formula.
lfdr_called <- qobj$lfdr < 0.2
mean_lfdr <- if (any(lfdr_called)) mean(qobj$lfdr[lfdr_called]) else NA_real_
estimate <- c(rnorm(n_alt, 1.2, 0.25), rnorm(m - n_alt, 0, 0.25))
se <- rep(0.25, m)
q <- 0.05
R <- sum(bh < q)
fcr_level <- 1 - q * R / m
alpha_fcr <- 1 - fcr_level
z <- qnorm(1 - alpha_fcr / 2)
ci_lower <- estimate[bh < q] - z * se[bh < q]
ci_upper <- estimate[bh < q] + z * se[bh < q]
stopifnot(all(is.finite(qobj$lfdr)), all(qobj$lfdr >= 0 & qobj$lfdr <= 1),
          is.na(mean_lfdr) || (mean_lfdr >= 0 && mean_lfdr <= 1),
          fcr_level >= 0 && fcr_level <= 1, length(ci_lower) == R,
          all(ci_lower <= ci_upper))
write_result("input2_local_fdr", list(
  called = sum(lfdr_called), mean_lfdr = sprintf("%.4f", mean_lfdr),
  fcr_level = sprintf("%.6f", fcr_level), selected_intervals = R, status = "PASS"))

# Input 3: small all-null family. The skill directs lambda=0 rather than the
# unstable default smoother; its pi0 should be exactly one for this construction.
set.seed(915)
small_p <- runif(30L)
small_q <- qvalue(small_p, lambda = 0)
stopifnot(identical(as.numeric(small_q$pi0), 1), length(small_q$qvalues) == 30L,
          all(is.finite(small_q$qvalues)), all(small_q$qvalues >= 0 & small_q$qvalues <= 1))
write_result("input3_small_family", list(pi0 = small_q$pi0,
  discoveries = sum(small_q$qvalues < 0.05), status = "PASS"))

# Input 4: source the shipped wrapper exactly as the SKILL.md directs. This
# exercises both a successful child IHW execution and its documented BH fallback
# without trusting a zero exit code alone.
old_wd <- getwd()
on.exit(setwd(old_wd), add = TRUE)
setwd(skill_dir)
source("scripts/ihw_safe.R")
set.seed(20260924)
ihw_m <- 1800L
ihw_p <- c(rbeta(180L, 0.25, 7), runif(ihw_m - 180L))
ihw_cov <- rgamma(ihw_m, 2, 0.5)
ihw_res <- ihw_safe(ihw_p, ihw_cov, alpha = 0.05, nbins = 5, tries = 2)
bh_ref <- p.adjust(ihw_p, method = "BH")
stopifnot(length(ihw_res$padj) == ihw_m, all(is.finite(ihw_res$padj)),
          all(ihw_res$padj >= 0 & ihw_res$padj <= 1), ihw_res$attempts >= 1L,
          ihw_res$attempts <= 2L)
if (identical(ihw_res$method, "BH (IHW solver crashed; fallback)")) {
  stopifnot(isTRUE(all.equal(ihw_res$padj, bh_ref, tolerance = 0)))
}
write_result("input4_ihw_function", list(method = ihw_res$method,
  attempts = ihw_res$attempts, discoveries = sum(ihw_res$padj < 0.05), status = "PASS"))

# Input 5: the shipped CLI entry point. Its output CSV must preserve all input
# rows and add bounded adjusted p-values.
cli_in <- file.path(data_dir, "ihw_cli_input.csv")
cli_out <- file.path(out_dir, "ihw_cli_output.csv")
write.csv(data.frame(pvalue = ihw_p, mean_expression = ihw_cov), cli_in, row.names = FALSE)
rscript <- file.path(R.home("bin"), "Rscript")
cli_status <- system2(rscript, c("scripts/ihw_safe.R", cli_in, "pvalue", "mean_expression", cli_out, "0.05"),
                      stdout = file.path(out_dir, "input5_cli_stdout.txt"),
                      stderr = file.path(out_dir, "input5_cli_stderr.txt"))
stopifnot(identical(cli_status, 0L), file.exists(cli_out))
cli <- read.csv(cli_out)
stopifnot(nrow(cli) == ihw_m, "padj_ihw" %in% names(cli), all(is.finite(cli$padj_ihw)),
          all(cli$padj_ihw >= 0 & cli$padj_ihw <= 1))
write_result("input5_ihw_cli", list(rows = nrow(cli), discoveries = sum(cli$padj_ihw < 0.05), status = "PASS"))

writeLines("ALL_DYNAMIC_INPUTS_PASS", file.path(out_dir, "summary.txt"))
