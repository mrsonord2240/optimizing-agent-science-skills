out_dir <- "F:/OpenScience/audits/bio-pathway-reactome/run/out_ora"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
source("F:/OpenScience/audits/bio-pathway-reactome/run/skill_copy/examples/reactome_ora.R", echo = FALSE)
tf <- list.files(tempdir(), full.names = TRUE)
cat("\n--- tempdir contents after run ---\n")
print(tf)
for (f in tf) {
  info <- file.info(f)
  cat(basename(f), "size=", info$size, "\n")
}
file.copy(tf, out_dir, overwrite = TRUE)
cat("copied to", out_dir, "\n")
