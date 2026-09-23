# Purpose: execute the corrective validation of copyKAT's genome selector.
# Usage: micromamba run -n cnv-audit Rscript input9_copykat_selector_fresh.R
suppressMessages(library(copykat))
f <- get('copykat', envir = asNamespace('copykat'))
default <- formals(f)$genome
body_text <- paste(deparse(body(f)), collapse = '\n')
cat('copyKAT version:', as.character(packageVersion('copykat')), '\n')
cat('genome default:', default, '\n')
cat('has hg20 branch:', grepl('hg20', body_text, fixed = TRUE), '\n')
cat('has mm10 branch:', grepl('mm10', body_text, fixed = TRUE), '\n')
cat('has hg19 branch:', grepl('hg19', body_text, fixed = TRUE), '\n')
stopifnot(identical(default, 'hg20'), grepl('hg20', body_text, fixed = TRUE),
  grepl('mm10', body_text, fixed = TRUE), !grepl('hg19', body_text, fixed = TRUE))
cat('PASS: v1.2.5 accepts the documented hg20/mm10 selector set; hg19 is not an accepted branch.\n')
