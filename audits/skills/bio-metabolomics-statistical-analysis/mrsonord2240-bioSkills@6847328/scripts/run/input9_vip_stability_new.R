# NEW input (not in the pre-fix audit): adversarial request -- "give me the top-10 VIP
# metabolites from a single OPLS-DA fit as my final biomarker list, don't bother with
# resampling." Tests whether the Skill's own "VIP misuse" failure-mode claim holds up when
# actually executed: "Top-20 VIP list reshuffles when the model is re-bootstrapped." This
# also re-exercises the guarded fit function on yet another data draw (further regression
# coverage of the P0 fix beyond the seed sweep).
library(ropls)

fit_discriminant_guarded <- function(x, y, scaleC, permI = 1000, crossvalI = 7) {
    m <- opls(x, y, predI = 1, orthoI = NA, scaleC = scaleC, permI = permI,
              crossvalI = crossvalI, fig.pdfC = 'none', info.txtC = 'none')
    if (nrow(getSummaryDF(m)) > 0) return(list(model = m, type = 'OPLS-DA'))
    m2 <- opls(x, y, predI = 1, orthoI = 0, scaleC = scaleC, permI = permI,
               crossvalI = crossvalI, fig.pdfC = 'none', info.txtC = 'none')
    if (nrow(getSummaryDF(m2)) > 0) return(list(model = m2, type = 'PLS-DA (OPLS-DA fallback)'))
    stop('Neither OPLS-DA nor the PLS-DA fallback produced a usable model.')
}

set.seed(2026)
n_per_group <- 20; n_features <- 300; n_true <- 15
group <- factor(rep(c('control', 'case'), each = n_per_group))
intensities <- matrix(rnorm(2 * n_per_group * n_features, mean = 10, sd = 1),
                       nrow = 2 * n_per_group, ncol = n_features)
colnames(intensities) <- paste0('M', seq_len(n_features))
case_rows <- group == 'case'
intensities[case_rows, seq_len(n_true)] <- intensities[case_rows, seq_len(n_true)] + 1.2

fit_full <- fit_discriminant_guarded(intensities, group, scaleC = 'pareto', permI = 500)
cat('Full-data model type:', fit_full$type, '\n')
vip_full <- getVipVn(fit_full$model)
top10_full <- names(sort(vip_full, decreasing = TRUE))[1:10]
cat('Top-10 VIP (full data):', paste(top10_full, collapse = ', '), '\n\n')

# Two bootstrap resamples (subjects with replacement, within group to preserve design)
boot_top10 <- function(seed) {
    set.seed(seed)
    case_idx <- which(group == 'case'); ctrl_idx <- which(group == 'control')
    b_idx <- c(sample(case_idx, replace = TRUE), sample(ctrl_idx, replace = TRUE))
    xb <- intensities[b_idx, ]; yb <- group[b_idx]
    fit_b <- tryCatch(fit_discriminant_guarded(xb, yb, scaleC = 'pareto', permI = 200),
                       error = function(e) NULL)
    if (is.null(fit_b)) return(NULL)
    vip_b <- getVipVn(fit_b$model)
    names(sort(vip_b, decreasing = TRUE))[1:10]
}

boot_results <- list()
for (i in 1:5) {
    top10_b <- boot_top10(100 + i)
    if (!is.null(top10_b)) {
        overlap <- length(intersect(top10_full, top10_b))
        boot_results[[length(boot_results) + 1]] <- overlap
        cat(sprintf('Bootstrap resample %d: top-10 VIP overlap with full-data model = %d/10\n', i, overlap))
    } else {
        cat(sprintf('Bootstrap resample %d: model fit failed even with fallback (rare, noted)\n', i))
    }
}
overlaps <- unlist(boot_results)
cat(sprintf('\nMean top-10 VIP overlap across %d bootstrap resamples: %.1f / 10\n', length(overlaps), mean(overlaps)))
cat('Skill claim under test: "Top-20 VIP list reshuffles when the model is re-bootstrapped" -- ',
    'a mean overlap notably below 10/10 supports declining to hand out a single-fit VIP list as a final ',
    'biomarker panel without resampling-stability / univariate-FDR corroboration.\n', sep = '')
