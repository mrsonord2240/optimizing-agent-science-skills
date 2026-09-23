library(dada2)
audit_root <- 'F:/OpenScience/audits/bio-microbiome-amplicon-processing'
work <- file.path(audit_root, 'work', 'final_pass_20260923')
in_dir <- file.path(work, 'trimmed')
samples <- paste0('S0', 1:5)
fF <- file.path(in_dir, paste0(samples, '_S1_L001_R1_001.fastq.gz'))
fR <- file.path(in_dir, paste0(samples, '_S1_L001_R2_001.fastq.gz'))
run_filter <- function(trunc, name) {
  out_dir <- file.path(work, 'ceiling', name)
  dir.create(out_dir, recursive=TRUE, showWarnings=FALSE)
  o <- filterAndTrim(fF, file.path(out_dir, paste0(samples, '_F.fastq.gz')), fR, file.path(out_dir, paste0(samples, '_R.fastq.gz')), truncLen=trunc, maxEE=c(2,2), truncQ=2, maxN=0, compress=TRUE, multithread=TRUE)
  sum(o[, 'reads.out'])
}
at <- run_filter(c(231,230), 'at_ceiling')
over <- run_filter(c(232,230), 'one_bp_over')
default <- run_filter(c(220,200), 'shipped_default')
stopifnot(at > 0, over == 0, default > at)
cat(sprintf('CEILING_PASS at=%d one_bp_over=%d default=%d\n', at, over, default))
