# Re-audit 6 (volcano-and-ma-plots): execute every ```r block of SKILL.md verbatim on the airway dds (undefined stand-ins supplied only as the text instructs).
# Usage: r.sh r6_skill_r_blocks.R <skilldir> <outdir>
a <- commandArgs(TRUE); skill <- a[1]; out <- a[2]; dir.create(out, FALSE, TRUE); setwd(out)
suppressMessages({library(DESeq2); library(ggplot2)})
ok <- TRUE
chk <- function(l, c) { ok <<- ok && isTRUE(c); cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l)) }
txt <- paste(readLines(file.path(skill, "SKILL.md"), encoding = "UTF-8"), collapse = "\n")
m <- gregexpr("(?s)```r
.*?```", txt, perl = TRUE); blocks <- sub("```$", "", sub("^```r
", "", regmatches(txt, m)[[1]]))
cat(length(blocks), "R blocks in SKILL.md\n")
dds <- readRDS("F:/OpenScience/audit-envs/data-visualization/public-data/derived/airway_dds_condition.rds")
env <- globalenv()
# block 1 (lfcShrink): runs DESeq(dds) again, then three lfcShrink calls
t0 <- Sys.time()
r1 <- try(eval(parse(text = blocks[1]), env), silent = FALSE); chk(sprintf("R block 1 (DESeq + lfcShrink apeglm/ashr/svalue) runs verbatim (%.0f s)", as.numeric(difftime(Sys.time(), t0, units = "secs"))), !inherits(r1, "try-error"))
chk("res_apeglm, res_ashr, res_s exist with expected columns", exists("res_apeglm") && exists("res_ashr") && identical(colnames(res_s), c("baseMean", "log2FoldChange", "lfcSE", "svalue")))
# block 2 (EnhancedVolcano): needs res and ev_col; construct them exactly as the text describes
okabe_ito <- c(Up = '#D55E00', Down = '#0072B2', NS = '#999999')
res <- res_apeglm[!is.na(res_apeglm$padj), ]
sig <- ifelse(res$padj < 0.05 & res$log2FoldChange > 1, 'Up', ifelse(res$padj < 0.05 & res$log2FoldChange < -1, 'Down', 'NS'))
ev_col <- setNames(okabe_ito[sig], sig)          # the sentence in SKILL.md: setNames(okabe_ito[sig], sig)
suppressMessages(library(EnhancedVolcano))
png("ev_skillmd.png", 900, 900, res = 110)
w <- character(); r2 <- withCallingHandlers(try(print(eval(parse(text = blocks[grep("EnhancedVolcano\\(res", blocks)[1]]), env)), silent = FALSE),
   warning = function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") })
invisible(dev.off())
chk("EnhancedVolcano SKILL.md block runs verbatim and draws", !inherits(r2, "try-error"))
cat("warnings (unique, 90 chars):", paste(unique(substr(w, 1, 90)), collapse = " | "), "\n")
p <- r2; bd <- ggplot_build(p)$data[[1]]
chk("block colours: Up #D55E00 and Down #0072B2 both present and counts match table", all(c('#D55E00', '#0072B2') %in% toupper(bd$colour)) && sum(toupper(bd$colour) == '#D55E00') == sum(sig == 'Up') && sum(toupper(bd$colour) == '#0072B2') == sum(sig == 'Down'))
chk("block y-axis label names adjusted P (ylab)", grepl("adjusted", paste(deparse(p$labels$y), collapse = "")))
# block 3 (plotMA)
png("plotMA.png", 600, 500); r3 <- try(eval(parse(text = blocks[grep("plotMA", blocks)[1]]), env), silent = FALSE); invisible(dev.off())
chk("plotMA block runs verbatim and writes a plot", !inherits(r3, "try-error") && file.size("plotMA.png") > 3000)
cat("RESULT", if (ok) "PASS" else "FAIL", "\n")
