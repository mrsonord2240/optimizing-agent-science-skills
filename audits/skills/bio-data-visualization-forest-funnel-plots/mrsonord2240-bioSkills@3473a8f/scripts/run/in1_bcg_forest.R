# Input 1: SKILL.md "metafor::rma + forest" block, run on REAL data (metafor::dat.bcg, Colditz 1994; 13 trials, binary outcome)
suppressMessages(library(metafor))
out <- "F:/OpenScience/audits/bio-data-visualization-forest-funnel-plots/figs"
dat <- dat.bcg
es <- escalc(measure = "OR", ai = tpos, bi = tneg, ci = cpos, di = cneg, data = dat)
studies <- data.frame(author = dat$author, year = dat$year, log_or = es$yi, log_or_se = sqrt(es$vi))
write.csv(studies, "F:/OpenScience/audits/bio-data-visualization-forest-funnel-plots/data/bcg_logor.csv", row.names = FALSE)

# ---- SKILL.md block, verbatim (only png() wrapper added) ----
png(file.path(out, "in1_forest_skillmd.png"), width = 1100, height = 700, res = 110)
res <- rma(yi = log_or, vi = log_or_se^2,
           data = studies, slab = paste(author, year),
           method = 'REML')
print(summary(res))
forest(res,
       atransf = exp,
       at = log(c(0.25, 0.5, 1, 2, 4)),
       refline = 0,
       xlab = 'Odds Ratio (95% CI)',
       header = c('Study', 'OR [95% CI]'),
       mlab = bquote(paste('RE Model (Q = ', .(round(res$QE, 2)),
                            ', df = ', .(res$k - 1),
                            ', p = ', .(format.pval(res$QEp, digits = 2)),
                            '; ', I^2, ' = ', .(round(res$I2, 1)), '%)')),
       addpred = TRUE)
dev.off()
# ---- end verbatim ----
cat(sprintf("\nFIT: b=%.6f se=%.6f ci=[%.6f,%.6f] OR=%.4f [%.4f, %.4f] tau2=%.6f I2=%.3f Q=%.4f Qp=%.3g\n",
  res$b, res$se, res$ci.lb, res$ci.ub, exp(res$b), exp(res$ci.lb), exp(res$ci.ub), res$tau2, res$I2, res$QE, res$QEp))
pr <- predict(res)
cat(sprintf("PRED: pi=[%.4f,%.4f] -> OR PI [%.4f, %.4f]\n", pr$pi.lb, pr$pi.ub, exp(pr$pi.lb), exp(pr$pi.ub)))
cat("per-study OR (first 13):\n"); print(round(exp(studies$log_or),4))
write.csv(data.frame(b=res$b, se=res$se, lb=res$ci.lb, ub=res$ci.ub, tau2=res$tau2, I2=res$I2, Q=res$QE, pi_lb=pr$pi.lb, pi_ub=pr$pi.ub),
          file.path(out, "in1_metafor_fit.csv"), row.names = FALSE)

# The Skill's "Fixed-effect vs RE" claim + weights: box size auto-encodes weight -> check weights() sums to 100
cat("weights sum:", sum(weights(res)), "\n")
# Linear-scale pitfall claim: run same forest WITHOUT atransf/at to see the log-scale default is still on log scale internally
png(file.path(out, "in1_forest_fixed.png"), width = 1100, height = 700, res = 110)
resFE <- rma(yi = log_or, vi = log_or_se^2, data = studies, slab = paste(author, year), method = 'FE')
forest(resFE, atransf = exp, at = log(c(0.25,0.5,1,2,4)), refline = 0, xlab = 'Odds Ratio (95% CI)')
dev.off()
cat(sprintf("FE: b=%.6f OR=%.4f [%.4f,%.4f]\n", resFE$b, exp(resFE$b), exp(resFE$ci.lb), exp(resFE$ci.ub)))
