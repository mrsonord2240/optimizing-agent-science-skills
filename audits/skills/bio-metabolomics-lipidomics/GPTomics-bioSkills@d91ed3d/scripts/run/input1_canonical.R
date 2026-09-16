# Input 1 (Canonical) -- exactly following bio-metabolomics-lipidomics SKILL.md's
# "Load, Normalize, and Run Differential Analysis (lipidr)" + the class-based
# internal-standard section, on the synthetic dataset with planted ground truth.
# User request: "Load my lipidomics table, normalize within class, and find
# lipids changing between groups between Control and Disease."
suppressMessages(library(lipidr))

raw <- read.csv("../data/synthetic_lipidomics_intensities.csv", check.names = FALSE)
d <- as_lipidomics_experiment(raw)
cat("Loaded LipidomicsExperiment:", nrow(d), "lipids x", ncol(d), "samples\n")
cat("Classes detected:", paste(unique(rowData(d)$Class), collapse = ", "), "\n")
cat("Flagged as internal standards by lipidr:",
    paste(rownames(d)[rowData(d)$istd], collapse = ", "), "\n\n")

d <- add_sample_annotation(d, "../data/synthetic_sample_annotation.csv")

# "normalize within class" -> class-based internal-standard normalization per SKILL.md
d_istd <- normalize_istd(d, measure = "Area", exclude = "blank", log = TRUE)

de_results <- de_analysis(d_istd, Disease - Control, measure = "Area")
sig <- significant_molecules(de_results, p.cutoff = 0.05, logFC.cutoff = 1)

cat("=== de_analysis results ===\n")
print(de_results[order(de_results$adj.P.Val),
                  c("Molecule", "Class", "logFC", "P.Value", "adj.P.Val")])

cat("\n=== Significant molecules (|log2FC|>1, adj.P<0.05) ===\n")
print(sig)

cat("\n=== Ground-truth check ===\n")
planted_up   <- c("PC 34:1", "PC 36:2", "TG 52:3")
planted_down <- c("PE 36:2")
planted_flat <- c("PC 32:0", "PC 16:0/18:1", "PE 34:1", "TG 54:4",
                   "Cer 18:1;O2/16:0", "LPC 16:0")
cat("Planted UP recovered as significant:",
    paste(planted_up[planted_up %in% sig], collapse = ", "), "\n")
cat("Planted DOWN recovered as significant:",
    paste(planted_down[planted_down %in% sig], collapse = ", "), "\n")
cat("Planted FLAT falsely flagged significant (should be none):",
    paste(planted_flat[planted_flat %in% sig], collapse = "(none)"), "\n")

out_dir <- "../data"
volcano <- plot_results_volcano(de_results, show.labels = FALSE)
ggplot2::ggsave(file.path(out_dir, "input1_volcano.png"), volcano, width = 7, height = 5)
write.csv(de_results, file.path(out_dir, "input1_de_results.csv"), row.names = FALSE)
cat("\nSaved input1_de_results.csv and input1_volcano.png\n")
