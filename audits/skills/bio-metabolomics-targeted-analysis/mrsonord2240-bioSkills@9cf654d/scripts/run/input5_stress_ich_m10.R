# Input 5 (Stress) -- "Here is 2-day, 3-replicate QC data at LLOQ/LOW/MID/HIGH for a clinical PK
# assay, plus a blank injected after the ULOQ calibrator. Run the full ICH M10 acceptance check
# (intra/inter-day accuracy and precision, carryover) and tell me whether this assay is fit for
# a regulated PK decision."
#
# Code follows SKILL.md's "Quantitative Thresholds" table directly:
#   QC accuracy +-15% (+-20% LLOQ); precision CV <=15% (<=20% LLOQ)
#   Carryover <=20% of LLOQ (analyte), <=5% (IS)

qc <- read.csv('F:/OpenScience/audits/bio-metabolomics-targeted-analysis/data/input5_ich_m10_validation.csv')
co <- read.csv('F:/OpenScience/audits/bio-metabolomics-targeted-analysis/data/input5_carryover_blanks.csv')

acc_tol <- function(level) ifelse(level == 'LLOQ', 20, 15)
prec_tol <- function(level) ifelse(level == 'LLOQ', 20, 15)

qc$pct_re <- (qc$measured_conc - qc$nominal_conc) / qc$nominal_conc * 100

# Intra-day accuracy/precision (per day x level)
intra <- aggregate(cbind(measured_conc, pct_re) ~ qc_level + day + nominal_conc, data = qc,
                    FUN = function(x) x)
intra_stats <- do.call(rbind, lapply(split(qc, list(qc$qc_level, qc$day)), function(g) {
  if (nrow(g) == 0) return(NULL)
  data.frame(qc_level = g$qc_level[1], day = g$day[1], nominal = g$nominal_conc[1],
             mean_re = mean(g$pct_re), cv_pct = sd(g$measured_conc) / mean(g$measured_conc) * 100)
}))
intra_stats$acc_tol <- acc_tol(intra_stats$qc_level)
intra_stats$prec_tol <- prec_tol(intra_stats$qc_level)
intra_stats$acc_pass <- abs(intra_stats$mean_re) <= intra_stats$acc_tol
intra_stats$prec_pass <- intra_stats$cv_pct <= intra_stats$prec_tol
intra_stats <- intra_stats[order(intra_stats$qc_level, intra_stats$day), ]

cat('=== Intra-day accuracy & precision ===\n')
print(intra_stats[, c('qc_level','day','mean_re','cv_pct','acc_pass','prec_pass')], row.names = FALSE)

# Inter-day (pool both days per level)
inter_stats <- do.call(rbind, lapply(split(qc, qc$qc_level), function(g) {
  data.frame(qc_level = g$qc_level[1], nominal = g$nominal_conc[1],
             mean_re = mean(g$pct_re), cv_pct = sd(g$measured_conc) / mean(g$measured_conc) * 100)
}))
inter_stats$acc_tol <- acc_tol(inter_stats$qc_level)
inter_stats$prec_tol <- prec_tol(inter_stats$qc_level)
inter_stats$acc_pass <- abs(inter_stats$mean_re) <= inter_stats$acc_tol
inter_stats$prec_pass <- inter_stats$cv_pct <= inter_stats$prec_tol

cat('\n=== Inter-day (pooled) accuracy & precision ===\n')
print(inter_stats[, c('qc_level','mean_re','cv_pct','acc_pass','prec_pass')], row.names = FALSE)

# Carryover: blank-after-ULOQ area converted to concentration via the calibration fit from
# Input 1 (slope/intercept reused as the same assay's calibration), expressed as % of LLOQ nominal.
fit_slope <- 1.001024507e-03    # from Input 1 weighted fit, coef(fit)[2]
fit_intercept <- -3.658276245e-05 # from Input 1 weighted fit, coef(fit)[1] (~0)
blank_ratio <- co$analyte_area[co$type == 'blank_after_ULOQ'] / co$istd_area[co$type == 'blank_after_ULOQ']
blank_conc <- (blank_ratio - fit_intercept) / fit_slope
lloq_nominal <- 2
carryover_pct_of_lloq <- blank_conc / lloq_nominal * 100

cat('\n=== Carryover (blank injected after ULOQ calibrator) ===\n')
cat('Blank-equivalent concentration:', round(blank_conc, 3), 'ng/mL\n')
cat('Carryover as % of LLOQ:', round(carryover_pct_of_lloq, 1), '% -- ICH M10 threshold: <=20%\n')
cat('Carryover PASS:', carryover_pct_of_lloq <= 20, '\n')

cat('\n=== OVERALL ASSAY VERDICT ===\n')
all_acc_prec_pass <- all(inter_stats$acc_pass) && all(inter_stats$prec_pass) &&
                      all(intra_stats$acc_pass) && all(intra_stats$prec_pass)
carryover_pass <- carryover_pct_of_lloq <= 20
cat('All accuracy/precision tiers pass:', all_acc_prec_pass, '\n')
cat('Carryover passes:', carryover_pass, '\n')
cat('Assay fit for regulated PK decision (ICH M10, this data subset):', all_acc_prec_pass && carryover_pass, '\n')

cat('\n=== ASSERTION CHECKS (planted failures the skill should catch) ===\n')
lloq_prec <- inter_stats$prec_pass[inter_stats$qc_level == 'LLOQ']
cat('LLOQ precision correctly FAILS (planted rep-3 outlier both days):', !lloq_prec, '\n')
cat('Carryover correctly FAILS (planted high blank-after-ULOQ signal):', !carryover_pass, '\n')
cat('LOW/MID/HIGH tiers correctly PASS (clean planted data):',
    all(inter_stats$acc_pass[inter_stats$qc_level != 'LLOQ']) &&
    all(inter_stats$prec_pass[inter_stats$qc_level != 'LLOQ']), '\n')
