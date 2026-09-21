suppressMessages({library(UpSetR); library(ggplot2)})
sets <- list(A=c("g1","g2","g3","g4"), B=c("g2","g3","g5"), C=c("g3","g6"))
x <- upset(fromList(sets), nsets=3, order.by="freq")
for (n in c("Main_bar","Matrix","Sizes","New_data")) { cat(n, ":", class(x[[n]]), "\n") }
mb <- x$Main_bar; b <- suppressWarnings(ggplot_build(mb))
cat("Main_bar layers:", paste(sapply(mb$layers, function(l) class(l$geom)[1]), collapse=","), "\n")
for (k in seq_along(b$data)) { cat("layer", k, "\n"); print(head(b$data[[k]], 8)) }
print(x$New_data)
cat("Matrix layers:", paste(sapply(x$Matrix$layers, function(l) class(l$geom)[1]), collapse=","), "\n")
bm <- suppressWarnings(ggplot_build(x$Matrix)); for (k in seq_along(bm$data)) { cat("mlayer", k, "\n"); print(head(bm$data[[k]], 10)) }
bs <- suppressWarnings(ggplot_build(x$Sizes)); print(bs$data[[1]][, c("x","y","ymin","ymax")])
print(bs$layout$panel_scales_x[[1]]$get_labels())
