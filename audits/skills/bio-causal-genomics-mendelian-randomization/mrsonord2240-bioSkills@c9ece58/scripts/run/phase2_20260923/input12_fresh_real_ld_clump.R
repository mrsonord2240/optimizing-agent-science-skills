# Input 12 (new, fresh) -- run the exact Phase-2 source copy of twosample_workflow.R
# through its default local LD-clumping branch against the real 1000G EUR PLINK panel.
# Three synthetic association rows use real panel SNP IDs: rs74048003 and rs60442576 have
# observed r2=0.960 in the panel; rs6728916 is on chr2. The test expects the first two
# to collapse to one independent instrument, while retaining the chr2 SNP.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 4L) stop("usage: input12_fresh_real_ld_clump.R <rscript> <workflow> <bfile> <plink>")
rscript <- args[[1]]; workflow <- args[[2]]; bfile <- args[[3]]; plink <- args[[4]]
outdir <- "../data/phase2_20260923/ld_clump_out"
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

exposure <- data.frame(
  SNP = c("rs74048003", "rs60442576", "rs6728916"),
  BETA = c(0.25, 0.24, 0.22), SE = c(0.02, 0.02, 0.02),
  A1 = c("A", "T", "T"), A2 = c("G", "C", "C"),
  EAF = c(0.25, 0.25, 0.25), P = c(1e-30, 1e-29, 1e-25), N = c(100000, 100000, 100000)
)
outcome <- exposure
outcome$BETA <- exposure$BETA * 0.35
outcome$SE <- 0.03
outcome$P <- 1e-10
write.table(exposure, file.path(outdir, "exposure.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
write.table(outcome, file.path(outdir, "outcome.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)

status <- system2(rscript, c(workflow, "--exposure", file.path(outdir, "exposure.tsv"),
  "--outcome", file.path(outdir, "outcome.tsv"), "--outdir", file.path(outdir, "workflow"),
  "--bfile", bfile, "--plink", plink), stdout = TRUE, stderr = TRUE)
cat(paste(status, collapse = "\n"), "\n")
if (!file.exists(file.path(outdir, "workflow", "harmonised.tsv"))) stop("workflow wrote no harmonised.tsv")
harm <- read.delim(file.path(outdir, "workflow", "harmonised.tsv"), stringsAsFactors = FALSE)
cat("fresh real-clump harmonised SNPs:", paste(harm$SNP, collapse = ","), "\n")
if (nrow(harm) != 2L || "rs60442576" %in% harm$SNP || !all(c("rs74048003", "rs6728916") %in% harm$SNP)) {
  stop("LD clumping did not retain exactly the expected independent SNPs")
}
cat("INPUT12 PASS: real-LD clumping removed the r2=0.960 SNP and retained two independent instruments.\n")
