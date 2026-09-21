o <- readRDS("F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots/data/airway_objs.rds")
write.csv(data.frame(symbol = unname(o$sym), row.names = names(o$sym)), "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots/data/airway_symbols.csv")
