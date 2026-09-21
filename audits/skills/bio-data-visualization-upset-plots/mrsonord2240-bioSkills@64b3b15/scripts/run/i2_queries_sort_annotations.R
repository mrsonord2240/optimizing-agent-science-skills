# Input 2: queries, degree sort, attribute panels, filtering (SKILL.md blocks 3,4 + sort/mode claims). SYNTHETIC planted data for the checks.
source("F:/OpenScience/audits/bio-data-visualization-upset-plots/run/helpers.R")
library(ComplexUpset); library(ggplot2)
OUT <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/"
sq <- function(expr) suppressWarnings(expr)
## ---- (a)+(b) verbatim blocks on the Skill's own 4-set df (no log2FC / significant columns in df)
sets4 <- list(SetA = c('Gene1','Gene2','Gene3','Gene4'), SetB = c('Gene2','Gene3','Gene5','Gene6'),
              SetC = c('Gene1','Gene3','Gene6','Gene7'), SetD = c('Gene3','Gene4','Gene7','Gene8'))
el <- unique(unlist(sets4)); df4 <- data.frame(element = el); for (s in names(sets4)) df4[[s]] <- df4$element %in% sets4[[s]]
sets <- sets4; df <- df4
p3 <- sq(upset(df, intersect = names(sets),
      queries = list(
          upset_query(intersect = c('SetA', 'SetB'), color = '#D55E00', fill = '#D55E00', only_components = c('intersections_matrix', 'Intersection size')),
          upset_query(intersect = c('SetA', 'SetC', 'SetD'), color = '#0072B2', fill = '#0072B2', only_components = c('intersections_matrix', 'Intersection size')))))
r3 <- tryCatch({ suppressWarnings(ggsave(paste0(OUT, "i2a_block3_queries_4set.png"), p3, width = 8, height = 5, dpi = 100)); "renders" }, error = function(e) paste("ERROR:", substr(gsub("\n", " ", conditionMessage(e)), 1, 140)))
cat("[block3 verbatim, both queries] ggsave ->", r3, "\n")
p3 <- sq(upset(df, intersect = names(sets), queries = list(
          upset_query(intersect = c('SetA', 'SetB'), color = '#D55E00', fill = '#D55E00', only_components = c('intersections_matrix', 'Intersection size')))))
ggsave(paste0(OUT, "i2a_block3_query1_only.png"), p3, width = 8, height = 5, dpi = 100)
ex <- extract_cu(p3); ex$bars$combo_n <- norm_combo(ex$bars$combo, names(sets))
cat("[block3 verbatim] bar colours by combo:\n"); print(ex$bars[, c("combo_n","height","fill")])
cat("C1 SetA-SetB bar is #D55E00:", ex$bars$fill[ex$bars$combo_n == "SetA-SetB"] == "#D55E00", "\n")
t4 <- truth_from_lists(sets)
cat("C2 a bar for SetA-SetC-SetD exists (query 2 target):", any(ex$bars$combo_n == "SetA-SetC-SetD"), " -> its exclusive size in truth:", t4$exclusive[t4$combo == "SetA-SetC-SetD"], "\n")
cat("C3 any bar coloured #0072B2 (query 2 visible):", any(ex$bars$fill == "#0072B2"), "\n")

r4 <- tryCatch({ p4 <- upset(df, intersect = names(sets), annotations = list(
          'log2 FC' = ggplot(mapping = aes(x = intersection, y = log2FC)) + geom_boxplot() + theme_classic(),
          'Significant fraction' = ggplot(mapping = aes(x = intersection, fill = significant)) + geom_bar(position = 'fill') +
                                    scale_fill_manual(values = c('TRUE' = '#D55E00', 'FALSE' = 'grey80')) + theme_classic()))
   ggsave(paste0(OUT, "i2b_block4_verbatim.png"), p4, width = 8, height = 7, dpi = 100); "rendered" }, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("[block4 verbatim on df without log2FC/significant] ->", r4, "\n")

## ---- planted data + per-gene attributes
D <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/data/"
sets <- read_lists(paste0(D, "planted_sets.tsv")); sets <- sets[c("A","B","C","D","E","F","G")]
el <- unique(unlist(sets)); set.seed(20260920)
df <- data.frame(element = el, log2FC = round(rnorm(length(el), 0, 1.5), 3), significant = runif(length(el)) < 0.4)
for (s in names(sets)) df[[s]] <- df$element %in% sets[[s]]
tr <- truth_from_lists(sets); tr_ex <- tr[tr$exclusive > 0, ]
df$pattern <- apply(df[, names(sets)], 1, function(r) paste(names(sets)[r], collapse = "-"))

## ---- (c) annotations block 4 with the columns present
p4 <- sq(upset(df, intersect = names(sets), n_intersections = 20, annotations = list(
   'log2 FC' = ggplot(mapping = aes(x = intersection, y = log2FC)) + geom_boxplot() + theme_classic(),
   'Significant fraction' = ggplot(mapping = aes(x = intersection, fill = significant)) + geom_bar(position = 'fill') +
        scale_fill_manual(values = c('TRUE' = '#D55E00', 'FALSE' = 'grey80')) + theme_classic())))
ggsave(paste0(OUT, "i2c_block4_annotations.png"), p4, width = 11, height = 9, dpi = 100)
ex <- extract_cu(p4); ex$bars$combo_n <- norm_combo(ex$bars$combo, names(sets))
cat("\n[block4 with columns] annotation panels found:", length(ex$annotations), " y labels:", paste(sapply(ex$annotations, function(a) a$ylab), collapse=" | "), "\n")
box <- Filter(function(a) "GeomBoxplot" %in% a$geoms, ex$annotations)[[1]]; bd <- box$b$data[[which(box$geoms == "GeomBoxplot")[1]]]
bd$combo <- ex$bars$combo_n[match(bd$x, ex$bars$x)]
bd$true_median <- sapply(bd$combo, function(cb) median(df$log2FC[df$pattern == cb]))
cat("C4 drawn boxplot medians == independent per-intersection medians:", all(abs(bd$middle - bd$true_median) < 1e-9), "(", nrow(bd), "boxes)\n")
fr <- Filter(function(a) "GeomBar" %in% a$geoms, ex$annotations)[[1]]; fd <- fr$b$data[[which(fr$geoms == "GeomBar")[1]]]
fd$combo <- ex$bars$combo_n[match(fd$x, ex$bars$x)]
fd$fillTRUE <- fd$fill == "#D55E00"
tp <- sapply(unique(fd$combo), function(cb) { r <- fd[fd$combo == cb & fd$fillTRUE, ]; if (nrow(r)) r$ymax - r$ymin else 0 })
tt <- sapply(names(tp), function(cb) mean(df$significant[df$pattern == cb]))
cat("C5 stacked-fraction 'significant' equals independent proportion:", all(abs(tp[names(tt)] - tt) < 1e-9), "\n")
print(data.frame(combo = names(tt), drawn = round(tp[names(tt)], 3), truth = round(tt, 3)))

## ---- (d) degree sort
mk <- function(...) sq(upset(df, intersect = names(sets), ...))
degree_of <- function(cb) lengths(strsplit(cb, "-", fixed = TRUE))
for (cfg in list(list(by = "degree", ord = "descending"), list(by = "degree", ord = "ascending"), list(by = "cardinality", ord = "ascending"))) {
  pp <- mk(n_intersections = 20, sort_intersections = cfg$ord, sort_intersections_by = cfg$by)
  e <- extract_cu(pp); e$bars$combo_n <- norm_combo(e$bars$combo, names(sets)); dg <- degree_of(e$bars$combo_n)
  cat(sprintf("\n[sort_intersections_by=%s, sort_intersections=%s]\n degrees L->R: %s\n heights L->R: %s\n", cfg$by, cfg$ord, paste(dg, collapse=" "), paste(e$bars$height, collapse=" ")))
  if (cfg$by == "degree") cat(" monotone in degree:", if (cfg$ord == "ascending") all(diff(dg) >= 0) else all(diff(dg) <= 0), "\n") else cat(" heights monotone ascending:", all(diff(e$bars$height) >= 0), "\n")
  ggsave(paste0(OUT, sprintf("i2d_sort_%s_%s.png", cfg$by, cfg$ord)), pp, width = 11, height = 5, dpi = 100)
}

## ---- (e) filters: intersections=list(), min_degree, min_size, n_intersections, mode
sig <- function(pp) { e <- extract_cu(pp); e$bars$combo_n <- norm_combo(e$bars$combo, names(sets)); e$bars[, c("combo_n","height")] }
cat("\n[min_degree=2]\n"); pm <- mk(min_degree = 2); s <- sig(pm); print(t(s)); cat(" all degree>=2:", all(degree_of(s$combo_n) >= 2), " count vs truth (exclusive>0 & degree>=2):", nrow(s), sum(tr_ex$degree >= 2), "\n")
cat("\n[min_size=4]\n"); pm <- mk(min_size = 4); s <- sig(pm); print(t(s)); cat(" all >=4:", all(s$height >= 4), " count vs truth:", nrow(s), sum(tr_ex$exclusive >= 4), "\n")
cat("\n[n_intersections=5]\n"); pm <- mk(n_intersections = 5); s <- sig(pm); print(t(s)); cat(" top5 heights equal truth top5:", identical(as.numeric(s$height), as.numeric(sort(tr_ex$exclusive, decreasing = TRUE)[1:5])), "\n")
cat("\n[intersections = list(c(A,B), c(A,B,D), c(E,F))]\n")
pm <- tryCatch(mk(intersections = list(c('A','B'), c('A','B','D'), c('E','F'))), error = function(e) { cat(" ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(pm)) { s <- sig(pm); print(t(s)); cat(" heights == truth:", all(s$height == tr_ex$exclusive[match(s$combo_n, tr_ex$combo)]), "\n") }
cat("\n[mode='intersect' -- the Skill suggests this to change how 1-set bars are counted]\n")
pm <- mk(mode = "intersect", n_intersections = 30); e <- extract_cu(pm); e$bars$combo_n <- norm_combo(e$bars$combo, names(sets))
mi <- merge(e$bars, tr, by.x = "combo_n", by.y = "combo"); print(t(mi[order(-mi$height), c("combo_n","height","inclusive","exclusive")][1:10, ]))
cat(" mode=intersect bar heights == INCLUSIVE truth:", all(mi$height == mi$inclusive), "; 1-set bars remain (bar for 'A' = ", mi$height[mi$combo_n == "A"], "= full |A|)\n")
ggsave(paste0(OUT, "i2e_mode_intersect.png"), pm, width = 11, height = 5, dpi = 100)
## ---- (f) query on planted data: exact-intersection highlighting
pq <- sq(upset(df, intersect = names(sets), queries = list(
   upset_query(intersect = c('A','B'), color = '#D55E00', fill = '#D55E00', only_components = c('intersections_matrix','Intersection size')),
   upset_query(intersect = c('A','B','D'), color = '#0072B2', fill = '#0072B2', only_components = c('intersections_matrix','Intersection size')))))
ggsave(paste0(OUT, "i2f_queries_planted.png"), pq, width = 11, height = 5, dpi = 100)
e <- extract_cu(pq); e$bars$combo_n <- norm_combo(e$bars$combo, names(sets)); print(e$bars[e$bars$fill != "#595959FF", c("combo_n","height","fill")])
cat("C6 exactly the A-B bar is orange and only the A-B-D bar is blue (exact, not superset match):",
    identical(e$bars$combo_n[e$bars$fill == "#D55E00"], "A-B") && identical(e$bars$combo_n[e$bars$fill == "#0072B2"], "A-B-D"), "\n")
md <- e$matrix$dots; cat("C7 matrix dot colours used:", paste(unique(md$colour), collapse=","), "\n")
