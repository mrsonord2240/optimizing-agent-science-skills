library(ape)
src <- paste(deparse(dist.dna), collapse = ' ')
m <- regmatches(src, regexpr('MODELS <- c\\([^)]*\\)', src))
cat(m, '\n')
x <- as.DNAbin(matrix(strsplit(c('ACGTACGTACGTACGTAAAA', 'ACGTACGTACGTACGTGGGG'), '')[[1]], nrow = 2, byrow = TRUE,
                      dimnames = list(c('a', 'b'), NULL)))
for (mod in c('raw', 'N', 'TS', 'TV', 'JC69', 'K80', 'TN93', 'logdet', 'paralin', 'indel')) {
  r <- try(dist.dna(x, model = mod), silent = TRUE)
  cat(sprintf('%-8s -> %s\n', mod, if (inherits(r, 'try-error')) conditionMessage(attr(r, 'condition')) else format(as.numeric(r))))
}
r <- try(dist.dna(x, model = 'logdet', gamma = 0.5), silent = TRUE)
cat('logdet+gamma ->', if (inherits(r, 'try-error')) conditionMessage(attr(r, 'condition')) else format(as.numeric(r)), '\n')
