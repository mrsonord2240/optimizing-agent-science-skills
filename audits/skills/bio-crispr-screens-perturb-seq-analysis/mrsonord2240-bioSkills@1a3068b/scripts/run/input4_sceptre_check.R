# Input 4 (Variant B) -- sanity-check the Skill's documented sceptre pipeline API
# (SKILL.md 'SCEPTRE for Low-MOI Differential Expression') against installed sceptre 0.99.0.
library(sceptre)

cat("sceptre version:", as.character(packageVersion("sceptre")), "\n")
cat("Functions the Skill documents, checking existence:\n")
fns <- c("import_data", "set_analysis_parameters", "assign_grnas", "run_qc",
         "run_calibration_check", "run_discovery_analysis", "get_result")
for (f in fns) {
  cat(sprintf("  %-25s exists: %s\n", f, exists(f, where = asNamespace("sceptre"), inherits = FALSE) || exists(f)))
}

cat("\nRunning sceptre's own bundled low-MOI example data end-to-end...\n")
data(lowmoi_example_data, package = "sceptre")

sceptre_object <- import_data(
  response_matrix = lowmoi_example_data$response_matrix,
  grna_matrix = lowmoi_example_data$grna_matrix,
  grna_target_data_frame = lowmoi_example_data$grna_target_data_frame,
  moi = "low",
  extra_covariates = lowmoi_example_data$extra_covariates
)
cat("import_data() OK\n")
print(sceptre_object)

discovery_pairs <- construct_trans_pairs(sceptre_object)
sceptre_object <- set_analysis_parameters(sceptre_object, discovery_pairs = discovery_pairs)
cat("set_analysis_parameters() OK\n")

sceptre_object <- assign_grnas(sceptre_object)
cat("assign_grnas() OK\n")

sceptre_object <- run_qc(sceptre_object)
cat("run_qc() OK\n")

sceptre_object <- run_calibration_check(sceptre_object, n_calibration_pairs = 50)
cat("run_calibration_check() OK\n")
calib_result <- get_result(sceptre_object, analysis = "run_calibration_check")
cat("Calibration result rows:", nrow(calib_result), "\n")
print(head(calib_result))

sceptre_object <- run_discovery_analysis(sceptre_object)
cat("run_discovery_analysis() OK\n")
results <- get_result(sceptre_object, analysis = "run_discovery_analysis")
cat("Discovery result rows:", nrow(results), "\n")
print(head(results))
cat("\nColumn names:", paste(colnames(results), collapse=", "), "\n")
