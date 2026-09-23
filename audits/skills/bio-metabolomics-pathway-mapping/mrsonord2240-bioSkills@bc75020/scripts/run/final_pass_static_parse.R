# Fresh Phase 2 structural checks for the exact audited source tree.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop("usage: final_pass_static_parse.R <skill-dir>")
skill_dir <- args[[1]]
scripts <- list.files(file.path(skill_dir, "scripts"), pattern = "\\.R$", full.names = TRUE)
stopifnot(length(scripts) == 5L)
for (script in scripts) parse(script)
skill <- readLines(file.path(skill_dir, "SKILL.md"), warn = FALSE)
refs <- list.files(file.path(skill_dir, "references"), pattern = "\\.md$", full.names = TRUE)
stopifnot(length(refs) == 3L, any(grepl("name: bio-metabolomics-pathway-mapping", skill, fixed = TRUE)))
stopifnot(all(file.exists(file.path(skill_dir, "scripts", c("map_compounds.R", "local_ora.R", "ora_api.R", "mummichog_psea.R", "fella_diffusion.R")))))
cat(sprintf("Parsed %d R scripts; verified %d reference files and required frontmatter.\n", length(scripts), length(refs)))
