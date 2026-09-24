# Real-data stress regression: validate the 10-set nonempty-intersection claim and a readable top 20.
suppressPackageStartupMessages({ library(ComplexUpset); library(ggplot2) })
x <- read.delim("F:/OpenScience/audits/bio-data-visualization-upset-plots/data/hallmark10_sets.tsv", check.names = FALSE)
sets <- lapply(split(as.character(x$gene), as.character(x$set)), unique)
stopifnot(length(sets) == 10L, all(lengths(sets) > 0L))
elements <- sort(unique(unlist(sets, use.names = FALSE))); df <- data.frame(element = elements)
for (s in names(sets)) df[[s]] <- df$element %in% sets[[s]]
labels <- apply(df[names(sets)], 1, function(x) paste(names(sets)[x], collapse = "|"))
truth <- sort(table(labels), decreasing = TRUE)
p <- ComplexUpset::upset(df, intersect = names(sets), n_intersections = 20,
  sort_intersections = "descending", sort_intersections_by = "cardinality",
  base_annotations = list("Intersection size" = intersection_size(counts = TRUE)))
out <- "out/hallmark/hallmark_top20.pdf"
ggsave(out, p, width = 14, height = 7, device = cairo_pdf)
stopifnot(length(truth) < 2^10 - 1L, length(truth) > 20L, file.info(out)$size > 2000L)
cat("PASS Hallmark stress: sets=10 union=", length(elements), " nonempty_exclusive=", length(truth),
    " top20 rendered; no false all-1023-combinations claim\n", sep = "")
