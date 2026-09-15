library(phangorn)
x <- phyDat(matrix(strsplit('ACGTACGTACGTACGTAAAAACGTACGTACGTACGTGGGG', '')[[1]], nrow = 2, byrow = TRUE,
                   dimnames = list(c('a', 'b'), NULL)), type = 'DNA')
for (m in c('JC69', 'F81', 'K80', 'HKY', 'GTR', 'LG')) {
  r <- try(dist.ml(x, model = m), silent = TRUE)
  cat(sprintf('dist.ml DNA model %-5s -> %s\n', m, if (inherits(r, 'try-error')) trimws(conditionMessage(attr(r, 'condition'))) else format(as.numeric(r))))
}
cat('phangorn NJ / upgma exported:', exists('NJ'), exists('upgma'), '\n')
