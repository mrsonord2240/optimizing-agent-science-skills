# Input 3 -- Edge / boundary: "We can only afford n=2 per group. What power do we get to detect a
# 1.5-fold change at CV=0.4? Separately, if I need 95% power to detect a tiny 1.05-fold change at
# CV=0.5, how many replicates would that take?"
# Exercises rnapower()'s behavior at the extremes: very small n (does it return a sane low number,
# or silently break like ssizeRNA's sibling Skill did?) and a near-impossible target (near-null
# effect at very high power -- does the closed form blow up, error, or just return a huge n?).

suppressPackageStartupMessages(library(RNASeqPower))

cat("=== A. n=2 per group, CV=0.4, 1.5-fold ===\n")
p2 <- tryCatch(rnapower(depth = 20, n = 2, cv = 0.4, effect = 1.5, alpha = 0.05),
               error = function(e) paste("ERROR:", conditionMessage(e)))
print(p2)

cat("\n=== B. Near-impossible target: 1.05-fold, CV=0.5, 95% power ===\n")
n_needed <- tryCatch(rnapower(depth = 20, cv = 0.5, effect = 1.05, alpha = 0.05, power = 0.95),
                      error = function(e) paste("ERROR:", conditionMessage(e)))
print(n_needed)
cat("ceiling:", if (is.numeric(n_needed)) ceiling(n_needed) else NA, "\n")

cat("\n=== C. Sanity: does rnapower silently return NA/negative/nonsense anywhere in a sweep? ===\n")
for (eff in c(1.01, 1.05, 1.1, 1.2, 1.5, 2, 4)) {
  n <- tryCatch(rnapower(depth = 20, cv = 0.4, effect = eff, alpha = 0.05, power = 0.80),
                error = function(e) NA)
  cat(sprintf("effect=%.2f -> n=%s (ceil %s)\n", eff,
              ifelse(is.na(n), "NA", sprintf("%.2f", n)),
              ifelse(is.na(n), "NA", ceiling(n))))
}
