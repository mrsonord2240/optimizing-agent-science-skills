# NEW SYNTHETIC planted-truth generator (auditor's own; different genes, effect sizes, replicate structure and HETEROGENEOUS isoform lengths from the
# regression set 02_gen_synth.R). Usage: Rscript 04_gen_new.R <outdir> <seed> <n_ctrl> <n_trt> [batch]
# 250 genes x 3 isoforms (A canonical; B = A + exon P; C = A minus E3). Exon sizes are log-uniform so isoform lengths differ up to ~10x within a gene.
# Counts are drawn proportional to (molar fraction x effective length), so the planted fractions equal the TPM-based isoform fractions ISAR reports.
# Types: 1-10 poison_switch (B 0.12 -> 0.42; B carries a premature stop), 11-20 skip_switch (C 0.25 -> 0.60; E3 carries ubiquitin), 21-30 small_switch (0.04 shift),
# 31-35 dge_only (x2.5 in trt), rest null. With 'batch': 25% of A moves to C in batch b2 in the 20 null genes GENE200-GENE219.
args <- commandArgs(trailingOnly = TRUE); out <- args[1]; seed <- as.integer(args[2]); nC <- as.integer(args[3]); nT <- as.integer(args[4]); use_batch <- length(args) >= 5 && args[5] == "batch"
set.seed(seed); unlink(out, recursive = TRUE); dir.create(file.path(out, "salmon_quant"), recursive = TRUE)
nt <- c("A", "C", "G", "T"); sense <- setdiff(apply(expand.grid(nt, nt, nt), 1, paste, collapse = ""), c("TAA", "TAG", "TGA", "ATG"))
codons <- function(k) paste(sample(sense, k, replace = TRUE), collapse = "")
utr <- function(n) repeat { s <- paste(sample(nt, n, replace = TRUE), collapse = ""); if (!grepl("ATG", s)) return(s) }
ubq <- "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG"
bt <- c(A="GCT",R="CGT",N="AAT",D="GAT",C="TGT",Q="CAA",E="GAA",G="GGT",H="CAT",I="ATT",L="CTG",K="AAA",M="ATG",F="TTT",P="CCT",S="TCT",T="ACT",W="TGG",Y="TAT",V="GTT")
ubq_nt <- paste(bt[strsplit(ubq, "")[[1]]], collapse = "")
lu <- function(a, b) round(exp(runif(1, log(a), log(b))))
G <- 250; gid <- sprintf("NEW%03d", 1:G); type <- rep("null", G)
type[1:10] <- "poison_switch"; type[11:20] <- "skip_switch"; type[21:30] <- "small_switch"; type[31:35] <- "dge_only"
strand <- sample(c("+", "-"), G, replace = TRUE)
tx_ids <- unlist(lapply(gid, function(g) paste0(g, "_", c("A", "B", "C")))); tx_seq <- setNames(character(length(tx_ids)), tx_ids); gtf <- character(); pos <- 1000L
defs <- list(A = c("E1", "E2", "E3", "E4"), B = c("E1", "E2", "P", "E3", "E4"), C = c("E1", "E2", "E4"))
for (i in 1:G) {
  e3 <- if (type[i] == "skip_switch") paste0(codons(5), ubq_nt, codons(lu(5, 400))) else codons(lu(20, 800))
  ex <- list(E1 = paste0(utr(30), "ATG", codons(lu(30, 400))), E2 = codons(lu(30, 400)),
             P = if (type[i] == "poison_switch") paste0("TAA", codons(lu(15, 300))) else codons(lu(15, 300)),
             E3 = e3, E4 = paste0(codons(lu(30, 300)), "TAA", utr(lu(90, 400))))
  cur <- pos; coords <- list(); for (e in c("E1", "E2", "P", "E3", "E4")) { L <- nchar(ex[[e]]); coords[[e]] <- c(cur, cur + L - 1L); cur <- cur + L + sample(400:900, 1) }
  pos <- cur + 2000L
  if (strand[i] == "-") { tot <- max(unlist(coords)) + min(unlist(coords)); coords <- lapply(coords, function(cc) sort(tot - cc)) }
  for (t in names(defs)) { tid <- paste0(gid[i], "_", t); tx_seq[tid] <- paste(unlist(ex[defs[[t]]]), collapse = "")
    for (e in defs[[t]]) gtf <- c(gtf, sprintf('chr1\tsynth\texon\t%d\t%d\t.\t%s\t.\tgene_id "%s"; transcript_id "%s"; gene_name "%s";', coords[[e]][1], coords[[e]][2], strand[i], gid[i], tid, gid[i])) }
}
writeLines(gtf, file.path(out, "annotation.gtf")); writeLines(unlist(lapply(tx_ids, function(t) c(paste0(">", t), tx_seq[[t]]))), file.path(out, "transcripts.fa"))
tlen <- nchar(tx_seq); efflen <- pmax(tlen - 74, 20)
base <- t(sapply(1:G, function(i) { a <- rgamma(3, c(6, 1, 3)); a / sum(a) })); alt <- base
base[type == "poison_switch", ] <- matrix(c(0.62, 0.12, 0.26), 10, 3, byrow = TRUE); alt[type == "poison_switch", ] <- matrix(c(0.33, 0.42, 0.25), 10, 3, byrow = TRUE)
base[type == "skip_switch", ] <- matrix(c(0.55, 0.20, 0.25), 10, 3, byrow = TRUE);   alt[type == "skip_switch", ] <- matrix(c(0.25, 0.15, 0.60), 10, 3, byrow = TRUE)
base[type == "small_switch", ] <- matrix(c(0.60, 0.10, 0.30), 10, 3, byrow = TRUE);  alt[type == "small_switch", ] <- matrix(c(0.56, 0.10, 0.34), 10, 3, byrow = TRUE)
alt[!type %in% c("poison_switch", "skip_switch", "small_switch"), ] <- base[!type %in% c("poison_switch", "skip_switch", "small_switch"), ]
gene_mu <- exp(rnorm(G, 7.0, 0.5)); mult_trt <- ifelse(type == "dge_only", 2.5, 1)
n <- nC + nT; cond <- c(rep("control", nC), rep("treatment", nT))
batch <- if (nC == 4 && nT == 7) c("b1", "b1", "b2", "b1", "b2", "b2", "b1", "b2", "b2", "b1", "b2") else rep(c("b1", "b2"), length.out = n)
ids <- sprintf("SRR73%05d", sample(10000:99999, n)); lib <- exp(rnorm(n, 0, 0.2)); conc <- 45
bg <- sprintf("NEW%03d", 200:219)
for (j in 1:n) {
  cnt <- numeric(0)
  for (i in 1:G) {
    p0 <- if (cond[j] == "treatment") alt[i, ] else base[i, ]
    if (use_batch && batch[j] == "b2" && gid[i] %in% bg) p0 <- c(p0[1] * 0.75, p0[2], p0[3] + p0[1] * 0.25)
    g <- rgamma(3, conc * p0); p <- g / sum(g)
    el <- efflen[paste0(gid[i], "_", c("A", "B", "C"))]; w <- p * el; w <- w / sum(w)
    cnt <- c(cnt, as.vector(rmultinom(1, rnbinom(1, mu = gene_mu[i] * lib[j] * (if (cond[j] == "treatment") mult_trt[i] else 1), size = 30), w)))
  }
  rpk <- cnt / efflen; d <- file.path(out, "salmon_quant", ids[j]); dir.create(d)
  write.table(data.frame(Name = tx_ids, Length = tlen, EffectiveLength = efflen, TPM = rpk / sum(rpk) * 1e6, NumReads = cnt), file.path(d, "quant.sf"), sep = "\t", quote = FALSE, row.names = FALSE)
}
meta <- data.frame(sample_id = ids, condition = cond, batch = batch); meta <- meta[sample(n), ]
write.table(meta, file.path(out, "sample_metadata.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
tg <- data.frame(gene_id = gid, type = type, strand = strand, IF_A_ctrl = base[, 1], IF_B_ctrl = base[, 2], IF_C_ctrl = base[, 3], IF_A_trt = alt[, 1], IF_B_trt = alt[, 2], IF_C_trt = alt[, 3])
tg$true_switch <- type %in% c("poison_switch", "skip_switch"); tg$is_batch_gene <- gid %in% bg
write.table(tg, file.path(out, "truth_genes.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(data.frame(tx = tx_ids, length = tlen), file.path(out, "truth_isoforms.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat("SYNTHETIC set written:", out, "| seed", seed, "|", nC, "v", nT, "| batch effect", use_batch, "\n")
cat("isoform length ratio within gene (max/min) quantiles:", paste(round(quantile(tapply(tlen, rep(1:G, each = 3), function(x) max(x) / min(x)), c(0.1, 0.5, 0.9)), 2), collapse = " / "), "\n")
cat("transcript length range:", paste(range(tlen), collapse = "-"), "\n"); print(table(type))
