# NEW Input 10, part 4: the guard tests the OFFSET. The variance run showed the
# harm comes from per-run median normalization halving the null standard error,
# not from the offset itself. So: can a normalization shrink the SE while leaving
# the median log2FC at ~0, i.e. pass the guard and still be anticonservative?
#
# Construction: centre each run on its OWN CONDITION's median. That removes
# exactly the within-condition run-to-run variation that per-run median
# normalization removes, but introduces no between-condition offset at all.
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
truth <- read.csv(file.path(DD, 'truth_proteins.csv'), stringsAsFactors = FALSE)
isnull <- setNames(truth$class == 'null', truth$protein)

fit <- function(M) {
  pw <- wide; pw[, runs] <- M
  env <- new.env()
  assign('peptide_wide', pw, env); assign('sample_info', sample_info, env); assign('runs', runs, env)
  suppressMessages(suppressWarnings(sys.source(file.path(DW, 'blocks', 'msqrob2.R'), envir = env)))
  get('res', env)
}

L0 <- log2(as.matrix(wide[, runs]))
med <- apply(L0, 2, median, na.rm = TRUE)
Lwithin <- L0
for (g in c(FALSE, TRUE)) {
  idx <- which(trt == g)
  Lwithin[, idx] <- sweep(L0[, idx, drop = FALSE], 2, med[idx]) + median(med[idx])
}

CENTRING <- readLines(file.path(DW, 'blocks', 'centring.R'))
guard <- function(res) {
  tested <- data.frame(log2FC = res$logFC)
  env <- new.env(); assign('tested', tested, env)
  out <- tryCatch({eval(parse(text = paste(CENTRING, collapse = '\n')), envir = env); 'PASSES'},
                  error = function(e) paste('STOPS:', sub('.*median log2FC', 'median log2FC', conditionMessage(e))))
  out
}

for (nm in c('no normalization', 'center.median over all peptides',
             'within-CONDITION median centring')) {
  M <- switch(nm,
    'no normalization' = L0,
    'center.median over all peptides' = sweep(L0, 2, med) + median(med),
    'within-CONDITION median centring' = Lwithin)
  r <- fit(2 ^ M); r$null <- isnull[r$protein]
  n <- r[r$null %in% TRUE, ]
  sig <- r[!is.na(r$adjPval) & r$adjPval < 0.05, ]
  fp <- sum(sig$null, na.rm = TRUE)
  cat(sprintf('%-34s median logFC %+0.3f | null median se %.4f | calls %3d | FP %2d | FDR %5.1f%%\n',
              nm, median(r$logFC, na.rm = TRUE), median(n$se, na.rm = TRUE),
              nrow(sig), fp, 100 * fp / max(1, nrow(sig))))
  cat(sprintf('%34s centring guard -> %s\n', '', guard(r)))
}
