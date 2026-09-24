# Exact-commit re-audit input 4: prior real ALL microarray input through the current split guard.
# Run with: r.sh reaudit_i4_real_all.R <example>
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1L)
suppressPackageStartupMessages({ library(Biobase); library(ALL) })
source(normalizePath(args[[1L]], mustWork = TRUE))

data(ALL)
e <- exprs(ALL)
pd <- pData(ALL)
keep <- !is.na(pd$BT)
e <- e[, keep, drop = FALSE]
pd <- pd[keep, , drop = FALSE]
lineage <- factor(substr(as.character(pd$BT), 1L, 1L), levels = c('B', 'T'))
stage <- sub('^[BT]', '', as.character(pd$BT))
stage[stage == ''] <- '0'
t_stats <- apply(e, 1L, function(value) abs(t.test(value ~ lineage)$statistic))
probe <- names(which.max(t_stats))
real <- data.frame(cluster = factor(stage), condition = ordered(lineage, levels = c('B', 'T')),
                   expression = as.numeric(e[probe, ]))
real <- real[real$cluster != '0', , drop = FALSE]
counts <- table(real$cluster, real$condition)
guarded <- prepare_split_violin_data(real, min_n = 30L)

# This old input has no stage with both B and T >=30. The current contract says omit it rather than
# drawing unstable/side-swapped half violins. The source function returns a valid empty frame.
stopifnot(nrow(guarded) == 0L, all(counts[, 'B'] < 30L | counts[, 'T'] < 30L))
cat('PASS i4: REAL ALL probe=', probe, '; stage-by-lineage counts=',
    paste(apply(counts, 1L, function(row) paste(row, collapse = '/')), collapse = ','),
    '; guarded split rows=0 (all ineligible cells safely omitted)\n', sep = '')
