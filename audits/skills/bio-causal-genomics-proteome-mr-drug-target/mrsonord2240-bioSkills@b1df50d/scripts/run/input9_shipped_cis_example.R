# Input 9 (new regression): execute the current, unmodified shipped
# examples/cis_pqtl_mr.R from a disposable audit copy. Input 1 has already
# created synthetic PCSK9-window data; this script supplies the filenames and
# a local PLINK bfile expected by the example without changing the source.

audit_root <- "F:/OpenScience/audits/bio-causal-genomics-proteome-mr-drug-target"
skill_copy <- file.path(audit_root, "run", "skill-copy")
data_dir <- file.path(skill_copy, "data")
dir.create(data_dir, recursive=TRUE, showWarnings=FALSE)

required <- c("synth_pcsk9_ukbppp_full_window.tsv", "synth_cad_gwas_pcsk9_window.tsv", "synth_pcsk9_vep_pav.tsv")
stopifnot(all(file.exists(file.path(audit_root, "data", required))))
file.copy(file.path(audit_root, "data", required),
          file.path(data_dir, c("ukbppp_pcsk9_full_window.tsv", "cad_gwas.tsv", "pcsk9_vep_pav.tsv")),
          overwrite=TRUE)

# The generated synthetic rs IDs are made resolvable by a disposable copy of
# the verified local test panel. Only bfile labels change; BED genotypes do not.
panel <- "F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/src/plink2R/data"
ld_dir <- file.path(skill_copy, "1kg_EUR")
dir.create(ld_dir, recursive=TRUE, showWarnings=FALSE)
stopifnot(all(file.exists(paste0(panel, c(".bed", ".bim", ".fam")))))
file.copy(paste0(panel, c(".bed", ".fam")), paste0(file.path(ld_dir, "EUR"), c(".bed", ".fam")), overwrite=TRUE)
bim <- read.table(paste0(panel, ".bim"), sep="\t", stringsAsFactors=FALSE)
bim[seq_len(60), 2] <- sprintf("rs%07d", 1000000 + seq_len(60))
write.table(bim, paste0(file.path(ld_dir, "EUR"), ".bim"), sep="\t", row.names=FALSE, col.names=FALSE, quote=FALSE)

oldwd <- getwd(); on.exit(setwd(oldwd), add=TRUE)
setwd(skill_copy)
source("examples/cis_pqtl_mr.R", echo=FALSE)

cat("Shipped-example instruments:", decision$n_instruments,
" PP.H4:", decision$coloc_pp_h4, "\n")
stopifnot(decision$n_instruments >= 2, decision$coloc_pp_h4 >= 0.8,
          !is.na(decision$cis_mr_beta), !is.null(result_correl))
cat("PASS: current unmodified shipped cis-pQTL example completed with local LD.\n")
