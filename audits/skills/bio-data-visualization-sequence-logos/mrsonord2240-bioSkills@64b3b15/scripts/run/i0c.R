library(ggseqlogo)
p <- ggseqlogo(c("ACG","ACT"))
print(class(p)); print(names(p)); print(class(p$data)); print(class(p$layers[[1]]$data)); str(p$layers[[1]]$data, max.level=1)
