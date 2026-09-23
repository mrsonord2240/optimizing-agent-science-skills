# Pipeline Input 4 (variant): TMT10 mzML -> SKILL.md TMT block verbatim with the lot CoA CSV its comment asks for. SYNTHETIC
# mzML whose reporter bleed follows the MSnbase TMT10 manufacturer template (truth in tmt10_truth.csv).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressMessages(library(MSnbase))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'runs', 'work4'))
tmpl <- makeImpuritiesMatrix(x = 10, edit = FALSE)
cat('makeImpuritiesMatrix(10) template diagonal:', round(diag(tmpl), 3), '| near-identity (all diag > 0.99)?', all(diag(tmpl) > 0.99), '\n')
# CoA sheet as a user would transcribe it: -1 Da and +1 Da percentages per reporter, in MSnbase's filename layout (10 columns)
ch <- colnames(tmpl); pm <- sapply(seq_along(ch), function(i) if (i > 2) 100 * tmpl[i, i - 2] else 0)
pp <- sapply(seq_along(ch), function(i) if (i < 9) 100 * tmpl[i, i + 2] else 0)
coa <- matrix(0, 10, 10, dimnames = list(ch, c('-5', '-4', '-3', '-2', '-1', '+1', '+2', '+3', '+4', '+5'))); coa[, '-1'] <- pm; coa[, '+1'] <- pp
write.csv(coa, 'tmt10_coa.csv')
blk <- list.files(file.path(PP, 'runs', 'blocks'), pattern = '^b03', full.names = TRUE)
res <- tryCatch({ suppressMessages(sys.source(blk, envir = globalenv())); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[TMT block verbatim]', res, '\n')
cat('CoA-route matrix off-diagonal positions (row 126):', names(which(impurities[1, ] > 0)), '| template row 126:', names(which(tmpl[1, ] > 0)), '\n')
truth <- read.csv(file.path(PP, 'data', 'tmt10_truth.csv'), check.names = FALSE)
rel <- function(m) m / rowSums(m); tm <- as.matrix(truth[, ch])
raw_q <- exprs(suppressMessages(quantify(raw, reporters = TMT10, method = 'max'))); n <- min(nrow(tm), nrow(raw_q))
err <- function(m) median(abs(rel(m[1:n, ]) - rel(tm[1:n, ])))
cat(sprintf('median |relative error|: uncorrected %.4f | Skill CoA-CSV route %.4f | template route %.4f\n', err(raw_q), err(exprs(tmt_data)),
            err(exprs(purityCorrect(quantify(raw, reporters = TMT10, method = 'max'), tmpl)))))
