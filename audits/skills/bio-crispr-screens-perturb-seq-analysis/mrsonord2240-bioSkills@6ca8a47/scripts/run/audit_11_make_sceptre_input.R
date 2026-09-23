# Fresh minimal file-input fixture for shipped_run_sceptre.R.
library(sceptre)
data(lowmoi_example_data, package = "sceptre")
inp <- lowmoi_example_data
tmp <- import_data(inp$response_matrix, inp$grna_matrix, inp$grna_target_data_frame,
                   moi = "low", extra_covariates = inp$extra_covariates)
inp$discovery_pairs <- head(construct_trans_pairs(tmp), 3)
saveRDS(inp, "F:/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/data/sceptre_file_input.rds")
cat("pairs=", nrow(inp$discovery_pairs), "\n", sep = "")
