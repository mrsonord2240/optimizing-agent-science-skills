# Input 3 (Edge, regression -- load-bearing clamp claim) -- prompt:
# "My DE came out of edgeR QL so there's no Wald stat, only logFC and PValue -- and a few PValue
# are exactly 0. The table is keyed by gene SYMBOL, it isn't sorted, and about 250 rows are
# duplicates. Build the ranking the right way and tell me what pathways are enriched."
#
# Uses the Skill's CURRENT documented recipe: sign(logFC) * -log10(pmax(PValue, 1e-30))
# (the fixed clamp -- SKILL.md "Build the Ranked Vector" table + usage-guide.md).

suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
  library(msigdbr)
})

edg <- read.csv("F:/OpenScience/audits/bio-pathway-gsea/data/SYNTHETIC_edger_qlf.csv")
cat("edgeR table rows =", nrow(edg), "| duplicate gene names =", sum(duplicated(edg$gene)),
    "| PValue == 0 exactly:", sum(edg$PValue == 0), "| has a stat column:", "stat" %in% names(edg), "\n")

# ---- (A) the Skill's CURRENT recipe: pmax(PValue, 1e-30) ----
gl_new <- sign(edg$logFC) * -log10(pmax(edg$PValue, 1e-30))
names(gl_new) <- edg$gene
gl_new <- gl_new[!is.na(gl_new)]
gl_new <- gl_new[!duplicated(names(gl_new))]
gl_new <- sort(gl_new, decreasing = TRUE)
cat("signed-p vector (clamp 1e-30): n =", length(gl_new), "| any Inf:", any(is.infinite(gl_new)),
    "| max", round(max(gl_new),2), "| min", round(min(gl_new),2), "\n")

zero_syms <- names(gl_new)[gl_new == max(gl_new) | gl_new == min(gl_new)]
n_zero <- sum(edg$PValue[!duplicated(edg$gene)] == 0)
weights <- sort(abs(gl_new), decreasing = TRUE)
clamped_weight <- 30  # -log10(1e-30)
n_clamped <- sum(abs(gl_new) >= clamped_weight - 1e-6)
next_largest <- max(weights[weights < clamped_weight - 1e-6])
cat("\n--- (B) weight-distortion check at the fixed clamp (1e-30) ---\n")
cat("clamped genes (PValue == 0):", n_clamped, "of", length(gl_new), "\n")
cat("their weight |stat| =", clamped_weight, "; next-largest measured |stat| =", round(next_largest,2),
    " ->", round(clamped_weight / next_largest, 1), "x the strongest measured gene\n")
cat("share of total sum(|stat|) held by the clamped genes:",
    round(100 * (n_clamped * clamped_weight) / sum(abs(gl_new)), 2), "%\n")

# ---- (C) same construction but with the OLD 1e-300 clamp, for direct before/after comparison ----
gl_old <- sign(edg$logFC) * -log10(pmax(edg$PValue, 1e-300))
names(gl_old) <- edg$gene
gl_old <- gl_old[!is.na(gl_old)]
gl_old <- gl_old[!duplicated(names(gl_old))]
gl_old <- sort(gl_old, decreasing = TRUE)
old_clamped_weight <- 300
old_n_clamped <- sum(abs(gl_old) >= old_clamped_weight - 1e-6)
old_next_largest <- max(abs(gl_old)[abs(gl_old) < old_clamped_weight - 1e-6])
cat("\n--- (C) same math at the OLD clamp (1e-300), for comparison ---\n")
cat("clamped genes:", old_n_clamped, "| weight", old_clamped_weight, "; next-largest",
    round(old_next_largest,2), " ->", round(old_clamped_weight/old_next_largest,1), "x\n")
cat("share of total sum(|stat|):", round(100*(old_n_clamped*old_clamped_weight)/sum(abs(gl_old)),2), "%\n")

# ---- (D) recovery test: fast Hallmark GSEA(TERM2GENE) under both clamps ----
map <- bitr(names(gl_new), fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)
cat("\nbitr SYMBOL->ENTREZID: mapped", nrow(map), "of", length(gl_new),
    sprintf("( %.1f %% )", 100*nrow(map)/length(gl_new)), "| one-to-many symbol rows:",
    sum(duplicated(map$SYMBOL)), "\n")
map <- map[!duplicated(map$SYMBOL), ]

to_entrez <- function(gl) {
  gl2 <- gl[names(gl) %in% map$SYMBOL]
  names(gl2) <- map$ENTREZID[match(names(gl2), map$SYMBOL)]
  gl2 <- gl2[!duplicated(names(gl2))]
  sort(gl2, decreasing = TRUE)
}
gl_new_ez <- to_entrez(gl_new)
gl_old_ez <- to_entrez(gl_old)

h <- msigdbr(species = "Homo sapiens", collection = "H")
t2g <- h[, c("gs_name", "ncbi_gene")]

run_h <- function(gl_ez, label) {
  set.seed(123)
  r <- tryCatch(GSEA(geneList = gl_ez, TERM2GENE = t2g, exponent = 1, minGSSize = 10,
                      maxGSSize = 500, eps = 0, pvalueCutoff = 0.05, seed = TRUE, verbose = FALSE),
                error = function(e) { cat(label, "ERROR:", conditionMessage(e), "\n"); NULL })
  if (is.null(r)) return(invisible(NULL))
  res <- as.data.frame(r)
  up_ok <- "HALLMARK_TNFA_SIGNALING_VIA_NFKB" %in% res$ID
  down_ok <- "HALLMARK_G2M_CHECKPOINT" %in% res$ID
  cat(label, ": ", nrow(res), "terms | planted UP recovered:", up_ok,
      "| planted DOWN recovered:", down_ok, "\n")
  res
}
cat("\n--- (D) recovery under each clamp (Hallmark GSEA, same ranking-construction path) ---\n")
res_new <- run_h(gl_new_ez, "clamp 1e-30 (current SKILL.md)")
res_old <- run_h(gl_old_ez, "clamp 1e-300 (pre-fix)      ")

# ---- (E) is "unsorted or duplicated" still a hard error on this stack? ----
cat("\n--- (E) unsorted / duplicated geneList: hard error or silent? ---\n")
base_ez <- gl_new_ez
r_ok <- tryCatch({ gseGO(geneList = base_ez, OrgDb = org.Hs.eg.db, keyType = "ENTREZID", ont = "BP",
                          minGSSize = 200, maxGSSize = 500, eps = 0, pvalueCutoff = 1, verbose = FALSE); "OK" },
                  error = function(e) paste("ERROR:", conditionMessage(e)))
cat("sorted, unique (baseline)         :", r_ok, "\n")

shuffled <- sample(base_ez)
r_shuf <- tryCatch({ gseGO(geneList = shuffled, OrgDb = org.Hs.eg.db, keyType = "ENTREZID", ont = "BP",
                            minGSSize = 200, maxGSSize = 500, eps = 0, pvalueCutoff = 1, verbose = FALSE); "OK" },
                    error = function(e) paste("ERROR:", conditionMessage(e)))
cat("SHUFFLED, unique                  :", r_shuf, "\n")

dup_ez <- c(base_ez, base_ez[1:5])
r_dup <- tryCatch({ gseGO(geneList = dup_ez, OrgDb = org.Hs.eg.db, keyType = "ENTREZID", ont = "BP",
                           minGSSize = 200, maxGSSize = 500, eps = 0, pvalueCutoff = 1, verbose = FALSE); "OK" },
                   error = function(e) paste("ERROR:", conditionMessage(e)))
cat("sorted, 5 DUPLICATE names          :", r_dup, "\n")

# ---- (F) ID-mismatch cascading error, as the Common Errors table now documents ----
cat("\n--- (F) SYMBOL names passed with keyType='ENTREZID' ---\n")
tryCatch({
  gseGO(geneList = gl_new, OrgDb = org.Hs.eg.db, keyType = "ENTREZID", ont = "BP",
        minGSSize = 10, maxGSSize = 500, eps = 0, pvalueCutoff = 1, verbose = TRUE)
}, error = function(e) cat("-> ERROR:", conditionMessage(e), "\n"))

cat("\nDONE\n")
