b <- "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots/run"
for (f in c(list.files(file.path(b, "blocks"), "[.]R$", full.names = TRUE), file.path(b, "skill/examples/volcano_phd.R"))) { invisible(parse(f)); cat("parses:", basename(f), "\n") }
