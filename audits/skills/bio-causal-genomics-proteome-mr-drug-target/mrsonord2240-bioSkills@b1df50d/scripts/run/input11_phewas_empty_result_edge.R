# Input 11 (new edge): exercise the current shipped curated-endpoint script
# when every endpoint returns fewer than two usable SNPs. A robust scan should
# emit an actionable empty-result message and a parseable empty TSV; capture
# the actual behaviour without altering source code.
suppressPackageStartupMessages(library(TwoSampleMR))
audit_root <- "F:/OpenScience/audits/bio-causal-genomics-proteome-mr-drug-target"
skill_copy <- file.path(audit_root, "run", "skill-copy")
work <- file.path(audit_root, "run", "input11_work")
dir.create(work, recursive=TRUE, showWarnings=FALSE)
pqtl <- read.table(file.path(audit_root, "data", "synth_pcsk9_ukbppp_full_window.tsv"), header=TRUE, sep="\t")
pqtl <- subset(pqtl, P < 5e-8)[1:8, c("SNP", "BETA", "SE", "A1", "A2", "EAF", "P")]
pqtl_path <- file.path(work, "pqtl.tsv"); endpoint_path <- file.path(work, "endpoints.tsv"); out_path <- file.path(work, "empty.tsv")
write.table(pqtl, pqtl_path, sep="\t", row.names=FALSE, quote=FALSE)
write.table(data.frame(id="mock_no_overlap"), endpoint_path, sep="\t", row.names=FALSE, quote=FALSE)
available_outcomes <- function() data.frame(id="mock_no_overlap", sample_size=100000, population="European")
extract_outcome_data <- function(snps, outcomes) NULL
commandArgs <- function(trailingOnly=FALSE, ...) if (isTRUE(trailingOnly)) c(pqtl_path, endpoint_path, out_path, "50000", "European") else base::commandArgs(...)
oldwd <- getwd(); on.exit(setwd(oldwd), add=TRUE); setwd(skill_copy)
err <- tryCatch({ source("scripts/phewas_curated_endpoints.R", echo=FALSE); NULL }, error=function(e) conditionMessage(e))
cat("Empty-result behaviour:", if (is.null(err)) "completed" else err, "\n")
cat("Output TSV exists:", file.exists(out_path), "\n")
stopifnot(!is.null(err), !file.exists(out_path))
cat("OBSERVED: current script has no empty-result guard; this is recorded as a P1 reliability finding.\n")
