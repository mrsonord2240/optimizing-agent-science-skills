# Regression test for the P0 skill-veto finding (pre-fix: ropls::opls(orthoI=NA) silently
# returned an empty model in ~40% of runs). Re-runs the guarded pattern the fix added to
# SKILL.md / examples/metabolomics_stats.R verbatim, across many more seeds than the original
# 10-seed probe, on three regimes: (1) the Skill's own n=40/p=300 signal-bearing distribution
# (identical to the pre-fix probe, seeds 1-50 instead of 1-10), (2) a harder n=24/p=1200
# regime cited in the fix log, and (3) pure noise with NO true signal at all -- the case most
# likely to exhaust the fallback and exercise the stop() path.
library(ropls)

# ---- fit_discriminant_guarded(), copied verbatim from SKILL.md / examples/metabolomics_stats.R ----
fit_discriminant_guarded <- function(x, y, scaleC, permI = 1000, crossvalI = 7) {
    m <- opls(x, y, predI = 1, orthoI = NA, scaleC = scaleC, permI = permI,
              crossvalI = crossvalI, fig.pdfC = 'none', info.txtC = 'none')
    if (nrow(getSummaryDF(m)) > 0) return(list(model = m, type = 'OPLS-DA'))
    m2 <- opls(x, y, predI = 1, orthoI = 0, scaleC = scaleC, permI = permI,
               crossvalI = crossvalI, fig.pdfC = 'none', info.txtC = 'none')
    if (nrow(getSummaryDF(m2)) > 0) return(list(model = m2, type = 'PLS-DA (OPLS-DA fallback)'))
    stop('Neither OPLS-DA nor the PLS-DA fallback produced a usable model: the first ',
         'predictive component was not significant under ropls\' own cross-validated ',
         'criterion. Report that no multivariate separation was detected -- do not force a model.')
}

run_sweep <- function(label, n_per_group, n_features, n_true, seeds, permI = 200) {
    cat('\n=== ', label, ' (n_per_group=', n_per_group, ' p=', n_features,
        ' n_true=', n_true, ', ', length(seeds), ' seeds) ===\n', sep = '')
    n_opls <- 0; n_fallback <- 0; n_stop <- 0; n_silent_empty <- 0
    for (s in seeds) {
        set.seed(s)
        group <- factor(rep(c('control', 'case'), each = n_per_group))
        intensities <- matrix(rnorm(2 * n_per_group * n_features, mean = 10, sd = 1),
                               nrow = 2 * n_per_group, ncol = n_features)
        colnames(intensities) <- paste0('M', seq_len(n_features))
        if (n_true > 0) {
            case_rows <- group == 'case'
            intensities[case_rows, seq_len(n_true)] <- intensities[case_rows, seq_len(n_true)] + 1.2
        }
        options(warn = 1)  # promote warnings to immediate output -- matches the pre-fix probe's check
        result <- tryCatch({
            fit <- fit_discriminant_guarded(intensities, group, scaleC = 'pareto', permI = permI)
            list(ok = TRUE, type = fit$type, rows = nrow(getSummaryDF(fit$model)))
        }, error = function(e) list(ok = FALSE, msg = conditionMessage(e)))

        if (!result$ok) {
            n_stop <- n_stop + 1
            cat(sprintf('  seed=%3d  STOP (loud error): %s\n', s, substr(result$msg, 1, 70)))
        } else if (result$type == 'OPLS-DA') {
            n_opls <- n_opls + 1
            if (result$rows == 0) { n_silent_empty <- n_silent_empty + 1; cat(sprintf('  seed=%3d  SILENT EMPTY (guard did not catch this!)\n', s)) }
        } else {
            n_fallback <- n_fallback + 1
            cat(sprintf('  seed=%3d  fallback to PLS-DA, summaryDF rows=%d\n', s, result$rows))
        }
    }
    cat(sprintf('  -> OPLS-DA direct: %d | PLS-DA fallback used: %d | loud stop(): %d | UNCAUGHT SILENT EMPTY: %d / %d\n',
                n_opls, n_fallback, n_stop, n_silent_empty, length(seeds)))
    invisible(list(opls = n_opls, fallback = n_fallback, stop = n_stop, silent = n_silent_empty, total = length(seeds)))
}

set.seed(42)
r1 <- run_sweep('Regime 1: Skill\'s own signal-bearing distribution (matches pre-fix probe)',
                 n_per_group = 20, n_features = 300, n_true = 15, seeds = 1:50)

r2 <- run_sweep('Regime 2: harder n=24/p=1200 (cited in fix log as a harder case)',
                 n_per_group = 12, n_features = 1200, n_true = 15, seeds = 1:30)

r3 <- run_sweep('Regime 3: pure noise, NO true signal at all (toughest case for the fallback)',
                 n_per_group = 20, n_features = 300, n_true = 0, seeds = 1001:1030)

cat('\n=== SUMMARY across all regimes ===\n')
cat(sprintf('Regime 1 (signal, n=40/p=300):  uncaught silent empty = %d/%d\n', r1$silent, r1$total))
cat(sprintf('Regime 2 (signal, n=24/p=1200): uncaught silent empty = %d/%d\n', r2$silent, r2$total))
cat(sprintf('Regime 3 (pure noise):          uncaught silent empty = %d/%d, loud stop() fired %d/%d\n',
            r3$silent, r3$total, r3$stop, r3$total))
total_silent <- r1$silent + r2$silent + r3$silent
total_n <- r1$total + r2$total + r3$total
cat(sprintf('\nTOTAL uncaught silent-empty models across %d runs: %d (%.1f%%)\n',
            total_n, total_silent, 100 * total_silent / total_n))
if (total_silent == 0) {
    cat('PASS: the guard caught every empty fit across all three regimes -- no silent empty model observed.\n')
} else {
    cat('FAIL: the guard did not catch every empty fit.\n')
}
