# Input 4 (stress): UpSetR route + reconciliation with ComplexUpset, on the shipped example's 6 simulated sets and SYNTHETIC planted 8 sets.
suppressMessages({library(UpSetR); library(ggplot2); library(grid)})
source("F:/OpenScience/audits/bio-data-visualization-upset-plots/run/helpers.R")
OUT <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/"
D <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/data/"
sq <- function(e) suppressWarnings(suppressMessages(e))
png_up <- function(x, f, w = 1100, h = 600) { png(paste0(OUT, f), w, h, res = 100); print(x); dev.off() }
combos_of <- function(e, rowsn) sapply(strsplit(e$members, "-", fixed = TRUE), function(z) paste(rowsn[rowsn %in% z], collapse = "-"))
check_upsetr <- function(label, x, sets, top = Inf) {
  e <- extract_upsetr(x); nm <- names(sets); cb <- combos_of(e, nm)
  tr <- truth_from_lists(sets); tr <- tr[tr$exclusive > 0, ]; tr <- tr[order(-tr$exclusive), ]
  m <- match(cb, tr$combo)
  cat(sprintf("[%s] drawn columns %d; heights L->R: %s\n", label, length(e$labels), paste(e$labels, collapse = " ")))
  cat(sprintf("   U1 each drawn bar == exclusive truth: %s\n", all(!is.na(m)) && all(e$labels == tr$exclusive[m])))
  cat(sprintf("   U2 non-increasing L->R: %s\n", all(diff(e$labels) <= 0)))
  cat(sprintf("   U3 drawn columns == top-%s truth (as multiset of heights): %s\n", ifelse(is.finite(top), top, "all"), identical(sort(e$labels, decreasing = TRUE), as.numeric(head(sort(tr$exclusive, decreasing = TRUE), top)))))
  invisible(list(e = e, cb = cb, tr = tr))
}

## ---- (a) SKILL UpSetR block VERBATIM on the Skill's 4 sets
sets4 <- list(SetA = c('Gene1','Gene2','Gene3','Gene4'), SetB = c('Gene2','Gene3','Gene5','Gene6'), SetC = c('Gene1','Gene3','Gene6','Gene7'), SetD = c('Gene3','Gene4','Gene7','Gene8'))
sets <- sets4
library(UpSetR)   # NB: with ComplexUpset attached first this is a no-op and upset() is ComplexUpset's; calls below are namespaced
xa <- sq(UpSetR::upset(fromList(sets),
      nsets = 4, nintersects = 20,
      order.by = 'freq',
      decreasing = TRUE,
      mb.ratio = c(0.6, 0.4),
      point.size = 3,
      line.size = 1,
      text.scale = c(1.5, 1.3, 1.3, 1, 1.5, 1.3)))
png_up(xa, "i4a_upsetr_block.png", 900, 550)
r <- check_upsetr("SKILL UpSetR block, 4 sets", xa, sets4)

## ---- (b) the same block on the planted 8 sets (nsets = 4 copied from the Skill) and with nsets = 8
sets8 <- read_lists(paste0(D, "planted_sets.tsv")); sets7 <- sets8[c("A","B","C","D","E","F","G")]
x4 <- sq(UpSetR::upset(fromList(sets7), nsets = 4, nintersects = 20, order.by = 'freq', decreasing = TRUE))
e4 <- extract_upsetr(x4); cat("\n[planted 7 sets, Skill's nsets = 4]: sets actually drawn (matrix rows):", paste(e4$rows, collapse = ","), "\n   heights:", paste(e4$labels, collapse = " "), "\n")
png_up(x4, "i4b_upsetr_nsets4_on7.png")
tr7 <- truth_from_lists(sets7); cat("   truth: 7 sets have", sum(tr7$exclusive > 0), "nonzero exclusive intersections; sum of drawn bars =", sum(e4$labels), "vs union", length(unique(unlist(sets7))), "\n")
x8 <- sq(UpSetR::upset(fromList(sets7), nsets = 7, nintersects = 40, order.by = 'freq', decreasing = TRUE))
png_up(x8, "i4b_upsetr_nsets7.png")
r8 <- check_upsetr("planted 7 sets, nsets=7", x8, sets7)
print(rbind(drawn = paste(r8$cb, r8$e$labels, sep = ":")))
## empty set in fromList
xe <- tryCatch(sq(UpSetR::upset(fromList(c(sets7, list(H = character(0)))), nsets = 8, nintersects = 40, order.by = 'freq')), error = function(e) paste("ERROR:", conditionMessage(e)))
if (is.character(xe)) cat("\n[fromList with an empty set H] ->", xe, "\n") else { ee <- extract_upsetr(xe); cat("\n[fromList with an empty set H] rows drawn:", paste(ee$rows, collapse = ","), "\n") }

## ---- (c) shipped example: source it verbatim (writes 3 PDFs into out/ex_R), then check its own gene_sets
setwd(paste0(OUT, "ex_R")); e0 <- new.env(); sq(sys.source("upset_gene_sets.R", envir = e0, keep.source = FALSE)); gs <- e0$gene_sets
cat("\n[shipped example] set sizes:", paste(names(gs), sapply(gs, length), sep = "=", collapse = "; "), "\n")
xs <- sq(UpSetR::upset(fromList(gs), nsets = 6, order.by = 'freq', mainbar.y.label = 'Genes in Intersection', sets.x.label = 'Total Genes per Set'))
png_up(xs, "i4c_example_basic.png", 1300, 700)
rs <- check_upsetr("shipped example basic (nintersects default 40)", xs, gs, top = 40)
xc <- sq(UpSetR::upset(fromList(gs), nsets = 6, nintersects = 30, order.by = 'freq', decreasing = TRUE))
rc <- check_upsetr("shipped example customized (nintersects = 30)", xc, gs, top = 30)
cat("   number of possible non-empty exclusive intersections in the data:", nrow(rs$tr), "\n")
## queries as in the example
xq <- sq(UpSetR::upset(fromList(gs), nsets = 6, order.by = 'freq', queries = list(
   list(query = intersects, params = list('Combined_Treatment'), color = '#E64B35', active = TRUE, query.name = 'Combined only'),
   list(query = intersects, params = list('Timepoint_6h', 'Timepoint_24h'), color = '#4DBBD5', active = TRUE, query.name = 'Both timepoints')), query.legend = 'bottom'))
png_up(xq, "i4c_example_queries.png", 1300, 750)
eq <- extract_upsetr(xq); cbq <- combos_of(eq, names(gs)); col_by_x <- tapply(eq$pcol, rep(seq_along(eq$members), each = length(eq$rows)), function(z) paste(unique(toupper(z)), collapse = "/"))
cat("[queries] columns whose dots are NOT the default grey/black:\n"); hl <- which(!grepl("^#3B3B3B/#D4D4D480$|^#D4D4D480/#3B3B3B$|^#3B3B3B$|^#D4D4D480$", col_by_x)); print(data.frame(col = hl, combo = cbq[hl], height = eq$labels[hl], colours = col_by_x[hl]))

## ---- (d) UpSetR vs ComplexUpset on the SAME sets: the Skill's reconciliation table says they may differ
dfc <- data.frame(element = unique(unlist(gs))); for (s in names(gs)) dfc[[s]] <- dfc$element %in% gs[[s]]
pc <- sq(ComplexUpset::upset(dfc, intersect = names(gs), n_intersections = 40)); ec <- extract_cu(pc); ec$bars$combo_n <- norm_combo(ec$bars$combo, names(gs))
ur <- data.frame(combo = combos_of(rs$e, names(gs)), u = rs$e$labels); cu <- data.frame(combo = ec$bars$combo_n, c = ec$bars$height)
mm <- merge(ur, cu, by = "combo", all = TRUE)
cat("\n[UpSetR vs ComplexUpset, shipped 6 sets, 40 intersections] columns UpSetR:", nrow(ur), "ComplexUpset:", nrow(cu), "; per-combo heights agree on the common combos:", all(mm$u[!is.na(mm$u) & !is.na(mm$c)] == mm$c[!is.na(mm$u) & !is.na(mm$c)]), "; combos in only one:", sum(is.na(mm$u) | is.na(mm$c)), "\n")
ggsave(paste0(OUT, "i4d_complexupset_shipped6.png"), pc, width = 12, height = 6, dpi = 100)

## ---- (e) duplicates: SKILL says fromList counts inflate unless lapply(sets, unique)
dsets <- sets7; dsets$A <- c(dsets$A, dsets$A[1:6]); dsets$B <- c(dsets$B, dsets$B[1:3])
xd <- sq(UpSetR::upset(fromList(dsets), nsets = 7, nintersects = 40, order.by = 'freq')); ed <- extract_upsetr(xd); cbd <- combos_of(ed, names(dsets))
tr <- truth_from_lists(sets7); tr <- tr[tr$exclusive > 0, ]
cat("\n[duplicates inside A and B, UpSetR fromList] drawn bars equal the de-duplicated truth (no inflation):", all(ed$labels == tr$exclusive[match(cbd, tr$combo)]), "\n")
dfd <- data.frame(element = unique(unlist(dsets))); for (s in names(dsets)) dfd[[s]] <- dfd$element %in% dsets[[s]]
pd <- sq(ComplexUpset::upset(dfd, intersect = names(dsets), n_intersections = 40)); edc <- extract_cu(pd); cat("[same, ComplexUpset via the Skill's %in% construction] bars equal truth:", all(edc$bars$height[order(edc$bars$x)] == sort(tr$exclusive, decreasing = TRUE)), "\n")

## ---- (f) hyphenated / spaced set names (typical DE comparison names)
hs <- list(`6h-vs-ctrl` = c('g1','g2','g3','g4','g9'), `24h-vs-ctrl` = c('g2','g3','g5','g6'), `Drug A` = c('g3','g4','g6','g7'))
hs_df <- data.frame(element = unique(unlist(hs))); for (s in names(hs)) hs_df[[s]] <- hs_df$element %in% hs[[s]]
ph <- tryCatch(sq(ComplexUpset::upset(hs_df, intersect = names(hs))), error = function(e) paste("ERROR:", conditionMessage(e)))
if (is.character(ph)) cat("\n[hyphen/space names, ComplexUpset]", ph, "\n") else {
  ggsave(paste0(OUT, "i4f_hyphen_names.png"), ph, width = 8, height = 4, dpi = 100)
  eh <- extract_cu(ph); trh <- truth_from_lists(hs); trh <- trh[trh$exclusive > 0, ]
  cat("\n[hyphen/space names, ComplexUpset] rows:", paste(eh$matrix$sets, collapse = " | "), "; bar heights (sorted):", paste(sort(eh$bars$height, decreasing = TRUE), collapse = " "), " truth:", paste(sort(trh$exclusive, decreasing = TRUE), collapse = " "), "\n") }
xh <- sq(UpSetR::upset(fromList(hs), nsets = 3, order.by = "freq")); eh2 <- extract_upsetr(xh); cat("[hyphen/space names, UpSetR] rows:", paste(eh2$rows, collapse = " | "), " heights:", paste(eh2$labels, collapse = " "), "\n")
