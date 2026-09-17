# Input 3 (Edge, regression): n=2/group boundary and near-impossible 1.05-fold @ 95% power target.
suppressPackageStartupMessages(library(RNASeqPower))

cat('power at n=2, 2-fold, cv=0.4, depth=20:', round(rnapower(depth=20, n=2, cv=0.4, effect=2, alpha=0.05), 4), '\n')

for (eff in c(1.01, 1.05, 1.1, 1.2, 1.5, 2, 4)) {
  n <- tryCatch(ceiling(rnapower(depth=20, cv=0.4, effect=eff, alpha=0.05, power=0.95)), error=function(e) NA)
  cat(sprintf('effect=%.2fx, target power=0.95 -> n=%s per group\n', eff, as.character(n)))
}
