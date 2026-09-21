# parse-check every R block of SKILL.md (run/blocks) and the shipped example
b <- "F:/OpenScience/audits/bio-outlier-splicing-detection/run"
for (f in c(list.files(file.path(b, "blocks"), pattern = "[.]R$", full.names = TRUE), file.path(b, "skill/examples/fraser2_rare_disease.R"))) {
  r <- try(parse(f), silent = TRUE)
  cat(basename(f), ":", if (inherits(r, "try-error")) paste("PARSE ERROR", conditionMessage(attr(r, "condition"))) else paste("parses,", length(r), "expressions"), "\n")
}
