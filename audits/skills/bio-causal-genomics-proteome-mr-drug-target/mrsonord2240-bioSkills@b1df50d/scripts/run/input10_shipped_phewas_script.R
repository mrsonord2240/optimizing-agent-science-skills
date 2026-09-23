# Input 10 (fresh executable regression): source the current unmodified
# scripts/phewas_curated_endpoints.R using local deterministic OpenGWAS-shaped
# stubs. Live catalogue access remains JWT-gated; this validates the shipped
# parsing, full curated-loop, MR, correction and TSV-write paths.
suppressPackageStartupMessages(library(TwoSampleMR))
set.seed(20260923)

audit_root <- "F:/OpenScience/audits/bio-causal-genomics-proteome-mr-drug-target"
skill_copy <- file.path(audit_root, "run", "skill-copy")
work <- file.path(audit_root, "run", "input10_work")
dir.create(work, recursive=TRUE, showWarnings=FALSE)

pqtl <- read.table(file.path(audit_root, "data", "synth_pcsk9_ukbppp_full_window.tsv"), header=TRUE, sep="\t")
pqtl <- subset(pqtl, P < 5e-8)[1:8, c("SNP", "BETA", "SE", "A1", "A2", "EAF", "P")]
pqtl_path <- file.path(work, "pqtl.tsv")
endpoint_path <- file.path(work, "endpoints.tsv")
out_path <- file.path(work, "phewas.tsv")
write.table(pqtl, pqtl_path, sep="\t", row.names=FALSE, quote=FALSE)
endpoint_ids <- paste0("mock_outcome_", sprintf("%02d", 1:12))
write.table(data.frame(id=endpoint_ids), endpoint_path, sep="\t", row.names=FALSE, quote=FALSE)

# These names deliberately shadow API calls only in this audit process.
available_outcomes <- function() data.frame(id=endpoint_ids, sample_size=rep(100000, 12), population=rep("European", 12))
extract_outcome_data <- function(snps, outcomes) {
  b <- if (outcomes == endpoint_ids[1]) 0.20 * pqtl$BETA else rnorm(nrow(pqtl), 0, 0.001)
  format_data(data.frame(SNP=pqtl$SNP, BETA=b, SE=rep(0.008, nrow(pqtl)), A1=pqtl$A1, A2=pqtl$A2,
                         EAF=pqtl$EAF, P=2*pnorm(-abs(b/0.008))),
              type="outcome", snp_col="SNP", beta_col="BETA", se_col="SE",
              effect_allele_col="A1", other_allele_col="A2", eaf_col="EAF", pval_col="P")
}
commandArgs <- function(trailingOnly=FALSE, ...) {
  if (isTRUE(trailingOnly)) c(pqtl_path, endpoint_path, out_path, "50000", "European") else base::commandArgs(...)
}

oldwd <- getwd(); on.exit(setwd(oldwd), add=TRUE)
setwd(skill_copy)
source("scripts/phewas_curated_endpoints.R", echo=FALSE)
result <- read.table(out_path, header=TRUE, sep="\t")
cat("Shipped pheWAS rows:", nrow(result), " leading adjusted p:", min(result$p_bonf), "\n")
stopifnot(nrow(result) == 12, all(c("p_bonf", "pval") %in% names(result)),
          min(result$p_bonf) < 0.05)
cat("PASS: current unmodified curated-endpoint script scanned every endpoint and wrote parseable results.\n")
