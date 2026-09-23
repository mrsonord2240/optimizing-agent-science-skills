audit_root <- 'F:/OpenScience/audits/bio-microbiome-amplicon-processing'
work <- file.path(audit_root, 'work', 'final_pass_20260923')
a <- readRDS(file.path(work, 'seqtab_nochim.rds'))
b <- readRDS(file.path(work, 'repeat', 'seqtab_nochim.rds'))
stopifnot(identical(dim(a), dim(b)), identical(colnames(a), colnames(b)), identical(unclass(a), unclass(b)))
cat(sprintf('DETERMINISM_PASS samples=%d asvs=%d values_identical=true\n', nrow(a), ncol(a)))
