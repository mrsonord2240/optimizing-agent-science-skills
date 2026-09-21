# Input 1: SKILL.md ComplexUpset block VERBATIM (4 sets), then assert on what was drawn.
source("F:/OpenScience/audits/bio-data-visualization-upset-plots/run/helpers.R")
library(ComplexUpset)
library(ggplot2)

sets <- list(SetA = c('Gene1','Gene2','Gene3','Gene4'),
             SetB = c('Gene2','Gene3','Gene5','Gene6'),
             SetC = c('Gene1','Gene3','Gene6','Gene7'),
             SetD = c('Gene3','Gene4','Gene7','Gene8'))
all_elements <- unique(unlist(sets))
df <- data.frame(element = all_elements)
for (s in names(sets)) df[[s]] <- df$element %in% sets[[s]]

p <- upset(df,
      intersect = names(sets),
      n_intersections = 20,
      sort_intersections = 'descending',
      sort_intersections_by = 'cardinality',
      base_annotations = list(
          'Intersection size' = intersection_size(
              counts = TRUE,
              text = list(size = 3))),
      themes = upset_modify_themes(
          list('Intersection size' = theme(panel.grid = element_blank()))))
ggsave("F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/i1_block1.png", p, width = 8, height = 5, dpi = 100)

# ---- assertions on the drawn figure vs independent set computation ----
tr <- truth_from_lists(sets)
ex <- extract_cu(p)
cat("drawn bars:\n"); print(ex$bars); cat("drawn set sizes:\n"); print(ex$setsize)
ex$bars$combo_n <- norm_combo(ex$bars$combo, names(sets))
tr_ex <- tr[tr$exclusive > 0, ]
m <- merge(ex$bars, tr_ex, by.x = "combo_n", by.y = "combo", all = TRUE)
cat("\nbar height vs independent exclusive count:\n"); print(m[, c("combo_n","height","exclusive","label")])
cat("A1 number of drawn intersections == number of nonzero exclusive combos:", nrow(ex$bars) == nrow(tr_ex), "(", nrow(ex$bars), "vs", nrow(tr_ex), ")\n")
cat("A2 every drawn bar height == independent exclusive size:", all(m$height == m$exclusive, na.rm=TRUE) && !anyNA(m$height) && !anyNA(m$exclusive), "\n")
cat("A3 sum of bar heights == size of union:", sum(ex$bars$height), "vs", length(all_elements), "\n")
ss <- setNames(sapply(sets, length), names(sets))
cat("A4 set-size bars == list lengths:", all(ex$setsize$size == ss[ex$setsize$set]), "\n"); print(ex$setsize)
cat("A5 count labels equal bar heights:", all(as.numeric(ex$bars$label) == ex$bars$height), "\n")
cat("A6 drawn order is non-increasing in height (cardinality descending):", all(diff(ex$bars$height) <= 0), "\n")
# sanity: is the *example* discriminating? all 8 bars equal 1 -> ordering/height checks are weak here
cat("distinct heights in this example:", paste(unique(ex$bars$height), collapse=","), "\n")
