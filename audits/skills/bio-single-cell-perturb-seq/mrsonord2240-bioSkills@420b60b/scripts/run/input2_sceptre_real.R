priv_lib <- 'F:/OpenScience/audits/bio-single-cell-perturb-seq/run/R-private-lib'
.libPaths(c(priv_lib, 'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))

# Input 2 (Variant A) re-audit: "Test each perturbation with SCEPTRE, running a calibration
# check (negative controls) before the discovery analysis." Follows the FIXED SKILL.md's
# "SCEPTRE: Calibrated Testing (R)" section. The original audit and the fix both reported
# sceptre as uninstallable under R 4.4.3 ("requires R >= 4.5"). Independent finding of this
# re-audit: sceptre is NOT on CRAN/Bioconductor at all (both 404); it is GitHub-only
# (Katsevich-Lab/sceptre) and its own DESCRIPTION states R (>= 4.1), not R (>= 4.5) -- verified
# by installing it here under this env's real R 4.4.3 via remotes::install_github (succeeded,
# sceptre 0.99.0, library(sceptre) loads). Using sceptre's own bundled low-MOI example data to
# actually execute the workflow SKILL.md documents, real code, not synthetic invention.
library(sceptre)
data(lowmoi_example_data)
cat("lowmoi_example_data components:", names(lowmoi_example_data), "\n")

response_matrix <- lowmoi_example_data$response_matrix
grna_matrix <- lowmoi_example_data$grna_matrix
grna_target_data_frame <- lowmoi_example_data$grna_target_data_frame
extra_covariates <- lowmoi_example_data$extra_covariates
response_names <- rownames(response_matrix)

cat("response_matrix dim:", dim(response_matrix), "\n")
cat("grna_matrix dim:", dim(grna_matrix), "\n")
cat("grna_target_data_frame head:\n"); print(head(grna_target_data_frame))

sceptre_object <- import_data(
  response_matrix = response_matrix,
  grna_matrix = grna_matrix,
  grna_target_data_frame = grna_target_data_frame,
  moi = "low",
  extra_covariates = extra_covariates
)
# lowmoi_example_data has no chr/start/end columns, so construct_cis_pairs (a cis-window helper)
# does not apply here; build discovery pairs directly (grna_target x response_id), the schema
# set_analysis_parameters expects, over the non-control targets.
targets <- setdiff(unique(grna_target_data_frame$grna_target), "non-targeting")
discovery_pairs <- expand.grid(grna_target = targets, response_id = response_names[1:20],
                                stringsAsFactors = FALSE)
cat("\ndiscovery_pairs:", nrow(discovery_pairs), "pairs\n")
sceptre_object <- set_analysis_parameters(sceptre_object, discovery_pairs = discovery_pairs)
sceptre_object <- assign_grnas(sceptre_object, method = "mixture")  # SKILL.md's documented default method
sceptre_object <- run_qc(sceptre_object)
sceptre_object <- run_calibration_check(sceptre_object)
cc <- get_result(sceptre_object, analysis = "run_calibration_check")
cat("\ncalibration check result rows:", nrow(cc), "\n")
print(head(cc))

sceptre_object <- run_discovery_analysis(sceptre_object)
disc <- get_result(sceptre_object, analysis = "run_discovery_analysis")
cat("\ndiscovery analysis result rows:", nrow(disc), "\n")
print(head(disc))
cat("\nn significant (p_value < 0.05):", sum(disc$p_value < 0.05, na.rm = TRUE), "/", nrow(disc), "\n")

cat("\nDONE input2_sceptre_real\n")
