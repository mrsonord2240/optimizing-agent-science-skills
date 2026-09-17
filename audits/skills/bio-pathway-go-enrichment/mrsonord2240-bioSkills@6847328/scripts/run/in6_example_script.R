# go-enrichment Input 6 (new, regression-tests fix claim #3): run the shipped
# examples/go_all_ontologies.R VERBATIM, unmodified, straight from the fork's copy of the
# Skill folder -- no synthetic data substituted -- to check it is genuinely self-contained
# now (the pre-fix version required an unshipped de_results.csv and could not be run at all).
t0 <- Sys.time()
res <- tryCatch({
  source('F:/OpenScience/audits/bio-pathway-go-enrichment/runs/skill_copy/examples/go_all_ontologies.R')
  'OK'
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[go_all_ontologies.R verbatim, as shipped] status:', res, '| elapsed s:', round(as.numeric(difftime(Sys.time(), t0, units='secs')),1), '\n')
out_csv <- file.path(tempdir(), 'go_all_simplified.csv')
cat('output file exists:', file.exists(out_csv), '\n')
if (file.exists(out_csv)) {
  d <- read.csv(out_csv)
  cat('rows:', nrow(d), '| columns:', paste(colnames(d), collapse=','), '\n')
  cat('distinct ONTOLOGY values in output:', paste(sort(unique(d$ONTOLOGY)), collapse=','), '\n')
}
