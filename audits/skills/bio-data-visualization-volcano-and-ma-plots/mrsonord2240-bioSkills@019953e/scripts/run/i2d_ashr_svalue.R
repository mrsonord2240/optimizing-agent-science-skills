# Does ashr return svalue? Skill code comment says 'ashr also returns svalue column' for lfcShrink(..., type = "ashr") with no svalue argument.
suppressMessages({library(DESeq2)})
o <- readRDS("F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots/data/airway_objs.rds"); dds <- o$dds
r0 <- suppressMessages(lfcShrink(dds, contrast = c("condition", "treated", "control"), type = "ashr"))
r1 <- suppressMessages(lfcShrink(dds, contrast = c("condition", "treated", "control"), type = "ashr", svalue = TRUE))
cat("ashr as written in the Skill      -> columns:", paste(colnames(r0), collapse = ","), "\n")
cat("ashr with svalue = TRUE           -> columns:", paste(colnames(r1), collapse = ","), "\n")
cat("s<0.005:", sum(r1$svalue < 0.005, na.rm = TRUE), " vs padj<0.05 (unshrunken Wald):", sum(o$raw$padj < 0.05, na.rm = TRUE), "\n")
cat("svalue arg documented for:", grep("svalue", capture.output(tools::Rd2txt(utils:::.getHelpFile(help("lfcShrink", package = "DESeq2")))), value = TRUE)[1:4], sep = "\n")
