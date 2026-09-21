# Helpers: parse an svglite SVG of a lollipop plot into (position, height) circles, domain rects and axis calibration.
suppressMessages({library(svglite); library(data.table)})
attr_num <- function(x, a) as.numeric(sub(paste0(".*", a, "='([^']*)'.*"), "\\1", x))
attr_chr <- function(x, a) sub(paste0(".*", a, "='([^']*)'.*"), "\\1", x)
svg_parse <- function(f) {
  s <- readLines(f, warn = FALSE)
  ci <- s[grepl("^<circle", s)]
  circ <- data.table(cx = attr_num(ci, "cx"), cy = attr_num(ci, "cy"), r = attr_num(ci, "r"),
                     fill = toupper(sub(".*fill: (#[0-9A-Fa-f]{6}|[a-z]+);.*", "\\1", ci)))
  ti <- s[grepl("^<text", s)]
  txt <- data.table(x = attr_num(ti, "x"), y = attr_num(ti, "y"),
                    anchor = ifelse(grepl("text-anchor='([a-z]+)'", ti), sub(".*text-anchor='([a-z]+)'.*", "\\1", ti), "start"),
                    label = sub("</text>.*", "", sub("^<text[^>]*>", "", ti)))
  ri <- s[grepl("^ *<rect x=", s)]
  rect <- data.table(x = attr_num(ri, "x"), y = attr_num(ri, "y"), w = attr_num(ri, "width"), h = attr_num(ri, "height"),
                     fill = toupper(sub(".*fill: (#[0-9A-Fa-f]{6}|[a-z]+|none);.*", "\\1", ri)))
  list(circ = circ, txt = txt, rect = rect, raw = s)
}
# x calibration: numeric labels centred on the bottom axis (same y, anchor middle); y calibration: numeric labels anchor 'end'
svg_calib <- function(p, xtick_y = NULL) {
  t <- p$txt[grepl("^[0-9]+$", label)]
  tm <- t[anchor == "middle"]
  yb <- if (is.null(xtick_y)) max(tm$y) else xtick_y
  xt <- tm[abs(y - yb) < 0.6]
  fx <- lm(as.numeric(label) ~ x, data = xt)
  ye <- t[anchor == "end"]
  ye[, y0 := y - 3.56]
  fy <- if (nrow(ye) >= 2) lm(as.numeric(label) ~ y0, data = ye) else NULL
  list(fx = fx, fy = fy, xt = xt, ye = ye)
}
svg_points <- function(p, cal) {
  d <- copy(p$circ)
  d[, pos := predict(cal$fx, newdata = data.frame(x = cx))]
  if (!is.null(cal$fy)) d[, height := predict(cal$fy, newdata = data.frame(y0 = cy))]
  d
}
