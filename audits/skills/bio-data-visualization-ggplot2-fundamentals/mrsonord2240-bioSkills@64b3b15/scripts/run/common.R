# shared helpers for the ggplot2-fundamentals audit (2026-09-20)
suppressPackageStartupMessages({library(ggplot2)})
GGV <- as.character(packageVersion("ggplot2"))
RUN <- "F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/run"
OUT <- file.path(RUN, paste0("out_", GGV)); dir.create(OUT, showWarnings = FALSE, recursive = TRUE)
DATA <- "F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/data"
DE <- "F:/OpenScience/audit-envs/data-visualization/public-data/differential-expression/airway_dex_deseq2_results.csv"
cat("ggplot2", GGV, "\n")

png_info <- function(f) {
  im <- png::readPNG(f); d <- dim(im)
  nonwhite <- mean(apply(im[,,1:3, drop=FALSE], c(1,2), function(v) any(v < 0.98)))
  cat(sprintf("PNG %s: %d bytes, %d x %d px, nonwhite %.3f\n", basename(f), file.size(f), d[2], d[1], nonwhite))
  invisible(list(w=d[2], h=d[1], nonwhite=nonwhite))
}
# PDF inspector: shells out to pdfinfo.py (decompresses object streams) via the env's py.sh
pdf_info <- function(f) {
  out <- system2("F:/OpenScience/audit-envs/data-visualization/Scripts/python.exe", c(file.path(RUN, "pdfinfo.py"), shQuote(f)), stdout = TRUE)
  cat(out, sep = "\n"); invisible(out)
}
chk <- function(label, cond) { cat(sprintf("[%s] %s\n", if (isTRUE(cond)) "PASS" else "FAIL", label)); invisible(isTRUE(cond)) }
