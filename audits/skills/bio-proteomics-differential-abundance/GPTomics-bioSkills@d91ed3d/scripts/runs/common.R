.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Shared helpers for the audit runs (audit scaffolding, not Skill code).
DATA <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data'

read_pg <- function(file = file.path(DATA, 'proteinGroups.txt')) {
  pg <- read.delim(file, check.names = FALSE, quote = '', stringsAsFactors = FALSE)
  keep <- pg$Reverse != '+' & pg$`Potential contaminant` != '+' & pg$`Only identified by site` != '+'
  pg <- pg[keep, ]
  pg$acc <- sub(';.*', '', pg$`Protein IDs`)
  pg
}

lfq_log2 <- function(pg, samples) {
  m <- as.matrix(pg[, paste('LFQ intensity', samples)])
  m[m == 0] <- NA
  m <- log2(m)
  colnames(m) <- samples
  rownames(m) <- pg$acc
  m
}

truth <- read.csv(file.path(DATA, 'truth_proteins.csv'), stringsAsFactors = FALSE)
rownames(truth) <- truth$protein

# score a set of called proteins against truth
score_calls <- function(called, tested, label) {
  cl <- truth[called, 'class']
  n <- length(called)
  fp <- sum(cl == 'null')
  tp_up <- sum(cl == 'up'); tp_down <- sum(cl == 'down'); tp_oo <- sum(cl == 'on_off')
  tst <- truth[tested, 'class']
  cat(sprintf('%-44s tested=%4d called=%4d  null(FP)=%3d  realizedFDR=%5.1f%%  up=%2d/%2d down=%2d/%2d onoff=%2d/%2d\n',
              label, length(tested), n, fp, ifelse(n > 0, 100 * fp / n, 0),
              tp_up, sum(tst == 'up'), tp_down, sum(tst == 'down'), tp_oo, sum(tst == 'on_off')))
  invisible(c(called = n, fp = fp))
}
