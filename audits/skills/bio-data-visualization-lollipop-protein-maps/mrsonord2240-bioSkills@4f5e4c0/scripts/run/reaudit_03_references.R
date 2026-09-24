# Verify cited TP53 coordinates/transcript and package semantics for the fixed skill.
# Usage: r.sh reaudit_03_references.R <worktree> <outdir>
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2L)
worktree <- normalizePath(args[[1L]], winslash = "/", mustWork = TRUE)
out <- normalizePath(args[[2L]], winslash = "/", mustWork = FALSE)
dir.create(out, recursive = TRUE, showWarnings = FALSE)
suppressPackageStartupMessages({library(jsonlite); library(maftools)})

skill <- paste(readLines(file.path(worktree, "data-visualization", "lollipop-protein-maps", "SKILL.md"), warn = FALSE), collapse = "\n")
stopifnot(as.character(packageVersion("maftools")) == "2.22.0")
stopifnot(grepl("bundled domain table", skill), grepl("not a live Pfam query", skill), grepl("printCount=TRUE.*prints a table", skill), grepl("returns a data table, not a ggplot object", skill))

# Fresh public reference checks. UniProt feature coordinates are inclusive.
u <- fromJSON("https://rest.uniprot.org/uniprotkb/P04637.json")
feat <- u$features
stopifnot(identical(as.integer(u$sequence$length), 393L))
cat("UNIPROT_FEATURES\n")
print(feat[grepl("Transcription activation|Oligomerization|^Basic", feat$description, ignore.case = TRUE), c("type", "description", "location")])
pick_pattern <- function(pattern, start, end) any(grepl(pattern, feat$description, ignore.case = TRUE) & as.integer(feat$location$start$value) == start & as.integer(feat$location$end$value) == end)
stopifnot(pick_pattern("Transcription activation", 1L, 44L), pick_pattern("Oligomerization", 325L, 356L), pick_pattern("^Basic", 368L, 387L))
stopifnot(grepl("IRanges\\(c\\(1, 102, 325, 368\\), c\\(44, 292, 356, 387\\)", skill))

ens <- fromJSON("https://rest.ensembl.org/lookup/id/ENST00000269305?content-type=application/json")
stopifnot(identical(ens$id, "ENST00000269305"), grepl("TP53", ens$display_name, fixed = TRUE))

cat("REFERENCE_PASS_WITH_DNA_ATTRIBUTION_NOTE\n")
cat("maftools=", as.character(packageVersion("maftools")), " TP53_length=", u$sequence$length, " transcript=", ens$id, " display_name=", ens$display_name, "\n", sep = "")
cat("Current UniProt P04637 JSON exposes DNA interaction at 273-280, but not a 102-292 feature labelled DNA-binding; the Skill's 102-292 range needs an explicit non-UniProt source or neutral attribution.\n")
