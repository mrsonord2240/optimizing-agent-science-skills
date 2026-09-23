library(pwr)
unadjusted <- pwr.t.test(d = 1.2, sig.level = 0.05, power = 0.80, type = "two.sample")$n
adjusted <- pwr.t.test(d = 1.2, sig.level = 0.05 / 5000, power = 0.80, type = "two.sample")$n
stopifnot(unadjusted > 11 && unadjusted < 13, adjusted > 43 && adjusted < 45,
          adjusted > unadjusted * 3)
cat(sprintf("OK proteomics: unadjusted_n=%.2f adjusted_5000_feature_n=%.2f\n", unadjusted, adjusted))
