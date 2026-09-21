# Reference: metafor 4.4+ | Verify API if version differs

# PhD-level forest + funnel plot encoding the four correctness traps:
# (1) random-effects REML, (2) log-scale x-axis for ratios,
# (3) I²/tau²/prediction interval reported, (4) Egger only when k>=10.

library(metafor)

# 1. INPUT -- per-study effect + variance
# yi = log-effect (log-OR / log-HR); vi = variance of log-effect
studies <- data.frame(
    author = c('Smith 2010', 'Jones 2012', 'Lee 2014', 'Patel 2015', 'Garcia 2017', 'Khan 2019',
               'Brown 2020', 'Liu 2021', 'Davis 2022', 'Singh 2023'),
    yi = log(c(1.3, 1.5, 0.9, 1.2, 1.4, 1.1, 1.8, 1.6, 0.95, 1.25)),
    vi = c(0.05, 0.08, 0.12, 0.06, 0.07, 0.09, 0.04, 0.05, 0.10, 0.06))

# 2. RANDOM-EFFECTS REML meta-analysis
res <- rma(yi = yi, vi = vi, data = studies,
           slab = author, method = 'REML')

# 3. HETEROGENEITY -- report I², tau², Q-test
cat(sprintf('I-squared = %.1f%%; tau^2 = %.3f; Q = %.2f, p = %s\n',
            res$I2, res$tau2, res$QE, format.pval(res$QEp, digits = 3)))

# 4. FOREST -- log-scale x with meaningful tick labels
png('F:/OpenScience/audits/bio-data-visualization-forest-funnel-plots/figs/ex_forest.png', width=800, height=600, res=110)
forest(res,
       atransf = exp,                                         # display as OR (exponentiated)
       at = log(c(0.5, 1, 1.5, 2, 3)),                       # ticks at meaningful values
       refline = 0,                                          # log(1) for OR/HR/RR
       xlab = 'Odds Ratio (95% CI)',
       header = c('Study', 'OR [95% CI]'),
       mlab = bquote(paste('RE Model (', I^2, ' = ', .(round(res$I2, 1)), '%; ',
                            tau^2, ' = ', .(round(res$tau2, 3)), '; Q-p = ',
                            .(format.pval(res$QEp, digits = 2)), ')')),
       addpred = TRUE)                                       # 95% prediction interval
dev.off()

# 5. FUNNEL + Egger test (k >= 10 required for Egger)
png('F:/OpenScience/audits/bio-data-visualization-forest-funnel-plots/figs/ex_funnel.png', width=700, height=600, res=110)
funnel(res,
       level = c(90, 95, 99),                                 # contour-enhanced (Peters 2008)
       shade = c('white', 'gray55', 'gray75'),
       refline = 0,
       legend = TRUE,
       xlab = 'log(OR)')
dev.off()

if (nrow(studies) >= 10) {
    egger <- regtest(res, model = 'lm', predictor = 'sei')
    cat(sprintf('Egger test: p = %s\n', format.pval(egger$pval, digits = 3)))
}

# 6. TRIM-AND-FILL as SENSITIVITY (NOT primary)
res_tf <- trimfill(res)
cat(sprintf('Trim-and-fill imputed k = %d studies; adjusted OR = %.2f\n',
            res_tf$k - res$k, exp(res_tf$b[1])))

# 7. SUBGROUP META-ANALYSIS with interaction test
studies$subtype <- c('A', 'A', 'B', 'B', 'A', 'B', 'A', 'B', 'A', 'B')
res_sub <- rma(yi = yi, vi = vi, mods = ~ subtype - 1, data = studies, method = 'REML')
res_int <- rma(yi = yi, vi = vi, mods = ~ subtype, data = studies, method = 'REML')
cat(sprintf('Interaction p-value (subtype): %s\n',
            format.pval(res_int$pval[2], digits = 3)))

# --- audit additions ---
cat(sprintf("b=%.6f se=%.6f OR=%.4f\n", res$b, res$se, exp(res$b)))
eg <- regtest(res, model='lm', predictor='sei'); print(eg)
print(res_tf$b); print(res_tf$fill)
write.csv(studies[,c("author","yi","vi")], "F:/OpenScience/audits/bio-data-visualization-forest-funnel-plots/data/example_studies.csv", row.names=FALSE)
