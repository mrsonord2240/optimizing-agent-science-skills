.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 4 (Variant B) -- "I have mean expression for every gene. Use IHW to weight
# hypotheses and compare discoveries against plain BH."
# Code follows SKILL.md "Covariate-Weighted FDR -- IHW" VERBATIM (formula interface),
# then also the positional call used in examples/multiple_testing_correction.R.
suppressMessages({library(IHW)})
de_table <- read.csv('F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/synthetic_de_pvalues.csv')
names(de_table)[names(de_table) == 'pvalue'] <- 'pvalue'
truth <- de_table$is_truly_de == 1
cat(sprintf('SYNTHETIC: %d genes, %d true alternatives. IHW %s\n',
            nrow(de_table), sum(truth), as.character(packageVersion('IHW'))))

# --- is the covariate legitimate? (SKILL.md: "must be independent of the p-value
#     under the null" AND informative) -------------------------------------------
strata <- cut(de_table$mean_expression, quantile(de_table$mean_expression, 0:5/5),
              include.lowest = TRUE, labels = paste0('Q', 1:5))
cat('\nNull-only p-value behaviour by covariate stratum (should be ~0.05 everywhere):\n')
print(round(tapply(de_table$pvalue[!truth] < 0.05, strata[!truth], mean), 4))
cat('Power by covariate stratum (should VARY if the covariate is informative):\n')
print(round(tapply(de_table$pvalue[truth] < 0.05, strata[truth], mean), 4))
cat('KS test of null p-values vs Uniform(0,1): p =',
    signif(ks.test(de_table$pvalue[!truth], 'punif')$p.value, 3), '\n')

# --- SKILL.md snippet, verbatim -------------------------------------------------
res <- ihw(pvalue ~ mean_expression, data = de_table, alpha = 0.05)
de_table$padj_ihw <- adj_pvalues(res)
cat('\nSKILL.md formula interface ihw(pvalue ~ mean_expression, data=, alpha=): OK\n')
cat('rejections(res) =', rejections(res), '\n')

# --- examples/multiple_testing_correction.R positional call ---------------------
res2 <- ihw(de_table$pvalue, de_table$mean_expression, alpha = 0.05)
cat('examples/ positional interface ihw(p, covariate, alpha=): OK, rejections =',
    rejections(res2), '\n')

bh <- p.adjust(de_table$pvalue, 'BH')
score <- function(sel, label) {
  R <- sum(sel); V <- sum(sel & !truth); S <- sum(sel & truth)
  cat(sprintf('%-26s R=%5d  true+=%5d  false+=%4d  realized FDP=%.4f  power=%.4f\n',
              label, R, S, V, ifelse(R > 0, V / R, 0), S / sum(truth)))
}
cat('\n-- against planted truth --\n')
score(bh < 0.05, 'BH')
score(de_table$padj_ihw < 0.05, 'IHW (mean expression)')
cat(sprintf('IHW / BH discovery ratio: %.3f\n',
            sum(de_table$padj_ihw < 0.05) / sum(bh < 0.05)))

# --- what the SHIPPED EXAMPLE actually demonstrates: a covariate drawn at random,
#     i.e. independent of the null p-value but also carrying NO information --------
set.seed(20260528)
uninformative <- rgamma(nrow(de_table), shape = 2, rate = 0.5)   # examples/ line 45
res3 <- ihw(de_table$pvalue, uninformative, alpha = 0.05)
score(adj_pvalues(res3) < 0.05, 'IHW (examples/ covariate)')
cat(sprintf('examples/ IHW vs BH: %d vs %d rejections -> power gain = %+d\n',
            rejections(res3), sum(bh < 0.05), rejections(res3) - sum(bh < 0.05)))
