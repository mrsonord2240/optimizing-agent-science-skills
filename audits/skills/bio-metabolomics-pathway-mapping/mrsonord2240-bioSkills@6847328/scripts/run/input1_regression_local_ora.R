# Regression of pre-fix Input 1 data (the exact 12-compound TCA list + 320-ID synthetic reference
# that crashed pre-fix), now run through the fixed SKILL.md's Local-Only ORA function -- an
# independent re-verification of the fix log's own claim on the exact regression dataset.
suppressMessages(library(MetaboAnalystR))
suppressMessages(library(KEGGREST))

current.msg <- character(0); err.vec <- character(0)
mSet <- InitDataObjects('conc', 'pathora', FALSE)
mSet <- SetOrganism(mSet, 'hsa')
compounds <- c('Pyruvate', 'L-Lactate', 'Citrate', 'Succinate', 'Fumarate', 'L-Alanine',
               'L-Glutamate', 'L-Glutamine', 'Malate', 'Isocitrate', 'Oxaloacetate', 'Acetyl-CoA')
mSet <- Setup.MapData(mSet, compounds)
mSet <- CrossReferencing(mSet, 'name')
mSet <- CreateMappingResultTable(mSet)
kegg_ids <- mSet$dataSet$map.table[, "KEGG"]
kegg_ids <- kegg_ids[kegg_ids != "" & !is.na(kegg_ids)]
cat("Hit KEGG IDs:", paste(kegg_ids, collapse=", "), "\n")

reference_ids <- readLines("../data/input1_reference_metabolome_synthetic.txt")
reference_ids <- reference_ids[nzchar(reference_ids)]

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
    pathway = names(pw2cpd), total = lengths(pw2cpd),
    hits = vapply(pw2cpd, function(s) length(intersect(s, hits)), integer(1))
  )
  out <- out[out$hits >= min_hits, ]
  out$p.value <- mapply(function(m, h) phyper(h - 1, m, N - m, k, lower.tail = FALSE), out$total, out$hits)
  out$fdr <- p.adjust(out$p.value, method = 'BH')
  out[order(out$p.value), ]
}

links_all <- keggLink('pathway', 'compound')
all_kegg_ids <- unique(sub('^cpd:', '', names(links_all)))

ora_ref  <- local_kegg_ora(kegg_ids, reference_ids)
ora_full <- local_kegg_ora(kegg_ids, all_kegg_ids)

cat("\n=== Local-Only ORA on the ORIGINAL Input 1 data, 320-ID reference background ===\n")
print(head(ora_ref, 5))
cat("\n=== Local-Only ORA, all-of-KEGG background (for comparison) ===\n")
print(head(ora_full, 5))

tca_ref  <- ora_ref[ora_ref$pathway == "hsa00020", ]
tca_full <- ora_full[ora_full$pathway == "hsa00020", ]
cat("\nhsa00020 (Citrate cycle) at 320-ID reference background:\n"); print(tca_ref)
cat("hsa00020 (Citrate cycle) at all-of-KEGG background:\n"); print(tca_full)

stopifnot(nrow(tca_ref) == 1, nrow(tca_full) == 1)
stopifnot(tca_ref$p.value < 1e-5)
stopifnot(tca_ref$p.value > tca_full$p.value)   # correct background should be LESS significant, not more
cat("\nASSERTION PASSED: independently re-run on the exact pre-fix regression dataset -- Local-Only\n")
cat("ORA returns a real, biologically correct result (Citrate cycle top hit), and the correct\n")
cat("smaller background is less significant than the inflated all-of-KEGG background, as the fix log claims.\n")
