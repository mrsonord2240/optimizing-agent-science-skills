library(ReactomePA)

captured <- tryCatch({
  enrichPathway(gene = c('1', '2'), organism = 'ecoli')
  list(error = FALSE, message = 'no error')
}, error = function(e) list(error = TRUE, message = conditionMessage(e)))
stopifnot(isTRUE(captured$error), nzchar(captured$message))
writeLines(captured$message,
           '/mnt/openscience/audits/bio-pathway-reactome/run/phase2_e66cde9_linux_20260923/outputs/input07_invalid_organism.txt')
cat('ASSERT invalid_organism_rejected=TRUE\n')
cat('ASSERT invalid_organism_message_nonempty=TRUE\n')
cat('ASSERT invalid_organism_message=', captured$message, '\n', sep = '')
