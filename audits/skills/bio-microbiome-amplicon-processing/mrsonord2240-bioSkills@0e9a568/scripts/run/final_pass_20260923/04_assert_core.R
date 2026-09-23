library(decontam)
audit_root <- 'F:/OpenScience/audits/bio-microbiome-amplicon-processing'
env_root <- 'F:/OpenScience/audit-envs/microbiome-metagenomics-analyst'
work <- file.path(audit_root, 'work', 'final_pass_20260923')
seqtab <- readRDS(file.path(work, 'seqtab_nochim.rds'))
track <- read.csv(file.path(work, 'read_tracking.csv'), row.names=1, check.names=FALSE)
truth <- read.delim(file.path(env_root, 'datagen', 'amplicon', 'truth.tsv'), check.names=FALSE)
meta <- read.csv(file.path(env_root, 'datagen', 'amplicon', 'sample_metadata.csv'), row.names=1, check.names=FALSE)
stopifnot(nrow(seqtab) == 10L, ncol(seqtab) == 11L, nrow(track) == 10L)
stopifnot(all(track$filtered > 0), all(track$merged > 0))
community <- truth$sequence[truth$role == 'community']
stopifnot(length(community) == 8L, all(community %in% colnames(seqtab)))
contam <- isContaminant(seqtab, neg=meta$is_control, conc=meta$dna_conc, method='combined', threshold=0.1)
flagged <- colnames(seqtab)[contam$contaminant]
stopifnot(length(flagged) == 1L)
flag_truth <- truth$role[match(flagged, truth$sequence)]
stopifnot(identical(flag_truth, 'kit_contaminant'))
cat(sprintf('CORE_ASSERTIONS_PASS samples=%d asvs=%d reads=%d contaminant=%s\n', nrow(seqtab), ncol(seqtab), sum(seqtab), flagged))
