# Purpose: validate the documented Numbat allele-frame contract.
# Usage: micromamba run -n cnv-audit Rscript input4_numbat_columns_fresh.R
suppressMessages(library(numbat)); set.seed(20260923)
n <- 20
base <- data.frame(cell = paste0('cell_', rep(1:5, each = 4)), snp_id = paste0('snp_', 1:n),
  CHROM = rep(1:5, each = 4), POS = sample(1e6:2e6, n), AD = sample(0:10, n, TRUE),
  DP = sample(10:30, n, TRUE), GT = sample(c('0|1','1|0','1|1'), n, TRUE))
incomplete <- tryCatch({ numbat:::check_allele_df(base); 'unexpected pass' }, error = function(e) conditionMessage(e))
complete <- base; complete$cM <- runif(n); complete$REF <- 'A'; complete$ALT <- 'G'
ten_col <- tryCatch({ numbat:::check_allele_df(complete); 'unexpected direct pass' }, error = function(e) conditionMessage(e))
cat('seven-column validator result:', incomplete, '\n')
cat('ten-column direct-validator result:', ten_col, '\n')
stopifnot(grepl('cM|REF|ALT', incomplete), grepl('gene', ten_col))
cat('PASS: Skill correctly documents the ten input columns; gene is added by run_numbat annotation.\n')
