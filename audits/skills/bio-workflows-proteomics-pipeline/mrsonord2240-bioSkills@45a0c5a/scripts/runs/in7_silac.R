# Pipeline Input 7 (adversarial): "just t-test my SILAC ratios against zero for all proteins". SKILL.md SILAC block verbatim. SYNTHETIC.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'runs', 'work7'))
blk <- list.files(file.path(PP, 'runs', 'blocks'), pattern = '^b04', full.names = TRUE)
res <- tryCatch({ sys.source(blk, envir = globalenv()); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[SILAC block verbatim]', res, '\n')
cat('ratio columns found:', if (exists('ratio_cols')) paste(ratio_cols, collapse = ',') else 'n/a', '\n')
if (exists('results')) cat('p-values:', length(results), '| NA:', sum(is.na(results)), '| raw p<0.05:', sum(results < 0.05, na.rm = TRUE), '| any multiple-testing correction in block: FALSE\n')
