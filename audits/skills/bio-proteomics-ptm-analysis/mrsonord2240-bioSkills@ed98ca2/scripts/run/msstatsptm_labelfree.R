#!/usr/bin/env Rscript
# Protein-adjusted phosphosite testing with MSstatsPTM, label-free (DDA/DIA) route.
#
# Class-I pre-filter on the enriched MaxQuant evidence -> MaxQtoMSstatsPTMFormat with a paired global run
# -> dataSummarizationPTM -> groupComparisonPTM (explicit Treatment-vs-Control contrast) -> site rows of
# ADJUSTED.Model -> TREAT-style test against |log2FC| > lfc.
#
# Inputs (key=value; files are looked up inside dir=):
#   dir=<folder>            folder holding the input files (default .)
#   out=<folder>            where adjusted_sites.csv is written (default .)
#   evidence=evidence_phospho.txt          enriched-run MaxQuant evidence.txt
#   annotation=annotation_ptm.csv          Raw.file, Condition, BioReplicate, IsotopeLabelType
#   fasta=uniprot_human.fasta
#   evidence_prot=evidence_global.txt      global (unenriched) run evidence.txt
#   proteinGroups=proteinGroups_global.txt
#   annotation_protein=annotation_protein.csv
#   use_unmod=FALSE         TRUE only when no global run exists (weak proxy, see SKILL.md Decision Tree)
#   lfc=1                   log2 fold-change threshold inside the test
# Output: <out>/adjusted_sites.csv (site rows of ADJUSTED.Model + pvalue_lfc, adj.pvalue_lfc).
#   MSstatsPTM also writes its own log files into the working directory.
# Usage: Rscript scripts/msstatsptm_labelfree.R dir=<data_dir> out=<out_dir> [use_unmod=FALSE] [lfc=1]
opt <- list(dir = '.', out = '.', evidence = 'evidence_phospho.txt', annotation = 'annotation_ptm.csv',
            fasta = 'uniprot_human.fasta', evidence_prot = 'evidence_global.txt',
            proteinGroups = 'proteinGroups_global.txt', annotation_protein = 'annotation_protein.csv',
            use_unmod = 'FALSE', lfc = '1')
for (a in strsplit(commandArgs(trailingOnly = TRUE), '=', fixed = TRUE)) opt[[a[1]]] <- paste(a[-1], collapse = '=')
inp <- function(n) file.path(opt$dir, opt[[n]])
dir.create(opt$out, showWarnings = FALSE, recursive = TRUE)

library(MSstatsPTM)
rd <- function(f) read.table(f, sep = '\t', header = TRUE, quote = '')

use_unmod <- as.logical(opt$use_unmod)   # TRUE only when no global run exists (weak proxy, see Decision Tree)

# The converter uses the best-localized sequence as is and keeps unmodified peptides from the
# enriched runs, so apply the class-I rule to the enriched evidence FIRST: keep rows carrying the
# modification whose best site probability (from 'Phospho (STY) Probabilities') is >= 0.75.
# The use_unmod proxy needs the unmodified rows, so keep those too when it is on.
ev <- rd(inp('evidence'))
site_prob <- vapply(regmatches(ev$Phospho..STY..Probabilities,
                               gregexpr('(?<=\\()[0-9.]+(?=\\))', ev$Phospho..STY..Probabilities, perl = TRUE)),
                    function(p) if (length(p)) max(as.numeric(p)) else NA_real_, numeric(1))
is_mod <- grepl('Phospho \\(STY\\)', ev$Modified.sequence)
keep <- is_mod & !is.na(site_prob) & site_prob >= 0.75
if (use_unmod) keep <- keep | !is_mod
ev <- ev[keep, ]

# Converters are <Tool>toMSstatsPTMFormat and return a list with $PTM and $PROTEIN.
# MaxQtoMSstatsPTMFormat reads the MaxQuant 'evidence.txt' (NOT the Phospho (STY)Sites
# table -- the pandas multiplicity-expansion is a SEPARATE workflow); the FASTA maps
# peptides back to site coordinates. $PROTEIN is built ONLY when `evidence_prot` (the GLOBAL
# run's evidence) is given together with its proteinGroups and annotation.
input <- MaxQtoMSstatsPTMFormat(
  evidence = ev,
  annotation = read.csv(inp('annotation')),
  fasta_path = inp('fasta'),
  evidence_prot = rd(inp('evidence_prot')),
  proteinGroups = rd(inp('proteinGroups')),
  annotation_protein = read.csv(inp('annotation_protein')),
  mod_id = '\\(Phospho \\(STY\\)\\)',
  which_proteinid_ptm = 'Proteins',
  which_proteinid_protein = 'Proteins',
  use_unmod_peptides = use_unmod
)
stopifnot('PROTEIN' %in% names(input))   # no protein dataset -> nothing to adjust against

# append defaults to TRUE and requires a log file, so set it FALSE when use_log_file = FALSE
summarized <- dataSummarizationPTM(input, use_log_file = FALSE, append = FALSE)

# data.type is 'LabelFree' (DDA/DIA label-free) or 'TMT' -- NOT the converter's labeling_type 'LF'.
# Pass an explicit contrast: the default pairwise Label is 'Control vs Treatment' (log2FC = Control - Treatment).
# Columns must follow the sorted Condition levels.
contrast <- matrix(c(-1, 1), nrow = 1, dimnames = list('Treatment vs Control', c('Control', 'Treatment')))
result <- groupComparisonPTM(summarized, data.type = 'LabelFree', contrast.matrix = contrast)

# Three models; the adjusted one is the deliverable. Keep site rows only (Protein_<residue><position>).
adjusted <- result$ADJUSTED.Model
adjusted <- adjusted[grepl('_[STY][0-9]+', adjusted$Protein), ]

# A claim of "changed more than 2-fold" needs the threshold INSIDE the test (TREAT-style), not
# adj.pvalue < 0.05 & |log2FC| > 1 as a post-hoc double filter, whose FDR refers to log2FC != 0.
lfc <- as.numeric(opt$lfc)
adjusted$pvalue_lfc <- pt((abs(adjusted$log2FC) - lfc) / adjusted$SE, adjusted$DF, lower.tail = FALSE)
adjusted$adj.pvalue_lfc <- p.adjust(adjusted$pvalue_lfc, method = 'BH')
regulated <- adjusted[!is.na(adjusted$adj.pvalue_lfc) & adjusted$adj.pvalue_lfc < 0.05, ]

# How much of each call was protein-driven: compare PTM.Model vs ADJUSTED.Model.
write.csv(adjusted, file.path(opt$out, 'adjusted_sites.csv'), row.names = FALSE)
cat('names(input):', names(input), '| ADJUSTED site rows:', nrow(adjusted), '| regulated (TREAT):', nrow(regulated),
    '| Label:', unique(as.character(adjusted$Label)), '\n')
