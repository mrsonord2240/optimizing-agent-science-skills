# Adapted verbatim from the Skill's examples/dada2_workflow.R (per-run error model ->
# mergeSequenceTables -> ONE chimera removal), pointed at the audit env's real DADA2 fixture.
# Real run structure from sample_metadata.csv: run1 = S01-S05, run2 = S06-S10.
library(dada2)

trimmed_dir <- 'F:/OpenScience/audits/bio-amplicon-processing/work/trimmed'
work_dir <- 'F:/OpenScience/audits/bio-amplicon-processing/work'

run1_samples <- c('S01','S02','S03','S04','S05')
run2_samples <- c('S06','S07','S08','S09','S10')

truncLen <- c(220, 200)   # per the Skill's V4 (~253bp) guidance: huge merge slack at 2x250.
# NOTE (audit adjustment): the fixture's primer-trimmed reads are only 231/230bp long (not 250bp),
# so c(240,200) truncated below zero and the filter dropped every read. c(220,200) fits within the
# available read length while still comfortably exceeding the Skill's own merge budget
# (insert 214bp + minOverlap 12 = 226bp needed; 220+200=420bp available).
maxEE <- c(2, 2)
truncQ <- 2

process_run <- function(sample_names, run_label) {
    fnFs <- file.path(trimmed_dir, paste0(sample_names, '_S1_L001_R1_001.fastq.gz'))
    fnRs <- file.path(trimmed_dir, paste0(sample_names, '_S1_L001_R2_001.fastq.gz'))
    filt_dir <- file.path(work_dir, 'filtered', run_label)
    dir.create(filt_dir, recursive = TRUE, showWarnings = FALSE)
    filtFs <- file.path(filt_dir, paste0(sample_names, '_F.fastq.gz'))
    filtRs <- file.path(filt_dir, paste0(sample_names, '_R.fastq.gz'))
    names(filtFs) <- sample_names
    names(filtRs) <- sample_names

    out <- filterAndTrim(fnFs, filtFs, fnRs, filtRs, truncLen = truncLen, maxEE = maxEE,
                          truncQ = truncQ, maxN = 0, rm.phix = TRUE, compress = TRUE, multithread = TRUE)

    errF <- learnErrors(filtFs, multithread = TRUE)
    errR <- learnErrors(filtRs, multithread = TRUE)

    dadaFs <- dada(filtFs, err = errF, multithread = TRUE)
    dadaRs <- dada(filtRs, err = errR, multithread = TRUE)
    mergers <- mergePairs(dadaFs, filtFs, dadaRs, filtRs, verbose = TRUE)
    seqtab <- makeSequenceTable(mergers)

    getN <- function(x) sum(getUniques(x))
    track <- cbind(out, sapply(dadaFs, getN), sapply(dadaRs, getN), sapply(mergers, getN))
    colnames(track) <- c('input', 'filtered', 'denoisedF', 'denoisedR', 'merged')
    rownames(track) <- sample_names
    list(seqtab = seqtab, track = track)
}

cat('=== Processing run1 (S01-S05) ===\n')
run1 <- process_run(run1_samples, 'run1')
cat('=== Processing run2 (S06-S10) ===\n')
run2 <- process_run(run2_samples, 'run2')

seqtab_all <- mergeSequenceTables(run1$seqtab, run2$seqtab)
seqtab_nochim <- removeBimeraDenovo(seqtab_all, method = 'consensus', multithread = TRUE, verbose = TRUE)

cat('\n=== RESULTS ===\n')
cat('seqtab_all dim (samples x ASVs before chimera removal):', dim(seqtab_all), '\n')
cat('seqtab_nochim dim (samples x ASVs after chimera removal):', dim(seqtab_nochim), '\n')
cat('reads retained after chimera removal:', round(100 * sum(seqtab_nochim) / sum(seqtab_all), 1), '%\n')
cat('ASVs removed as chimeric:', ncol(seqtab_all) - ncol(seqtab_nochim), '\n')

cat('\nASV length distribution (post-chimera-removal):\n')
print(table(nchar(getSequences(seqtab_nochim))))

track_all <- rbind(run1$track, run2$track)
cat('\nRead-tracking table:\n')
print(track_all)

write.csv(track_all, file.path(work_dir, 'read_tracking.csv'))
saveRDS(seqtab_nochim, file.path(work_dir, 'seqtab_nochim_myrun.rds'))
saveRDS(seqtab_all, file.path(work_dir, 'seqtab_all_myrun.rds'))
cat('\nSaved seqtab_nochim_myrun.rds and read_tracking.csv\n')
