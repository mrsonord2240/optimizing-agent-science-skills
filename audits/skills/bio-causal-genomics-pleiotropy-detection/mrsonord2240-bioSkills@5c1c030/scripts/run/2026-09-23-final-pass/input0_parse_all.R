root <- 'F:/OpenScience/wt/causal-genomics-pleiotropy-detection/causal-genomics/pleiotropy-detection'
files <- c(file.path(root, 'SKILL.md'), list.files(file.path(root, 'examples'), pattern='\\.R$', full.names=TRUE))
r_files <- files[grepl('\\.R$', files)]
for (f in r_files) parse(f)
cat('PARSE_OK=', length(r_files), ' R examples\n', sep='')
cat('ASSERTION: every shipped R example parses in R 4.4.3.\n')
