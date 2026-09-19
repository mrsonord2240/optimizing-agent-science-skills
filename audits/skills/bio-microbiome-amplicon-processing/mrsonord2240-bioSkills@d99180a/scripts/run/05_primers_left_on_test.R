# Empirical test: does leaving primers on inflate false-chimera detection, as SKILL.md's
# Common Errors table claims ("Large read fraction 'chimeric' <- primers not trimmed")?
# Use the SAME 5 samples (run1), SAME truncLen/maxEE/truncQ, only vary whether cutadapt ran first.
library(dada2)

run_pipeline <- function(fastq_dir, truncLen) {
  fnFs <- sort(list.files(fastq_dir, pattern = "_R1_001.fastq.gz", full.names = TRUE))
  fnRs <- sort(list.files(fastq_dir, pattern = "_R2_001.fastq.gz", full.names = TRUE))
  sample_names <- sapply(strsplit(basename(fnFs), "_"), `[`, 1)
  filtFs <- file.path(fastq_dir, "filt", paste0(sample_names, "_F.fastq.gz"))
  filtRs <- file.path(fastq_dir, "filt", paste0(sample_names, "_R.fastq.gz"))
  out <- filterAndTrim(fnFs, filtFs, fnRs, filtRs, truncLen = truncLen, maxEE = c(2,2),
                        truncQ = 2, maxN = 0, rm.phix = TRUE, compress = TRUE, multithread = TRUE)
  errF <- learnErrors(filtFs, multithread = TRUE)
  errR <- learnErrors(filtRs, multithread = TRUE)
  dadaFs <- dada(filtFs, err = errF, multithread = TRUE)
  dadaRs <- dada(filtRs, err = errR, multithread = TRUE)
  mergers <- mergePairs(dadaFs, filtFs, dadaRs, filtRs, verbose = TRUE)
  seqtab <- makeSequenceTable(mergers)
  seqtab_nochim <- removeBimeraDenovo(seqtab, method = "consensus", multithread = TRUE, verbose = TRUE)
  list(seqtab = seqtab, nochim = seqtab_nochim)
}

# Condition A: primers removed first (run1, already cutadapt-trimmed -> 231bp/230bp)
resA <- run_pipeline("run1", truncLen = c(220, 200))

# Condition B: primers left ON (raw reads, untrimmed -> 250bp), same truncLen budget applied
# but this time to the RAW (primer-containing) reads.
resB <- run_pipeline("raw_reads_run1_only", truncLen = c(220, 200))

reads_total_A <- sum(resA$seqtab); reads_nochim_A <- sum(resA$nochim)
reads_total_B <- sum(resB$seqtab); reads_nochim_B <- sum(resB$nochim)
chim_frac_A <- 1 - reads_nochim_A / reads_total_A
chim_frac_B <- 1 - reads_nochim_B / reads_total_B

cat(sprintf("\n=== RESULT ===\nPrimers removed:  %d total reads, %.1f%% flagged chimeric\n",
            reads_total_A, 100*chim_frac_A))
cat(sprintf("Primers left on:   %d total reads, %.1f%% flagged chimeric\n",
            reads_total_B, 100*chim_frac_B))
cat(sprintf("ASVs (bimera input) A: %d, B: %d\n", ncol(resA$seqtab), ncol(resB$seqtab)))
