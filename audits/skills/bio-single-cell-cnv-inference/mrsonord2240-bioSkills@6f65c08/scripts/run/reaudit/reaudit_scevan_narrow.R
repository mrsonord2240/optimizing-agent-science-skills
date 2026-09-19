# RE-AUDIT (2026-09-19): confirm the SKILL's claim that a narrow (few-
# chromosome) gene panel fails SCEVAN's per-chromosome coverage filter
# ("all cells are filtered"), using the audit's existing 3-chromosome
# data_realgenes panel (chr1, chr7, chr10; real gene symbols).
suppressMessages(library(SCEVAN))

setwd("/mnt/openscience/audits/bio-single-cell-cnv-inference")

counts <- read.table("data_realgenes/counts.matrix", header = TRUE, row.names = 1,
                      sep = "\t", check.names = FALSE)
count_mtx <- as.matrix(counts)
cat("panel dims:", dim(count_mtx), "\n")

annot <- read.table("data_realgenes/cell_annotations.txt", header = FALSE, sep = "\t",
                     col.names = c("cell", "group"))
normal_cell_names <- annot$cell[annot$group %in% c("Tcell", "Myeloid")]

dir.create("run/reaudit/scevan_narrow", showWarnings = FALSE)
setwd("run/reaudit/scevan_narrow")

result <- tryCatch({
    pipelineCNA(
        count_mtx,
        sample = "narrow_panel",
        par_cores = 4,
        norm_cell = normal_cell_names,
        SUBCLONES = TRUE,
        ClonalCN = TRUE,
        plotTree = FALSE,
        organism = "human",
        ngenes_chr = 5)
}, error = function(e) {
    cat("CAUGHT ERROR on narrow panel:", conditionMessage(e), "\n")
    NULL
})

cat("\nresult is NULL:", is.null(result), "\n")
cat("DONE: narrow-panel SCEVAN test\n")
