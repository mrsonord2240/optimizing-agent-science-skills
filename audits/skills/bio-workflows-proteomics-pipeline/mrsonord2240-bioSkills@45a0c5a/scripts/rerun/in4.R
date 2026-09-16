
# RE-AUDIT Input 4 (Variant B): TMT10 mzML -> fixed TMT block VERBATIM with the channel-named lot CoA it now asks for.
# SYNTHETIC mzML; bleed follows the MSnbase TMT10 manufacturer template (truth: data/tmt10_truth.csv).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressMessages(library(MSnbase))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'rerun', 'work4'))
tmpl <- makeImpuritiesMatrix(x = 10, edit = FALSE)
ch <- colnames(tmpl)
cat('makeImpuritiesMatrix(10) diagonal:', round(diag(tmpl), 3), '| near-identity (all > 0.99)?', all(diag(tmpl) > 0.99), '\n')
cat('template row 126 non-zero columns:', paste(names(which(tmpl[1, ] > 0)), collapse = ','), '\n')

# Build the CoA the FIXED block asks for: square percentage matrix, rows = SOURCE reagent,
# columns = OBSERVED channel, both labelled with channel names. Lot values = the template.
coa <- tmpl * 100
dimnames(coa) <- list(ch, ch)
write.csv(coa, 'tmt10_coa.csv')

blk <- list.files(file.path(PP, 'rerun', 'blocks'), pattern = '^b03', full.names = TRUE)
res <- tryCatch({ suppressMessages(sys.source(blk, envir = globalenv())); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[TMT block verbatim]', res, '\n')
cat('block impurities row 126 non-zero columns:', paste(names(which(impurities[1, ] > 0)), collapse = ','), '\n')
cat('block matrix identical to template?', isTRUE(all.equal(unname(impurities), unname(tmpl))), '\n')

truth <- read.csv(file.path(PP, 'data', 'tmt10_truth.csv'), check.names = FALSE)
rel <- function(m) m / rowSums(m); tm <- as.matrix(truth[, ch])
raw_q <- exprs(suppressMessages(quantify(raw, reporters = TMT10, method = 'max')))
n <- min(nrow(tm), nrow(raw_q))
err <- function(m) median(abs(rel(m[1:n, ]) - rel(tm[1:n, ])))

# The OLD route the pre-fix Skill told users to use, for comparison: makeImpuritiesMatrix(filename=)
# reading a -1Da/+1Da CoA sheet in MSnbase filename layout.
pm <- sapply(seq_along(ch), function(i) if (i > 2) 100 * tmpl[i, i - 2] else 0)
pp <- sapply(seq_along(ch), function(i) if (i < 9) 100 * tmpl[i, i + 2] else 0)
old <- matrix(0, 10, 10, dimnames = list(ch, c('-5','-4','-3','-2','-1','+1','+2','+3','+4','+5')))
old[, '-1'] <- pm; old[, '+1'] <- pp
write.csv(old, 'tmt10_coa_daoffset.csv')
oldm <- makeImpuritiesMatrix(filename = 'tmt10_coa_daoffset.csv', edit = FALSE)
cat('OLD filename-route row 126 non-zero columns:', paste(names(which(oldm[1, ] > 0)), collapse = ','), '(truth: 127C)\n')
old_q <- exprs(purityCorrect(suppressMessages(quantify(raw, reporters = TMT10, method = 'max')), oldm))
cat(sprintf('median |relative error| vs truth: uncorrected %.4f | OLD filename CoA route %.4f | NEW channel-named route %.4f\n',
    err(raw_q), err(old_q), err(exprs(tmt_data))))
cat('negative cells after the new correction:', sum(exprs(tmt_data) < 0, na.rm = TRUE), '\n')

# Does the block's guard catch a mis-ordered / transposed CoA?
bad <- t(coa); write.csv(bad, 'tmt10_coa.csv')
g <- tryCatch({ suppressMessages(sys.source(blk, envir = new.env(parent = globalenv()))); 'NO ERROR - guard did not fire' },
              error = function(e) paste('guard fired:', conditionMessage(e)))
cat('transposed-CoA guard:', g, '\n')
# And a CoA with the wrong channel labels
write.csv(`dimnames<-`(coa, list(paste0('R', 1:10), paste0('R', 1:10))), 'tmt10_coa.csv')
g2 <- tryCatch({ suppressMessages(sys.source(blk, envir = new.env(parent = globalenv()))); 'NO ERROR - guard did not fire' },
               error = function(e) paste('guard fired:', conditionMessage(e)))
cat('wrong-channel-name guard:', g2, '\n')
