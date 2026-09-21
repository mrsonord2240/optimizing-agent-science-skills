# Which part of SKILL block 3 breaks at render on ggplot2 4.0.3? Test each query alone on the Skill's own 4-set data.
suppressMessages({library(ComplexUpset); library(ggplot2)})
sets <- list(SetA = c('Gene1','Gene2','Gene3','Gene4'), SetB = c('Gene2','Gene3','Gene5','Gene6'),
             SetC = c('Gene1','Gene3','Gene6','Gene7'), SetD = c('Gene3','Gene4','Gene7','Gene8'))
el <- unique(unlist(sets)); df <- data.frame(element = el); for (s in names(sets)) df[[s]] <- df$element %in% sets[[s]]
OUT <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/"
try_render <- function(label, qs, f) {
  r <- tryCatch({ p <- suppressWarnings(upset(df, intersect = names(sets), queries = qs)); suppressWarnings(ggsave(paste0(OUT, f), p, width = 8, height = 5, dpi = 100)); "renders" },
                error = function(e) paste("ERROR:", conditionMessage(e)))
  cat(sprintf("%-55s -> %s\n", label, substr(gsub("\n", " ", r), 1, 150)))
}
qAB  <- upset_query(intersect = c('SetA','SetB'), color = '#D55E00', fill = '#D55E00', only_components = c('intersections_matrix','Intersection size'))
qACD <- upset_query(intersect = c('SetA','SetC','SetD'), color = '#0072B2', fill = '#0072B2', only_components = c('intersections_matrix','Intersection size'))
qAB_all <- upset_query(intersect = c('SetA','SetB'), color = '#D55E00', fill = '#D55E00')
try_render("query A&B only (only_components as in Skill)", list(qAB), "i2a_qAB.png")
try_render("query A&C&D only (empty exclusive intersection)", list(qACD), "i2a_qACD.png")
try_render("both queries (Skill block 3 verbatim)", list(qAB, qACD), "i2a_both.png")
try_render("query A&B, no only_components", list(qAB_all), "i2a_qAB_all.png")
