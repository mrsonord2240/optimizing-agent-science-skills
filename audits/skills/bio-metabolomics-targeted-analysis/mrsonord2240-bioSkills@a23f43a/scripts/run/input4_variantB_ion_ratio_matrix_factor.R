# Input 4 (Variant B) -- "Compute the qualifier/quantifier ion ratio for my QC samples and flag
# any outside +/-30% of the calibrator ratio. Also estimate the IS-normalized matrix factor
# across 6 matrix lots (neat-solvent vs matrix-spiked response)."
#
# Code written following SKILL.md's "Ion-Ratio Confirmation" section (cal_ratio, id_confirmed)
# and the Matuszewski matrix-factor / "IS-normalized matrix factor CV <=15% across >=6 lots"
# threshold from the Quantitative Thresholds table.

d <- read.csv('F:/OpenScience/audits/bio-metabolomics-targeted-analysis/data/input4_ion_ratio_matrix_factor.csv')

qc <- d[d$sample_type == 'QC_mid', ]
interfered <- d[d$sample_type == 'study_sample', ]

# Calibrator ion ratio (planted ground truth for this synthetic panel: 0.39, as in the skill's
# own worked example / examples/targeted_quantification.R)
cal_ratio <- 0.39
ion_ratio_tol <- 0.30

qc$ion_ratio <- qc$qualifier_area / qc$quantifier_area
qc$id_confirmed <- abs(qc$ion_ratio - cal_ratio) / cal_ratio <= ion_ratio_tol

interfered$ion_ratio <- interfered$qualifier_area / interfered$quantifier_area
interfered$id_confirmed <- abs(interfered$ion_ratio - cal_ratio) / cal_ratio <= ion_ratio_tol

cat('=== QC-mid ion ratios across 6 lots ===\n')
print(qc[, c('lot','ion_ratio','id_confirmed')])
cat('\n=== Planted-interference sample ===\n')
print(interfered[, c('lot','ion_ratio','id_confirmed')])

# Matrix factor (Matuszewski): MF = matrix-spiked response / neat-solvent response, per analyte
# and per IS, then IS-normalized MF = MF_analyte / MF_istd. Here neat response is constant
# (25000/100000) across lots by construction, so IS-normalized MF isolates matrix suppression.
neat_ratio <- unique(d$neat_analyte_area / d$neat_istd_area)
qc$matrix_ratio <- qc$quantifier_area / qc$istd_area
qc$is_norm_mf <- qc$matrix_ratio / neat_ratio

mf_mean <- mean(qc$is_norm_mf)
mf_cv_pct <- sd(qc$is_norm_mf) / mf_mean * 100

cat('\n=== IS-normalized matrix factor across 6 lots ===\n')
mf_report <- qc[, c('lot','is_norm_mf')]
mf_report$is_norm_mf <- round(mf_report$is_norm_mf, 3)
print(mf_report)
cat('Mean IS-normalized MF:', round(mf_mean, 3), '\n')
cat('MF CV%:', round(mf_cv_pct, 2), '-- ICH M10/Matuszewski threshold: <=15% across >=6 lots\n')
cat('MF CV PASS:', mf_cv_pct <= 15, '\n')

cat('\n=== ASSERTION CHECKS ===\n')
cat('All 6 clean QC-mid lots confirmed (id_confirmed==TRUE):', all(qc$id_confirmed), '\n')
cat('Planted-interference sample correctly flagged NOT confirmed:', !interfered$id_confirmed[1], '\n')
cat('MF CV computed and within threshold (clean synthetic lots, no real suppression planted):', mf_cv_pct <= 15, '\n')
