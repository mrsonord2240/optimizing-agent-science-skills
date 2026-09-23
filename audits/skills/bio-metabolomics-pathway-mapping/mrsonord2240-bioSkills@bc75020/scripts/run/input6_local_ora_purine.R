# New Input 6: independent regression check of the fixed SKILL.md's "Local-Only ORA" function,
# on a DIFFERENT biology (purine metabolism) than the fix's own TCA-cycle example, to make sure
# the fix generalizes rather than being tuned to one worked example.
suppressMessages(library(MetaboAnalystR))
suppressMessages(library(KEGGREST))
set.seed(42)

# --- Step 1: map compound names -> KEGG IDs using the Skill's own documented mapping call
# (local only: CrossReferencing() matches against MetaboAnalystR's bundled/cached compound_db.qs,
# no network send of the compound list -- confirmed by source inspection in source_audit2.log)
compounds <- readLines("../data/input6_purine_compounds.txt")
compounds <- compounds[nzchar(compounds)]
current.msg <- character(0); err.vec <- character(0)
mSet <- InitDataObjects('conc', 'pathora', FALSE)
mSet <- SetOrganism(mSet, 'hsa')
mSet <- Setup.MapData(mSet, compounds)
mSet <- CrossReferencing(mSet, 'name')
mSet <- CreateMappingResultTable(mSet)
map_tbl <- mSet$dataSet$map.table
cat("=== Mapping table (purine set) ===\n"); print(map_tbl)
kegg_ids <- map_tbl[, "KEGG"]
kegg_ids <- kegg_ids[kegg_ids != "" & !is.na(kegg_ids)]
cat(sprintf("\nMapped %d/%d compounds to KEGG IDs: %s\n", length(kegg_ids), length(compounds), paste(kegg_ids, collapse=", ")))
stopifnot(length(kegg_ids) >= 6)   # assert mapping actually worked before trusting anything downstream

# --- Step 2: SKILL.md's Local-Only ORA function, copied verbatim ---
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

# --- Step 3: build two DIFFERENT backgrounds than the fix's own test ---
# All-of-KEGG background: every compound KEGGREST links to at least one pathway.
links_all <- keggLink('pathway', 'compound')
all_kegg_ids <- unique(sub('^cpd:', '', names(links_all)))
cat(sprintf("\nAll-of-KEGG background size: %d\n", length(all_kegg_ids)))

# Assay-coverage background: a REAL random sample of 250 KEGG compound IDs actually in the
# pathway-linked universe (not the fix's own sequential C00001-C00320 list), forced to include
# the purine hits so they are assay-detectable, mimicking a realistic small polar-metabolite panel.
non_hit_pool <- setdiff(all_kegg_ids, kegg_ids)
assay_bg <- unique(c(kegg_ids, sample(non_hit_pool, 240)))
cat(sprintf("Assay-coverage background size: %d\n", length(assay_bg)))

ora_all   <- local_kegg_ora(kegg_ids, all_kegg_ids)
ora_assay <- local_kegg_ora(kegg_ids, assay_bg)

cat("\n=== Local-Only ORA: all-of-KEGG background (top 5) ===\n")
print(head(ora_all, 5))
cat("\n=== Local-Only ORA: assay-coverage background (top 5) ===\n")
print(head(ora_assay, 5))

# --- Step 4: assertions against known purine biology ---
purine_row_all   <- ora_all[ora_all$pathway == "hsa00230", ]
purine_row_assay <- ora_assay[ora_assay$pathway == "hsa00230", ]
cat("\nhsa00230 (Purine metabolism) row, all-of-KEGG background:\n"); print(purine_row_all)
cat("hsa00230 (Purine metabolism) row, assay-coverage background:\n"); print(purine_row_assay)

stopifnot(nrow(purine_row_all) == 1)
stopifnot(nrow(purine_row_assay) == 1)
stopifnot(purine_row_all$p.value < 0.001)          # should be a strong hit either way
stopifnot(purine_row_assay$p.value < 0.05)
stopifnot(ora_all$pathway[1] == "hsa00230" || ora_assay$pathway[1] == "hsa00230")  # top or near-top hit in at least one background
cat("\nALL ASSERTIONS PASSED: Local-Only ORA reproduces purine metabolism as a strong, biologically\n")
cat("correct hit under two independently constructed backgrounds, confirming the fix generalizes\n")
cat("beyond its own TCA-cycle worked example.\n")
