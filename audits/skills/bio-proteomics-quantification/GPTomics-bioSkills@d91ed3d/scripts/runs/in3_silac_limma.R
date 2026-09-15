.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 3 downstream: limma one-sample (intercept) test on median-normalized SILAC log2 ratios that contain +/-Inf
suppressPackageStartupMessages(library(limma))
x <- read.csv('F:/OpenScience/audits/bio-proteomics-quantification/runs/in3_silac_log2_norm.csv', row.names = 1)
tr <- read.csv('F:/OpenScience/audits/bio-proteomics-quantification/data/silac_truth.csv', row.names = 1)
m <- as.matrix(x); cat('Inf cells:', sum(is.infinite(m)), '| NA cells:', sum(is.na(m)), '| all-NA rows:', sum(rowSums(!is.na(m)) == 0), '\n')
try_eb <- function(mm, tag, ...) {
  fit <- tryCatch(lmFit(mm), error = function(e) { cat(tag, 'lmFit ERROR:', conditionMessage(e), '\n'); NULL })
  if (is.null(fit)) return(invisible(NULL))
  cat(tag, 'lmFit OK; coefficients for heavy_only rows:', paste(round(fit$coefficients[tr[rownames(mm), 'class'] == 'heavy_only'], 2), collapse = ' '),
      '| sigma of those rows:', paste(round(fit$sigma[tr[rownames(mm), 'class'] == 'heavy_only'], 2), collapse = ' '), '\n')
  eb <- tryCatch(eBayes(fit, ...), error = function(e) { cat(tag, 'eBayes ERROR:', conditionMessage(e), '\n'); NULL })
  if (!is.null(eb)) { cat(tag, 'eBayes OK; s2.prior =', signif(eb$s2.prior[1], 3), '| df.prior =', signif(eb$df.prior[1], 3), '\n'); tt <- topTable(eb, number = Inf, sort.by = 'none')
    sig <- rownames(tt)[which(tt$adj.P.Val < 0.05)]
    cat(tag, 'BH<0.05 calls:', length(sig), '| true up/down among them:', sum(tr[sig, 'class'] %in% c('up', 'down')), 'of 60 | heavy/light-only among them:', sum(tr[sig, 'class'] %in% c('heavy_only', 'light_only')), '\n') }
  invisible(eb)
}
try_eb(m, '[A Inf kept, trend+robust]', trend = TRUE, robust = TRUE)
try_eb(m, '[B Inf kept, plain eBayes]')
keep <- rowSums(!is.na(m)) > 0
try_eb(m[keep, ], '[C Inf kept, all-NA rows dropped, trend+robust]', trend = TRUE, robust = TRUE)
m2 <- m; m2[is.infinite(m2)] <- NA; keep2 <- rowSums(!is.na(m2)) > 0
try_eb(m2[keep2, ], '[D Inf->NA, all-NA rows dropped, trend+robust]', trend = TRUE, robust = TRUE)
cat('on/off proteins that silently leave the test in D:', sum(!keep2 & tr[rownames(m2), 'class'] %in% c('heavy_only', 'light_only')), 'of 12\n')
