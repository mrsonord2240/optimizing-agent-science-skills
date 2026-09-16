# Audit input 3 (Variant B) -- bio-metabolomics-statistical-analysis
# User request: "Build an OPLS-DA model between my two groups and permutation-test
# it before you tell me it separates. I want to run this a few times as I tweak
# my pipeline, so it needs to be reliable."
#
# Uses the Skill's own canonical code pattern verbatim: opls(x, y, predI=1,
# orthoI=NA, scaleC=..., permI>=1000, ...). First: a 10-consecutive-call
# reliability probe across different seeds (same code, same distribution,
# only the RNG seed changes) -- this directly measures Skill Veto T1
# (Operational Stability: failure rate must stay <=20% across 10 calls).
# Second: the full validated-model + Pareto-vs-UV comparison on a working seed.
library(ropls)

cat('=== Reliability probe: 10 consecutive OPLS-DA fits, Skill\'s own example code/params ===\n')
cat('(n=40 samples, p=300 features, 15 truly shifted -- identical to examples/metabolomics_stats.R,\n')
cat(' only the seed varies 1-10)\n\n')

n_ok <- 0
for (sd in 1:10) {
    set.seed(sd)
    n_per_group <- 20; n_features <- 300; n_true <- 15
    group <- factor(rep(c('control', 'case'), each = n_per_group))
    intensities <- matrix(rnorm(2 * n_per_group * n_features, mean = 10, sd = 1),
                          nrow = 2 * n_per_group, ncol = n_features)
    colnames(intensities) <- paste0('M', seq_len(n_features))
    case_rows <- group == 'case'
    intensities[case_rows, seq_len(n_true)] <- intensities[case_rows, seq_len(n_true)] + 1.2
    m <- opls(intensities, group, predI = 1, orthoI = NA, scaleC = 'pareto',
              permI = 100, crossvalI = 7, fig.pdfC = 'none', info.txtC = 'none')
    s <- getSummaryDF(m)
    ok <- nrow(s) > 0
    n_ok <- n_ok + as.integer(ok)
    vip_len <- tryCatch(length(getVipVn(m)), error = function(e) NA)
    cat(sprintf('  seed=%2d  class=%s  summaryDF_rows=%d  getVipVn_length=%s  %s\n',
                sd, class(m), nrow(s), vip_len, ifelse(ok, 'OK', 'SILENT EMPTY MODEL -- no error/warning printed')))
}
cat(sprintf('\nSuccess rate: %d/10 (%.0f%%) -- failure rate %.0f%% %s\n',
            n_ok, 100 * n_ok / 10, 100 * (10 - n_ok) / 10,
            ifelse((10 - n_ok) / 10 > 0.2, '>>> EXCEEDS the 20% Skill-Veto T1 threshold', '(within 20% threshold)')))

cat('\n=== Full validated analysis on a known-working seed (1, matching the bundled example) ===\n')
set.seed(1)
n_per_group <- 20; n_features <- 300; n_true <- 15
group <- factor(rep(c('control', 'case'), each = n_per_group))
intensities <- matrix(rnorm(2 * n_per_group * n_features, mean = 10, sd = 1),
                      nrow = 2 * n_per_group, ncol = n_features)
colnames(intensities) <- paste0('M', seq_len(n_features))
case_rows <- group == 'case'
intensities[case_rows, seq_len(n_true)] <- intensities[case_rows, seq_len(n_true)] + 1.2
null_group <- factor(sample(as.character(group)))

run_model <- function(y, scaleC) {
    opls(intensities, y, predI = 1, orthoI = NA, scaleC = scaleC,
         permI = 1000, crossvalI = 7, fig.pdfC = 'none', info.txtC = 'none')
}

real_pareto <- run_model(group, 'pareto')
s1 <- getSummaryDF(real_pareto)
cat('Real labels, Pareto:\n'); print(s1[, c('R2X(cum)', 'R2Y(cum)', 'Q2(cum)', 'pR2Y', 'pQ2')])

null_pareto <- run_model(null_group, 'pareto')
s2 <- getSummaryDF(null_pareto)
cat('\nPermuted (null) labels, Pareto:\n'); print(s2[, c('R2X(cum)', 'R2Y(cum)', 'Q2(cum)', 'pR2Y', 'pQ2')])

real_uv <- run_model(group, 'standard')
s3 <- getSummaryDF(real_uv)
cat('\nReal labels, unit-variance:\n'); print(s3[, c('R2X(cum)', 'R2Y(cum)', 'Q2(cum)', 'pR2Y', 'pQ2')])

vip_pareto <- getVipVn(real_pareto)
vip_uv <- getVipVn(real_uv)
top10_pareto <- names(sort(vip_pareto, decreasing = TRUE))[1:10]
top10_uv <- names(sort(vip_uv, decreasing = TRUE))[1:10]
true_features <- paste0('M', seq_len(n_true))
cat(sprintf('\nTop-10 VIP overlap Pareto vs UV: %d of 10\n', length(intersect(top10_pareto, top10_uv))))
cat(sprintf('True planted features in Pareto top-10 VIP: %d of 10\n', length(intersect(top10_pareto, true_features))))
cat(sprintf('Real model: Q2(cum)=%.3f, pQ2=%.3f -> licensed: %s\n', s1[['Q2(cum)']], s1[['pQ2']], s1[['pQ2']] < 0.05))
cat(sprintf('Null  model: Q2(cum)=%.3f, pQ2=%.3f -> licensed: %s\n', s2[['Q2(cum)']], s2[['pQ2']], s2[['pQ2']] < 0.05))
