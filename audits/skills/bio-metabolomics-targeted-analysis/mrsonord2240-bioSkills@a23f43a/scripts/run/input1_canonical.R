# Input 1 (Canonical) -- "I have calibration standards and unknown plasma samples for an
# SIL-IS-normalized LC-MS/MS assay. Build a 1/x^2-weighted calibration curve, accept it by
# back-calculated %RE (not R-squared), and report concentrations for my unknown samples,
# flagging anything below the LLOQ."
#
# Code written following bio-metabolomics-targeted-analysis SKILL.md 's
# "Build a Weighted Calibration Curve With a Back-Calculated %RE Check" +
# "Internal-Standard Normalization" sections verbatim.

standards <- read.csv('F:/OpenScience/audits/bio-metabolomics-targeted-analysis/data/input1_calibration_standards.csv')
samples   <- read.csv('F:/OpenScience/audits/bio-metabolomics-targeted-analysis/data/input1_unknown_samples.csv')

standards$ratio <- standards$analyte_area / standards$istd_area

fit <- lm(ratio ~ conc_ngml, data = standards, weights = 1 / standards$conc_ngml^2)
standards$back_calc <- (standards$ratio - coef(fit)[1]) / coef(fit)[2]
standards$re_pct <- (standards$back_calc - standards$conc_ngml) / standards$conc_ngml * 100

# ICH M10: each calibrator within +-15%, +-20% at the LLOQ (lowest level)
tol <- ifelse(standards$conc_ngml == min(standards$conc_ngml), 20, 15)
standards$pass <- abs(standards$re_pct) <= tol
lloq <- min(standards$conc_ngml[standards$pass])

cat('=== Calibration back-calculation (weighted 1/x^2) ===\n')
print(round(standards[, c('conc_ngml','re_pct','pass')], 2))
cat('LLOQ set to:', lloq, 'ng/mL\n\n')

# Internal-standard normalization + quantification of unknowns
samples$ratio <- samples$analyte_area / samples$istd_area
samples$conc_est <- (samples$ratio - coef(fit)[1]) / coef(fit)[2]
samples$reportable <- samples$conc_est >= lloq
samples$conc_reported <- ifelse(samples$reportable, samples$conc_est, NA)

# Verification against planted ground truth (synthetic data, not part of the skill's own output)
samples$pct_error_vs_truth <- (samples$conc_est - samples$true_conc_ngml) / samples$true_conc_ngml * 100

cat('=== Unknown sample quantification vs planted true concentration ===\n')
report <- samples[, c('sample','true_conc_ngml','conc_est','pct_error_vs_truth','reportable')]
report$conc_est <- round(report$conc_est, 2)
report$pct_error_vs_truth <- round(report$pct_error_vs_truth, 2)
print(report)

cat('\n=== ASSERTION CHECKS ===\n')
cat('All non-below-LLOQ samples within +-15% of planted truth:',
    all(abs(samples$pct_error_vs_truth[samples$reportable]) <= 15), '\n')
cat('U6 (true=3, near LLOQ=2) correctly flagged reportable==TRUE (since 3 > LLOQ 2):', samples$reportable[samples$sample=='U6'], '\n')
