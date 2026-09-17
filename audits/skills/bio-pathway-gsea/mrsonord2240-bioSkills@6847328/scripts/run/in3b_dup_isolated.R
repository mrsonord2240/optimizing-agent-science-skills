# Follow-up to Input 3, part (E): isolate the "duplicated names, otherwise still sorted decreasing"
# case cleanly (the first attempt appended duplicates to the tail, which broke sort order too, so
# the sort-check fired first and masked the duplicate-name check).

suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

edg <- read.csv("F:/OpenScience/audits/bio-pathway-gsea/data/SYNTHETIC_edger_qlf.csv")
gl <- sign(edg$logFC) * -log10(pmax(edg$PValue, 1e-30))
names(gl) <- edg$gene
gl <- gl[!is.na(gl)]
gl <- gl[!duplicated(names(gl))]
gl <- sort(gl, decreasing = TRUE)

map <- bitr(names(gl), fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)
map <- map[!duplicated(map$SYMBOL), ]
gl_ez <- gl[names(gl) %in% map$SYMBOL]
names(gl_ez) <- map$ENTREZID[match(names(gl_ez), map$SYMBOL)]
gl_ez <- gl_ez[!duplicated(names(gl_ez))]
gl_ez <- sort(gl_ez, decreasing = TRUE)

# duplicate 5 names at DIFFERENT values (same gene appearing twice in the raw messy table with two
# different p/logFC, as real duplicate rows would), then re-sort the WHOLE augmented vector so the
# result is strictly decreasing by value -- only the "duplicate names" condition is isolated.
dup_names <- names(gl_ez)[c(1000, 3000, 6000, 9000, 12000)]
extra_vals <- setNames(gl_ez[dup_names] * 0.37 + 0.01, dup_names)  # distinct values, no ties
dup_ez <- c(gl_ez, extra_vals)
dup_ez <- sort(dup_ez, decreasing = TRUE)
cat("dup vector strictly decreasing:", !is.unsorted(-dup_ez), "| duplicate names:", sum(duplicated(names(dup_ez))), "\n")

r <- tryCatch({
  gseGO(geneList = dup_ez, OrgDb = org.Hs.eg.db, keyType = "ENTREZID", ont = "BP",
        minGSSize = 200, maxGSSize = 500, eps = 0, pvalueCutoff = 1, verbose = FALSE)
  "OK (no error)"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("sorted, 5 DUPLICATE names (isolated):", r, "\n")
cat("DONE\n")
