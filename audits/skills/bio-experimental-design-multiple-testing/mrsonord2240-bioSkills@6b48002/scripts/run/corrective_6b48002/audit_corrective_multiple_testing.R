# Fresh corrective Phase 2 execution tests for bio-experimental-design-multiple-testing.
# Usage: r.sh audit_corrective_multiple_testing.R <skill-dir> <data-dir> <output-dir>
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 3L)
skill_dir <- normalizePath(args[[1]], winslash = "/", mustWork = TRUE)
data_dir <- normalizePath(args[[2]], winslash = "/", mustWork = FALSE)
out_dir <- normalizePath(args[[3]], winslash = "/", mustWork = FALSE)
dir.create(data_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

write_result <- function(name, fields) {
  writeLines(sprintf("%s=%s", names(fields), fields), file.path(out_dir, paste0(name, ".txt")))
}

# qvalue has an environment-specific outer-process teardown crash. Run it only
# in a worker, then parse a saved, testable result in the parent process.
qvalue_detail_safe <- function(p, lambda = NULL) {
  inp <- tempfile(fileext = ".rds")
  out <- tempfile(fileext = ".rds")
  on.exit(unlink(c(inp, out)), add = TRUE)
  saveRDS(list(p = p, lambda = lambda), inp)
  code <- sprintf(paste0(
    "d <- readRDS('%s'); library(qvalue); ",
    "q <- if (is.null(d$lambda)) qvalue(d$p) else qvalue(d$p, lambda = d$lambda); ",
    "saveRDS(list(pi0=q$pi0,qvalues=q$qvalues,lfdr=q$lfdr),'%s')"),
    normalizePath(inp, winslash = "/", mustWork = FALSE),
    normalizePath(out, winslash = "/", mustWork = FALSE))
  status <- system2(file.path(R.home("bin"), "Rscript"), c("-e", shQuote(code)), stdout = FALSE, stderr = FALSE)
  # qvalue may terminate its worker during teardown after saveRDS(); the
  # parent deliberately treats a complete, parseable result as success.
  stopifnot(file.exists(out))
  answer <- readRDS(out)
  stopifnot(is.list(answer), is.finite(answer$pi0), length(answer$qvalues) == length(p),
            all(is.finite(answer$qvalues)), all(answer$qvalues >= 0 & answer$qvalues <= 1))
  c(answer, list(worker_status = status))
}

old_wd <- getwd()
on.exit(setwd(old_wd), add = TRUE)
setwd(skill_dir)
source("scripts/qvalue_safe.R")
source("scripts/ihw_safe.R")

# Input 1: canonical genome-wide discovery, including the shipped qvalue_safe helper.
set.seed(2026092301)
m <- 5000L
n_alt <- 500L
p <- c(rbeta(n_alt, 0.25, 7), runif(m - n_alt))
is_alt <- c(rep(TRUE, n_alt), rep(FALSE, m - n_alt))
bh <- p.adjust(p, method = "BH")
by <- p.adjust(p, method = "BY")
qsafe <- qvalue_safe(p)
qdetail <- qvalue_detail_safe(p)
bh_rej <- bh < 0.05
bh_fdp <- sum(bh_rej & !is_alt) / max(1L, sum(bh_rej))
stopifnot(length(bh) == m, all(is.finite(bh)), all(bh >= 0 & bh <= 1),
          all(by >= 0 & by <= 1), identical(qsafe$method, "qvalue"),
          is.finite(qsafe$pi0), is.finite(qsafe$discoveries),
          qsafe$discoveries == sum(qdetail$qvalues < 0.05))
write_result("input1_canonical", list(
  bh_discoveries = sum(bh_rej), by_discoveries = sum(by < 0.05),
  bh_fdp = sprintf("%.4f", bh_fdp), qvalue_pi0 = sprintf("%.4f", qsafe$pi0),
  qvalue_discoveries = qsafe$discoveries, status = "PASS"))
write.csv(data.frame(pvalue = p, mean_expression = rgamma(m, 2, 0.4), is_alt = is_alt),
          file.path(data_dir, "canonical_de.csv"), row.names = FALSE)

# Input 2: local FDR and the inline false-coverage-rate construction.
lfdr_called <- qdetail$lfdr < 0.2
mean_lfdr <- if (any(lfdr_called)) mean(qdetail$lfdr[lfdr_called]) else NA_real_
estimate <- c(rnorm(n_alt, 1.2, 0.25), rnorm(m - n_alt, 0, 0.25))
se <- rep(0.25, m)
q <- 0.05
R <- sum(bh < q)
fcr_level <- 1 - q * R / m
z <- qnorm(1 - (1 - fcr_level) / 2)
ci_lower <- estimate[bh < q] - z * se[bh < q]
ci_upper <- estimate[bh < q] + z * se[bh < q]
stopifnot(length(qdetail$lfdr) == m, all(is.finite(qdetail$lfdr)),
          all(qdetail$lfdr >= 0 & qdetail$lfdr <= 1),
          is.na(mean_lfdr) || (mean_lfdr >= 0 && mean_lfdr <= 1),
          fcr_level >= 0 && fcr_level <= 1, length(ci_lower) == R,
          all(ci_lower <= ci_upper))
write_result("input2_local_fdr", list(called = sum(lfdr_called),
  mean_lfdr = sprintf("%.4f", mean_lfdr), fcr_level = sprintf("%.6f", fcr_level),
  selected_intervals = R, status = "PASS"))

# Input 3: the documented lambda=0 small-family qvalue fallback.
set.seed(2026092303)
small_p <- runif(30L)
small_q <- qvalue_detail_safe(small_p, lambda = 0)
stopifnot(identical(as.numeric(small_q$pi0), 1), length(small_q$qvalues) == 30L,
          all(small_q$qvalues >= 0 & small_q$qvalues <= 1))
write_result("input3_small_family", list(pi0 = small_q$pi0,
  discoveries = sum(small_q$qvalues < 0.05), status = "PASS"))

# Input 4: sourceable IHW safety wrapper. Its fallback must exactly be BH.
set.seed(2026092304)
ihw_m <- 100L
ihw_p <- c(rbeta(10L, 0.25, 7), runif(ihw_m - 10L))
ihw_cov <- rgamma(ihw_m, 2, 0.5)
ihw_res <- ihw_safe(ihw_p, ihw_cov, alpha = 0.05, nbins = 5, tries = 3)
bh_ref <- p.adjust(ihw_p, method = "BH")
stopifnot(length(ihw_res$padj) == ihw_m, all(is.finite(ihw_res$padj)),
          all(ihw_res$padj >= 0 & ihw_res$padj <= 1), ihw_res$attempts >= 1L,
          ihw_res$attempts <= 3L)
if (identical(ihw_res$method, "BH (IHW solver crashed; fallback)")) {
  stopifnot(isTRUE(all.equal(ihw_res$padj, bh_ref, tolerance = 0)))
}
write_result("input4_ihw_function", list(method = ihw_res$method,
  attempts = ihw_res$attempts, discoveries = sum(ihw_res$padj < 0.05), status = "PASS"))

# Input 5: the documented IHW CLI must preserve the full CSV shape and bounds.
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

writeLines("ALL_CORRECTIVE_DYNAMIC_INPUTS_PASS", file.path(out_dir, "summary.txt"))
