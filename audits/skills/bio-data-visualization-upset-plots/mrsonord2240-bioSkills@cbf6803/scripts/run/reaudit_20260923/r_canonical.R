# Exact-commit R canonical and guard regression.
suppressPackageStartupMessages({ library(ComplexUpset); library(UpSetR); library(ggplot2) })

prepare_sets <- function(sets) {
  stopifnot(is.list(sets), !is.null(names(sets)), all(nzchar(names(sets))))
  cleaned <- lapply(names(sets), function(nm) {
    x <- trimws(as.character(sets[[nm]])); bad <- is.na(x) | !nzchar(x)
    if (any(bad)) warning(sprintf("%s: removed %d NA/blank identifier(s)", nm, sum(bad)))
    x <- x[!bad]; before <- length(x); x <- unique(x)
    if (length(x) != before) warning(sprintf("%s: removed %d duplicate identifier(s)", nm, before - length(x)))
    x
  })
  names(cleaned) <- names(sets)
  empty <- names(cleaned)[lengths(cleaned) == 0L]
  if (length(empty)) stop("empty set(s) after preflight: ", paste(empty, collapse = ", "), ". Fix input or omit deliberately.")
  cleaned
}

raw <- list(A = c(" x ", "x", NA, "", "ab"), B = c("ab", "bc"), C = c("bc", "c"))
cleaned <- suppressWarnings(prepare_sets(raw))
stopifnot(identical(cleaned$A, c("x", "ab")), identical(names(cleaned), c("A", "B", "C")))
stopifnot(inherits(try(prepare_sets(list(A = character(), B = "b")), silent = TRUE), "try-error"))

sets <- list(
  SetA = c(paste0("g", 1:6), paste0("ab", 1:5), paste0("ac", 1:3), paste0("abc", 1:4)),
  SetB = c(paste0("b", 1:4), paste0("ab", 1:5), paste0("bc", 1:2), paste0("abc", 1:4)),
  SetC = c(paste0("c", 1:2), paste0("ac", 1:3), paste0("bc", 1:2), paste0("abc", 1:4))
)
sets <- prepare_sets(sets); elements <- sort(unique(unlist(sets, use.names = FALSE)))
df <- data.frame(element = elements)
for (s in names(sets)) df[[s]] <- df$element %in% sets[[s]]
truth <- c(6L, 5L, 4L, 4L, 3L, 2L, 2L)
observed <- sort(as.integer(table(apply(df[names(sets)], 1, paste0, collapse = ""))), decreasing = TRUE)
stopifnot(identical(observed, truth), sum(observed) == length(elements))

p_cardinality <- ComplexUpset::upset(df, intersect = names(sets), n_intersections = 20,
  sort_intersections = "descending", sort_intersections_by = "cardinality",
  base_annotations = list("Intersection size" = intersection_size(counts = TRUE, text = list(size = 3))))
ggsave("out/r_canonical/complex_cardinality.pdf", p_cardinality, width = 9, height = 5, device = cairo_pdf)
p_degree <- ComplexUpset::upset(df, intersect = names(sets), min_degree = 2,
  sort_intersections = "ascending", sort_intersections_by = "degree")
ggsave("out/r_canonical/complex_degree.pdf", p_degree, width = 9, height = 5, device = cairo_pdf)
p_query <- ComplexUpset::upset(df, intersect = names(sets), queries = list(
  upset_query(intersect = c("SetA", "SetB"), color = "#D55E00", fill = "#D55E00",
              only_components = c("intersections_matrix", "Intersection size"))))
ggsave("out/r_canonical/complex_single_query.pdf", p_query, width = 9, height = 5, device = cairo_pdf)
set.seed(20260923); df$log2FC <- rnorm(nrow(df), sd = 1.5); df$significant <- df$log2FC > 1
p_attrs <- ComplexUpset::upset(df, intersect = names(sets), annotations = list(
  "log2FC" = ggplot(mapping = aes(x = intersection, y = log2FC)) + geom_boxplot() + theme_classic(),
  "Significant fraction" = ggplot(mapping = aes(x = intersection, fill = significant)) +
    geom_bar(position = "fill") + scale_fill_manual(values = c("TRUE" = "#D55E00", "FALSE" = "grey80")) + theme_classic()))
ggsave("out/r_canonical/complex_attributes.pdf", p_attrs, width = 9, height = 7, device = cairo_pdf)

u <- UpSetR::fromList(sets)
cairo_pdf("out/r_canonical/upsetr_all_sets.pdf", width = 9, height = 5)
UpSetR::upset(u, nsets = length(sets), nintersects = 20, order.by = "freq", decreasing = TRUE)
dev.off()
outputs <- list.files("out/r_canonical", pattern = "pdf$", full.names = TRUE)
stopifnot(length(outputs) == 5L, all(file.info(outputs)$size > 2000L))
cat("PASS R canonical: guards, planted exclusive counts, sorting, query, attributes, all-set UpSetR, Cairo PDFs\n")
