.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 3 (Edge) -- 40 GO terms, nothing truly enriched (SYNTHETIC, planted truth).
# Follows SKILL.md "FDR -- Benjamini-Hochberg and the q-value" verbatim, then asks
# whether the skill's guidance survives a small family with pi0 = 1.

d <- read.csv('F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/synthetic_go_all_null.csv')
p <- d$pvalue
cat(sprintf('SYNTHETIC: %d terms, %d truly enriched (true pi0 = 1.000)\n',
            length(p), sum(d$is_truly_enriched)))
cat('min p =', signif(min(p), 3), ' max p =', signif(max(p), 3), '\n')

padj <- p.adjust(p, method = 'BH')
cat(sprintf('BH discoveries at FDR 0.05 : %d\n', sum(padj < 0.05)))
cat(sprintf('Bonferroni discoveries     : %d\n', sum(p.adjust(p, "bonferroni") < 0.05)))

cat('\n--- SKILL.md q-value pattern, applied as written: qvalue(pvalues) ---\n')
library(qvalue)
res <- try(qvalue(p), silent = TRUE)
if (inherits(res, 'try-error')) {
  cat('qvalue() FAILED. Error text:\n')
  cat(as.character(res))
} else {
  cat(sprintf('pi0 = %.4f ; discoveries q<0.05 = %d\n', res$pi0, sum(res$qvalues < 0.05)))
}

cat('\n--- documented workaround (NOT mentioned anywhere in SKILL.md/usage-guide) ---\n')
res2 <- try(qvalue(p, pi0.method = 'bootstrap'), silent = TRUE)
if (inherits(res2, 'try-error')) cat('bootstrap also FAILED:\n', as.character(res2)) else
  cat(sprintf('pi0.method="bootstrap": pi0 = %.4f ; q<0.05 = %d\n', res2$pi0, sum(res2$qvalues < 0.05)))
res3 <- try(qvalue(p, lambda = 0), silent = TRUE)
if (inherits(res3, 'try-error')) cat('lambda=0 also FAILED:\n', as.character(res3)) else
  cat(sprintf('lambda=0 (pi0 forced to 1): pi0 = %.4f ; q<0.05 = %d\n', res3$pi0, sum(res3$qvalues < 0.05)))

cat('\n--- how small can the family get before qvalue() breaks? ---\n')
set.seed(7)
for (m in c(20, 40, 60, 100, 200, 500, 1000)) {
  pv <- runif(m)
  r <- try(qvalue(pv), silent = TRUE)
  cat(sprintf('m=%4d  qvalue(): %s\n', m,
      if (inherits(r, 'try-error')) 'ERROR' else sprintf('pi0=%.3f OK', r$pi0)))
}
