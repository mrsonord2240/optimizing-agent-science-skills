# Audit helpers: build the ;-string matrix from a MAF and verify a drawn ComplexHeatmap oncoPrint from its SVG.
suppressMessages({library(ComplexHeatmap);library(circlize);library(maftools);library(xml2)})
CLS <- c(Missense_Mutation="Missense", In_Frame_Ins="Missense", In_Frame_Del="Missense",
         Nonsense_Mutation="Truncating", Frame_Shift_Ins="Truncating", Frame_Shift_Del="Truncating",
         Nonstop_Mutation="Truncating", Splice_Site="Splice", Translation_Start_Site="Truncating")
read_maf_df <- function(f) read.delim(f, sep="\t", comment.char="#", stringsAsFactors=FALSE, check.names=FALSE, quote="")
maf_to_long <- function(df) {
  df$cls <- unname(CLS[df$Variant_Classification]); df <- df[!is.na(df$cls),]
  unique(df[,c("Hugo_Symbol","Tumor_Sample_Barcode","cls")])
}
build_mat <- function(long, genes, samples) {
  mat <- matrix("", nrow=length(genes), ncol=length(samples), dimnames=list(genes, samples))
  for (i in seq_len(nrow(long))) { g <- long$Hugo_Symbol[i]; s <- long$Tumor_Sample_Barcode[i]
    if (g %in% genes && s %in% samples) { v <- mat[g,s]; mat[g,s] <- if (v=="") long$cls[i] else paste(v, long$cls[i], sep=";") } }
  mat
}
# The Skill's alter_fun block, verbatim (only wrapped in a function so `col` can be passed)
get_alter_fun <- function(col) list(
    background = function(x, y, w, h)
        grid.rect(x, y, w - unit(0.5, 'mm'), h - unit(0.5, 'mm'),
                  gp = gpar(fill = '#EEEEEE', col = NA)),
    Amp = function(x, y, w, h)
        grid.rect(x, y, w - unit(0.5, 'mm'), h - unit(0.5, 'mm'),
                  gp = gpar(fill = col['Amp'], col = NA)),
    HomDel = function(x, y, w, h)
        grid.rect(x, y, w - unit(0.5, 'mm'), h - unit(0.5, 'mm'),
                  gp = gpar(fill = col['HomDel'], col = NA)),
    Missense = function(x, y, w, h)
        grid.rect(x, y, w - unit(0.5, 'mm'), h * 0.5,
                  gp = gpar(fill = col['Missense'], col = NA)),
    Truncating = function(x, y, w, h)
        grid.rect(x, y, w - unit(0.5, 'mm'), h * 0.33,
                  gp = gpar(fill = col['Truncating'], col = NA)),
    Splice = function(x, y, w, h)
        grid.rect(x, y, w - unit(0.5, 'mm'), h * 0.25,
                  gp = gpar(fill = col['Splice'], col = NA)),
    Fusion = function(x, y, w, h)
        grid.points(x, y, pch = 17, size = unit(2, 'mm'),
                    gp = gpar(col = col['Fusion'])))
SKILL_COL <- c('Missense'='#56B4E9','Truncating'='#000000','Splice'='#CC79A7','Amp'='#D55E00','HomDel'='#0072B2','Fusion'='#009E73')

sty <- function(s, key) { m <- regmatches(s, regexpr(paste0(key, ": *[^;]+"), s)); if (length(m)==0) NA_character_ else sub(paste0(key, ": *"), "", m) }
parse_svg <- function(f) {
  doc <- read_xml(f); ns <- xml_ns(doc)
  rs <- xml_find_all(doc, "//d1:rect", ns)
  rect <- data.frame(x=as.numeric(xml_attr(rs,"x")), y=as.numeric(xml_attr(rs,"y")), w=as.numeric(xml_attr(rs,"width")), h=as.numeric(xml_attr(rs,"height")),
                     fill=toupper(vapply(xml_attr(rs,"style"), function(s) sty(s,"fill"), "")), stringsAsFactors=FALSE)
  rect <- rect[!is.na(rect$x) & !is.na(rect$w) & !is.na(rect$h) & !is.na(rect$y),]
  rect$cx <- rect$x+rect$w/2; rect$cy <- rect$y+rect$h/2
  ps <- xml_find_all(doc, "//d1:polygon", ns)
  poly <- NULL
  if (length(ps)>0) poly <- do.call(rbind, lapply(seq_along(ps), function(i) { pts <- as.numeric(unlist(strsplit(trimws(xml_attr(ps[[i]],"points")), "[ ,]+")))
    xs <- pts[c(TRUE,FALSE)]; ys <- pts[c(FALSE,TRUE)]; data.frame(cx=mean(xs), cy=mean(ys), w=diff(range(xs)), h=diff(range(ys)),
       fill=toupper(sty(xml_attr(ps[[i]],"style"),"fill")), stringsAsFactors=FALSE) }))
  ts <- xml_find_all(doc, "//d1:text", ns)
  txt <- data.frame(x=as.numeric(xml_attr(ts,"x")), y=as.numeric(xml_attr(ts,"y")), label=xml_text(ts), stringsAsFactors=FALSE)
  list(rect=rect, poly=poly, txt=txt)
}
# Decode the drawn cells from an oncoPrint SVG. Background rects are '#EEEEEE'.
decode_cells <- function(svg, col) {
  P <- parse_svg(svg); R <- P$rect
  R <- R[!is.na(R$fill),]; bg <- R[R$fill=="#EEEEEE",]
  tx <- table(round(bg$cx,1)); ty <- table(round(bg$cy,1))
  # body cells: the legend also draws background rects, so keep only the most frequent x/y grid values
  xs <- sort(as.numeric(names(tx)[tx==max(tx)])); ys <- sort(as.numeric(names(ty)[ty==max(ty)]))
  cells <- matrix("", nrow=length(ys), ncol=length(xs))
  find <- function(cx, cy) { j <- which.min(abs(xs-cx)); i <- which.min(abs(ys-cy)); if (abs(xs[j]-cx)<0.3 && abs(ys[i]-cy)<0.6) c(i,j) else NULL }
  cls_of <- setNames(names(col), toupper(col))
  add <- function(i,j,nm) cells[i,j] <<- if (cells[i,j]=="") nm else paste(cells[i,j], nm, sep=";")
  bw <- median(bg$w)
  cand <- R[R$fill %in% names(cls_of) & abs(R$w-bw)<0.2,]
  for (k in seq_len(nrow(cand))) { ij <- find(cand$cx[k], cand$cy[k]); if (!is.null(ij)) add(ij[1], ij[2], cls_of[[cand$fill[k]]]) }
  if (!is.null(P$poly)) for (k in seq_len(nrow(P$poly))) { if (P$poly$fill[k] %in% names(cls_of)) { ij <- find(P$poly$cx[k], P$poly$cy[k]); if (!is.null(ij)) add(ij[1], ij[2], cls_of[[P$poly$fill[k]]]) } }
  list(cells=cells, xs=xs, ys=ys, P=P, bg=bg)
}
norm_cell <- function(s) vapply(strsplit(s, ";"), function(z) paste(sort(z[z!=""]), collapse=";"), "")
