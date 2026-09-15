# Input 4 (Variant B): compositional heterogeneity. Data: SYNTHETIC comp8.fa (branch-specific GC-rich/AT-rich models).
library(ape); library(phangorn)
aln  <- read.dna('../../data/comp8.fa', format = 'fasta')
rownames(aln) <- trimws(rownames(aln))   # AliSim pads FASTA names; read.dna keeps the padding
true <- read.tree('../../data/comp8_true.nwk')
bf <- t(sapply(rownames(aln), function(n) base.freq(aln[n, ])))
cat('GC per taxon:', paste(sprintf('%s=%.2f', rownames(bf), bf[, 'c'] + bf[, 'g']), collapse = ' '), '\n')
rf <- function(t) RF.dist(unroot(t), unroot(true), normalize = FALSE)
gc_split <- function(t) {           # does any split put all four GC taxa alone on one side?
  pp <- prop.part(unroot(t)); lab <- attr(pp, 'labels')
  any(sapply(pp, function(s) { x <- sort(lab[s]); setequal(x, c('GC1', 'GC2', 'GC3', 'GC4')) ||
    setequal(setdiff(lab, x), c('GC1', 'GC2', 'GC3', 'GC4')) }))
}
out <- NULL
for (m in c('raw', 'JC69', 'K80', 'TN93', 'logdet', 'paralin')) {
  d <- dist.dna(aln, model = m)
  nnan <- sum(is.nan(d))
  for (alg in c('nj', 'fastme')) {
    # nj()/fastme.bal() refuse NaN ('missing values are not allowed'); record it, fall back to njs() for NJ
    t <- tryCatch(if (alg == 'nj') nj(d) else fastme.bal(d, nni = TRUE, spr = TRUE), error = function(e) NULL)
    if (is.null(t) && alg == 'nj') { t <- tryCatch(njs(d), error = function(e) NULL); alg <- 'njs (NaN fallback)' }
    out <- rbind(out, data.frame(model = m, algorithm = alg, RF = if (is.null(t)) NA else rf(t),
                                 GC_taxa_grouped = if (is.null(t)) NA else gc_split(t), NaN_in_d = nnan))
  }
}
cat('max RF =', 2 * (Ntip(true) - 3), '\n'); print(out)
for (m in c('JC69', 'K80', 'TN93')) { dm <- as.matrix(dist.dna(aln, m)); w <- which(is.nan(dm), arr.ind = TRUE)
  if (nrow(w)) cat(m, 'NaN pairs:', paste(unique(apply(w, 1, function(r) paste(sort(rownames(dm)[r]), collapse = '-'))), collapse = ' '), '\n') }
p <- as.matrix(dist.dna(aln, 'raw')); cat('p for GC1-AT1', round(p['GC1', 'AT1'], 3), ' GC1-GC2', round(p['GC1', 'GC2'], 3), '\n')
t_tn <- njs(dist.dna(aln, 'TN93')); t_ld <- nj(dist.dna(aln, 'logdet'))
cat('TN93 NJ :', write.tree(t_tn), '\n'); cat('LogDet NJ:', write.tree(t_ld), '\n')
set.seed(20260915)
b_tn <- boot.phylo(t_tn, aln, function(x) njs(dist.dna(x, 'TN93')), B = 200, quiet = TRUE)
b_ld <- boot.phylo(t_ld, aln, function(x) nj(dist.dna(x, 'logdet')), B = 200, quiet = TRUE)
cat('TN93 NJ bootstrap %:', round(100 * b_tn / 200), ' | node in true tree:', prop.clades(unroot(t_tn), unroot(true), rooted = FALSE), '\n')
cat('LogDet NJ bootstrap %:', round(100 * b_ld / 200), ' | node in true tree:', prop.clades(unroot(t_ld), unroot(true), rooted = FALSE), '\n')
# short-sequence LogDet edge case the Skill mentions
sub <- aln[, 1:150]
dsub <- dist.dna(sub, 'logdet')
cat('LogDet on first 150 sites: NaN count', sum(is.nan(dsub)), '| nj():',
    tryCatch({ rf(nj(dsub)); 'ran' }, error = function(e) conditionMessage(e)),
    '| njs() RF', tryCatch(rf(njs(dsub)), error = function(e) conditionMessage(e)), '\n')
