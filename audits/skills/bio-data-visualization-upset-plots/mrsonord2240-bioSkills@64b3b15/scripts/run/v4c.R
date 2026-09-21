suppressMessages({library(UpSetR); library(grid)})
source("F:/OpenScience/audits/bio-data-visualization-upset-plots/run/helpers.R")
sets <- list(A=c("g1","g2","g3","g4"), B=c("g2","g3","g5"), C=c("g3","g6"))
x <- upset(fromList(sets), nsets=3, order.by="freq")
mt <- walk_grobs(x$Matrix)$items; pts <- Filter(function(i) i$cls == "points", mt)[[1]]$g
print(data.frame(x = as.numeric(pts$x), y = as.numeric(pts$y), col = pts$gp$col))
print(class(pts$x)); print(pts$gp$col[1:15])
e <- extract_upsetr(x); print(e)
