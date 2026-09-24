# staging helpers: build a Salmon dir from a source dir, renaming samples to shuffled SRR-style IDs (no symlinks: copies)
stage_salmon <- function(wd, from_ids, new_ids, cond, extra = NULL, src = file.path(SYN, "salmon_quant"),
                         gtf = file.path(SYN, "annotation.gtf"), fa = file.path(SYN, "transcripts.fa")) {
  unlink(wd, recursive = TRUE); dir.create(file.path(wd, "salmon_quant"), recursive = TRUE)
  for (k in seq_along(from_ids)) { d <- file.path(wd, "salmon_quant", new_ids[k]); dir.create(d)
    file.copy(file.path(src, from_ids[k], "quant.sf"), file.path(d, "quant.sf")) }
  meta <- data.frame(sample_id = new_ids, condition = cond, stringsAsFactors = FALSE)
  if (!is.null(extra)) meta <- cbind(meta, extra)
  meta <- meta[sample(nrow(meta)), ]                       # metadata rows shuffled too
  write.table(meta, file.path(wd, "sample_metadata.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
  file.copy(gtf, file.path(wd, "annotation.gtf")); file.copy(fa, file.path(wd, "transcripts.fa"))
  invisible(meta)
}
# run a Skill block verbatim (echo off) in the current dir
run_block <- function(f) source(file.path("F:/OpenScience/audits/bio-isoform-switching/run/blocks", f), echo = FALSE, local = FALSE)
# hit-list scorer on planted truth for arbitrary truth table t (columns gene_id, type, IF_*_ctrl/_trt)
dir_mag <- function(f, t, genes) {
  ok_dir <- 0; ok_mag <- 0
  for (g in genes) { tt <- t[t$gene_id == g, ]; iso <- if (tt$type == "poison_switch") paste0(g, "_B") else paste0(g, "_C")
    tru <- if (tt$type == "poison_switch") tt$IF_B_trt - tt$IF_B_ctrl else tt$IF_C_trt - tt$IF_C_ctrl
    row <- f[f$isoform_id == iso, ]; ok_dir <- ok_dir + as.integer(row$dIF > 0); ok_mag <- ok_mag + as.integer(abs(row$dIF - tru) < 0.1) }
  c(dir = ok_dir, mag = ok_mag, n = length(genes))
}

# run part 1 (before the marker line) or part 2 (from the marker line) of a Skill block verbatim
run_block_part <- function(f, part, marker = "after running the external tools") {
  txt <- readLines(file.path("F:/OpenScience/audits/bio-isoform-switching/run/blocks", f)); i <- grep(marker, txt, fixed = TRUE)[1]
  stopifnot(!is.na(i)); code <- if (part == 1) txt[seq_len(i - 1)] else txt[i:length(txt)]
  eval(parse(text = code), envir = globalenv()) }
