# Input 3 (Edge): k=3 small-k regime. SYNTHETIC 3 trials with planted heterogeneity (ORs 0.55, 0.90, 1.60).
suppressMessages(library(metafor))
D <- "F:/OpenScience/audits/bio-data-visualization-forest-funnel-plots"
studies <- data.frame(author = c("Alpha","Beta","Gamma"), year = c(2018,2020,2022),
                      log_or = log(c(0.55, 0.90, 1.60)), log_or_se = c(0.20, 0.25, 0.30))
write.csv(studies, file.path(D, "data/synthetic_k3.csv"), row.names = FALSE)
# ---- SKILL.md standard REML block ----
res <- rma(yi = log_or, vi = log_or_se^2, data = studies, slab = paste(author, year), method = 'REML')
print(summary(res))
# ---- SKILL.md HKSJ block, verbatim ----
res_hksj <- rma(yi = log_or, vi = log_or_se^2, data = studies,
                method = 'REML', test = 'knha')           # HKSJ for k<5
print(res_hksj)
cat(sprintf("REML z:  b=%.6f ci=[%.6f, %.6f]\n", res$b, res$ci.lb, res$ci.ub))
cat(sprintf("HKSJ:    b=%.6f se=%.6f ci=[%.6f, %.6f] dfs=%d tau2=%.6f\n", res_hksj$b, res_hksj$se, res_hksj$ci.lb, res_hksj$ci.ub, res_hksj$dfs, res_hksj$tau2))
# forest from the SKILL block on k=3
png(file.path(D, "figs/in3_forest_k3.png"), width = 1000, height = 450, res = 110)
res_s <- rma(yi = log_or, vi = log_or_se^2, data = studies, slab = paste(author, year), method = 'REML', test = 'knha')
forest(res_s, atransf = exp, at = log(c(0.25, 0.5, 1, 2, 4)), refline = 0, xlab = 'Odds Ratio (95% CI)',
       header = c('Study', 'OR [95% CI]'), addpred = TRUE)
dev.off()
# Egger at k=3 (the Skill says k>=10; does the tool refuse or silently return?)
eg <- try(regtest(res, model = 'lm', predictor = 'sei')); print(eg)
# k=2: does rma run? Skill says "not advisable; report individuals only"
r2 <- rma(yi = log_or[1:2], vi = (log_or_se[1:2])^2, data = studies, method = 'REML'); cat("k=2 pooled:", r2$b, " I2=", r2$I2, "\n")
# Skill: "Do not report I2 for k<5" -- the SKILL's own summary()/example cat() prints I2 anyway:
cat(sprintf("I2 printed for k=3 by the Skill's own example line: %.1f%%\n", res$I2))
# Fixed-effect on the same data (heterogeneous): CI narrowness claim
fe <- rma(yi = log_or, vi = log_or_se^2, data = studies, method = 'FE')
cat(sprintf("FE: OR=%.3f [%.3f, %.3f] ; RE-REML OR=%.3f [%.3f,%.3f]; HKSJ OR=%.3f [%.3f, %.3f]\n",
    exp(fe$b), exp(fe$ci.lb), exp(fe$ci.ub), exp(res$b), exp(res$ci.lb), exp(res$ci.ub), exp(res_hksj$b), exp(res_hksj$ci.lb), exp(res_hksj$ci.ub)))
