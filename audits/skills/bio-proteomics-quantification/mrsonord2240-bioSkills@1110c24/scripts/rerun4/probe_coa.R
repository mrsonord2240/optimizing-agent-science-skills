suppressPackageStartupMessages(library(MSnbase))
f <- dir(system.file('extdata', package='MSnbase'), pattern='Purity', full.names=TRUE)
cat('templates:', basename(f), '\n')
for (x in f) { cat('---', basename(x), '---\n'); cat(readLines(x), sep='\n'); cat('\n') }
print(MSnbase::makeImpuritiesMatrix)
