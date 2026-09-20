# source only the function definitions of the shipped example (skip its top-level side effects) by eval-ing its parsed exprs
exprs <- parse('example.R')
for (e in exprs) {
  if (is.call(e) && identical(e[[1]], as.name('<-')) && is.call(e[[3]]) && identical(e[[3]][[1]], as.name('function'))) eval(e, globalenv())
}
res <- load_leafcutter_results('differential_cluster_significance.txt', 'differential_effect_sizes.txt')
print(res)
stopifnot(nrow(res) == 3, all(res$p.adjust < 0.05))
stopifnot(abs(max(res$deltapsi) - 0.5446) < 0.01)
cat('ASSERT OK: example merge returns 3 introns, max deltapsi 0.545 (truth ~0.55)\n')
ann <- annotate_clusters(res, 'exons.txt')
print(ann[, c('intron','chr','start','end')])
