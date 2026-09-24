# Check the Skill's statement that ISAR 2.6.0 has neither an auto-selecting DTU wrapper nor long-read/single-cell modes: exports, NEWS, importRdata docs.
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
cat("version:", as.character(packageVersion("IsoformSwitchAnalyzeR")), "\n")
ex <- getNamespaceExports("IsoformSwitchAnalyzeR"); cat("exports matching Test/Satu/Long/Single/Nano/Iso-Seq:", paste(sort(grep("Test|Satu|long|Long|single|Single|Nanopore|Iso", ex, value = TRUE)), collapse = ", "), "\n")
nf <- system.file("NEWS", package = "IsoformSwitchAnalyzeR"); if (!nzchar(nf)) nf <- system.file("NEWS.md", package = "IsoformSwitchAnalyzeR")
cat("NEWS file:", nf, "\n"); if (nzchar(nf)) { n <- readLines(nf); i <- grep("long|single.cell|satuRn|SatuRn|automatic|auto", n, ignore.case = TRUE); cat(paste(n[sort(unique(c(i)))][1:40], collapse = "\n"), "\n") }
cat("importRdata args:", paste(names(formals(importRdata)), collapse = ", "), "\n")
h <- capture.output(tools::Rd2txt(utils:::.getHelpFile(help("importRdata", package = "IsoformSwitchAnalyzeR")), options = list(underline_titles = FALSE)))
i <- grep("long|single.?cell|nanopore|pacbio|Iso-Seq", h, ignore.case = TRUE); cat("importRdata help lines mentioning long-read/single-cell:\n"); cat(h[i], sep = "\n")
cat("DONE 62\n")
