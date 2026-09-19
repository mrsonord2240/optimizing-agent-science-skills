# New input (auditor's own, not in fix log): quantitatively test the fixed SKILL.md's new claim that
# truncLen has a ceiling at the POST-cutadapt read length (231bp F / 230bp R for this fixture), and that
# crossing it by even 1bp silently empties the filter output ("No reads passed the filter").
library(dada2)

fnFs <- sort(list.files("run1", pattern = "_R1_001.fastq.gz", full.names = TRUE))
fnRs <- sort(list.files("run1", pattern = "_R2_001.fastq.gz", full.names = TRUE))
sample_names <- sapply(strsplit(basename(fnFs), "_"), `[`, 1)

test_trunclen <- function(tl, label) {
  filtFs <- file.path("ceiling_test", label, paste0(sample_names, "_F.fastq.gz"))
  filtRs <- file.path("ceiling_test", label, paste0(sample_names, "_R.fastq.gz"))
  out <- filterAndTrim(fnFs, filtFs, fnRs, filtRs, truncLen = tl, maxEE = c(2,2),
                        truncQ = 2, maxN = 0, rm.phix = TRUE, compress = TRUE, multithread = TRUE)
  cat(sprintf("truncLen=c(%d,%d) [%s]: total_in=%d total_filtered=%d\n",
              tl[1], tl[2], label, sum(out[,1]), sum(out[,2])))
}

test_trunclen(c(231, 230), "at_ceiling")     # exactly at the post-cutadapt length -> should pass
test_trunclen(c(232, 230), "one_over_F")     # 1bp over on F only -> should silently drop everything
test_trunclen(c(220, 200), "fixed_default")  # the shipped fixed default, for comparison
