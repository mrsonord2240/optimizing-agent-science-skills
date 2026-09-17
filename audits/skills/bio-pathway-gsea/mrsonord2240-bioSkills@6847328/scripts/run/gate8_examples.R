# Gate 8 -- run both shipped examples verbatim from the read-only clone, to confirm the fix log's
# claim that they now plant a real signal instead of returning zero terms by construction.
# Only .libPaths() is set; nothing inside F:\OpenScience\external\ is written.

skill_dir <- "F:/OpenScience/external/mrsonord2240__bioSkills/pathway-analysis/gsea/examples"

cat("================ gsea_go.R (exists:", file.exists(file.path(skill_dir, "gsea_go.R")), ") ================\n")
t0 <- Sys.time()
source(file.path(skill_dir, "gsea_go.R"), local = new.env())
t1 <- Sys.time()
cat("[ gsea_go.R ] COMPLETED -", round(as.numeric(difftime(t1,t0,units="secs")),1), "s\n")

cat("\n================ gsea_msigdb.R (exists:", file.exists(file.path(skill_dir, "gsea_msigdb.R")), ") ================\n")
t0 <- Sys.time()
source(file.path(skill_dir, "gsea_msigdb.R"), local = new.env())
t1 <- Sys.time()
cat("[ gsea_msigdb.R ] COMPLETED -", round(as.numeric(difftime(t1,t0,units="secs")),1), "s\n")
