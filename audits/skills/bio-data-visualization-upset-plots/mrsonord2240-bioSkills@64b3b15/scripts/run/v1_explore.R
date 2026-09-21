suppressMessages({library(ComplexUpset); library(ggplot2); library(patchwork)})
sets <- list(SetA = c('Gene1','Gene2','Gene3','Gene4'),
             SetB = c('Gene2','Gene3','Gene5','Gene6'),
             SetC = c('Gene1','Gene3','Gene6','Gene7'),
             SetD = c('Gene3','Gene4','Gene7','Gene8'))
all_elements <- unique(unlist(sets))
df <- data.frame(element = all_elements)
for (s in names(sets)) df[[s]] <- df$element %in% sets[[s]]
p <- suppressWarnings(upset(df, intersect=names(sets), n_intersections=20, sort_intersections='descending', sort_intersections_by='cardinality',
  base_annotations=list('Intersection size'=intersection_size(counts=TRUE, text=list(size=3))),
  themes=upset_modify_themes(list('Intersection size'=theme(panel.grid=element_blank())))))
subs <- c(p$patches$plots, list(p))
for (i in seq_along(subs)) {
  s <- subs[[i]]
  if (inherits(s, "spacer")) next
  cat("== subplot", i, "layers:", paste(sapply(s$layers, function(l) class(l$geom)[1]), collapse=","), "\n")
  b <- suppressWarnings(ggplot_build(s))
  for (k in seq_along(b$data)) { cat(" layer",k,"\n"); print(head(b$data[[k]][, intersect(c("x","y","label","fill","colour","PANEL","xmin","xmax","ymin","ymax","intersection","group"), names(b$data[[k]]))], 30)) }
}
cat("\n\n--- scales ---\n")
for (i in seq_along(subs)) {
  s <- subs[[i]]; if (inherits(s,"spacer")) next
  b <- suppressWarnings(ggplot_build(s))
  ps <- b$layout$panel_scales_x[[1]]; py <- b$layout$panel_scales_y[[1]]
  cat("subplot", i, "x labels:", paste(ps$get_labels(), collapse="|"), " x breaks:", paste(ps$get_breaks(), collapse=","), " rev:", "\n")
  cat("   y labels:", paste(py$get_labels(), collapse="|"), "\n")
  cat("   x range:", paste(ps$dimension(), collapse=" "), " | y range:", paste(py$dimension(), collapse=" "), "\n")
}
