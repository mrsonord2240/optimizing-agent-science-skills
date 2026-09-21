# Input 5: REAL MSigDB Hallmark gene sets (msigdbr 26.1.0), 10 sets -> ComplexUpset / UpSetR at scale, the Skill's "2^N columns" claim, NA/blank IDs.
suppressMessages({library(msigdbr); library(dplyr); library(ggplot2)})
source("F:/OpenScience/audits/bio-data-visualization-upset-plots/run/helpers.R")
OUT <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/"; D <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/data/"
sq <- function(e) suppressWarnings(suppressMessages(e))
h <- msigdbr(species = "Homo sapiens", collection = "H")
want <- c("HALLMARK_INFLAMMATORY_RESPONSE","HALLMARK_TNFA_SIGNALING_VIA_NFKB","HALLMARK_IL6_JAK_STAT3_SIGNALING","HALLMARK_INTERFERON_GAMMA_RESPONSE",
          "HALLMARK_INTERFERON_ALPHA_RESPONSE","HALLMARK_COMPLEMENT","HALLMARK_ALLOGRAFT_REJECTION","HALLMARK_IL2_STAT5_SIGNALING","HALLMARK_APOPTOSIS","HALLMARK_P53_PATHWAY")
hs <- lapply(setNames(want, sub("HALLMARK_", "", want)), function(w) unique(h$gene_symbol[h$gs_name == w]))
cat("hallmark set sizes:", paste(names(hs), lengths(hs), sep = "=", collapse = "; "), "\n")
write.table(data.frame(set = rep(names(hs), lengths(hs)), gene = unlist(hs)), paste0(D, "hallmark10_sets.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
tr <- truth_from_lists(hs); trx <- tr[tr$exclusive > 0, ]; trx <- trx[order(-trx$exclusive), ]
cat("union", length(unique(unlist(hs))), "; possible combos 2^10-1 =", 2^10 - 1, "; non-empty exclusive intersections in real data:", nrow(trx), "\n")
df <- data.frame(element = unique(unlist(hs))); for (s in names(hs)) df[[s]] <- df$element %in% hs[[s]]

library(ComplexUpset)
t1 <- system.time(p20 <- sq(upset(df, intersect = names(hs), n_intersections = 20, sort_intersections = 'descending', sort_intersections_by = 'cardinality',
      base_annotations = list('Intersection size' = intersection_size(counts = TRUE, text = list(size = 3))))))
ggsave(paste0(OUT, "i5_hallmark10_top20.png"), p20, width = 14, height = 7, dpi = 100)
ex <- extract_cu(p20); ex$bars$combo_n <- norm_combo(ex$bars$combo, names(hs))
cat("\n[ComplexUpset 10 real sets, n_intersections=20] build+save s:", round(sum(t1[1:3]), 1), "\n")
cat(" V1 drawn columns:", nrow(ex$bars), "; heights:", paste(ex$bars$height, collapse = " "), "\n")
cat(" V2 each bar == exclusive truth:", all(ex$bars$height == trx$exclusive[match(ex$bars$combo_n, trx$combo)], na.rm = FALSE) && !anyNA(match(ex$bars$combo_n, trx$combo)), "\n")
cat(" V3 heights == top-20 of truth:", identical(as.numeric(ex$bars$height), as.numeric(head(trx$exclusive, 20))), "\n")
ss <- lengths(hs); cat(" V4 set-size bars == list lengths:", all(ex$setsize$size == ss[ex$setsize$set]), "\n")
cat(" V5 drawn intersections cover this share of the union:", round(sum(ex$bars$height) / length(unique(unlist(hs))), 3), " (top-20 of", nrow(trx), ")\n")

t2 <- system.time(pall <- sq(upset(df, intersect = names(hs), n_intersections = Inf, min_size = 1)))
ex2 <- extract_cu(pall); cat("[ComplexUpset n_intersections=Inf] build s:", round(sum(t2[1:3]), 1), "; columns drawn:", nrow(ex2$bars), "(2^10-1 =", 2^10 - 1, "; the Skill's claim of ~1023 columns would need every combination non-empty)\n")
t3 <- system.time(pall2 <- sq(upset(df, intersect = names(hs), n_intersections = Inf, min_size = 0, keep_empty_groups = TRUE)))
ex3 <- tryCatch(extract_cu(pall2), error = function(e) NULL); cat("[ComplexUpset n_intersections=Inf, keep_empty_groups=TRUE] columns:", if (is.null(ex3)) "extract failed" else nrow(ex3$bars), "; s:", round(sum(t3[1:3]), 1), "\n")

# UpSetR on the same data
x <- sq(UpSetR::upset(UpSetR::fromList(hs), nsets = 10, nintersects = 20, order.by = 'freq', decreasing = TRUE))
png(paste0(OUT, "i5_hallmark10_upsetr.png"), 1400, 700, res = 100); print(x); dev.off()
eu <- extract_upsetr(x); cb <- sapply(strsplit(eu$members, "-", fixed = TRUE), function(z) paste(names(hs)[names(hs) %in% z], collapse = "-"))
cat("[UpSetR same 10 sets, nintersects=20] heights:", paste(eu$labels, collapse = " "), "; each == truth:", all(eu$labels == trx$exclusive[match(cb, trx$combo)]), "; multiset == top-20:", identical(sort(eu$labels, decreasing = TRUE), as.numeric(head(trx$exclusive, 20))), "\n")
cat("   ComplexUpset vs UpSetR top-20 heights identical:", identical(as.numeric(ex$bars$height), as.numeric(eu$labels)), "\n")

## NA / blank identifiers (real ID lists often carry them): Skill only advises unique()
na_sets <- list(S1 = c("TP53","MYC",NA,"EGFR",""), S2 = c("TP53",NA,"KRAS",""), S3 = c("MYC","KRAS","EGFR"))
nd <- data.frame(element = unique(unlist(na_sets))); for (s in names(na_sets)) nd[[s]] <- nd$element %in% na_sets[[s]]
pn <- sq(upset(nd, intersect = names(na_sets))); en <- extract_cu(pn); en$bars$combo_n <- norm_combo(en$bars$combo, names(na_sets))
cat("\n[NA and '' in the lists] elements counted:", nrow(nd), "(", sum(is.na(nd$element)), "NA row,", sum(nd$element %in% "", na.rm = TRUE), "blank row ) ; bars:", paste(en$bars$combo_n, en$bars$height, sep = ":", collapse = " "), "\n")
xn <- sq(UpSetR::upset(UpSetR::fromList(na_sets), nsets = 3, order.by = "freq")); en2 <- extract_upsetr(xn); cat("   UpSetR bars:", paste(en2$members, en2$labels, sep = ":", collapse = " "), " (real genes only would give S1&S2 = TP53 -> 1)\n")
