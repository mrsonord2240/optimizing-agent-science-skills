suppressMessages(library(lipidr))
example_path <- 'F:/OpenScience/wt/metabolomics-lipidomics/metabolomics/lipidomics/examples/lipidomics_workflow.R'
source(example_path, echo = FALSE)
stopifnot(exists('de_results'), exists('results_table'), exists('out_dir'))
expected <- c('Molecule', 'Class', 'total_cl', 'total_cs', 'logFC', 'P.Value', 'adj.P.Val')
stopifnot(identical(names(results_table), expected))
outputs <- c('lipid_volcano.png', 'lipid_class_enrichment.png', 'lipidomics_de_results.csv')
paths <- file.path(out_dir, outputs)
sizes <- file.info(paths)$size
print(data.frame(file = outputs, bytes = sizes))
stopifnot(all(file.exists(paths)), all(sizes > 1000), nrow(results_table) > 0)
cat(sprintf('PASS shipped_workflow rows=%d significant=%d output_dir=%s\n', nrow(results_table), length(sig), out_dir))
