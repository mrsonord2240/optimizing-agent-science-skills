# Follows the Skill's SKILL.md "Decontamination and Controls (low-biomass)" section verbatim:
# isContaminant(seqtab_nochim, neg=is_control, conc=dna_conc, method='combined', threshold=0.1)
# Uses the real chimera-free table from run 02 and the fixture's real sample_metadata.csv
# (S09/S10 are true no-template-PCR blanks: is_control=TRUE, dna_conc ~0.1 vs 5.6-25.2 for real samples).
library(decontam)

seqtab_nochim <- readRDS('F:/OpenScience/audits/bio-amplicon-processing/work/seqtab_nochim_myrun.rds')
meta <- read.csv('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/amplicon/sample_metadata.csv',
                  stringsAsFactors = FALSE)
truth <- read.delim('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/amplicon/truth.tsv',
                     stringsAsFactors = FALSE)

# Align metadata to seqtab row order (SKILL.md's decontam call needs meta$is_control / meta$dna_conc
# in the same sample order as seqtab_nochim's rows).
meta <- meta[match(rownames(seqtab_nochim), meta$sample), ]
stopifnot(all(meta$sample == rownames(seqtab_nochim)))

cat('Samples:', paste(meta$sample, collapse=', '), '\n')
cat('is_control:', paste(meta$is_control, collapse=', '), '\n')
cat('dna_conc:', paste(meta$dna_conc, collapse=', '), '\n\n')

contam <- isContaminant(seqtab_nochim, neg = meta$is_control, conc = meta$dna_conc,
                         method = 'combined', threshold = 0.1)

cat('=== isContaminant results ===\n')
print(contam[, c('freq', 'prev', 'p.freq', 'p.prev', 'p', 'contaminant')])

flagged_seqs <- colnames(seqtab_nochim)[contam$contaminant]
cat('\nFlagged as contaminant:', length(flagged_seqs), 'of', ncol(seqtab_nochim), 'ASVs\n')

cat('\n=== Identity check against truth.tsv ===\n')
for (s in flagged_seqs) {
    hit <- truth[truth$sequence == s, ]
    if (nrow(hit) > 0) {
        cat(sprintf('  FLAGGED: %s (%s / %s)\n', hit$id, hit$genus, hit$role))
    } else {
        cat('  FLAGGED: unknown sequence (not in truth.tsv)\n')
    }
}

cat('\n=== Did decontam catch the known kit_contaminant (Ralstonia, ASV_true_10)? ===\n')
ralstonia_seq <- truth$sequence[truth$id == 'ASV_true_10']
ralstonia_idx <- which(colnames(seqtab_nochim) == ralstonia_seq)
cat('Ralstonia flagged as contaminant:', contam$contaminant[ralstonia_idx], '\n')

seqtab_clean <- seqtab_nochim[, !contam$contaminant]
cat('\nseqtab_clean dim after decontam removal:', dim(seqtab_clean), '\n')
