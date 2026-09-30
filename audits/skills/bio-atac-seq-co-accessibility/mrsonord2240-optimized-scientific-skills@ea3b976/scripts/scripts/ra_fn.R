# Re-audit function-level tests of run_cicero_pipeline (CLI tail removed). Modes: guards | planted | empty | window | seedrep
suppressPackageStartupMessages(library(Matrix))
mode <- commandArgs(TRUE)[1]; CO <- Sys.getenv("CO"); SKILL <- Sys.getenv("SKILL"); I <- file.path(CO, "work/reaudit/input")
W <- file.path(CO, "work/reaudit", paste0("fn_", mode)); dir.create(W, showWarnings=FALSE, recursive=TRUE); setwd(W)
src <- readLines(file.path(SKILL, "scripts/cicero_workflow.R"))
src <- src[seq_len(grep("^args <- commandArgs", src)[1] - 1)]
eval(parse(text=src))
chk <- function(n, ok, d="") cat(if (isTRUE(ok)) "PASS" else "FAIL", n, d, "\n")
TSS <- file.path(Sys.getenv("ATACDATA"), "annotation/gencode_v29_protein_coding_tss.chr1.bed")
real <- function() list(m=readMM(file.path(I,"peak_matrix.mtx")), pm=read.delim(file.path(I,"peak_metadata.tsv"), row.names=1), cm=read.delim(file.path(I,"cell_metadata.tsv"), row.names=1))
planted <- function(seed=42) {
  set.seed(seed); npk <- 60; ncell <- 2400
  st <- rep(1:4, each=ncell/4)
  starts <- 100000 + 5000*(seq_len(npk)-1)
  grp <- c(rep(1:4, each=6), rep(0, npk-24))
  P <- matrix(0.15, npk, ncell)
  for (g in 1:4) P[grp==g, ] <- ifelse(rep(st==g, each=sum(grp==g)), 0.55, 0.03)
  m <- Matrix((matrix(runif(npk*ncell), npk, ncell) < P) * 1, sparse=TRUE)
  pn <- sprintf("chr1_%d_%d", starts, starts+500)
  list(m=as(m, "CsparseMatrix"), pm=data.frame(row.names=pn, site_name=pn)[, 0, drop=FALSE], cm=data.frame(row.names=paste0("c", seq_len(ncell)), state=st), grp=setNames(grp, pn))
}
if (mode == "guards") {
  r <- real(); ok <- function(expr) tryCatch({ force(expr); "no error" }, error=function(e) conditionMessage(e))
  t0 <- Sys.time()
  e1 <- ok(run_cicero_pipeline(r$m[-1,], r$pm, r$cm)); chk("dim mismatch rejected", grepl("nrow|ncol|==", e1), e1)
  pm2 <- r$pm; rownames(pm2) <- sub("^(chr[0-9]+)_([0-9]+)_([0-9]+)$", "\\1:\\2-\\3", rownames(pm2))
  e2 <- ok(run_cicero_pipeline(r$m, pm2, r$cm)); chk("colon peak names rejected", grepl("chr_start_end", e2), e2)
  e3 <- ok(run_cicero_pipeline(r$m, r$pm, r$cm, tss_bed="/nonexistent.bed")); chk("missing tss_bed rejected early", grepl("not found", e3), e3)
  writeLines(c("chr1\t100\t200", "chr1\t300\t400"), "no_name.bed")
  e4 <- ok(run_cicero_pipeline(r$m, r$pm, r$cm, tss_bed="no_name.bed")); chk("BED without gene names rejected early", grepl("column 4", e4), e4)
  chk("all guards fire before the long run (<60 s total)", as.numeric(difftime(Sys.time(), t0, units="secs")) < 60, sprintf("%.1f s", as.numeric(difftime(Sys.time(), t0, units="secs"))))
}
if (mode %in% c("planted", "empty")) {
  p <- planted(); thr <- if (mode == "planted") 0.25 else 0.999
  res <- run_cicero_pipeline(p$m, p$pm, p$cm, output_prefix="pl", coaccess_threshold=thr, tss_bed=TSS, seed=1)
  cn <- res$conns; cat("scored", nrow(cn), "neg", sum(cn$coaccess < 0), "range", range(cn$coaccess), "\n")
  if (mode == "planted") {
    g1 <- p$grp[cn$Peak1]; g2 <- p$grp[cn$Peak2]
    within <- g1 > 0 & g1 == g2; cross <- g1 > 0 & g2 > 0 & g1 != g2; bg <- g1 == 0 & g2 == 0
    fr <- function(i) mean(cn$coaccess[i] > 0.25)
    cat(sprintf("strong fraction: within-group %.2f (n=%d), cross-group %.2f (n=%d), background %.2f (n=%d)\n", fr(within), sum(within), fr(cross), sum(cross), fr(bg), sum(bg)))
    chk("planted within-group pairs mostly strong (>=0.8)", fr(within) >= 0.8)
    chk("cross-group and background rarely strong (<=0.1)", fr(cross) <= 0.1 && fr(bg) <= 0.1)
    chk("cross-group mean score lower than within", mean(cn$coaccess[cross]) < mean(cn$coaccess[within]) - 0.3, sprintf("%.2f vs %.2f", mean(cn$coaccess[cross]), mean(cn$coaccess[within])))
  } else {
    chk("empty strong set handled (no crash), files written", file.exists("pl_connections.tsv"), paste(list.files(), collapse=" "))
    cat("connections rows:", nrow(read.delim("pl_connections.tsv")), "\n")
  }
}
if (mode == "window") {
  r <- real()
  res <- run_cicero_pipeline(r$m, r$pm, r$cm, output_prefix="w1", window=1e6, tss_bed=TSS)
  cn <- res$conns; pos <- function(x) as.numeric(sapply(strsplit(x, "_"), `[`, 2))
  ch <- function(x) sub("_.*", "", x); span <- abs(pos(cn$Peak1) - pos(cn$Peak2))
  chk("no cross-chromosome pairs", all(ch(cn$Peak1) == ch(cn$Peak2)))
  chk("all three chromosomes scored", setequal(unique(ch(cn$Peak1)), c("chr1","chr2","chr19")), paste(table(ch(cn$Peak1)), collapse="/"))
  pe <- function(x) as.numeric(sapply(strsplit(x, "_"), `[`, 3)); gap <- pmax(pos(cn$Peak1), pos(cn$Peak2)) - pmin(pe(cn$Peak1), pe(cn$Peak2))
  chk("window=1e6: end-to-start gap <= 1 Mb (peaks up to 67 kb wide, so start-to-start may exceed the window by one peak width)", max(gap) <= 1e6, sprintf("max gap %.0f; max start-start %.0f", max(gap), max(span)))
  chk("window=1e6 reaches beyond 500 kb", sum(span > 5e5) > 1000, sprintf("%d scored pairs beyond 500 kb", sum(span > 5e5)))
}
if (mode == "zero") {   # observation: one cell with no reads in the peak set (e.g. after subsetting peaks)
  r <- real(); m <- r$m; m[, 1] <- 0; m <- as(m, "CsparseMatrix"); cat("cell 1 zeroed; column sums==0:", sum(Matrix::colSums(m) == 0), "\n")
  e <- tryCatch({ run_cicero_pipeline(m, r$pm, r$cm); "no error" }, error=function(e) conditionMessage(e))
  cat("RESULT:", e, "\n")
  chk("zero-read cell halts with an actionable message naming the cause", grepl("zero|empty|no reads|colSums", e), e)
}
if (mode == "nulltss") {   # optional-TSS branch: no BED -> connections only, message, no enhancer-gene file
  p <- planted(); res <- run_cicero_pipeline(p$m, p$pm, p$cm, output_prefix="nt", seed=1)
  chk("tss_bed=NULL writes connections only", file.exists("nt_connections.tsv") && !file.exists("nt_enhancer_gene_pairs.csv"), paste(list.files(), collapse=" "))
  ref <- read.delim(file.path(dirname(getwd()), "fn_planted", "pl_connections.tsv"))
  chk("strong table identical to the run with a TSS BED (seed=1, same input)", isTRUE(all.equal(ref, read.delim("nt_connections.tsv"))), sprintf("%d rows", nrow(ref)))
}
