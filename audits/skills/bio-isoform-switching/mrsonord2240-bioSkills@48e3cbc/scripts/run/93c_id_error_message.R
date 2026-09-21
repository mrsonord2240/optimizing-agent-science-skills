# Round-2 claim: the workflow block's sample-ID check now names the offending IDs. Run blocks/r_01.R verbatim on a staged 3v3 synthetic set with (a) a metadata row
# missing, (b) an extra metadata row, (c) a case-mismatched ID, (d) a duplicated metadata row; record the message. (e) control: correct metadata runs to completion.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
src <- "../data/het_3v3"; base <- read.delim(file.path(src, "sample_metadata.tsv"), stringsAsFactors = FALSE)
try_meta <- function(label, m) {
  wd <- "w93c"; unlink(wd, recursive = TRUE); dir.create(wd); file.copy(file.path(src, c("salmon_quant", "annotation.gtf", "transcripts.fa")), wd, recursive = TRUE)
  write.table(m, file.path(wd, "sample_metadata.tsv"), sep = "\t", quote = FALSE, row.names = FALSE); setwd(wd)
  r <- tryCatch({ invisible(capture.output(suppressMessages(suppressWarnings(run_block("r_01.R"))))); "no error" }, error = function(e) conditionMessage(e)); setwd("..")
  cat(sprintf("(%s) -> %s\n", label, gsub("\n", " | ", r))); r }
r <- try_meta("a missing row", base[-1, ]);           chk("93c-a message names the sample only in quant", grepl(base$sample_id[1], r, fixed = TRUE) && grepl("only in quant", r), r)
x <- rbind(base, data.frame(sample_id = "SRR_EXTRA", condition = "control")); r <- try_meta("b extra row", x); chk("93c-b message names the ID only in metadata", grepl("only in metadata: SRR_EXTRA", r, fixed = TRUE))
y <- base; y$sample_id[1] <- tolower(y$sample_id[1]); r <- try_meta("c case mismatch", y); chk("93c-c case mismatch: both spellings named", grepl(tolower(base$sample_id[1]), r, fixed = TRUE) && grepl(base$sample_id[1], r, fixed = TRUE))
z <- rbind(base, base[1, ]); r <- try_meta("d duplicated row", z); chk("93c-d duplicated metadata row stops with the duplicate message", grepl("duplicated sample_id", r, fixed = TRUE))
r <- try_meta("e control", base); chk("93c-e correct metadata runs to completion", r == "no error", r)
cat("DONE 93c\n")
