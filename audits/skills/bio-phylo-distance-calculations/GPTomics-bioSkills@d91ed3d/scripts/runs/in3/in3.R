# Input 3 (Edge): saturation pre-flight. Data: SYNTHETIC sat12.fa (deep12 tree x4) and deep12.fa for contrast.
library(ape); library(phangorn)
slopes <- function(aln, lab) {
  L <- ncol(aln)
  d_jc  <- dist.dna(aln, model = 'JC69')
  ts_tv <- dist.dna(aln, model = 'TS')                      # Skill code
  ts <- as.numeric(ts_tv) / L; tv <- as.numeric(dist.dna(aln, model = 'TV')) / L
  tn <- as.numeric(dist.dna(aln, model = 'TN93')); p <- as.numeric(dist.dna(aln, model = 'raw'))
  o <- tn < median(tn, na.rm = TRUE)
  s <- function(y, i) unname(coef(lm(y[i] ~ tn[i]))[2])
  cat(sprintf('%s: L=%d  TS count range %d-%d  p range %.3f-%.3f  frac p>0.5 %.2f  JC69 range %.2f-%.2f  NaN JC %d\n',
              lab, L, min(ts_tv), max(ts_tv), min(p), max(p), mean(p > 0.5), min(d_jc, na.rm = TRUE),
              max(d_jc, na.rm = TRUE), sum(is.nan(d_jc))))
  cat(sprintf('   ts-vs-TN93 slope low half %.3f high half %.3f | tv slope low %.3f high %.3f | ts/tv mean %.2f\n',
              s(ts, o), s(ts, !o), s(tv, o), s(tv, !o), mean(ts / tv)))
  invisible(list(d_jc = d_jc, ts_tv = ts_tv, tn = tn, ts = ts, tv = tv))
}
sat <- read.dna('../../data/sat12.fa', format = 'fasta')
deep <- read.dna('../../data/deep12.fa', format = 'fasta')
rownames(sat) <- trimws(rownames(sat)); rownames(deep) <- trimws(rownames(deep))   # AliSim name padding
a <- slopes(sat, 'sat12 '); b <- slopes(deep, 'deep12')

png('skill_plot_sat12.png', 600, 500); plot(a$d_jc, a$ts_tv, main = 'Skill plot: TS counts vs JC69 (sat12)'); dev.off()
png('tstv_vs_tn93.png', 900, 450); par(mfrow = c(1, 2))
for (z in list(list(b, 'deep12'), list(a, 'sat12'))) {
  plot(z[[1]]$tn, z[[1]]$ts, col = 'blue', ylim = c(0, 0.45), xlab = 'TN93 distance', ylab = 'proportion', main = z[[2]])
  points(z[[1]]$tn, z[[1]]$tv, col = 'red'); legend('topleft', c('transitions', 'transversions'), col = c('blue', 'red'), pch = 1)
}
dev.off()

true <- read.tree('../../data/sat12_true.nwk')
rf <- function(t) RF.dist(unroot(t), unroot(true), normalize = FALSE)
cat('true patristic distance range (subs/site):', format(range(cophenetic(true)[upper.tri(cophenetic(true))]), digits = 3), '\n')
cat('RF (max 18): raw NJ', rf(nj(dist.dna(sat, 'raw'))), '| TN93 NJ', rf(nj(dist.dna(sat, 'TN93'))),
    '| TN93+G0.4 FastME', rf(fastme.bal(dist.dna(sat, 'TN93', gamma = 0.4))), '| TN93+G0.5 FastME',
    rf(fastme.bal(dist.dna(sat, 'TN93', gamma = 0.5))), '\n')
# third-codon / transversion-only fallback suggested by the Skill's fix line
cat('RF transversion-only (TV counts) NJ:', rf(nj(dist.dna(sat, 'TV'))), '\n')
set.seed(1)
tr <- fastme.bal(dist.dna(sat, 'TN93', gamma = 0.4))
bs <- boot.phylo(tr, sat, function(x) fastme.bal(dist.dna(x, 'TN93', gamma = 0.4)), B = 200, quiet = TRUE)
cat('TN93+G0.4 FastME bootstrap %:', round(100 * bs / 200), '\n')
cat('node in true tree:', prop.clades(unroot(tr), unroot(true), rooted = FALSE), '\n')
