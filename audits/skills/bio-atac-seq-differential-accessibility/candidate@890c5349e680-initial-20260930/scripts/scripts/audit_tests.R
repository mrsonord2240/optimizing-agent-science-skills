# Initial-audit probes for bio-atac-seq-differential-accessibility. Usage: Rscript audit_tests.R <mode>
# Modes: cli | norm | null | labels | plots.  Runs Skill script UNMODIFIED (sourced with commandArgs neutralised, or via CLI).
suppressPackageStartupMessages({library(GenomicRanges); library(rtracklayer)})
mode <- commandArgs(TRUE)[1]
SKILL <- "/mnt/openscience/wt/atac-differential-accessibility/skills/bio-atac-seq-differential-accessibility/scripts/diff_accessibility.R"
R0 <- "/mnt/openscience/audits/bio-atac-seq-differential-accessibility/initial-20260930"
W <- file.path(R0, "work", mode); dir.create(W, recursive = TRUE, showWarnings = FALSE)
D <- "/mnt/openscience/audit-envs/atac-seq/public-data/encode"
bams <- paste0(file.path(D, c("GM12878_rep1_filtered","GM12878_rep2_filtered","K562_rep1_filtered","K562_rep2_filtered")), ".chr1_1-30000000.bam")
pk <- file.path(R0, "work", c("gm1.narrowPeak","gm2.narrowPeak","k.narrowPeak","k.narrowPeak"))
mk <- function(cond) { ss <- data.frame(SampleID=c("GM1","GM2","K1","K2"), Condition=cond, Replicate=c(1,2,1,2), bamReads=bams, Peaks=pk, PeakCaller="narrow"); write.csv(ss, file.path(W,"samples.csv"), row.names=FALSE) }
setwd(W)
gm <- import(file.path(R0,"work","gm1.narrowPeak"), format="narrowPeak"); kp <- import(file.path(R0,"work","k.narrowPeak"), format="narrowPeak")
gmall <- c(gm, import(file.path(R0,"work","gm2.narrowPeak"), format="narrowPeak"))
k_only <- kp[!overlapsAny(kp, gmall)]
load_skill <- function() { assign("commandArgs", function(trailingOnly=FALSE) character(0), envir=globalenv()); source(SKILL) }
summ <- function(out) { r <- out$results; cat(sprintf("RESULT n=%d opened=%d closed=%d\n", length(r), sum(r$Fold>0), sum(r$Fold<0)))
  ko <- r[overlapsAny(r, k_only)]; cat(sprintf("RESULT k_only_hits=%d frac_opened=%.3f\n", length(ko), mean(ko$Fold>0))) }
if (mode == "cli") {
  mk(c("control","control","treated","treated"))
  # documented usage: Rscript diff_accessibility.R <sample_sheet.csv> [output_prefix] [normalize_mode] [fdr_thr] [lfc_thr]
  rc <- system2(file.path(R.home("bin"),"Rscript"), c(shQuote(SKILL), "samples.csv", "mypfx", "DBA_NORM_LIB", "0.01", "3"))
  cat("EXIT", rc, "\n"); cat("FILES:", paste(sort(list.files(".", pattern="pdf|bed|csv$")), collapse=" "), "\n")
  cat("mypfx_* exist:", any(file.exists(list.files(".", pattern="^mypfx"))), "\n")
}
if (mode == "norm") {
  mk(c("control","control","treated","treated")); load_skill()
  print(formals(DiffBind::dba.normalize)[c("normalize","library","background")])
  cat("DBA_NORM_NATIVE =", DBA_NORM_NATIVE, " DBA_NORM_LIB =", DBA_NORM_LIB, " DBA_NORM_DEFAULT =", DBA_NORM_DEFAULT, "\n")
  for (nm in c("NATIVE","LIB")) { nmode <- get(paste0("DBA_NORM_", nm)); cat("=== normalize", nm, "===\n")
    out <- run_diff("samples.csv", output_prefix=paste0("norm_", nm), normalize_mode=nmode); summ(out)
    print(dba.normalize(out$dba, bRetrieve=TRUE)$norm.factors); print(dba.normalize(out$dba, bRetrieve=TRUE)[c("norm.method","lib.method")]) }
}
if (mode == "null") {
  mk(c("control","control","treated","treated")); load_skill()
  r <- try(run_diff("samples.csv", output_prefix="null", lfc_thr=10)); cat("null-result run class:", class(r), "\n")
}
if (mode == "labels") {
  mk(c("GM12878","GM12878","K562","K562")); load_skill()
  r <- try(run_diff("samples.csv", output_prefix="lab")); cat("nonstandard-labels run class:", class(r)[1], "\n")
}
if (mode == "plots") {   # render the Skill's diagnostic plot calls to PNG (no PDF rasteriser available); same calls as run_diff
  mk(c("control","control","treated","treated")); load_skill()
  out <- run_diff("samples.csv", output_prefix="plt"); d <- out$dba
  png("plt_pca.png", 900, 700); dba.plotPCA(d, attributes=DBA_CONDITION, label=DBA_ID); dev.off()
  png("plt_ma.png", 900, 700); dba.plotMA(d); dev.off()
  png("plt_volcano.png", 900, 700); dba.plotVolcano(d); dev.off()
  png("plt_heatmap.png", 900, 900); dba.plotHeatmap(d, contrast=1, correlations=FALSE); dev.off()
  png("plt_annopie.png", 900, 700); ChIPseeker::plotAnnoPie(out$anno); dev.off()
  png("plt_disttss.png", 900, 500); ChIPseeker::plotDistToTSS(out$anno); dev.off()
  cat("PNG:", paste(list.files(".", pattern="png$"), collapse=" "), "\n")
}
if (mode == "sva") {   # use_sva=TRUE is unreachable from CLI; source with commandArgs neutralised
  mk(c("control","control","treated","treated")); load_skill()
  r <- try(run_diff("samples.csv", output_prefix="sva", use_sva=TRUE)); cat("sva run class:", class(r)[1], "\n")
}
