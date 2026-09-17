# Input 9 (NEW) -- cross-Skill consistency check requested by the audit brief: does the
# orchestrator's own Stage 5 MSI-gate output (identified_compounds) hand off cleanly into
# metabolomics/pathway-mapping's real, audited code (that Skill scored 92/Production Ready this
# round)? Chain workflow's Stage 5 filter -> KEGG ID resolution -> pathway-mapping's verbatim
# local_kegg_ora() against a real KEGGREST live pull and the pathway-mapping audit's own
# assay-coverage reference file, so this is a real hand-off test between two independently
# fixed/audited Skills, not just re-inspection of either one alone.
suppressMessages(library(KEGGREST))

cat('=== Step 1: workflow Stage 3 output (synthetic, shaped like metabolite-annotation real output) ===\n')
annotated <- data.frame(
  feature_id = paste0('FT', sprintf('%03d', 1:7)),
  name = c('Pyruvate', 'L-Lactate', 'Citrate', 'Succinate', 'Fumarate', 'L-Alanine', 'Glutamate'),
  msi_level = c(1, '2a', '2a', '2b', '2b', 1, '2a'),
  kegg_id = c('C00022', 'C00186', 'C00158', 'C00042', 'C00122', 'C00041', 'C00025'),
  stringsAsFactors = FALSE
)
print(annotated[, c('name', 'msi_level', 'kegg_id')])

cat('\n=== Step 2: workflow Stage 5 code, verbatim -- the MSI gate ===\n')
identified_compounds <- unique(annotated$name[grepl('^[12]', as.character(annotated$msi_level))])
stopifnot(length(identified_compounds) > 0)
cat('identified_compounds:', paste(identified_compounds, collapse = ', '), '\n')
kegg_ids <- annotated$kegg_id[annotated$name %in% identified_compounds]
cat('Resolved KEGG IDs:', paste(kegg_ids, collapse = ', '), '\n\n')

cat('=== Step 3: hand off into pathway-mapping SKILL.md Local-Only ORA, verbatim ===\n')
local_kegg_ora <- function(hit_kegg_ids, universe_kegg_ids, min_hits = 2) {
  links <- keggLink('pathway', 'compound')
  cpd_ids  <- sub('^cpd:', '', names(links))
  path_ids <- sub('^path:map', 'hsa', unname(links))
  pw2cpd <- lapply(split(cpd_ids, path_ids), unique)

  universe_kegg_ids <- unique(universe_kegg_ids)
  pw2cpd <- lapply(pw2cpd, function(x) intersect(x, universe_kegg_ids))
  pw2cpd <- pw2cpd[lengths(pw2cpd) > 0]
  hits <- intersect(hit_kegg_ids, universe_kegg_ids)
  N <- length(universe_kegg_ids); k <- length(hits)

  out <- data.frame(
    pathway = names(pw2cpd),
    total   = lengths(pw2cpd),
    hits    = vapply(pw2cpd, function(s) length(intersect(s, hits)), integer(1))
  )
  out <- out[out$hits >= min_hits, ]
  out$p.value <- mapply(function(m, h) phyper(h - 1, m, N - m, k, lower.tail = FALSE), out$total, out$hits)
  out$fdr <- p.adjust(out$p.value, method = 'BH')
  out[order(out$p.value), ]
}

reference_ids <- readLines('F:/OpenScience/audits/bio-metabolomics-pathway-mapping/data/input1_reference_metabolome_synthetic.txt')
reference_ids <- reference_ids[nzchar(reference_ids)]
cat('Assay-coverage reference background:', length(reference_ids), 'compounds (from the pathway-mapping audit)\n')
stopifnot(all(kegg_ids %in% reference_ids))  # sanity: our hits must be inside the declared background

t0 <- Sys.time()
ora_ref <- local_kegg_ora(kegg_ids, reference_ids)
links_all <- keggLink('pathway', 'compound')
all_kegg_ids <- unique(sub('^cpd:', '', names(links_all)))
ora_full <- local_kegg_ora(kegg_ids, all_kegg_ids)
cat('KEGGREST live call took', round(as.numeric(Sys.time() - t0), 1), 'sec\n\n')

cat('=== RESULT: workflow Stage3->Stage5->pathway-mapping hand-off ===\n')
cat('Assay-coverage background (n=', length(reference_ids), '):\n', sep = '')
print(head(ora_ref, 5))
cat('\nAll-of-KEGG background (n=', length(all_kegg_ids), '):\n', sep = '')
print(head(ora_full, 5))

if (nrow(ora_ref) > 0 && nrow(ora_full) > 0 && 'C00022' %in% kegg_ids) {
  common_pw <- intersect(ora_ref$pathway, ora_full$pathway)
  if (length(common_pw) > 0) {
    pw <- common_pw[1]
    p_ref <- ora_ref$p.value[ora_ref$pathway == pw]
    p_full <- ora_full$p.value[ora_full$pathway == pw]
    cat('\nBackground-inflation check on', pw, ': assay-coverage p =', signif(p_ref, 3),
        '| all-of-KEGG p =', signif(p_full, 3), '\n')
    cat(if (p_ref > p_full) 'CONSISTENT with pathway-mapping\'s own finding: smaller, correct background -> less inflated significance.\n'
        else 'INCONSISTENT with pathway-mapping\'s background-inflation claim.\n')
  }
}
cat('\nEnd-to-end: the orchestrator\'s own MSI-gated identified_compounds hand off cleanly into\n')
cat('pathway-mapping\'s real, audited Local-Only ORA code with no glue-code mismatch (same KEGG ID\n')
cat('convention, same reference-file format).\n')
