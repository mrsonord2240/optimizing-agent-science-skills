# Empirical test of the Skill's specific claim (SKILL.md "Combine Runs, Then Remove Chimeras" and
# "Per-Method Failure Modes -> Primers left on before truncation"):
# "A large READ fraction removed as chimeric is a leftover-primer smell ... not a real chimera storm."
# Runs the identical DADA2 pipeline as run 02, but SKIPPING cutadapt (raw_reads, primers still on),
# using the same truncLen budget, to see whether chimera-flagged read/ASV fraction inflates.
library(dada2)

raw_dir <- 'F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/amplicon/raw_reads'
work_dir <- 'F:/OpenScience/audits/bio-amplicon-processing/work/primers_on_test'
dir.create(work_dir, recursive = TRUE, showWarnings = FALSE)

samples <- c('S01','S02','S03','S04','S05')   # run1 only, for speed
truncLen <- c(220, 200)   # identical parameters to run 02 (primers-removed case)
maxEE <- c(2, 2)
truncQ <- 2

fnFs <- file.path(raw_dir, paste0(samples, '_S1_L001_R1_001.fastq.gz'))
fnRs <- file.path(raw_dir, paste0(samples, '_S1_L001_R2_001.fastq.gz'))
filtFs <- file.path(work_dir, paste0(samples, '_F.fastq.gz'))
filtRs <- file.path(work_dir, paste0(samples, '_R.fastq.gz'))
names(filtFs) <- samples
names(filtRs) <- samples

out <- filterAndTrim(fnFs, filtFs, fnRs, filtRs, truncLen = truncLen, maxEE = maxEE,
                      truncQ = truncQ, maxN = 0, rm.phix = TRUE, compress = TRUE, multithread = TRUE)

errF <- learnErrors(filtFs, multithread = TRUE)
errR <- learnErrors(filtRs, multithread = TRUE)
dadaFs <- dada(filtFs, err = errF, multithread = TRUE)
dadaRs <- dada(filtRs, err = errR, multithread = TRUE)
mergers <- mergePairs(dadaFs, filtFs, dadaRs, filtRs, verbose = TRUE)
seqtab_primerson <- makeSequenceTable(mergers)

seqtab_nochim_primerson <- removeBimeraDenovo(seqtab_primerson, method = 'consensus',
                                               multithread = TRUE, verbose = TRUE)

cat('\n=== PRIMERS LEFT ON (run1 only, S01-S05) ===\n')
cat('ASVs before chimera removal:', ncol(seqtab_primerson), '\n')
cat('ASVs after chimera removal:', ncol(seqtab_nochim_primerson), '\n')
cat('ASVs flagged chimeric:', ncol(seqtab_primerson) - ncol(seqtab_nochim_primerson), '\n')
cat('reads retained after chimera removal:',
    round(100 * sum(seqtab_nochim_primerson) / sum(seqtab_primerson), 1), '%\n')
cat('READ fraction removed as chimeric:',
    round(100 * (1 - sum(seqtab_nochim_primerson) / sum(seqtab_primerson)), 1), '%\n')

cat('\n=== For comparison, PRIMERS REMOVED (run 02, run1 only, S01-S05) ===\n')
seqtab_run1_trimmed <- readRDS('F:/OpenScience/audits/bio-amplicon-processing/work/seqtab_all_myrun.rds')
run1_rows <- c('S01','S02','S03','S04','S05')
seqtab_run1_only <- seqtab_run1_trimmed[run1_rows, , drop = FALSE]
seqtab_run1_only <- seqtab_run1_only[, colSums(seqtab_run1_only) > 0, drop = FALSE]
nochim_run1 <- removeBimeraDenovo(seqtab_run1_only, method = 'consensus', multithread = TRUE, verbose = TRUE)
cat('ASVs before chimera removal (primers-removed, run1 subset):', ncol(seqtab_run1_only), '\n')
cat('ASVs after chimera removal:', ncol(nochim_run1), '\n')
cat('READ fraction removed as chimeric:',
    round(100 * (1 - sum(nochim_run1) / sum(seqtab_run1_only)), 1), '%\n')
