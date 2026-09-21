suppressMessages({library(UpSetR); library(grid)})
source("F:/OpenScience/audits/bio-data-visualization-upset-plots/run/helpers.R")
sets <- list(A=c("g1","g2","g3","g4"), B=c("g2","g3","g5"), C=c("g3","g6"))
x <- upset(fromList(sets), nsets=3, order.by="freq")
for (n in c("Main_bar","Matrix","Sizes")) {
  a <- walk_grobs(x[[n]]); cat("==", n, "\n"); print(table(sapply(a$items, function(i) i$cls)))
  for (i in a$items) if (i$cls %in% c("text","titleGrob")) { cat(i$name, ": ", paste(tryCatch(as.character(i$g$label), error=function(e) "?"), collapse=","), " x=", paste(round(tryCatch(as.numeric(i$g$x), error=function(e) NA),3), collapse=","), "\n") }
}
print(x$New_data)
