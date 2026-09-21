# Input 4: the shipped examples/volcano_phd.R run VERBATIM (source()) with a `dds` in the workspace, in a scratch cwd. Two datasets:
#   (a) airway with Ensembl rownames as delivered; (b) same fit, rownames converted to gene symbols (what a user with named genes has).
suppressMessages({library(DESeq2)})
D <- "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots"
o <- readRDS(file.path(D, "data/airway_objs.rds")); dds0 <- o$dds; sym <- o$sym
fails <- 0; chk <- function(name, ok, note="") { cat(sprintf("[%s] %s %s\n", if (ok) "PASS" else "FAIL", name, note)); if (!ok) fails <<- fails + 1 }
run_example <- function(dds, tag) {
  wd <- file.path(D, "run/scratch4", tag); dir.create(wd, showWarnings = FALSE, recursive = TRUE); old <- setwd(wd); on.exit(setwd(old))
  env <- new.env(); env$dds <- dds
  w <- character()
  png(file.path(D, "figs", paste0("i4_", tag, "_enhancedvolcano.png")), 1600, 1200, res = 200)
  withCallingHandlers(
    { sys.source(file.path(D, "run/skill/examples/volcano_phd.R"), envir = env, keep.source = FALSE)
      print(env$p_volcano); },   # (sys.source does not auto-print the EnhancedVolcano value; print the last call explicitly below)
    warning = function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") })
  dev.off()
  cat("[", tag, "] warnings:", length(w), "\n"); print(unique(substr(w, 1, 140)))
  env
}
# ---- (a) Ensembl
envA <- run_example(dds0, "ensembl")
cat("files written:", paste(list.files(file.path(D, "run/scratch4/ensembl")), collapse = ", "), "\n")
# ---- (b) symbols
ok <- !is.na(sym[rownames(dds0)]) & !duplicated(sym[rownames(dds0)]) & !duplicated(sym[rownames(dds0)], fromLast = TRUE)
newn <- sym[rownames(dds0)][ok]; dds1 <- dds0[ok, ]; rownames(dds1) <- newn
envB <- run_example(dds1, "symbols")
for (tag in c("ensembl", "symbols")) {
  e <- if (tag == "ensembl") envA else envB
  cat("\n=====", tag, "=====\n")
  rd <- e$res_df
  cat("genes:", nrow(rd), " Up:", sum(rd$significance == "Up"), " Down:", sum(rd$significance == "Down"), "\n")
  lab <- e$labels; cat("labels requested (", length(lab), "):", paste(lab, collapse = ","), "\n")
  gi <- e$genes_of_interest; cat("genes_of_interest present in data:", paste(gi[gi %in% rd$gene], collapse = ","), "| absent:", paste(gi[!gi %in% rd$gene], collapse = ","), "\n")
  # y cap effect
  ycap <- e$y_cap; above <- which(!is.na(rd$neg_log10_p) & rd$neg_log10_p > ycap)
  cat(sprintf("points with -log10 p > y_cap(%g): %d of %d; among them Up/Down: %d; labelled ones above cap: %d of %d labelled\n", ycap, length(above), nrow(rd),
      sum(rd$significance[above] != "NS"), sum(rd$label[above] != ""), sum(rd$label != "")))
  cat("max -log10 p:", round(max(rd$neg_log10_p, na.rm = TRUE), 1), "\n")
  chk(paste(tag, ": no significant gene is hidden by the y cap (Skill: 'without losing data')"), length(above) == 0, paste0("hidden Up/Down: ", sum(rd$significance[above] != "NS")))
  b <- ggplot_build(e$p_volcano); hl <- b$data[[3]]$yintercept
  cat("hline y:", hl, " | coord ylim:", b$layout$panel_params[[1]]$y.range, "\n")
  chk(paste(tag, ": drawn hline coincides with padj<0.05 boundary on the -log10 p axis"),
      abs(hl - (-log10(max(rd$pvalue[!is.na(rd$padj) & rd$padj < .05])))) < 0.05,
      sprintf("line=%.2f; true boundary=%.2f", hl, -log10(max(rd$pvalue[!is.na(rd$padj) & rd$padj < .05]))))
  # outputs
  wd <- file.path(D, "run/scratch4", tag)
  for (f in c("volcano.pdf", "ma_plot.pdf")) { p <- file.path(wd, f); cat(f, "exists:", file.exists(p), " size:", file.size(p), "\n")
    rw <- readBin(p, "raw", file.size(p)); rw[rw == as.raw(0)] <- as.raw(32); rw[rw > as.raw(126)] <- as.raw(32); txt <- rawToChar(rw); mb <- regmatches(txt, regexpr("MediaBox.{0,40}", txt)); cat("  ", mb, " fonts TrueType:", lengths(regmatches(txt, gregexpr("/TrueType", txt))), " Type3:", lengths(regmatches(txt, gregexpr("/Type3", txt))), "
") }
}
cat("\nSUMMARY fails =", fails, "\n")
