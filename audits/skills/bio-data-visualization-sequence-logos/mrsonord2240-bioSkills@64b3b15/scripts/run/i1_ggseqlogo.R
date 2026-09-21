# Input 1: ggseqlogo (R) -- SKILL.md blocks verbatim + content assertions
suppressPackageStartupMessages({library(ggseqlogo); library(ggplot2)})
cat("ggseqlogo", as.character(packageVersion("ggseqlogo")), " ggplot2", as.character(packageVersion("ggplot2")), "\n")
OUT <- "out"
rd <- function(f) readLines(file.path("data", f))
eqic <- function(top, ind) all(abs(top-ind) < 1e-6 | ind < 0.004*max(top)*2.5)
ok <- function(name, cond, note="") cat(sprintf("ASSERT %-72s %s %s\n", name, if (isTRUE(cond)) "PASS" else "FAIL", note))
withw <- function(expr) { ws <- character(); v <- withCallingHandlers(expr, warning=function(w){ws <<- c(ws,conditionMessage(w)); invokeRestart("muffleWarning")}); list(v=v, w=ws) }

# ---- independent IC (base R) ----
ic_ind <- function(seqs, alpha, bg=NULL, small=TRUE) {
  L <- nchar(seqs[1]); n <- length(seqs); K <- length(alpha)
  m <- do.call(rbind, strsplit(seqs, ""))
  sapply(1:L, function(i) { p <- table(factor(m[,i], levels=alpha))/n
    if (is.null(bg)) { H <- -sum(ifelse(p>0, p*log2(p), 0)); ic <- log2(K)-H; if (small) ic <- ic-(K-1)/(2*log(2)*n); max(ic,0) }
    else sum(ifelse(p>0, p*log2(p/bg[alpha]), 0)) }) }
# letter heights from a ggseqlogo plot: per (position, letter) y0,y1 of the glyph box
lh <- function(p) { d <- p$layers[[1]]$data; d <- d[!is.na(d$position) & !is.na(d$letter),]
  do.call(rbind, lapply(split(d, list(d$position, d$letter), drop=TRUE), function(g) data.frame(position=g$position[1], letter=g$letter[1], y0=min(g$y), y1=max(g$y)))) }
# columns with zero (corrected) IC are not drawn at all: report them as height 0 / letter "-"
col_top <- function(p) { h <- lh(p); L <- max(h$position); v <- rep(0, L); t <- tapply(h$y1, h$position, max); v[as.integer(names(t))] <- as.numeric(t); v }
dom_letters <- function(p, L) { h <- lh(p); sapply(1:L, function(i){g<-h[h$position==i & (h$y1-h$y0)>1e-9,]; if(nrow(g)==0) "-" else g$letter[which.max(g$y1-g$y0)]}) }

# ================= SKILL.md block 1 (verbatim) =================
seqs <- c('ATGCAA', 'ATGCAC', 'ATGCAG', 'ATGCAT', 'ACGCAA')
p1 <- ggseqlogo(seqs, method = 'bits'); ggsave(file.path(OUT,"r_block1_seqs.png"), p1, width=4, height=2, dpi=120)
pwm <- matrix(c(0.7, 0.1, 0.1, 0.1,
                0.1, 0.7, 0.1, 0.1,
                0.4, 0.1, 0.4, 0.1), ncol = 3,
              dimnames = list(c('A', 'C', 'G', 'T'), NULL))
p2 <- ggseqlogo(pwm, method = 'bits'); ggsave(file.path(OUT,"r_block1_pwm.png"), p2, width=3, height=2, dpi=120)
seqs_a <- seqs; seqs_b <- rev(seqs)   # SKILL leaves seqs_a/seqs_b undefined
p3 <- ggseqlogo(list(TFA = seqs_a, TFB = seqs_b), method = 'bits', col_scheme = 'nucleotide'); ggsave(file.path(OUT,"r_block1_multi.png"), p3, width=4, height=3, dpi=120)
alpha <- c("A","C","G","T")
ic5 <- ic_ind(seqs, alpha, small=TRUE); top5 <- col_top(p1)
ok("block1 seqs n=5: column tops == independent IC with e_n", all(abs(top5-ic5)<1e-6), sprintf("gg=%s ind=%s", paste(round(top5,3),collapse=","), paste(round(ic5,3),collapse=",")))
ok("block1 seqs n=5: differs from uncorrected IC (correction active)", !all(abs(top5-ic_ind(seqs,alpha,small=FALSE))<1e-6))
pm <- apply(pwm,2,function(x)x/sum(x)); Hh <- -colSums(ifelse(pm>0,pm*log2(pm),0)); topP <- col_top(p2)
ok("block1 PWM (prob): column tops == 2 - H (no small-sample term)", all(abs(topP-(2-Hh))<1e-6), sprintf("gg=%s ind=%s", paste(round(topP,4),collapse=","), paste(round(2-Hh,4),collapse=",")))
h3 <- lh(p2); h3 <- h3[h3$position==3,]; ok("PWM col3: A and G are the two tallest letters", setequal(h3$letter[order(-(h3$y1-h3$y0))][1:2], c("A","G")))

# ================= background handling: SKILL/example say bg_freq =================
seq200 <- rd("dna_n200.txt"); human_bg <- c(A=0.29,C=0.21,G=0.21,T=0.29)
r0 <- withw(ggseqlogo(seq200, method='bits'))
r1 <- withw(ggseqlogo(seq200, method='bits', bg_freq = human_bg))
r1w <- withw({ pdf(NULL); print(r1$v); dev.off() })
cat("bg_freq build/print warnings:", paste(unique(c(r1$w, r1w$w)), collapse=" | "), "\n")
ok("bg_freq=human_bg changes heights vs no bg_freq", !all(abs(col_top(r0$v)-col_top(r1$v))<1e-9), sprintf("max |diff| = %g", max(abs(col_top(r0$v)-col_top(r1$v)))))
ok("bg_freq is a formal argument of ggseqlogo()/geom_logo()", "bg_freq" %in% c(names(formals(ggseqlogo)), names(formals(geom_logo))))
ok("tops == uniform-background IC (bg silently ignored)", eqic(col_top(r1$v), ic_ind(seq200,alpha,small=TRUE)))
ok("tops == human-background IC (what the SKILL promises)", all(abs(col_top(r1$v)-ic_ind(seq200,alpha,bg=human_bg))<1e-2))
cat("planted fully-C pos 9: uniform IC =", round(ic_ind(seq200,alpha,small=FALSE)[9],3), " human-bg IC =", round(ic_ind(seq200,alpha,bg=human_bg)[9],3), "\n")

# ================= n = 5, 20, 200, 2000 =================
planted <- c("A","C",NA,NA,"T","G",NA,"A","C",NA)
for (n in c(5,20,200,2000)) {
  s <- rd(sprintf("dna_n%d.txt", n)); p <- ggseqlogo(s, method='bits'); ggsave(file.path(OUT,sprintf("r_dna_n%d.png",n)), p, width=5, height=2, dpi=120)
  top <- col_top(p); ind <- ic_ind(s, alpha, small=TRUE)
  ok(sprintf("n=%d column IC == independent (uniform bg + e_n)", n), eqic(top,ind), sprintf("max|d|=%.2g (cols below the stack pad are not drawn)", max(abs(top-ind))))
  dom <- dom_letters(p, 10)
  mm_ <- do.call(rbind, strsplit(s,"")); am <- sapply(1:10, function(i) names(which.max(table(mm_[,i]))))
  ok(sprintf("n=%d dominant letter == sample argmax at every drawn column", n), all(dom[dom!="-"]==am[dom!="-"]), paste(dom,collapse=""))
  if (n>=20) ok(sprintf("n=%d dominant letter == planted at positions 1,2,5,6,8,9", n), all(dom[c(1,2,5,6,8,9)]==planted[c(1,2,5,6,8,9)]))
  h <- lh(p); h <- h[(h$y1-h$y0)>1e-9,]; hs <- tapply(h$y1-h$y0, h$position, sum); pad <- 0.004*max(top); nl <- table(h$position)
  ok(sprintf("n=%d letter heights + stack pads == column IC", n), all(abs((hs+pad*as.numeric(nl)) - top[as.integer(names(hs))])<1e-6))
  cat(sprintf("   n=%d  IC gg      : %s\n", n, paste(round(top,3),collapse=" ")))
  cat(sprintf("   n=%d  IC uncorr. : %s\n", n, paste(round(ic_ind(s,alpha,small=FALSE),3),collapse=" ")))
}
set.seed(1); rs <- replicate(5000, {x<-sample(alpha,5,TRUE); as.numeric(table(factor(x,levels=alpha))/5)})
raw <- apply(rs,2,function(p) 2+sum(ifelse(p>0,p*log2(p),0)))
cat("random n=5 columns: mean raw IC =", round(mean(raw),3), "; theory (K-1)/(2 ln2 n) =", round(3/(2*log(2)*5),3), "\n")
ok("raw IC of RANDOM n=5 columns is >0.4 bits (small-sample bias is real; e_n first-order approx 0.433 slightly under-corrects)", mean(raw)>0.4)

# ================= probability method =================
pp <- ggseqlogo(seq200, method='probability'); tp <- col_top(pp)
ok("probability: every column totals 1 (flat)", all(abs(tp-1)<1e-6)); ggsave(file.path(OUT,"r_prob_n200.png"), pp, width=5, height=2, dpi=120)

# ================= counts matrix route =================
cnt <- sapply(1:10, function(i) table(factor(substr(seq200,i,i), levels=alpha))); rownames(cnt) <- alpha
pc <- ggseqlogo(cnt, method='bits')
ok("counts matrix == probability matrix heights", all(abs(col_top(pc)-col_top(ggseqlogo(apply(cnt,2,function(x)x/sum(x)), method='bits')))<1e-9))
ok("matrix input has NO small-sample correction (tops == uniform IC)", eqic(col_top(pc), ic_ind(seq200,alpha,small=FALSE)))
s5 <- rd("dna_n5.txt"); c5 <- sapply(1:10, function(i) table(factor(substr(s5,i,i), levels=alpha))); rownames(c5)<-alpha
d5 <- col_top(ggseqlogo(s5, method='bits')) - col_top(ggseqlogo(c5, method='bits'))
cat("n=5: (sequence-input) minus (counts-matrix) column IC:", paste(round(d5,3),collapse=" "), "\n")
ok("n=5: sequence and counts routes give the same height", all(abs(d5)<1e-9), "route silently changes IC by ~0.43 bits")
tr <- tryCatch({ ggseqlogo(t(pwm)) ; "no error" }, error=function(e) paste("ERROR:", conditionMessage(e)))
cat("transposed PWM (positions x letters, no rownames):", tr, "\n")

# ================= JASPAR MA0106.3 TP53 =================
j <- readLines("F:/OpenScience/audit-envs/data-visualization/public-data/sequence-logos/MA0106.3_TP53.jaspar")
mm <- do.call(rbind, lapply(j[-1], function(l){ v <- strsplit(gsub("[][]", "", substring(l,4)), " +")[[1]]; as.numeric(v[v!=""]) })); rownames(mm) <- c("A","C","G","T")
pj <- ggseqlogo(mm, method='bits'); ggsave(file.path(OUT,"r_jaspar_TP53_bits.png"), pj, width=7, height=2, dpi=120)
pmj <- apply(mm,2,function(x)x/sum(x)); Hj <- -colSums(ifelse(pmj>0,pmj*log2(pmj),0))
ok("JASPAR TP53 (18 cols): tops == 2 - H", all(abs(col_top(pj)-(2-Hj))<1e-6), sprintf("max IC %.3f at col %d", max(col_top(pj)), which.max(col_top(pj))))
dj <- dom_letters(pj, 18); cons <- paste(rownames(mm)[apply(mm,2,which.max)],collapse="")
ok("logo dominant letter per column == argmax counts", identical(paste(dj,collapse=""), cons), cons)
ggsave(file.path(OUT,"r_jaspar_TP53_prob.png"), ggseqlogo(mm, method='probability'), width=7, height=2, dpi=120)

# ================= RNA / alphabet =================
rna <- rd("rna_n200.txt"); pr1 <- ggseqlogo(rna, method='bits'); ggsave(file.path(OUT,"r_rna_auto.png"), pr1, width=5, height=2, dpi=120)
cat("RNA auto: letters:", paste(sort(unique(pr1$layers[[1]]$data$letter)),collapse=""), "\n")
ok("RNA auto-detected without seq_type (letters ACGU, no T)", setequal(unique(pr1$layers[[1]]$data$letter), c("A","C","G","U")))
pr2 <- ggseqlogo(rna, method='bits', seq_type='rna'); ok("RNA explicit seq_type='rna' == auto heights", all(abs(col_top(pr2)-col_top(pr1))<1e-9))
ok("RNA IC == DNA IC of same data", all(abs(col_top(pr1)-col_top(ggseqlogo(seq200,method='bits')))<1e-9))
mx <- c("ACGT-","ACGTN","ACGTA"); rr <- tryCatch({ ggseqlogo(mx); "ok" }, error=function(e) paste("ERROR:", conditionMessage(e))); cat("gap/N containing input:", rr, "\n")
ne <- tryCatch({ x <- withw(ggseqlogo(c("ACGT","ACG","ACGTA"))); paste("built; warn:", paste(x$w,collapse="|")) }, error=function(e) paste("ERROR:", conditionMessage(e))); cat("unequal-length input:", ne, "\n")
o1 <- withw(ggseqlogo("ACGTAC", method='bits')); cat("n=1 input warnings:", paste(o1$w, collapse=" | "), "; tops:", paste(round(col_top(o1$v),3),collapse=","), "\n")
ok("n=1: heights are real IC (not fabricated)", !any(grepl("Setting all information content to 2", o1$w)), "ggseqlogo warns and draws every column at 2 bits")
n2 <- withw(ggseqlogo(c("ACGTAC","ACGTAC"), method='bits')); cat("n=2 identical seqs: warn:", paste(n2$w,collapse="|"), " tops:", paste(round(col_top(n2$v),3), collapse=","), "\n")

# ================= protein =================
prot <- rd("prot_n200.txt"); AA <- strsplit("ACDEFGHIKLMNPQRSTVWY","")[[1]]
pa <- ggseqlogo(prot, method='bits', seq_type='aa'); ggsave(file.path(OUT,"r_protein_default.png"), pa, width=7, height=2.5, dpi=120)
topA <- col_top(pa); indA <- ic_ind(prot, AA, small=TRUE)
ok("protein n=200: tops == independent IC (K=20, e_n)", eqic(topA,indA), sprintf("pos8 %.3f (max log2 20 = 4.322)", topA[8]))
domA <- dom_letters(pa, 15)
ok("protein dominant letter: S at position 8", domA[8]=="S", paste(domA,collapse=""))
ha <- lh(pa); g5 <- ha[ha$position==5,]; ok("protein pos 5 two tallest letters are K/R", all(g5$letter[order(-(g5$y1-g5$y0))][1:2] %in% c("K","R")))
protein_pwm <- prot
cs <- make_col_scheme(chars = c('S','T','Y','K','R','H','D','E','A','V','L','I','M'),
    cols  = c('#D55E00','#D55E00','#D55E00','#0072B2','#0072B2','#0072B2','#CC79A7','#CC79A7','#009E73','#009E73','#009E73','#009E73','#009E73'))
pcs <- ggseqlogo(protein_pwm, method = 'bits', seq_type = 'aa', col_scheme = cs); ggsave(file.path(OUT,"r_protein_custom_scheme.png"), pcs, width=7, height=2.5, dpi=120)
cat("custom scheme block ran; letters absent from the scheme use na_col grey20\n")
un <- tryCatch({ ggseqlogo(c("ACDEFJ","ACDEFZ")); "ok" }, error=function(e) paste("ERROR:", conditionMessage(e))); cat("protein input with J/Z:", un, "\n")
