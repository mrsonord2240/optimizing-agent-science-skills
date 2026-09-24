# Q3: ranked DE table only (no matrix). Skill's guardrails, executed.
suppressMessages({library(clusterProfiler); library(msigdbr); library(limma)})
D <- "F:/OpenScience/comparisons/gsva-vs-gsea/data/"; O <- "F:/OpenScience/comparisons/gsva-vs-gsea/out/"
E <- as.matrix(read.csv(paste0(D,"expr.csv"), row.names=1, check.names=FALSE)); g <- read.csv(paste0(D,"group.csv"))
grp <- factor(g$group[match(colnames(E), g$sample)], levels=c("Control","Case"))
tt <- topTable(eBayes(lmFit(E, model.matrix(~grp))), coef=2, n=Inf)
kegg <- msigdbr(species="Homo sapiens", collection="C2", subcollection="CP:KEGG_LEGACY"); t2g <- unique(kegg[,c("gs_name","gene_symbol")])
mk <- function(v, ids) { names(v) <- ids; v <- v[!is.na(v) & !duplicated(names(v))]; sort(v, decreasing=TRUE) }
run <- function(gl, ...) { set.seed(123); as.data.frame(GSEA(gl, TERM2GENE=t2g, exponent=1, minGSSize=10, maxGSSize=500, eps=0, pvalueCutoff=1, seed=TRUE, verbose=FALSE, ...)) }
pick <- function(r, lbl) { for (s in c("KEGG_CELL_CYCLE","KEGG_OXIDATIVE_PHOSPHORYLATION")) { i <- match(s, r$ID)
  cat(sprintf("%-26s %-32s NES=%+.2f FDR=%.2e\n", lbl, s, r$NES[i], r$p.adjust[i])) } }
r_t   <- run(mk(tt$t, rownames(tt)))                                     # skill-correct: limma t
r_sp  <- run(mk(sign(tt$logFC) * -log10(pmax(tt$P.Value, 1e-30)), rownames(tt)))   # skill: signed -log10 p, clamp 1e-30
r_raw <- run(mk(-log10(tt$P.Value), rownames(tt)))                       # skill failure mode: raw p, sign erased
pick(r_t, "limma t (correct)"); pick(r_sp, "sign*-log10p (ok)"); pick(r_raw, "-log10p, NO sign (bad)")
cat("sets FDR<0.05 (t):", sum(r_t$p.adjust<0.05), " (raw-p, no sign):", sum(r_raw$p.adjust<0.05), " of those with NES>0 (raw-p):", sum(r_raw$p.adjust<0.05 & r_raw$NES>0), "\n")
# stale nPerm: silently accepted, engine downgrade
gl <- mk(tt$t, rownames(tt))
w <- character(); set.seed(123)
res <- withCallingHandlers(GSEA(gl, TERM2GENE=t2g, nPerm=1000, minGSSize=10, maxGSSize=500, pvalueCutoff=1, verbose=FALSE),
  warning=function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") })
cat("nPerm=1000 ran to completion:", inherits(res, "gseaResult"), "; warnings:", length(w), "\n"); cat(substr(w, 1, 110), sep="\n")
cat("'nPerm' in gse@params:", "nPerm" %in% names(res@params), "\n")
# unsorted vector -> hard error
e <- tryCatch({ GSEA(sample(gl), TERM2GENE=t2g, verbose=FALSE); "no error" }, error=function(x) conditionMessage(x)); cat("unsorted ->", substr(e,1,90), "\n")
