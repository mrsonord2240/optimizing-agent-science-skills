#!/usr/bin/env Rscript
# Construct an audit-only strict no-global fixture from MSstatsPTM's bundled LF data.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop('usage: build_fixture.R <fixture-dir>')
fixture <- normalizePath(args[[1]], winslash = '/', mustWork = FALSE)
dir.create(fixture, recursive = TRUE, showWarnings = FALSE)
library(MSstatsPTM)
data('maxq_lf_evidence', package = 'MSstatsPTM')
data('maxq_lf_annotation', package = 'MSstatsPTM')
e <- maxq_lf_evidence
a <- maxq_lf_annotation
is_mod <- grepl('Phospho \\(STY\\)', e$Modified.sequence)
prob <- vapply(regmatches(e$Phospho..STY..Probabilities,
  gregexpr('(?<=\\()[0-9.]+(?=\\))', e$Phospho..STY..Probabilities, perl = TRUE)),
  function(x) if (length(x)) max(as.numeric(x)) else NA_real_, numeric(1))
class_i <- is_mod & !is.na(prob) & prob >= 0.75
ann <- unique(a[, c('Raw.file', 'Condition', 'BioReplicate'), drop = FALSE])
raws <- as.character(ann$Raw.file)
valid <- vapply(sort(unique(as.character(e$Proteins[class_i]))), function(protein) {
  un <- e[!is_mod & as.character(e$Proteins) == protein, , drop = FALSE]
  ptm <- e[class_i & as.character(e$Proteins) == protein, , drop = FALSE]
  if (!nrow(ptm) || length(unique(as.character(un$Sequence))) < 2L || !all(raws %in% as.character(un$Raw.file))) return(FALSE)
  all(vapply(split(ann$BioReplicate, ann$Condition), function(x) length(unique(x)) >= 2L, integer(1)))
}, logical(1))
candidates <- names(valid)[valid]
if (!length(candidates)) stop('No bundled-data protein meets strict proxy fixture criteria.')
target <- candidates[[1]]
fixture_e <- e[as.character(e$Proteins) == target, , drop = FALSE]
write.table(fixture_e, file.path(fixture, 'evidence_phospho.txt'), sep = '\t', row.names = FALSE, quote = FALSE)
write.csv(a, file.path(fixture, 'annotation_ptm.csv'), row.names = FALSE)
fasta <- system.file('extdata', 'maxq_lf_fasta.fasta', package = 'MSstatsPTM')
if (!nzchar(fasta) || !file.copy(fasta, file.path(fixture, 'uniprot_human.fasta'), overwrite = FALSE)) stop('Could not copy bundled FASTA.')
un <- fixture_e[!grepl('Phospho \\(STY\\)', fixture_e$Modified.sequence), , drop = FALSE]
summary <- c(
  paste('target_protein=', target),
  paste('ptm_rows=', sum(grepl('Phospho \\(STY\\)', fixture_e$Modified.sequence))),
  paste('unmodified_rows=', nrow(un)),
  paste('unique_unmodified_peptides=', length(unique(as.character(un$Sequence)))),
  paste('raw_files=', paste(sort(unique(as.character(a$Raw.file))), collapse = ',')),
  paste('conditions=', paste(sort(unique(as.character(a$Condition))), collapse = ',')),
  paste('bioreplicates_per_condition=', paste(vapply(split(a$BioReplicate, a$Condition), function(x) length(unique(x)), integer(1)), collapse = ','))
)
writeLines(summary, file.path(fixture, 'fixture_summary.txt'))
cat(paste(summary, collapse = '\n'), '\n')
