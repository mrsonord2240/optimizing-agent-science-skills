.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Is the realized_fdr = 0.108 that examples/multiple_testing_correction.R prints for BH
# a property of its shipped seed, or does its simulation systematically violate FDR?
n_genes <- 10000; n_de <- 500
is_de <- c(rep(TRUE, n_de), rep(FALSE, n_genes - n_de))
f <- numeric(0); R <- numeric(0)
for (s in 1:300) {
  set.seed(s)
  p <- c(rbeta(n_de, 0.3, 5), runif(n_genes - n_de))
  sel <- p.adjust(p, 'BH') < 0.05
  R <- c(R, sum(sel)); f <- c(f, if (sum(sel)) sum(sel & !is_de)/sum(sel) else 0)
}
cat(sprintf('examples/ simulation, 300 seeds: mean realized FDP = %.4f (sd %.4f), mean R = %.1f\n',
            mean(f), sd(f), mean(R)))
cat(sprintf('fraction of seeds with realized FDP > 0.05 : %.3f\n', mean(f > 0.05)))
cat(sprintf('fraction of seeds with realized FDP > 0.10 : %.3f\n', mean(f > 0.10)))
set.seed(20260528)
p <- c(rbeta(n_de, 0.3, 5), runif(n_genes - n_de))
sel <- p.adjust(p, 'BH') < 0.05
cat(sprintf('SHIPPED seed 20260528: R = %d, realized FDP = %.4f  (percentile among seeds: %.3f)\n',
            sum(sel), sum(sel & !is_de)/sum(sel), mean(f <= sum(sel & !is_de)/sum(sel))))
