library(ReactomePA)
z <- try(enrichPathway(c('1','2'),organism='ecoli'),silent=TRUE)
stopifnot(inherits(z,'try-error') || is.null(z))
cat('ASSERT unsupported_organism_no_result\n')
