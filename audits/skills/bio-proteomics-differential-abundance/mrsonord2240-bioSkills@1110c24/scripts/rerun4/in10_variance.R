# NEW Input 10, part 3. The per-protein log2FC shift is nearly uniform (sd 0.028),
# so heterogeneity is not the missing ingredient either. Second independent check:
# does per-run median normalization also SHRINK the within-condition residual,
# which is what would turn a -0.20 offset into a callable one?
suppressPackageStartupMessages({library(QFeatures); library(msqrob2); library(MsCoreUtils)})
DD <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
DW <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun4'

ann <- read.csv(file.path(DD, 'annotation_msstats.csv'), stringsAsFactors = FALSE)
ev <- read.table(file.path(DD, 'evidence.txt'), sep = '\t', header = TRUE, quote = '', comment.char = '')
ev <- ev[!(ev$Reverse %in% '+') & !(ev$Potential.contaminant %in% '+') &
           !is.na(ev$Intensity) & ev$Intensity > 0, ]
ev$feature <- paste(ev$Modified.sequence, ev$Charge, sep = '_')
runs <- as.character(ann$Raw.file); trt <- ann$Condition == 'Treatment'
agg <- aggregate(Intensity ~ feature + Raw.file + Leading.razor.protein, data = ev, FUN = sum)
wide <- reshape(agg, idvar = c('feature', 'Leading.razor.protein'), timevar = 'Raw.file', direction = 'wide')
colnames(wide) <- sub('Intensity.', '', colnames(wide), fixed = TRUE)
wide <- wide[, c('feature', 'Leading.razor.protein', runs)]; names(wide)[2] <- 'protein'
sample_info <- data.frame(run = runs, condition = ann$Condition, stringsAsFactors = FALSE)

fit <- function(M) {
  pw <- wide; pw[, runs] <- M
  env <- new.env()
  assign('peptide_wide', pw, env); assign('sample_info', sample_info, env); assign('runs', runs, env)
  suppressMessages(suppressWarnings(sys.source(file.path(DW, 'blocks', 'msqrob2.R'), envir = env)))
  get('res', env)
}

L0 <- log2(as.matrix(wide[, runs]))
med <- apply(L0, 2, median, na.rm = TRUE)
variants <- list(
  'no normalization'              = L0,
  'uniform -0.20 into Treatment'  = { A <- L0; A[, trt] <- A[, trt] - 0.20; A },
  'center.median over all peptides' = sweep(L0, 2, med) + median(med))

truth <- read.csv(file.path(DD, 'truth_proteins.csv'), stringsAsFactors = FALSE)
isnull <- setNames(truth$class == 'null', truth$protein)

for (nm in names(variants)) {
  r <- fit(2 ^ variants[[nm]])
  r$null <- isnull[r$protein]
  n <- r[r$null %in% TRUE, ]
  sig <- r[!is.na(r$adjPval) & r$adjPval < 0.05, ]
  cat(sprintf('%-32s median logFC %+0.3f | NULL proteins: median se %.4f, sd(logFC) %.4f, median |t| %.2f | calls %3d FP %2d\n',
              nm, median(r$logFC, na.rm = TRUE), median(n$se, na.rm = TRUE),
              sd(n$logFC, na.rm = TRUE), median(abs(n$t), na.rm = TRUE),
              nrow(sig), sum(sig$null, na.rm = TRUE)))
}

cat('\nwithin-condition spread of the per-run median shifts that center.median removes:\n')
s <- med - median(med)
cat('  Control  ', paste(sprintf('%+.3f', s[!trt]), collapse = ' '), ' sd', sprintf('%.3f', sd(s[!trt])), '\n')
cat('  Treatment', paste(sprintf('%+.3f', s[trt]), collapse = ' '), ' sd', sprintf('%.3f', sd(s[trt])), '\n')
