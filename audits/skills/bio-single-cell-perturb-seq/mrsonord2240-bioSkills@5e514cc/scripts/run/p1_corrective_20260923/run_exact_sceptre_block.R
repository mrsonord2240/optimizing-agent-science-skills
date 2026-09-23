private_lib <- "F:/OpenScience/audits/bio-single-cell-perturb-seq/run/p1_corrective_20260923/R-private-lib"
.libPaths(c(private_lib, "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib", .libPaths()))
library(sceptre)
data(lowmoi_example_data, package = "sceptre")
rna_counts <- lowmoi_example_data$response_matrix
grna_counts <- lowmoi_example_data$grna_matrix
grna_targets <- lowmoi_example_data$grna_target_data_frame
extra_covariates <- lowmoi_example_data$extra_covariates
seed_obj <- import_data(response_matrix = rna_counts, grna_matrix = grna_counts,
                        grna_target_data_frame = grna_targets, moi = "low",
                        extra_covariates = extra_covariates)
pairs <- head(construct_trans_pairs(seed_obj), 4)

obj <- import_data(response_matrix = rna_counts, grna_matrix = grna_counts,
                   grna_target_data_frame = grna_targets, moi = "low",
                   extra_covariates = extra_covariates)
obj <- set_analysis_parameters(obj, discovery_pairs = pairs)
obj <- assign_grnas(obj, method = "mixture")
obj <- run_qc(obj)
obj <- run_calibration_check(obj)
calibration <- get_result(obj, analysis = "run_calibration_check")
stopifnot(nrow(calibration) > 0)
obj <- run_discovery_analysis(obj)
results <- get_result(obj, analysis = "run_discovery_analysis")
stopifnot(nrow(results) == nrow(pairs))
write.table(calibration, "F:/OpenScience/audits/bio-single-cell-perturb-seq/run/p1_corrective_20260923/calibration.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
write.table(results, "F:/OpenScience/audits/bio-single-cell-perturb-seq/run/p1_corrective_20260923/discovery.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
cat("PASS exact block sceptre=", as.character(packageVersion("sceptre")),
    " calibration=", nrow(calibration), " discovery=", nrow(results), "\n", sep = "")
