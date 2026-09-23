# Pass-5: does the NEW orientation guard in the TMT block catch a transposed CoA, which the old
# negative-count check provably did not? SYNTHETIC mzML + CoA.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressMessages(library(MSnbase))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP,'pass5','work4'))
coa_ok <- as.matrix(read.csv('tmt10_coa.csv', row.names = 1, check.names = FALSE))
coa_t  <- t(coa_ok); dimnames(coa_t) <- dimnames(coa_ok)

# the guard exactly as SKILL.md now writes it
guard <- function(coa, label) {
  row_dev <- sum((rowSums(coa) - 100)^2); col_dev <- sum((colSums(coa) - 100)^2)
  cat(sprintf('%-22s row_dev %8.2f | col_dev %8.2f | ', label, row_dev, col_dev))
  if (col_dev < row_dev) { cat('GUARD FIRES: CoA looks TRANSPOSED\n'); return(FALSE) }
  ok <- tryCatch({ stopifnot(all(diag(coa) == apply(coa, 1, max)), all(diag(coa) > 50)); TRUE },
                 error = function(e) { cat('GUARD FIRES (diag check): ', conditionMessage(e), '\n'); FALSE })
  if (ok) cat('passes\n'); ok
}
guard(coa_ok, 'correct orientation')
guard(coa_t,  'transposed sheet')
guard(coa_ok/100, 'fractions not percent')

# and confirm the OLD check still would not have caught it
raw <- readMSData('tmt.mzML', mode = 'onDisk')
q <- suppressMessages(quantify(raw, reporters = TMT10, method = 'max'))
ch <- colnames(makeImpuritiesMatrix(x = 10, edit = FALSE))
bad <- purityCorrect(q, coa_t[ch, ch]/100)
cat('negatives after purityCorrect with the TRANSPOSED CoA:',
    sum(exprs(bad) < 0, na.rm = TRUE), '-> the old stopifnot(negatives==0) would still pass\n')
