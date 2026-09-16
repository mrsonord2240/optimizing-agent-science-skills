# Re-audit 2026-09-15 helper: load SYNTHETIC data and run Skill blocks VERBATIM via source().
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(limma))
RR <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance'
BLK <- file.path(RR, 'rerun', 'blocks')

run_block <- function(name, env = globalenv()) {
  f <- list.files(BLK, pattern = paste0('^', name), full.names = TRUE)
  stopifnot(length(f) == 1)
  res <- tryCatch({ withCallingHandlers(sys.source(f, envir = env),
                     warning = function(w) { cat('  [warning in', basename(f), ']', conditionMessage(w), '\n'); invokeRestart('muffleWarning') }); 'OK' },
                  error = function(e) paste('ERROR:', conditionMessage(e)))
  cat(sprintf('[block %s] %s\n', basename(f), res))
  invisible(res)
}

load_maxquant_lfq <- function(path = file.path(RR, 'data', 'proteinGroups.txt')) {
  pg <- read.delim(path, quote = '', check.names = FALSE, stringsAsFactors = FALSE)
  keep <- pg$Reverse != '+' & pg$`Potential contaminant` != '+' & pg$`Only identified by site` != '+'
  keep[is.na(keep)] <- TRUE
  pg <- pg[keep, ]
  lfq <- as.matrix(pg[, grep('^LFQ intensity ', names(pg))])
  lfq[lfq == 0] <- NA
  m <- log2(lfq)
  colnames(m) <- sub('LFQ intensity ', '', colnames(m))
  rownames(m) <- sapply(strsplit(pg$`Protein IDs`, ';'), `[`, 1)
  list(matrix = m, peptides = setNames(pg$`Razor + unique peptides`, rownames(m)))
}

truth_eval <- function(ids, truth, label) {
  cls <- truth$class[match(ids, truth$protein)]
  n <- length(ids); fp <- sum(cls == 'null', na.rm = TRUE)
  cat(sprintf('%-48s called=%4d null(FP)=%3d realizedFDR=%5.1f%% up=%d down=%d onoff=%d\n', label, n, fp,
              ifelse(n > 0, 100 * fp / n, 0), sum(cls == 'up', na.rm = TRUE), sum(cls == 'down', na.rm = TRUE),
              sum(cls == 'on_off', na.rm = TRUE)))
}
