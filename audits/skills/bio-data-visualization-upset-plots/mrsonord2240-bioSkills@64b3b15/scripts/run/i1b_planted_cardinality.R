# Input 1 (cont.): the same SKILL block-1 call pattern on SYNTHETIC planted 8-set data (D subset of A, H empty, 8 sets)
source("F:/OpenScience/audits/bio-data-visualization-upset-plots/run/helpers.R")
library(ComplexUpset); library(ggplot2)
D <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/data/"
sets <- read_lists(paste0(D, "planted_sets.tsv"))
# 'H' is empty -> read_lists loses it (no rows); re-add explicitly as a user with an empty result set would have
sets <- c(sets, list(H = character(0))); sets <- sets[c("A","B","C","D","E","F","G","H")]
print(sapply(sets, length))
all_elements <- unique(unlist(sets))
df <- data.frame(element = all_elements)
for (s in names(sets)) df[[s]] <- df$element %in% sets[[s]]
print(colSums(df[, names(sets)]))

# truth: two independent computations must agree
tr <- truth_from_lists(sets); py <- read.delim(paste0(D, "planted_truth.tsv"))
chk <- merge(tr, py, by = "combo", suffixes = c(".R", ".py"))
cat("truth R(setops) vs truth Python(setops) agree:", all(chk$exclusive.R == chk$exclusive.py & chk$inclusive.R == chk$inclusive.py), nrow(chk), "combos\n")
tr_ex <- tr[tr$exclusive > 0, ]; tr_ex <- tr_ex[order(-tr_ex$exclusive), ]

run <- function(label, ...) {
  p <- tryCatch(suppressWarnings(upset(df, intersect = names(sets), ...)), error = function(e) { cat(label, "ERROR:", conditionMessage(e), "\n"); NULL })
  p
}
# (a) SKILL block-1 arguments, all 8 sets incl. empty H
p <- run("a", n_intersections = 20, sort_intersections = 'descending', sort_intersections_by = 'cardinality',
   base_annotations = list('Intersection size' = intersection_size(counts = TRUE, text = list(size = 3))),
   themes = upset_modify_themes(list('Intersection size' = theme(panel.grid = element_blank()))))
if (!is.null(p)) {
  ggsave("F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/i1b_planted_card.png", p, width = 11, height = 6, dpi = 100)
  ex <- extract_cu(p); ex$bars$combo_n <- norm_combo(ex$bars$combo, names(sets))
  print(ex$bars[, c("x","combo_n","height","label")])
  m <- merge(ex$bars, tr_ex, by.x = "combo_n", by.y = "combo", all = TRUE)
  cat("B1 all 14 nonzero exclusive intersections drawn:", nrow(ex$bars), " expected", nrow(tr_ex), "\n")
  cat("B2 every bar height == exclusive truth:", !anyNA(m$height) && !anyNA(m$exclusive) && all(m$height == m$exclusive), "\n")
  cat("B3 heights non-increasing left->right:", all(diff(ex$bars$height) <= 0), "\n")
  cat("B4 height sequence:", paste(ex$bars$height, collapse = " "), " truth sorted:", paste(sort(tr_ex$exclusive, decreasing = TRUE), collapse = " "), "\n")
  ss <- sapply(sets, length); cat("B5 set-size bars == list lengths:", all(ex$setsize$size == ss[ex$setsize$set]), "\n"); print(ex$setsize)
  cat("B6 empty set H present in matrix rows:", "H" %in% ex$matrix$sets, "; matrix rows:", paste(ex$matrix$sets, collapse = ","), "\n")
  cat("B7 subset case: D is only ever drawn with A (no bar with D and without A):", !any(grepl("D", ex$bars$combo_n) & !grepl("A", ex$bars$combo_n)), "\n")
}
