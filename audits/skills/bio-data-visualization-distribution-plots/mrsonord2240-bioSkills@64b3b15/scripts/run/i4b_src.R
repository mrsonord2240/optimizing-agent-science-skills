suppressMessages({library(ggplot2); library(introdataviz)})
print(ls(asNamespace("introdataviz")))
print(introdataviz::geom_split_violin)
g <- get("GeomSplitViolin", envir=asNamespace("introdataviz")) 
