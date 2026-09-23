# Install only the omitted Suggests dependency into a Phase 2 private overlay.
overlay <- "/home/sci/.local/share/openscience-pathway-enrichment-phase2-overlay-20260923"
dir.create(overlay, recursive = TRUE, showWarnings = FALSE)
install.packages("ggupset", lib = overlay, repos = "https://cloud.r-project.org", dependencies = NA)
library(ggupset, lib.loc = overlay)
cat("ggupset=", as.character(packageVersion("ggupset", lib.loc = overlay)), "\n", sep = "")
