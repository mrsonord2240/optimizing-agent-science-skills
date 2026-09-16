
# RE-AUDIT B, NEW PTM Input D (Edge): does the pass-2 KSEA fix generalize, or did it only patch the
# one degenerate case the previous auditor happened to hit? Four PX shapes the Skill's own contract
# permits are pushed through the SKILL.md KSEA block's PX construction + KSEA.Scores.
# SYNTHETIC data throughout (audit phospho set + its synthetic prior).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(KSEAapp))
RR <- 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun2'
W  <- file.path(RR, 'workD'); dir.create(W, showWarnings = FALSE, recursive = TRUE)
file.copy(file.path(RR, 'work4', 'PSP&NetworKIN_Kinase_Substrate_Dataset.csv'), W, overwrite = TRUE)
setwd(W)
KSD <- read.csv('PSP&NetworKIN_Kinase_Substrate_Dataset.csv')
adjusted <- readRDS(file.path(RR, 'in1_result.rds'))$adjusted
pg <- read.table(file.path(RR, 'work1', 'proteinGroups_global.txt'), sep='\t', header=TRUE, quote='')
gene_symbol <- setNames(sub(';.*', '', pg$Gene.names), sub(';.*', '', pg$Protein.IDs))

# The Skill's PX construction, exactly as SKILL.md writes it
build_PX <- function(adj) {
  ks <- adj[is.finite(adj$log2FC), ]
  PX <- data.frame(Protein = sub('_[STY][0-9]+$', '', ks$Protein),
                   Gene = gene_symbol[sub('_[STY][0-9]+$', '', ks$Protein)],
                   Peptide = 'NULL',
                   Residue.Both = sub('^.*_', '', ks$Protein),
                   p = ks$adj.pvalue, FC = 2^ks$log2FC)
  PX[!is.na(PX$Gene), ]
}
probe <- function(label, adj, ksd = KSD) {
  PX <- tryCatch(build_PX(adj), error = function(e) { cat("---", label, "---", '
', "  PX CONSTRUCTION ERROR:", conditionMessage(e), '
'); NULL })
  if (is.null(PX)) return(invisible(NULL))
  r <- tryCatch(KSEA.Scores(ksd, PX, NetworKIN = FALSE, NetworKIN.cutoff = 3),
                error = function(e) paste('ERROR:', conditionMessage(e)),
                warning = function(w) paste('WARNING:', conditionMessage(w)))
  cat('\n---', label, '---\n  PX rows:', nrow(PX), '| non-finite FC:', sum(!is.finite(PX$FC)),
      '| NA p:', sum(is.na(PX$p)), '\n')
  if (is.character(r)) { cat('  result:', r, '\n'); return(invisible(NULL)) }
  cat('  kinases:', nrow(r), '| NaN z:', sum(is.nan(r$z.score)), '| non-finite z:', sum(!is.finite(r$z.score)),
      '| NA FDR:', sum(is.na(r$FDR)), '\n')
  print(r[, c('Kinase.Gene','m','z.score','FDR')], row.names = FALSE)
  invisible(r)
}

probe('D1 baseline (Input 1 adjusted table, one -Inf row)', adjusted)

# D2: a site quantified only in TREATMENT -> log2FC = +Inf as well as the existing -Inf
a2 <- adjusted; a2$log2FC[which(is.finite(a2$log2FC))[1]] <- Inf
probe('D2 both +Inf and -Inf present', a2)

# D3: adj.pvalue NA on several rows (MSstats returns NA when a model cannot be fit)
a3 <- adjusted; a3$adj.pvalue[1:5] <- NA
probe('D3 NA adjusted p-values in PX', a3)

# D4: a prior that matches only ONE site (m = 1 for one kinase, 0 for the rest)
one <- KSD[1, , drop = FALSE]
probe('D4 prior matching a single substrate site (m = 1)', adjusted, one)

# D5: every substrate of one kinase has an identical fold change (zero within-set variance)
a5 <- adjusted
subs <- paste0(KSD$SUB_ACC_ID[KSD$GENE == 'SYN_PRO_KINASE'], '_', KSD$SUB_MOD_RSD[KSD$GENE == 'SYN_PRO_KINASE'])
a5$log2FC[a5$Protein %in% subs] <- 1.0
probe('D5 zero within-kinase variance (all substrates same FC)', a5)

# D6: ALL sites non-finite -> PX empty
a6 <- adjusted; a6$log2FC <- -Inf
probe('D6 every site non-finite -> empty PX', a6)
