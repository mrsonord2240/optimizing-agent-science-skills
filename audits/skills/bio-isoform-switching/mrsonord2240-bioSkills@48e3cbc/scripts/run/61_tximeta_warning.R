# 6B follow-up: capture the tximeta warning text (the Skill says 'couldn't find matching transcriptome') and the rowData contents.
suppressPackageStartupMessages({ library(tximeta); library(SummarizedExperiment) })
PD <- "F:/OpenScience/audit-envs/alternative-splicing/public-data"; sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916")
coldata <- data.frame(names = sm, files = file.path(PD, "derived/salmon_gibbs", sm, "quant.sf"), condition = factor(c("GBR", "GBR", "YRI", "YRI")))
makeLinkedTxome(indexDir = file.path(PD, "derived/salmon_idx"), source = "LocalEnsembl", organism = "Homo sapiens", release = "75", genome = "GRCh37", fasta = file.path(PD, "derived/chrX_tx.fa"), gtf = file.path(PD, "rnasplice/reference/genes_chrX.gtf"), write = FALSE)
w <- character(); se <- withCallingHandlers(tximeta(coldata), warning = function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") })
cat("warnings:\n"); print(substr(w, 1, 200)); cat("rowData ncol:", ncol(rowData(se)), " rownames head:", head(rownames(se), 3), "\n")
cat("has gene_id column:", "gene_id" %in% colnames(rowData(se)), "\n"); cat("DONE 61\n")
