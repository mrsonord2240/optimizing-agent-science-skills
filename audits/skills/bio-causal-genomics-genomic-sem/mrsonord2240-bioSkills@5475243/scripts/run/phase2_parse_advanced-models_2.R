# Test SNP -> F path + SNP -> trait1 direct path simultaneously
model <- '
    F =~ NA*trait1 + trait2 + trait3
    F ~~ 1*F
    F ~ SNP
    trait1 ~ SNP    # direct effect on trait1, partialed out of F
'
user_results <- userGWAS(covstruc = ldsc_results,
                         SNPs = ss,
                         estimation = 'DWLS',
                         model = model,
                         sub = c('F~SNP', 'trait1~SNP'),
                         parallel = TRUE,
                         cores = 8)
# Output (one data frame per SNP set; checked on 0.0.5): SNP, CHR, BP, MAF, A1, A2, lhs, op, rhs,
# free, label, est, SE, Z_Estimate, Pval_Estimate, chisq, chisq_df, chisq_pval, AIC, error, warning.
# There is NO Q_pval column: chisq / chisq_pval is the fit of the whole SNP-augmented model, so a
# small chisq_pval means unmodelled SNP paths remain (a third path may be needed).
