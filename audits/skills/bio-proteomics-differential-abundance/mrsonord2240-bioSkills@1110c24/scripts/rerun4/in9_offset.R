# Input 9 regression + NEW Input 10: reproduce or refute the pass-4 root-cause
# claim for the 21.2% realized FDR, then test it harder than the fixer did.
#
# Claim under test (fixes log, pass 4): the 21.2% came from a global -0.18 log2
# offset introduced by per-run median normalization of the PEPTIDE table, and
# realized FDR tracks the offset monotonically (0.0 / 7.0 / 21.2 / 28.6 %) while
# the true-hit count never moves.
#
# The four SKILL.md blocks (msqrob2, msqrobAggregate, MSstats, centring check)
# are sourced VERBATIM from rerun4/blocks/.
suppressPackageStartupMessages({
  library(QFeatures); library(msqrob2); library(MSstats); library(MsCoreUtils)
})
DD <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
DW <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun4'
cat('msqrob2', as.character(packageVersion('msqrob2')),
    '| QFeatures', as.character(packageVersion('QFeatures')),
    '| MSstats', as.character(packageVersion('MSstats')), '\n')

truth <- read.csv(file.path(DD, 'truth_proteins.csv'), stringsAsFactors = FALSE)
is_null_protein <- setNames(truth$class == 'null', truth$protein)
cat('truth: null', sum(truth$class == 'null'), '| changed', sum(truth$class != 'null'), '\n')

ann <- read.csv(file.path(DD, 'annotation_msstats.csv'), stringsAsFactors = FALSE)
ev <- read.table(file.path(DD, 'evidence.txt'), sep = '\t', header = TRUE,
                 quote = '', comment.char = '')
ev <- ev[!(ev$Reverse %in% '+') & !(ev$Potential.contaminant %in% '+') &
           !is.na(ev$Intensity) & ev$Intensity > 0, ]
ev$feature <- paste(ev$Modified.sequence, ev$Charge, sep = '_')
runs <- as.character(ann$Raw.file)
agg <- aggregate(Intensity ~ feature + Raw.file + Leading.razor.protein, data = ev, FUN = sum)
wide <- reshape(agg, idvar = c('feature', 'Leading.razor.protein'),
                timevar = 'Raw.file', direction = 'wide')
colnames(wide) <- sub('Intensity.', '', colnames(wide), fixed = TRUE)
wide <- wide[, c('feature', 'Leading.razor.protein', runs)]
names(wide)[2] <- 'protein'
sample_info <- data.frame(run = runs, condition = ann$Condition, stringsAsFactors = FALSE)
cat('peptide_wide:', nrow(wide), 'precursors x', length(runs), 'runs |',
    length(unique(wide$protein)), 'proteins\n')

BLK <- readLines(file.path(DW, 'blocks', 'msqrob2.R'))

# ---- msqrob2 route with a chosen peptide-level normalization -----------------
run_msqrob <- function(norm = c('none', 'all', 'complete', 'offset'), offset_log2 = 0) {
  norm <- match.arg(norm)
  peptide_wide <- wide
  M <- as.matrix(peptide_wide[, runs])
  trt <- sample_info$condition == 'Treatment'
  if (norm == 'all') {                 # per-run median over EVERY peptide detected in that run
    L <- log2(M); L <- sweep(L, 2, apply(L, 2, median, na.rm = TRUE)) +
      median(apply(L, 2, median, na.rm = TRUE)); M <- 2 ^ L
  } else if (norm == 'complete') {     # per-run median over COMPLETE-CASE peptides only
    L <- log2(M); cc <- stats::complete.cases(L)
    med <- apply(L[cc, , drop = FALSE], 2, median, na.rm = TRUE)
    L <- sweep(L, 2, med) + median(med); M <- 2 ^ L
  } else if (norm == 'offset') {       # inject a KNOWN global offset into the treatment runs
    L <- log2(M); L[, trt] <- L[, trt] + offset_log2; M <- 2 ^ L
  }
  peptide_wide[, runs] <- M
  env <- new.env()
  assign('peptide_wide', peptide_wide, env); assign('sample_info', sample_info, env)
  assign('runs', runs, env)
  suppressMessages(suppressWarnings(sys.source(file.path(DW, 'blocks', 'msqrob2.R'), envir = env)))
  res <- get('res', env)
  res$null <- is_null_protein[res$protein]
  sig <- res[!is.na(res$adjPval) & res$adjPval < 0.05, ]
  fp <- sum(sig$null, na.rm = TRUE)
  list(offset = median(res$logFC, na.rm = TRUE), tested = nrow(res), calls = nrow(sig),
       fp = fp, fdr = if (nrow(sig)) fp / nrow(sig) else NA_real_,
       true_up = sum(!sig$null & sig$logFC > 0, na.rm = TRUE),
       true_dn = sum(!sig$null & sig$logFC < 0, na.rm = TRUE),
       untestable = length(get('untestable', env)),
       undetected = length(get('undetected', env)))
}

show <- function(tag, r) cat(sprintf(
  '%-46s offset %+0.3f | tested %3d | calls %3d | FP %2d | realized FDR %5.1f%% | true up/dn %2d/%2d\n',
  tag, r$offset, r$tested, r$calls, r$fp, 100 * r$fdr, r$true_up, r$true_dn))

cat('\n=== msqrob2, block verbatim, three normalizations ===\n')
r_none <- run_msqrob('none');      show('no normalization (the shipped block)', r_none)
cat(sprintf('%50s undetected %d | untestable %d\n', '', r_none$undetected, r_none$untestable))
r_cc   <- run_msqrob('complete');  show('center.median over complete-case peptides', r_cc)
r_all  <- run_msqrob('all');       show('center.median over ALL detected peptides', r_all)

cat('\n=== NEW: sweep a KNOWN offset, everything else held fixed ===\n')
for (d in c(-0.40, -0.30, -0.20, -0.10, -0.05, 0.00, 0.05, 0.10, 0.20, 0.30)) {
  show(sprintf('injected offset %+0.2f log2 into Treatment', d), run_msqrob('offset', d))
}
