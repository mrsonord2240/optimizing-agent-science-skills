args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) stop("usage: run_candidate_section.R SECTION OUTPUT_JSON")

section_id <- as.integer(args[[1]])
output_json <- args[[2]]
root <- "/mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs"
candidate <- "/mnt/openscience/wt/opt10-adaptive-designs/skills/bio-clinical-biostatistics-adaptive-designs"
script <- file.path(candidate, "scripts", "adaptive_designs.R")

candidate_identity <- function() {
  paths <- list.files(candidate, recursive = TRUE, all.files = TRUE,
                      full.names = FALSE, no.. = TRUE)
  paths <- paths[!file.info(file.path(candidate, paths))$isdir]
  paths <- sort(chartr("\\", "/", paths), method = "radix")
  rows <- vapply(paths, function(path) {
    full <- file.path(candidate, path)
    paste(path, file.info(full)$size,
          digest::digest(full, algo = "sha256", file = TRUE), sep = "\t")
  }, character(1))
  manifest <- paste(rows, collapse = "\n")
  list(
    sha256 = digest::digest(manifest, algo = "sha256", serialize = FALSE),
    file_count = length(paths),
    manifest_bytes = nchar(manifest, type = "bytes")
  )
}

identity <- candidate_identity()
expected <- "73116b86978447d18f14945b236561b0685796da68f1a993420352c3c6953546"
if (!identical(identity$sha256, expected)) {
  stop("candidate identity drift: ", identity$sha256)
}

lines <- readLines(script, warn = FALSE)
starts <- grep("^# [0-9]+\\. ", lines)
ids <- as.integer(sub("^# ([0-9]+)\\..*$", "\\1", lines[starts]))
idx <- match(section_id, ids)
if (is.na(idx)) stop("unknown section: ", section_id)
end <- if (idx < length(starts)) starts[idx + 1L] - 1L else length(lines)
code <- lines[starts[idx]:end]

packages <- c(
  `1` = "gsDesign", `2` = "gsDesign", `3` = "rpact", `4` = "rpact",
  `5` = "BOIN", `6` = "dfcrm", `8` = "RBesT"
)
conceptual <- section_id %in% c(7L, 9L, 10L)
warnings <- character()
messages <- character()
error <- NULL
objects <- character()
elapsed <- 0
status <- if (conceptual) "DOCUMENTED_ONLY" else "NOT_RUN"

if (!conceptual) {
  package <- unname(packages[as.character(section_id)])
  suppressPackageStartupMessages(library(package, character.only = TRUE))
  env <- new.env(parent = globalenv())
  plot_file <- file.path(root, "evidence", sprintf("section-%02d-plot.pdf", section_id))
  grDevices::pdf(plot_file, width = 7, height = 5)
  started <- proc.time()[["elapsed"]]
  tryCatch(
    withCallingHandlers({
      exprs <- parse(text = code, keep.source = TRUE)
      for (expr in exprs) eval(expr, envir = env)
      status <- "PASS"
    }, warning = function(w) {
      warnings <<- c(warnings, conditionMessage(w))
      invokeRestart("muffleWarning")
    }, message = function(m) {
      messages <<- c(messages, conditionMessage(m))
      invokeRestart("muffleMessage")
    }),
    error = function(e) {
      error <<- conditionMessage(e)
      status <<- "ERROR"
    }
  )
  elapsed <- proc.time()[["elapsed"]] - started
  objects <- ls(env, all.names = TRUE)
  grDevices::dev.off()
  if (file.info(plot_file)$size == 3611L) unlink(plot_file)
}

jsonlite::write_json(list(
  section = section_id,
  heading = sub("^# ", "", lines[starts[idx]]),
  classification = if (conceptual) "conceptual-scaffold" else "candidate-executable",
  required_package = if (conceptual) NA_character_ else unname(packages[as.character(section_id)]),
  package_version = if (conceptual) NA_character_ else as.character(packageVersion(unname(packages[as.character(section_id)]))),
  candidate_identity = identity,
  status = status,
  elapsed_seconds = elapsed,
  warnings = warnings,
  messages = messages,
  error = error,
  objects_created = objects
), output_json, auto_unbox = TRUE, pretty = TRUE, null = "null")

if (identical(status, "ERROR")) quit(status = 1L)
