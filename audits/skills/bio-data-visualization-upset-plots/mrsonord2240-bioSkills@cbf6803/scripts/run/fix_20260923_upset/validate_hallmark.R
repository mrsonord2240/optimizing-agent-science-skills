# Regression on the audited real Hallmark membership table, using current documented ComplexUpset settings.
suppressPackageStartupMessages({ library(ComplexUpset); library(ggplot2) })
source("F:/OpenScience/audits/bio-data-visualization-upset-plots/run/helpers.R")
x <- read.delim("F:/OpenScience/audits/bio-data-visualization-upset-plots/data/hallmark10_sets.tsv", check.names = FALSE)
sets <- split(as.character(x$gene), as.character(x$set)); sets <- lapply(sets, unique)
stopifnot(length(sets) == 10L, all(lengths(sets) > 0L))
elements <- sort(unique(unlist(sets))); df <- data.frame(element = elements)
for (s in names(sets)) df[[s]] <- df$element %in% sets[[s]]
truth <- truth_from_lists(sets); truth <- truth[truth$exclusive > 0, ]; truth <- truth[order(-truth$exclusive), ]
p <- ComplexUpset::upset(df, intersect = names(sets), n_intersections = 20,
  sort_intersections = "descending", sort_intersections_by = "cardinality",
  base_annotations = list("Intersection size" = intersection_size(counts = TRUE)))
ggsave("hallmark_top20.pdf", p, width = 14, height = 7, device = cairo_pdf)
ex <- extract_cu(p); ex$bars$combo_n <- norm_combo(ex$bars$combo, names(sets))
stopifnot(nrow(ex$bars) == 20L,
          identical(as.numeric(ex$bars$height), as.numeric(head(truth$exclusive, 20))),
          all(ex$setsize$size == lengths(sets)[ex$setsize$set]),
          file.info("hallmark_top20.pdf")$size > 2000)
cat("Hallmark regression PASS: 10 sets; union=", length(elements), "; non-empty combinations=", nrow(truth),
    "; current top-20 bars equal independent truth\n", sep = "")
