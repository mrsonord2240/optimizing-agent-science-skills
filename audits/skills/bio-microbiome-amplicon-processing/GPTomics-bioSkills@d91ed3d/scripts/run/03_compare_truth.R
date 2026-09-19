# Compare the real DADA2 output (seqtab_nochim_myrun.rds) against the fixture's known ground truth
# (truth.tsv: labeled community ASVs, one mitochondria decoy, one kit_contaminant decoy, two chimeras).
seqtab <- readRDS('F:/OpenScience/audits/bio-amplicon-processing/work/seqtab_nochim_myrun.rds')
truth <- read.delim('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/amplicon/truth.tsv',
                     stringsAsFactors = FALSE)

my_seqs <- colnames(seqtab)
cat('My pipeline produced', length(my_seqs), 'ASVs across', nrow(seqtab), 'samples\n\n')

cat('=== Match against truth.tsv ===\n')
matched <- truth$sequence %in% my_seqs
for (i in seq_len(nrow(truth))) {
    cat(sprintf('%-15s %-20s %-15s : %s\n', truth$id[i], truth$genus[i], truth$role[i],
                if (matched[i]) 'PRESENT in my seqtab' else 'ABSENT (removed)'))
}

cat('\nASVs in my seqtab NOT in truth.tsv (novel/unexpected):', sum(!(my_seqs %in% truth$sequence)), '\n')

cat('\nTotal abundance per matched ASV (sum across 10 samples):\n')
for (i in seq_len(nrow(truth))) {
    if (matched[i]) {
        idx <- which(colnames(seqtab) == truth$sequence[i])
        cat(sprintf('  %-15s %-20s total_reads=%d\n', truth$id[i], truth$role[i], sum(seqtab[, idx])))
    }
}
