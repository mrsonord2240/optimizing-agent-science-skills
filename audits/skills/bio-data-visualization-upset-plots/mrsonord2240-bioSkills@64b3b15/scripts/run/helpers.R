# Shared helpers: independent set-operation truth + extraction of what ComplexUpset / UpSetR actually drew.
suppressMessages({library(ggplot2)})
truth_from_lists <- function(sets) {
  nm <- names(sets); res <- list()
  for (k in seq_along(nm)) for (cb in combn(nm, k, simplify = FALSE)) {
    inter <- Reduce(intersect, sets[cb]); oth <- setdiff(nm, cb)
    excl <- if (length(oth)) setdiff(inter, unlist(sets[oth])) else inter
    if (length(inter)) res[[length(res)+1]] <- data.frame(combo = paste(cb, collapse = "-"), exclusive = length(excl), inclusive = length(inter), degree = k)
  }
  do.call(rbind, res)
}
read_lists <- function(path) { d <- read.delim(path, stringsAsFactors = FALSE); lapply(split(d$gene, factor(d$set, levels = unique(d$set))), unique) }

# Everything ComplexUpset drew: per-position membership, bar height, label, plus set-size bars.
extract_cu <- function(p) {
  subs <- c(p$patches$plots, list(p)); subs <- subs[!sapply(subs, function(s) inherits(s, "spacer"))]
  out <- list(matrix = NULL, bars = NULL, setsize = NULL, annotations = list())
  info <- lapply(subs, function(s) {
    b <- suppressWarnings(ggplot_build(s)); g <- sapply(s$layers, function(l) class(l$geom)[1])
    ylab <- tryCatch(b$layout$resolve_label(b$layout$panel_scales_y[[1]], b$plot$labels)$primary, error = function(e) NA)
    list(s = s, b = b, geoms = g, ylab = ylab)
  })
  for (it in info) {
    g <- it$geoms; b <- it$b
    if ("GeomPoint" %in% g) {   # matrix
      xs <- b$layout$panel_scales_x[[1]]$get_labels(); ys <- b$layout$panel_scales_y[[1]]$get_labels()
      pl <- which(g == "GeomPoint")[1]; d <- b$data[[pl]]
      d$member <- !(d$colour %in% c("grey70"))
      out$matrix <- list(pos_labels = xs, sets = ys, dots = d[, c("x","y","colour","member")])
    } else if ("GeomBar" %in% g && any(b$data[[which(g=="GeomBar")[1]]]$ymin < 0)) {
      d <- b$data[[which(g == "GeomBar")[1]]]
      out$setsize <- data.frame(x = d$x, size = -d$ymin)
    } else if ("GeomBar" %in% g && !is.na(it$ylab) && grepl("size|Intersection", it$ylab, ignore.case = TRUE)) {
      d <- b$data[[which(g == "GeomBar")[1]]]; bar <- data.frame(x = d$x, height = d$ymax, fill = d$fill)
      # later GeomBar layers are query-highlight overlays: last layer touching an x decides the drawn fill
      for (li in which(g == "GeomBar")[-1]) { o <- b$data[[li]]; bar$fill[match(o$x, bar$x)] <- o$fill; bar$overlay_height <- NULL }
      tl <- which(g == "GeomText")
      if (length(tl)) { t <- b$data[[tl[1]]]; bar$label <- t$label[match(bar$x, t$x)] }
      out$bars <- bar; out$bars_ylab <- it$ylab
    } else out$annotations[[length(out$annotations)+1]] <- list(ylab = it$ylab, geoms = g, b = b)
  }
  if (!is.null(out$matrix) && !is.null(out$bars)) {
    m <- out$matrix; d <- m$dots
    mem <- tapply(seq_len(nrow(d)), d$x, function(ix) paste(m$sets[d$y[ix][d$member[ix]]], collapse = "-"))
    out$bars$combo <- mem[as.character(out$bars$x)]
    out$bars <- out$bars[order(out$bars$x), ]
  }
  if (!is.null(out$setsize) && !is.null(out$matrix)) out$setsize$set <- out$matrix$sets[out$setsize$x]
  out
}
norm_combo <- function(x, order_names) sapply(strsplit(x, "-", fixed = TRUE), function(z) paste(order_names[order_names %in% z], collapse = "-"))

# ---- UpSetR: walk the gtable/grob trees the package returns and collect what was drawn ----
walk_grobs <- function(g, acc = new.env()) {
  cls <- class(g)[1]
  if (is.null(acc$items)) acc$items <- list()
  acc$items[[length(acc$items) + 1]] <- list(cls = cls, name = g$name, g = g)
  kids <- NULL
  if (inherits(g, "gtable")) kids <- g$grobs else if (inherits(g, "gTree")) kids <- g$children
  for (k in kids) if (inherits(k, "grob")) walk_grobs(k, acc)
  acc
}
num <- function(u) as.numeric(grid::convertUnit(u, "native", valueOnly = TRUE))

# Everything UpSetR drew, from the grobs of upset()'s return value (bar labels L->R, dot matrix, set-size bars).
extract_upsetr <- function(x) {
  mb <- walk_grobs(x$Main_bar)$items; mt <- walk_grobs(x$Matrix)$items; sz <- walk_grobs(x$Sizes)$items
  npc <- function(u) as.numeric(u)   # units here are npc
  # bar labels: the text grob whose label vector is as long as the number of drawn columns
  pts <- Filter(function(i) i$cls == "points", mt)[[1]]$g
  px <- npc(pts$x); py <- npc(pts$y); pcol <- pts$gp$col
  ux <- sort(unique(round(px, 6))); uy <- sort(unique(round(py, 6)))
  rows <- (trimws(as.character(Filter(function(i) i$cls == "text" && any(grepl("[A-Za-z0-9]", as.character(i$g$label))) && length(i$g$label) == length(uy), mt)[[1]]$g$label)))
  rows <- rows  # bottom-to-top order of y
  txt <- Filter(function(i) i$cls == "text" && length(i$g$label) == length(ux) && all(grepl("^[0-9]+$", as.character(i$g$label))), mb)
  labs <- as.numeric(as.character(txt[[1]]$g$label)); lx <- npc(txt[[1]]$g$x)
  lab_order <- order(lx); labs <- labs[lab_order]
  cols <- lapply(seq_along(ux), function(j) { ix <- which(round(px, 6) == ux[j]); ix })
  members <- sapply(seq_along(ux), function(j) { ix <- cols[[j]]; m <- ix[!grepl("^#D4D4D4", toupper(pcol[ix]))]
                     paste(rows[match(round(py[m], 6), uy)], collapse = "-") })
  list(labels = labs, members = members, pcol = pcol, rows = rows)
}
