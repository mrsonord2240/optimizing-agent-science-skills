# Run the exact committed R example in an isolated output directory.
src <- "F:/OpenScience/wt/data-visualization-upset-plots/data-visualization/upset-plots/examples/upset_gene_sets.R"
out <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/run/reaudit_20260923/out/r_example"
stopifnot(file.exists(src), dir.exists(out)); setwd(out)
source(src, echo = FALSE)
files <- c("upset_basic.pdf", "upset_customized.pdf", "upset_queries.pdf")
stopifnot(all(file.exists(files)), all(file.info(files)$size > 2000L))
cat("PASS exact R example: three nonempty named Cairo PDFs\n")
