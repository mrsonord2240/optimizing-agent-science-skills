# Re-audit: independent assertions on the shipped CLI outputs (3-chromosome real PBMC Multiome ATAC slice, pattern .mtx, chr1 TSS BED)
a <- commandArgs(TRUE); tag <- if (length(a)) a[1] else "cli"; CO <- Sys.getenv("CO"); D <- file.path(CO, "work/reaudit", tag); I <- if (tag == "stress") file.path(CO, "work/input") else file.path(CO, "work/reaudit/input")
exp_chr <- if (tag == "stress") "chr1" else c("chr1","chr2","chr19")
chk <- function(n, ok, d="") cat(if (isTRUE(ok)) "PASS" else "FAIL", n, d, "\n")
s <- read.delim(file.path(D, "cicero_connections.tsv"), stringsAsFactors=FALSE)
pm <- read.delim(file.path(I, "peak_metadata.tsv"), row.names=1)
pos <- function(x, i) as.numeric(sapply(strsplit(x, "_"), `[`, i)); ch <- function(x) sub("_.*", "", x)
cat("strong rows:", nrow(s), " cols:", paste(colnames(s), collapse=","), "\n")
chk("columns Peak1,Peak2,coaccess", identical(colnames(s), c("Peak1","Peak2","coaccess")))
chk("all anchors are input peak names", all(c(s$Peak1, s$Peak2) %in% rownames(pm)))
chk("unordered unique pairs, one row each", !any(duplicated(paste(pmin(s$Peak1,s$Peak2), pmax(s$Peak1,s$Peak2)))) && all(s$Peak1 < s$Peak2))
chk("scores in (0.25, 1]", all(s$coaccess > 0.25 & s$coaccess <= 1), sprintf("%.3f..%.3f", min(s$coaccess), max(s$coaccess)))
chk("no cross-chromosome pairs", all(ch(s$Peak1) == ch(s$Peak2)))
chk("expected chromosomes contribute strong pairs", setequal(unique(ch(s$Peak1)), exp_chr), paste(names(table(ch(s$Peak1))), table(ch(s$Peak1)), collapse=" "))
span <- abs(pos(s$Peak1,2) - pos(s$Peak2,2)); chk("start-to-start span within default 500 kb window", max(span) <= 5e5, sprintf("max %.0f, median %.0f", max(span), median(span)))
e <- read.csv(file.path(D, "cicero_enhancer_gene_pairs.csv"), stringsAsFactors=FALSE)
chk("CSV schema", identical(colnames(e), c("enhancer","gene","coaccess","enhancer_is_promoter")), paste(colnames(e), collapse=","))
chk("enhancer values are peak names (COACC-002)", all(e$enhancer %in% rownames(pm)) && !any(grepl("^[0-9]+$", e$enhancer)))
chk("no duplicate (enhancer,gene)", !any(duplicated(paste(e$enhancer, e$gene))))
# independent recomputation from the BED (chr1 only TSS): +-2 kb around TSS midpoint
tss <- read.delim(file.path(Sys.getenv("ATACDATA"), "annotation/gencode_v29_protein_coding_tss.chr1.bed"), header=FALSE)
mid <- (tss$V2 + tss$V3)/2; ts <- mid - 2000; te <- mid + 2000
hit <- function(p) { c_ <- ch(p); st <- pos(p,2)+1; en <- pos(p,3); lapply(seq_along(p), function(i) tss$V4[c_[i]=="chr1" & ts <= en[i] & te >= st[i]]) }
h1 <- hit(s$Peak1); h2 <- hit(s$Peak2)
ex <- rbind(do.call(rbind, lapply(seq_along(h1), function(i) if (length(h1[[i]])) data.frame(enhancer=s$Peak2[i], gene=h1[[i]], stringsAsFactors=FALSE))),
            do.call(rbind, lapply(seq_along(h2), function(i) if (length(h2[[i]])) data.frame(enhancer=s$Peak1[i], gene=h2[[i]], stringsAsFactors=FALSE))))
ex <- unique(ex)
chk("enhancer-gene set equals independent recomputation", setequal(paste(ex$enhancer, ex$gene), paste(e$enhancer, e$gene)), sprintf("independent %d vs csv %d", nrow(ex), nrow(e)))
# promoter flag: enhancer overlaps any TSS window
pf <- vapply(e$enhancer, function(p) length(hit(p)[[1]]) > 0, TRUE)
chk("enhancer_is_promoter flag matches independent overlap", all(pf == e$enhancer_is_promoter), sprintf("%d TRUE of %d", sum(e$enhancer_is_promoter), nrow(e)))
chk("no enhancer-gene rows on chr2/chr19 (BED is chr1-only)", all(ch(e$enhancer) == "chr1"))
# planted-biology sanity: distance decay
allc <- s; near <- span < 1e5; cat(sprintf("strong pairs <100 kb: %d, >=100 kb: %d\n", sum(near), sum(!near)))
