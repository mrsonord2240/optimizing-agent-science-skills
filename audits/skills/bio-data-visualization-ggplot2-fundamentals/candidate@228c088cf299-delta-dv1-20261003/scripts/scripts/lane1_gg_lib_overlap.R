# Measure drawn ggrepel label boxes (mm, device coords) and report pairwise overlaps / out-of-panel labels.
# label_boxes(plot, w_mm, h_mm): draws plot on an off-screen png, forces grobs, returns data.frame of text boxes per panel.
suppressMessages(library(grid))
label_boxes <- function(p, w_mm, h_mm, file = tempfile(fileext = ".png")) {
  png(file, width = w_mm/25.4*150, height = h_mm/25.4*150, res = 150)
  on.exit(dev.off())
  print(p); grid.force()
  g <- grid.grep("textrepelgrob", grep = TRUE, global = TRUE, grobs = TRUE, viewports = TRUE, strict = FALSE)
  out <- list()
  for (i in seq_along(g)) {
    gp <- g[[i]]
    grob <- grid.get(gp)
    if (is.null(grob$label) || !nzchar(as.character(grob$label))) next
    vpp <- attr(gp, "vpPath")
    upViewport(0); downViewport(do.call(vpPath, as.list(strsplit(vpp, "::", fixed = TRUE)[[1]])))
    tg <- grob
    x <- convertX(tg$x, "inches", valueOnly = TRUE); y <- convertY(tg$y, "inches", valueOnly = TRUE)
    w <- convertWidth(grobWidth(tg), "mm", valueOnly = TRUE); h <- convertHeight(grobHeight(tg), "mm", valueOnly = TRUE)
    # position in device mm: use current vp transform
    tr <- current.transform()
    xy <- c(x, y, 1) %*% tr   # inches
    pw <- convertWidth(unit(1, "npc"), "mm", valueOnly = TRUE); ph <- convertHeight(unit(1, "npc"), "mm", valueOnly = TRUE)
    o <- c(0, 0, 1) %*% tr; px0 <- o[1]*25.4; py0 <- o[2]*25.4
    out[[length(out)+1]] <- data.frame(label = as.character(tg$label), cx = xy[1]*25.4, cy = xy[2]*25.4, w = w, h = h,
       hjust = if (is.null(tg$hjust)) 0.5 else tg$hjust, vp = as.character(vpp), panel_w = pw, panel_h = ph, px0 = px0, py0 = py0)
    upViewport(0)
  }
  do.call(rbind, out)
}
overlaps <- function(b) {
  if (is.null(b) || nrow(b) < 2) return(data.frame())
  b$x0 <- b$cx - b$w/2; b$x1 <- b$cx + b$w/2; b$y0 <- b$cy - b$h/2; b$y1 <- b$cy + b$h/2
  res <- list()
  for (i in 1:(nrow(b)-1)) for (j in (i+1):nrow(b)) {
    if (b$vp[i] != b$vp[j]) next
    ox <- min(b$x1[i], b$x1[j]) - max(b$x0[i], b$x0[j]); oy <- min(b$y1[i], b$y1[j]) - max(b$y0[i], b$y0[j])
    if (ox > 0 && oy > 0) res[[length(res)+1]] <- data.frame(a = b$label[i], b = b$label[j], ox_mm = round(ox,2), oy_mm = round(oy,2))
  }
  if (length(res)) do.call(rbind, res) else data.frame()
}
outside <- function(b) {
  if (is.null(b) || !nrow(b)) return(data.frame())
  k <- with(b, cx - w/2 < px0 - 0.01 | cx + w/2 > px0 + panel_w + 0.01 | cy - h/2 < py0 - 0.01 | cy + h/2 > py0 + panel_h + 0.01)
  b[k, c("label","vp")]
}
