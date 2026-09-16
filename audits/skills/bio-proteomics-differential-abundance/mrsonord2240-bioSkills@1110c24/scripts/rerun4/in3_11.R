# Input 3 regression (proDA on/off proteins) and NEW Input 11: the Skill says
# ridge = TRUE is "for three or more groups". Does it actually work there, and
# does the decision-tree guidance survive a three-arm design?
suppressPackageStartupMessages({library(proDA); library(QFeatures); library(msqrob2); library(MsCoreUtils)})
DD <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
DW <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun4'

cat('=== Input 3 (regression): proDA on the 4v4 set, on/off proteins ===\n')
pg <- read.table(file.path(DD, 'proteinGroups.txt'), sep = '\t', header = TRUE, quote = '', comment.char = '')
si <- read.csv(file.path(DD, 'sample_annotation.csv'), stringsAsFactors = FALSE)
truth <- read.csv(file.path(DD, 'truth_proteins.csv'), stringsAsFactors = FALSE)
icols <- grep('^LFQ.intensity', colnames(pg), value = TRUE)
M <- as.matrix(pg[, icols]); rownames(M) <- pg$Majority.protein.IDs
colnames(M) <- sub('^LFQ\\.intensity\\.', '', icols)
M[M == 0] <- NA; M <- log2(M)
M <- sweep(M, 2, apply(M, 2, median, na.rm = TRUE)) + median(apply(M, 2, median, na.rm = TRUE))
si <- si[match(colnames(M), si[[1]]), ]
sample_info <- data.frame(condition = si$condition, batch = factor(si$batch))
protein_matrix <- M
env <- new.env()
assign('protein_matrix', protein_matrix, env); assign('sample_info', sample_info, env)
suppressMessages(suppressWarnings(
  eval(parse(text = paste(readLines(file.path(DW, 'blocks', 'proda.R')), collapse = '\n')), envir = env)))
pr <- get('results', env)
pr$class <- truth$class[match(pr$name, truth$protein)]
sig <- pr[!is.na(pr$adj_pval) & pr$adj_pval < 0.05, ]
cat(sprintf('proDA: tested %d | calls %d | FP %d | realized FDR %.1f%%\n',
            nrow(pr), nrow(sig), sum(sig$class == 'null', na.rm = TRUE),
            100 * sum(sig$class == 'null', na.rm = TRUE) / max(1, nrow(sig))))
# on/off proteins: absent from one whole condition
cond <- sample_info$condition
onoff <- rownames(M)[apply(sapply(unique(cond), function(g)
  rowSums(!is.na(M[, cond == g, drop = FALSE]))), 1, min) == 0]
cat('on/off proteins (0 values in one condition):', length(onoff),
    '| called by proDA:', sum(onoff %in% sig$name), '\n')
cat('  -> the Skill says not to report proDA `diff` for these; the count is the',
    'basis of the standing "proDA oversold for on/off at n=4" note\n')

cat('\n=== NEW Input 11: three-arm design, ridge = TRUE as the Skill prescribes ===\n')
ta <- read.csv(file.path(DD, 'three_arm_log2.csv'), row.names = 1, check.names = FALSE)
ts <- read.csv(file.path(DD, 'three_arm_samples.csv'), stringsAsFactors = FALSE)
tt <- read.csv(file.path(DD, 'three_arm_truth.csv'), stringsAsFactors = FALSE)
ts <- ts[match(colnames(ta), ts[[1]]), ]
cat('three-arm matrix:', dim(ta), '| groups:',
    paste(names(table(ts[[2]])), table(ts[[2]]), collapse = ', '), '\n')

# build a peptide-like QFeatures from the protein matrix: 1 feature per protein,
# enough to exercise the ridge path the Skill prescribes for >= 3 groups
pw <- data.frame(feature = rownames(ta), protein = rownames(ta), 2 ^ ta, check.names = FALSE)
runs <- colnames(ta)
cd <- data.frame(quantCols = runs, condition = factor(ts[[2]]), sample = factor(runs), row.names = runs)
pe <- readQFeatures(assayData = pw, quantCols = runs, colData = cd, name = 'peptideRaw')
pe <- zeroIsNA(pe, 'peptideRaw')
pe <- logTransform(pe, base = 2, i = 'peptideRaw', name = 'peptideLog')
pe <- suppressMessages(aggregateFeatures(pe, i = 'peptideLog', fcol = 'protein', name = 'protein',
                                         fun = MsCoreUtils::robustSummary, na.rm = TRUE))
lv <- levels(cd$condition)
cat('condition levels:', paste(lv, collapse = ', '), '\n')
r <- tryCatch({
  pe2 <- suppressMessages(suppressWarnings(msqrob(pe, i = 'protein', formula = ~condition,
                                                  robust = TRUE, ridge = TRUE)))
  'ridge = TRUE ACCEPTED on a three-group mean model'
}, error = function(e) paste('ridge = TRUE ERROR:', conditionMessage(e)))
cat(' ', r, '\n')
r2 <- tryCatch({
  pe3 <- suppressMessages(suppressWarnings(msqrob(pe, i = 'protein', formula = ~condition, robust = TRUE)))
  L <- makeContrast(sprintf('ridgecondition%s = 0', lv[2]), parameterNames = sprintf('ridgecondition%s', lv[2]))
  'ridge = FALSE accepted'
}, error = function(e) paste('ridge = FALSE ERROR:', conditionMessage(e)))
cat(' ', r2, '\n')
cat('  the Skill also offers `~ -1 + condition` as the escape; testing it:\n')
r3 <- tryCatch({
  suppressMessages(suppressWarnings(msqrob(pe, i = 'protein', formula = ~ -1 + condition,
                                           robust = TRUE, ridge = TRUE)))
  '  ~ -1 + condition with ridge = TRUE ACCEPTED'
}, error = function(e) paste('  ~ -1 + condition with ridge = TRUE ERROR:', conditionMessage(e)))
cat(r3, '\n')
