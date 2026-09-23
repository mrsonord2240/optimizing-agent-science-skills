files <- c(
  "F:/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/run/shipped_run_sceptre.R",
  "F:/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/run/audit_11_make_sceptre_input.R"
)
for (f in files) parse(f)
cat("r_parse_passed=", length(files), "\n", sep = "")
