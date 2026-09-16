# Pass-5 confirmation audit, Input 7: the KSEA block of the FIXED SKILL.md, extracted programmatically
# and eval'd VERBATIM on six degenerate PX shapes. Two questions:
#   (1) do the new guards catch D4 (single-match prior) and D6 (empty PX) with their own messages?
#   (2) are D1, D2, D3 and D5 -- which the pass-2 correctness fix already handled -- UNCHANGED
#       to the last digit, i.e. were the guards added AROUND the fix and not inside it?
# SYNTHETIC data throughout.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(KSEAapp))
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
RR <- 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun2'
W <- 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/pass5/ksea'
dir.create(W, showWarnings = FALSE, recursive = TRUE)
file.copy(file.path(RR, 'work4', 'PSP&NetworKIN_Kinase_Substrate_Dataset.csv'), W, overwrite = TRUE)
file.copy(file.path(RR, 'work1', 'proteinGroups_global.txt'), W, overwrite = TRUE)
setwd(W)

blk <- ksea_block()
cat('KSEA block:', nchar(blk), 'chars\n')
cat('correctness filter line present verbatim:',
    grepl("ks <- adjusted[is.finite(adjusted$log2FC), ]", blk, fixed = TRUE), '\n')
cat('guards present: nrow(ks)==0', grepl('nrow(ks) == 0', blk, fixed = TRUE),
    '| rep(NULL,nrow(ks))', grepl("rep('NULL', nrow(ks))", blk, fixed = TRUE),
    '| nrow(PX)==0', grepl('nrow(PX) == 0', blk, fixed = TRUE),
    '| coverage', grepl('covered < 2', blk, fixed = TRUE), '\n\n')

rd <- function(f) read.table(f, sep = '\t', header = TRUE, quote = '')
base_adjusted <- readRDS(file.path(RR, 'in1_result.rds'))$adjusted
KSD_full <- read.csv('PSP&NetworKIN_Kinase_Substrate_Dataset.csv')

run_block <- function(label, adj, ksd = NULL, drop_genes = FALSE) {
  e <- new.env(parent = globalenv())
  assign('rd', rd, envir = e)
  assign('adjusted', adj, envir = e)
  b <- blk
  if (!is.null(ksd)) {
    assign('.KSD_OVERRIDE', ksd, envir = e)
    b <- sub("KSData <- read.csv('PSP&NetworKIN_Kinase_Substrate_Dataset.csv')   # user-supplied prior",
             'KSData <- .KSD_OVERRIDE', b, fixed = TRUE)
  }
  if (drop_genes) {
    b <- sub("gene_symbol <- setNames(sub(';.*', '', pg$Gene.names), sub(';.*', '', pg$Protein.IDs))",
             "gene_symbol <- setNames(rep(NA_character_, nrow(pg)), sub(';.*', '', pg$Protein.IDs))",
             b, fixed = TRUE)
  }
  out <- capture.output(
    r <- tryCatch(eval(parse(text = b), envir = e),
                  error = function(x) paste('STOP:', conditionMessage(x))))
  cat('---', label, '---\n')
  cat(grep('^sites in PX', out, value = TRUE), sep = '\n')
  if (is.character(r)) {
    cat('  ', substr(gsub('\\s+', ' ', r), 1, 250), '\n\n', sep = '')
  } else {
    d <- as.data.frame(r)
    cat('  kinases:', nrow(d), '| NaN z:', sum(is.nan(d$z.score)), '\n')
    print(format(d[, c('Kinase.Gene', 'm', 'z.score', 'FDR')], digits = 10), row.names = FALSE)
    cat('\n')
  }
  invisible(r)
}

run_block('D1 baseline (Input 1 adjusted table, one -Inf row)', base_adjusted)

a2 <- base_adjusted; a2$log2FC[which(is.finite(a2$log2FC))[1]] <- Inf
run_block('D2 both +Inf and -Inf present', a2)

a3 <- base_adjusted; a3$adj.pvalue[1:5] <- NA
run_block('D3 NA adjusted p-values in PX', a3)

run_block('D4 prior matching a single substrate site (m = 1)', base_adjusted,
          ksd = KSD_full[1, , drop = FALSE])

a5 <- base_adjusted
subs <- paste0(KSD_full$SUB_ACC_ID[KSD_full$GENE == 'SYN_PRO_KINASE'], '_',
               KSD_full$SUB_MOD_RSD[KSD_full$GENE == 'SYN_PRO_KINASE'])
a5$log2FC[a5$Protein %in% subs] <- 1.0
run_block('D5 zero within-kinase variance (all substrates same FC)', a5)

a6 <- base_adjusted; a6$log2FC <- -Inf
run_block('D6 every site non-finite -> empty PX', a6)

run_block('D7 NEW: proteinGroups carries no gene symbols -> PX empty after the Gene drop',
          base_adjusted, drop_genes = TRUE)
