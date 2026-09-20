# Bambu NDR sweep on the same SYNTHETIC BAMs (SKILL table: 0.05 stringent, 0.1 default, 0.2-0.3 permissive)
D <- "F:/OpenScience/audits/bio-long-read-splicing/run"
setwd(paste0(D, "/out/bambu"))
suppressMessages(library(bambu))
bam_files <- paste0(D, "/out/flair/", c("ctrl1","ctrl2","ctrl3","trt1","trt2","trt3"), ".bam")
genome <- paste0(D, "/data/synth/chrS1.fa"); gtf <- paste0(D, "/data/synth/ref.gtf")
ann <- prepareAnnotations(gtf)
for (ndr in c(0.05, 0.3, 1)) {
  se <- suppressMessages(bambu(reads = bam_files, annotations = ann, genome = genome, NDR = ndr, ncore = 1))
  rr <- rowRanges(se)
  novel <- !(names(rr) %in% c("GA.1", "GA.2", "GB.1", "GC.1"))
  cat(sprintf("NDR=%.2f -> %d transcripts; novel = %d\n", ndr, length(rr), sum(novel)))
  cat("   ids:", paste(names(rr), collapse = ", "), "\n")
}
