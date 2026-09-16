
# RE-AUDIT new Input C: three-condition dose design (Control/LowDose/HighDose, n=4, 2 batches).
# Step 1: run the Skill's Complete R Workflow block VERBATIM and see what it does with >2 conditions.
# Step 2: the minimal adaptation a researcher following the Skill would have to make, and whether the
#         Skill tells them to make it. SYNTHETIC data (rerun/make_3cond.py).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(limma))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'rerun', 'workC'))
blk <- list.files(file.path(PP, 'rerun', 'blocks'), pattern = '^b01', full.names = TRUE)
e <- new.env(parent = globalenv())
r <- tryCatch({ suppressWarnings(sys.source(blk, envir = e)); 'OK' }, error = function(z) paste('ERROR:', conditionMessage(z)))
cat('[Complete R Workflow block VERBATIM on a 3-condition design]', r, '\n')
if (exists('design', envir = e)) cat('design columns built:', paste(colnames(get('design', envir = e)), collapse = ' '), '\n')
if (exists('results', envir = e)) { rs <- get('results', envir = e)
  cat('results rows:', nrow(rs), '| significant:', sum(rs$significant), '\n') }

# --- adapted path: what the block would need to become ---
cat('\n--- minimal adaptation (three-level factor, two contrasts) ---\n')
prot <- read.delim('proteinGroups.txt', stringsAsFactors = FALSE, quote = '', comment.char = '')
prot <- prot[!(prot$Potential.contaminant %in% '+') & !(prot$Reverse %in% '+') & !(prot$Only.identified.by.site %in% '+'), ]
lfq <- grep('^LFQ.intensity.', colnames(prot), value = TRUE)
X <- prot[, lfq]; rownames(X) <- prot$Majority.protein.IDs
colnames(X) <- gsub('^LFQ.intensity.', '', colnames(X))
X[X == 0] <- NA; L <- log2(X)
L <- sweep(L, 2, apply(L, 2, median, na.rm = TRUE) - median(apply(L, 2, median, na.rm = TRUE)))
si <- read.csv('sample_annotation.csv'); si <- si[match(colnames(L), si$sample), ]
si$condition <- factor(si$condition, levels = c('Ctl','Low','High'))
gc2 <- sapply(levels(si$condition), function(g) rowSums(!is.na(L[, si$sample[si$condition == g], drop = FALSE])) >= ceiling(4 * 0.6))
F2 <- L[rowSums(gc2) > 0, ]
cat('proteins after per-group completeness filter:', nrow(F2), '\n')
d <- model.matrix(~ 0 + condition + factor(batch), data = si)
colnames(d)[1:3] <- levels(si$condition); colnames(d) <- make.names(colnames(d))
fit <- lmFit(as.matrix(F2), d)
cm <- makeContrasts(Low_vs_Ctl = Low - Ctl, High_vs_Ctl = High - Ctl, levels = d)
f2 <- treat(contrasts.fit(fit, cm), lfc = log2(1.5), trend = TRUE, robust = TRUE)
truth <- read.csv('truth.csv')
for (k in colnames(cm)) {
  tt <- topTreat(f2, coef = k, number = Inf)
  s <- rownames(tt)[!is.na(tt$adj.P.Val) & tt$adj.P.Val < 0.05]
  cl <- truth$class[match(s, truth$protein)]
  allcl <- truth$class[match(rownames(tt), truth$protein)]
  cat(sprintf('%-12s called %3d | FALSE POS (null) %3d | dose_up %2d | dose_down %2d | high_only %2d | nulls tested %d\n',
      k, length(s), sum(cl == 'null', na.rm = TRUE), sum(cl == 'dose_up', na.rm = TRUE),
      sum(cl == 'dose_down', na.rm = TRUE), sum(cl == 'high_only', na.rm = TRUE), sum(allcl == 'null', na.rm = TRUE)))
}
cat('multiple-contrast adjustment across the 2 contrasts: topTreat adjusts WITHIN a contrast only;',
    'the Skill says nothing about adjusting across contrasts\n')
cat('\nDoes SKILL.md mention >2 conditions / multi-contrast / ANOVA anywhere?\n')
sk <- readLines(file.path('F:/OpenScience/external/mrsonord2240__bioSkills/workflows/proteomics-pipeline','SKILL.md'))
for (k in c('three condition','multi-contrast','more than two','ANOVA','decideTests','several contrasts','time course','dose')) {
  cat(sprintf('  %-18s hits: %d\n', k, length(grep(k, sk, ignore.case = TRUE))))
}
