# New-surface probe: default top_n = NULL heuristic with 8-char boundary and NA / missing labels among the smallest padj.
a <- commandArgs(TRUE); skill <- a[1]
suppressMessages({library(ggplot2); library(ggrepel); library(patchwork)})
cat("ggplot2", as.character(packageVersion("ggplot2")), "\n")
chk <- function(l, c) cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l)); flush(stdout())
suppressMessages(source(file.path(skill, "scripts/publication_figures.R")))
raw <- read.csv("F:/OpenScience/audit-envs/data-visualization/public-data/derived/airway_dex_deseq2_results_symbol.csv")
tmp <- raw; tmp$l8 <- sprintf("G%07d", seq_len(nrow(tmp))); tmp$l9 <- sprintf("G%08d", seq_len(nrow(tmp)))
chk("8-char labels -> 10 labels", sum(create_volcano(tmp, label_col = "l8")$data$label != "") == 10)
chk("9-char labels -> 3 labels", sum(create_volcano(tmp, label_col = "l9")$data$label != "") == 3)
cat("rows with NA symbol:", sum(is.na(raw$symbol)), " empty:", sum(raw$symbol == "", na.rm = TRUE), " NA among 10 smallest padj:", sum(is.na(raw$symbol[order(raw$padj)][1:10])), "\n")
# realistic case: an unmapped gene (NA symbol) is the 4th most significant
na1 <- raw; na1$symbol[order(na1$padj)[4]] <- NA
r <- tryCatch({ v <- create_volcano(na1, label_col = "symbol"); suppressWarnings(ggplot_build(v)); paste("builds,", sum(v$data$label != "", na.rm = TRUE), "labels") }, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("NA symbol at padj rank 4 (label_col = 'symbol') ->", r, "\n")
chk("NA label among the smallest padj does not crash the helper", !grepl("^ERROR", r))
# same with top_n given explicitly (the pre-fix code path)
r2 <- tryCatch({ v <- create_volcano(na1, label_col = "symbol", top_n = 10); suppressWarnings(ggplot_build(v)); paste("builds,", sum(v$data$label != "", na.rm = TRUE), "labels") }, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("same with explicit top_n = 10 ->", r2, "\n")
# empty-string symbol is fine
em <- raw; em$symbol[order(em$padj)[4]] <- ""; r3 <- tryCatch({ v <- create_volcano(em, label_col = "symbol"); paste("builds,", sum(v$data$label != ""), "labels") }, error = function(e) paste("ERROR:", conditionMessage(e))); cat("empty-string symbol ->", r3, "\n")
# NA among the top-10 on the Ensembl path is impossible (ids); NA padj rows are filtered
cat("NA-padj rows filtered ->", nrow(create_volcano(raw)$data), "of", nrow(raw), "\n")
