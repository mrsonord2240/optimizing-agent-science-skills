# Input 4 (Edge/boundary): "Run ZicoSeq with Batch as a covariate on my ASV table." Tests
# the TOOLS.md-documented trap: GUniFrac::ZicoSeq() refuses zero-variance features outright
# rather than dropping them like the other tools' prv_cut/min_prevalence filters do. The
# differential-abundance SKILL.md mentions ZicoSeq only briefly ("winsorizes, posterior-
# samples...returns permutation FDR") and does NOT warn about this trap or show the fix.
suppressMessages({
  library(phyloseq)
  library(GUniFrac)
})

ps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/phyloseq_object.rds')
truth <- read.delim('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/truth_da.tsv', stringsAsFactors = FALSE)
true_pos <- truth$ASV[truth$role != 'null']

# Step 1: follow the SKILL.md's own prevalence-filter code VERBATIM (prv_cut=0.10) - this is
# exactly the filter shown in the "Filter Before Testing" section, applied generically to
# "every tool" per that section's own claim.
keep <- filter_taxa(ps, function(x) sum(x > 0) >= 0.10 * nsamples(ps), TRUE)
otu <- as.matrix(otu_table(keep)); if (!taxa_are_rows(keep)) otu <- t(otu)
meta <- data.frame(as(sample_data(keep), 'data.frame'))

n_zerovar <- sum(apply(otu, 1, function(x) length(unique(x)) == 1))
cat('Zero-variance features remaining after SKILL.md prv_cut=0.10 filter:', n_zerovar, '\n')

cat('\n--- Attempt 1: ZicoSeq exactly as the SKILL.md-style filter leaves the data ---\n')
result1 <- tryCatch({
  ZicoSeq(meta.dat = meta, feature.dat = otu, grp.name = 'Group', adj.name = 'Batch',
          feature.dat.type = 'count', prev.filter = 0, perm.no = 99, return.feature.dat = TRUE)
}, error = function(e) { cat('ERROR:', conditionMessage(e), '\n'); NULL })
cat('Attempt 1 succeeded:', !is.null(result1), '\n')

cat('\n--- Attempt 2: explicit zero-variance removal (the undocumented required fix) ---\n')
keep2 <- apply(otu, 1, function(x) length(unique(x)) > 1)
otu2 <- otu[keep2, ]
cat('Dropped', sum(!keep2), 'zero-variance features; ', nrow(otu2), 'remain\n')
result2 <- tryCatch({
  ZicoSeq(meta.dat = meta, feature.dat = otu2, grp.name = 'Group', adj.name = 'Batch',
          feature.dat.type = 'count', prev.filter = 0, perm.no = 99, return.feature.dat = TRUE)
}, error = function(e) { cat('ERROR:', conditionMessage(e), '\n'); NULL })
cat('Attempt 2 succeeded:', !is.null(result2), '\n')

if (!is.null(result2)) {
  padj <- result2$p.adj.fdr
  sig <- names(padj)[padj < 0.05]
  cat('\nZicoSeq significant (p.adj.fdr<0.05), Batch-adjusted:', length(sig), '\n')
  tp <- sum(sig %in% true_pos); fp <- sum(!(sig %in% true_pos)); fn <- length(true_pos) - tp
  cat(sprintf('TP=%d/%d, FP=%d, FN=%d\n', tp, length(true_pos), fp, fn))
  cat('Recovered:', paste(sort(intersect(sig, true_pos)), collapse=', '), '\n')
  cat('Missed:', paste(sort(setdiff(true_pos, sig)), collapse=', '), '\n')
}
