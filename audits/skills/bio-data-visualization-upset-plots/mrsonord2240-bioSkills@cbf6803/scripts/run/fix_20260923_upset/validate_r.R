# Exact current-source ComplexUpset/UpSetR regression vectors for the backlog fix.
suppressPackageStartupMessages({ library(ComplexUpset); library(UpSetR); library(ggplot2) })
prepare_sets <- function(sets) {
  cleaned <- lapply(names(sets), function(nm) {
    x <- trimws(as.character(sets[[nm]])); bad <- is.na(x) | !nzchar(x)
    if (any(bad)) warning(sprintf("%s: removed %d NA/blank identifier(s)", nm, sum(bad)))
    x <- x[!bad]; old_n <- length(x); x <- unique(x)
    if (length(x) != old_n) warning(sprintf("%s: removed %d duplicate identifier(s)", nm, old_n - length(x)))
    x
  }); names(cleaned) <- names(sets)
  empty <- names(cleaned)[lengths(cleaned) == 0L]
  if (length(empty)) stop("empty set(s) after preflight: ", paste(empty, collapse = ", "))
  cleaned
}
raw <- list(A = c(" x ", "x", NA, "", "ab"), B = c("ab", "bc"), C = c("bc", "c"))
sets <- suppressWarnings(prepare_sets(raw))
stopifnot(identical(sets$A, c("x", "ab")), identical(names(sets), c("A", "B", "C")))
empty_stops <- inherits(try(prepare_sets(list(A = character(), B = "b")), silent = TRUE), "try-error")
stopifnot(empty_stops)

sets <- list(
  SetA = c(paste0("g", 1:6), paste0("ab", 1:5), paste0("ac", 1:3), paste0("abc", 1:4)),
  SetB = c(paste0("b", 1:4), paste0("ab", 1:5), paste0("bc", 1:2), paste0("abc", 1:4)),
  SetC = c(paste0("c", 1:2), paste0("ac", 1:3), paste0("bc", 1:2), paste0("abc", 1:4))
)
sets <- prepare_sets(sets); el <- sort(unique(unlist(sets))); df <- data.frame(element = el)
for (s in names(sets)) df[[s]] <- df$element %in% sets[[s]]
truth <- c(6, 5, 4, 4, 3, 2, 2)
calc <- function(d) {
  tab <- table(apply(d[names(sets)], 1, paste0, collapse = "")); sort(as.integer(tab), decreasing = TRUE)
}
stopifnot(isTRUE(all.equal(calc(df), truth)), sum(calc(df)) == length(el))

p <- ComplexUpset::upset(df, intersect = names(sets), n_intersections = 20,
  sort_intersections = "descending", sort_intersections_by = "cardinality",
  base_annotations = list("Intersection size" = intersection_size(counts = TRUE)))
ggsave("complex_cardinality.pdf", p, width = 9, height = 5, device = cairo_pdf)
p_degree <- ComplexUpset::upset(df, intersect = names(sets), min_degree = 2,
  sort_intersections = "ascending", sort_intersections_by = "degree")
ggsave("complex_degree.pdf", p_degree, width = 9, height = 5, device = cairo_pdf)
p_query <- ComplexUpset::upset(df, intersect = names(sets), queries = list(
  upset_query(intersect = c("SetA", "SetB"), color = "#D55E00", fill = "#D55E00",
              only_components = c("intersections_matrix", "Intersection size"))))
ggsave("complex_single_query.pdf", p_query, width = 9, height = 5, device = cairo_pdf)
set.seed(20260923); df$log2FC <- rnorm(nrow(df)); df$significant <- df$log2FC > 1
p_attrs <- ComplexUpset::upset(df, intersect = names(sets), annotations = list(
  "log2FC" = ggplot(mapping = aes(x = intersection, y = log2FC)) + geom_boxplot(),
  "Significant fraction" = ggplot(mapping = aes(x = intersection, fill = significant)) + geom_bar(position = "fill")))
ggsave("complex_attrs.pdf", p_attrs, width = 9, height = 7, device = cairo_pdf)
u <- UpSetR::fromList(sets)
cairo_pdf("upsetr_all_sets.pdf", width = 9, height = 5)
UpSetR::upset(u, nsets = length(sets), nintersects = 20, order.by = "freq")
dev.off()
stopifnot(file.info(c("complex_cardinality.pdf", "complex_degree.pdf", "complex_single_query.pdf", "complex_attrs.pdf", "upsetr_all_sets.pdf"))$size > 2000)
cat("R vectors PASS: hygiene, empty-stop, planted truth, cardinality, degree filter, single query, attributes, Cairo exports\n")
