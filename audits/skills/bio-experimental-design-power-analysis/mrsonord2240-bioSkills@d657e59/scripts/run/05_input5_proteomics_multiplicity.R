# Input 5 (Stress, regression - the fixed P1): DIA proteomics ~4000 proteins, multiplicity now handled.
suppressPackageStartupMessages(library(pwr))

n_proteins <- 4000
d <- 1.2
raw <- pwr.t.test(d = d, sig.level = 0.05, power = 0.80, type = 'two.sample')
corrected <- pwr.t.test(d = d, sig.level = 0.05 / n_proteins, power = 0.80, type = 'two.sample')
cat('Raw per-protein alpha=0.05: n =', ceiling(raw$n), 'per group\n')
cat('Bonferroni-corrected for', n_proteins, 'proteins: n =', ceiling(corrected$n), 'per group\n')
cat('Ratio (understatement factor):', round(corrected$n / raw$n, 2), 'x\n')

# Independent cross-check with a different d, to confirm the multiplicity ratio is not a fluke of d=1.2
for (dd in c(0.5, 0.8, 1.2, 2.0)) {
  r <- pwr.t.test(d = dd, sig.level = 0.05, power = 0.80, type = 'two.sample')
  c2 <- pwr.t.test(d = dd, sig.level = 0.05 / n_proteins, power = 0.80, type = 'two.sample')
  cat(sprintf('d=%.1f: raw n=%d, Bonferroni n=%d, ratio=%.2fx\n', dd, ceiling(r$n), ceiling(c2$n), c2$n/r$n))
}
