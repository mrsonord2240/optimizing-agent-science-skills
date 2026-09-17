# LLOQ-level QC, 2 days x 3 replicates, nominal 2 ng/mL -- planted a low rep-3
# outlier both days (real within-day imprecision, not a day-to-day shift).
qc <- data.frame(
  day = rep(1:2, each = 3),
  measured_conc = c(2.35, 2.30, 1.55, 2.40, 2.28, 1.60)
)

intra <- aggregate(measured_conc ~ day, qc, function(x) sd(x) / mean(x) * 100)
print(intra)
# day 1: 21.7% | day 2: 20.6% -- both FAIL the 20% LLOQ tolerance

naive_pooled_cv <- sd(qc$measured_conc) / mean(qc$measured_conc) * 100
cat('naive_pooled_cv:', naive_pooled_cv, '\n')
# 18.9% -- WRONG for inter-day: ignores the day structure and PASSES, masking the failure

fit <- aov(measured_conc ~ factor(day), data = qc)
ms <- summary(fit)[[1]][["Mean Sq"]]
n_per_day <- nrow(qc) / length(unique(qc$day))
var_within <- ms[2]
var_between <- max(0, (ms[1] - ms[2]) / n_per_day)
inter_day_cv <- sqrt(var_within + var_between) / mean(qc$measured_conc) * 100
cat('inter_day_cv (nested ANOVA):', inter_day_cv, '\n')
# 21.1% -- correct nested-ANOVA inter-day (total) precision, correctly FAILS
