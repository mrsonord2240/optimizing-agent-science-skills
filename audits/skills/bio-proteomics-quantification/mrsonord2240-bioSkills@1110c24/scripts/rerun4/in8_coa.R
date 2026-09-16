suppressPackageStartupMessages(library(MSnbase))
QW <- 'F:/OpenScience/audits/bio-proteomics-quantification/rerun4'
# Layout copied from MSnbase's own TMT6plexPurityCorrections.csv: a leading `Tag`
# column (read as row.names) then n neighbour-offset columns in percent.
n <- 16
tags <- reporterNames(TMT16)
offs <- c(seq(-n/2, -1), seq(1, n/2))
coa <- data.frame(Tag = tags)
for (o in offs) coa[[as.character(o)]] <- 0
coa[['-1']] <- c(0, seq(0.4, 2.0, length.out = n - 1))
coa[['1']]  <- seq(6.1, 2.1, length.out = n)
f <- file.path(QW, 'tmtpro16_coa.csv')
write.csv(coa, f, row.names = FALSE, quote = FALSE)
cat('CoA csv:', n, 'channels x', length(offs), 'offset columns + Tag\n')
cat(head(readLines(f), 3), sep='\n'); cat('\n')
imp16 <- tryCatch(makeImpuritiesMatrix(filename = f, edit = FALSE),
                  error = function(e) {cat('ERROR:', conditionMessage(e), '\n'); NULL})
if (!is.null(imp16)) {
  cat('impurity matrix:', paste(dim(imp16), collapse='x'),
      '| row sums all 1:', all(abs(rowSums(imp16) - 1) < 1e-9),
      '| dimnames set:', !is.null(rownames(imp16)), '\n')
  set.seed(1)
  e <- matrix(runif(300*16, 1e4, 1e6), nrow=300,
              dimnames=list(paste0('P',1:300), rownames(imp16)))
  ms <- new('MSnSet', exprs = e)
  pc <- tryCatch(purityCorrect(ms, imp16), error=function(e){cat('purityCorrect ERROR:', conditionMessage(e),'\n'); NULL})
  if (!is.null(pc)) cat('purityCorrect on a 16-channel MSnSet:',
      paste(dim(exprs(pc)), collapse='x'), '| negatives:', sum(exprs(pc) < 0), '\n')
}
# and the failure the Skill's comment does NOT mention: no Tag column
coa2 <- coa[, -1]
f2 <- file.path(QW, 'tmtpro16_coa_notag.csv')
write.csv(coa2, f2, row.names = FALSE, quote = FALSE)
r <- tryCatch({dim(makeImpuritiesMatrix(filename = f2, edit = FALSE))},
              error = function(e) conditionMessage(e))
cat('same CSV without the leading Tag column ->', paste(r, collapse=' '), '\n')
