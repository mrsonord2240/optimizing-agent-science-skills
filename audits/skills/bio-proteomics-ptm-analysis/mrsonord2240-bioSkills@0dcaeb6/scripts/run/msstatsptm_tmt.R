#!/usr/bin/env Rscript
# Protein-adjusted phosphosite testing with MSstatsPTM, TMT / isobaric route.
#
# Same adjustment as msstatsptm_labelfree.R; only three calls differ: labeling_type = 'TMT' on the
# converter, dataSummarizationPTM_TMT, and data.type = 'TMT'. Every plex needs a pooled reference
# channel carried as Condition = 'Norm' in the annotation.
#
# Inputs (key=value; files are looked up inside dir=):
#   dir=<folder>   out=<folder>
#   evidence=evidence_phospho_tmt.txt   annotation=annotation_ptm_tmt.csv   fasta=uniprot_human.fasta
#   evidence_prot=evidence_global_tmt.txt   proteinGroups=proteinGroups_global.txt
#   annotation_protein=annotation_protein_tmt.csv
#   Channel names in the annotations follow MaxQuant's 0-indexed reporter suffixes (channel.0 .. channel.9).
# Output: <out>/adjusted_sites_tmt.csv (site rows of ADJUSTED.Model). MSstatsPTM/MSstatsTMT write log files
#   into the working directory.
# Usage: Rscript scripts/msstatsptm_tmt.R dir=<data_dir> out=<out_dir>
opt <- list(dir = '.', out = '.', evidence = 'evidence_phospho_tmt.txt', annotation = 'annotation_ptm_tmt.csv',
            fasta = 'uniprot_human.fasta', evidence_prot = 'evidence_global_tmt.txt',
            proteinGroups = 'proteinGroups_global.txt', annotation_protein = 'annotation_protein_tmt.csv')
for (a in strsplit(commandArgs(trailingOnly = TRUE), '=', fixed = TRUE)) opt[[a[1]]] <- paste(a[-1], collapse = '=')
inp <- function(n) file.path(opt$dir, opt[[n]])
dir.create(opt$out, showWarnings = FALSE, recursive = TRUE)

library(MSstatsPTM)
rd <- function(f) read.table(f, sep = '\t', header = TRUE, quote = '')

# Class-I pre-filter on the ENRICHED evidence, exactly as in the label-free route.
ev <- rd(inp('evidence'))
site_prob <- vapply(regmatches(ev$Phospho..STY..Probabilities,
                               gregexpr('(?<=\\()[0-9.]+(?=\\))', ev$Phospho..STY..Probabilities, perl = TRUE)),
                    function(p) if (length(p)) max(as.numeric(p)) else NA_real_, numeric(1))
ev <- ev[grepl('Phospho \\(STY\\)', ev$Modified.sequence) & !is.na(site_prob) & site_prob >= 0.75, ]

# TMT annotation: Run, Fraction, TechRepMixture, Channel, Condition, Mixture, BioReplicate.
# Channel names follow the reporter-column suffixes MaxQuant wrote, and those are 0-indexed: a
# 10-plex has 'Reporter intensity corrected 0' .. '9', so the annotation needs 'channel.0' .. 'channel.9'
# (the CORRECTED columns, not the raw reporters). Read the suffixes off your own evidence header;
# 'channel.1' .. 'channel.10' is rejected with 'the channel name must be matched with that in input
# data', which never mentions the off-by-one.
# Give the pooled reference channel Condition = 'Norm' in EVERY plex.
input <- MaxQtoMSstatsPTMFormat(
  evidence = ev,
  annotation = read.csv(inp('annotation')),
  fasta_path = inp('fasta'),
  evidence_prot = rd(inp('evidence_prot')),
  proteinGroups = rd(inp('proteinGroups')),
  annotation_protein = read.csv(inp('annotation_protein')),
  labeling_type = 'TMT',          # the single converter switch; default is 'LF'
  mod_id = '\\(Phospho \\(STY\\)\\)',
  which_proteinid_ptm = 'Proteins',
  which_proteinid_protein = 'Proteins',
  use_unmod_peptides = FALSE)
stopifnot('PROTEIN' %in% names(input))

# TMT summarization is its own function. reference_norm / reference_norm.PTM (default TRUE) apply
# the 'Norm'-channel bridge; remove_norm_channel (default TRUE) drops that channel afterwards, so
# the contrast below names only the biological conditions.
summarized <- dataSummarizationPTM_TMT(input, use_log_file = FALSE, append = FALSE)

contrast <- matrix(c(-1, 1), nrow = 1, dimnames = list('Treatment vs Control', c('Control', 'Treatment')))
result <- groupComparisonPTM(summarized, data.type = 'TMT', contrast.matrix = contrast)

adjusted <- result$ADJUSTED.Model
adjusted <- adjusted[grepl('_[STY][0-9]+', adjusted$Protein), ]
# From here the TREAT-style threshold and the PTM.Model-vs-ADJUSTED.Model comparison are identical to
# the label-free route (msstatsptm_labelfree.R); only the three calls above differ.
write.csv(adjusted, file.path(opt$out, 'adjusted_sites_tmt.csv'), row.names = FALSE)
cat('names(input):', names(input), '| ADJUSTED site rows:', nrow(adjusted), '| Label:', unique(as.character(adjusted$Label)), '\n')
