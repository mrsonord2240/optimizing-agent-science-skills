# Audit run: reproduce the enhancer-gene table step of scripts/cicero_workflow.R verbatim and compare with the CSV the shipped function wrote
suppressPackageStartupMessages({library(GenomicRanges); library(rtracklayer)})
CO <- Sys.getenv("CO"); r <- readRDS(file.path(CO, "work/chr1/res_chr1.rds")); strong <- r$strong
csv <- read.csv(file.path(CO, "work/chr1/ex_chr1_enhancer_gene_pairs.csv"), colClasses="character")
tss <- import(file.path(CO, "work/patched/gencode_v29_protein_coding_tss.bed")); tss_extended <- resize(tss, width=2*2000, fix='center')
peak1 <- GRanges(sub('_(\\d+)_(\\d+)$', ':\\1-\\2', strong$Peak1)); peak2 <- GRanges(sub('_(\\d+)_(\\d+)$', ':\\1-\\2', strong$Peak2))
ov1 <- findOverlaps(peak1, tss_extended); ov2 <- findOverlaps(peak2, tss_extended)
eg <- data.frame(enhancer = c(strong$Peak2[queryHits(ov1)], strong$Peak1[queryHits(ov2)]),
   gene = c(tss_extended$name[subjectHits(ov1)], tss_extended$name[subjectHits(ov2)]),
   coaccess = c(strong$coaccess[queryHits(ov1)], strong$coaccess[queryHits(ov2)]))
cat("rows before unique:", nrow(eg), " after unique:", nrow(unique(eg)), " csv rows:", nrow(csv), "\n")
cat("class(strong$Peak1)=", class(strong$Peak1), " class(strong$Peak2)=", class(strong$Peak2), "\n")
cat("enhancer col class:", class(eg$enhancer), "\n")
n1 <- length(queryHits(ov1)); n2 <- length(queryHits(ov2))
cat(sprintf("first block (from Peak2, factor) n=%d, second block (from Peak1, character) n=%d\n", n1, n2))
e <- as.character(eg$enhancer)
cat("first-block values (head):", head(e[seq_len(n1)], 6), "| second-block values (head):", head(e[n1 + seq_len(n2)], 3), "\n")
cat("first-block all integer-like codes:", all(grepl("^[0-9]+$", e[seq_len(n1)])), "; second-block all peak-name strings:", all(grepl("^chr", e[n1 + seq_len(n2)])), "\n")
cat("csv fraction of numeric-only enhancer values:", round(mean(grepl("^[0-9]+$", csv$enhancer)), 3), "\n")
u <- unique(eg)
cat("identical to shipped CSV (enhancer,gene):", identical(paste(u$enhancer, u$gene), paste(csv$enhancer, csv$gene)), "\n")
lev <- levels(strong$Peak2); codes <- csv$enhancer[grepl("^[0-9]+$", csv$enhancer)]
cat("first 3 codes map to peak names via levels(Peak2):", head(lev[as.integer(head(codes, 3))], 3), "\n")
# how many distinct real peaks are hidden behind codes, and does any code collide with a legitimate string value?
cat("distinct integer codes in csv:", length(unique(codes)), "\n")
