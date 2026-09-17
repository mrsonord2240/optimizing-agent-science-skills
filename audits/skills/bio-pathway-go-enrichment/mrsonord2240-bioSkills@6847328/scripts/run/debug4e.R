suppressPackageStartupMessages({library(clusterProfiler)})
f <- clusterProfiler:::simplify_ALL
cat('simplify_ALL exists:', is.function(f), '\n')
print(f)
