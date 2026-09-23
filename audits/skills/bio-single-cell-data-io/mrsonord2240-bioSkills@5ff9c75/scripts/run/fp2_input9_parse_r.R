# Phase-2 Input 9 companion: parse every R code block extracted by fp2_input9_code_blocks.py.
files <- list.files('F:/OpenScience/audits/bio-single-cell-data-io/data/fp2_r_blocks', pattern='\\.R$', full.names=TRUE)
for (f in files) parse(f)
cat('r_blocks_parsed', length(files), '\n')
stopifnot(length(files) == 7L)
cat('PASS input9_R\n')
