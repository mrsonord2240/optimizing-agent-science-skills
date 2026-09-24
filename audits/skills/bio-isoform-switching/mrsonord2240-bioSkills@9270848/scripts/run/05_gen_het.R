# NEW SYNTHETIC generator (this audit's own; not used by earlier auditors): planted truth + INDIVIDUAL-LEVEL heterogeneity.
# Purpose: reproduce, under known truth, the real-chrX observation that label-shuffled small designs are called (subject-level isoform variation the
# small-n dispersion estimate does not absorb), and see how many replicates it takes for the Skill's raw-count route to stop calling them.
# Usage: Rscript 05_gen_het.R <outdir> <seed> <n_ctrl> <n_trt> <planted 0|1> <hetfrac> <idstyle srr|odd>
# 250 genes x 3 isoforms (A canonical; B = A + exon P; C = A minus E3; log-uniform exon sizes). If planted: genes 1-10 poison (B 0.12 -> 0.45), 11-20 skip
# (C 0.20 -> 0.55). In a random hetfrac of the null genes ("het" genes) every SAMPLE carries its own multiplicative shift of the isoform proportions
# (lognormal sd 0.6), i.e. individual-level variation on top of Dirichlet noise; het genes are NOT related to condition.
args <- commandArgs(trailingOnly = TRUE); out <- args[1]; seed <- as.integer(args[2]); nC <- as.integer(args[3]); nT <- as.integer(args[4])
planted <- args[5] == "1"; hetfrac <- as.numeric(args[6]); idstyle <- args[7]
set.seed(seed); unlink(out, recursive = TRUE); dir.create(file.path(out, "salmon_quant"), recursive = TRUE)
nt <- c("A", "C", "G", "T"); sense <- setdiff(apply(expand.grid(nt, nt, nt), 1, paste, collapse = ""), c("TAA", "TAG", "TGA", "ATG"))
codons <- function(k) paste(sample(sense, k, replace = TRUE), collapse = "")
utr <- function(n) repeat { s <- paste(sample(nt, n, replace = TRUE), collapse = ""); if (!grepl("ATG", s)) return(s) }
lu <- function(a, b) round(exp(runif(1, log(a), log(b))))
G <- 250; gid <- sprintf("HET%03d", 1:G); type <- rep("null", G)
if (planted) { type[1:10] <- "poison_switch"; type[11:20] <- "skip_switch" }
nulls <- which(type == "null"); het <- sort(sample(nulls, round(hetfrac * length(nulls)))); is_het <- seq_len(G) %in% het
strand <- sample(c("+", "-"), G, replace = TRUE)
tx_ids <- unlist(lapply(gid, function(g) paste0(g, "_", c("A", "B", "C")))); tx_seq <- setNames(character(length(tx_ids)), tx_ids); gtf <- character(); pos <- 1000L
defs <- list(A = c("E1", "E2", "E3", "E4"), B = c("E1", "E2", "P", "E3", "E4"), C = c("E1", "E2", "E4"))
for (i in 1:G) {
  ex <- list(E1 = paste0(utr(30), "ATG", codons(lu(30, 300))), E2 = codons(lu(30, 300)),
             P = if (type[i] == "poison_switch") paste0("TAA", codons(lu(15, 200))) else codons(lu(15, 200)),
             E3 = codons(lu(20, 500)), E4 = paste0(codons(lu(30, 250)), "TAA", utr(lu(90, 300))))
  cur <- pos; coords <- list(); for (e in c("E1", "E2", "P", "E3", "E4")) { L <- nchar(ex[[e]]); coords[[e]] <- c(cur, cur + L - 1L); cur <- cur + L + sample(400:900, 1) }
  pos <- cur + 2000L
  if (strand[i] == "-") { tot <- max(unlist(coords)) + min(unlist(coords)); coords <- lapply(coords, function(cc) sort(tot - cc)) }
  for (t in names(defs)) { tid <- paste0(gid[i], "_", t); tx_seq[tid] <- paste(unlist(ex[defs[[t]]]), collapse = "")
    for (e in defs[[t]]) gtf <- c(gtf, sprintf('chr1\tsynth\texon\t%d\t%d\t.\t%s\t.\tgene_id "%s"; transcript_id "%s"; gene_name "%s";', coords[[e]][1], coords[[e]][2], strand[i], gid[i], tid, gid[i])) }
}
writeLines(gtf, file.path(out, "annotation.gtf")); writeLines(unlist(lapply(tx_ids, function(t) c(paste0(">", t), tx_seq[[t]]))), file.path(out, "transcripts.fa"))
tlen <- nchar(tx_seq); efflen <- pmax(tlen - 74, 20)
base <- t(sapply(1:G, function(i) { a <- rgamma(3, c(6, 1, 3)); a / sum(a) })); alt <- base
if (planted) {
  base[type == "poison_switch", ] <- matrix(c(0.62, 0.12, 0.26), 10, 3, byrow = TRUE); alt[type == "poison_switch", ] <- matrix(c(0.30, 0.45, 0.25), 10, 3, byrow = TRUE)
  base[type == "skip_switch", ] <- matrix(c(0.55, 0.20, 0.25), 10, 3, byrow = TRUE);   alt[type == "skip_switch", ] <- matrix(c(0.25, 0.20, 0.55), 10, 3, byrow = TRUE)
}
gene_mu <- exp(rnorm(G, 7.0, 0.5)); n <- nC + nT; cond <- c(rep("control", nC), rep("treatment", nT)); lib <- exp(rnorm(n, 0, 0.2)); conc <- 45
ids <- if (idstyle == "srr") sprintf("SRR74%05d", sample(10000:99999, n)) else
  c(sprintf("%d-ctrl", 1:nC), sprintf("trt.%d-b", 1:nT))   # 'odd' IDs: leading digit, dash, dot
for (j in 1:n) {
  cnt <- numeric(0)
  for (i in 1:G) {
    p0 <- if (cond[j] == "treatment") alt[i, ] else base[i, ]
    if (is_het[i]) { p0 <- p0 * exp(rnorm(3, 0, 0.6)); p0 <- p0 / sum(p0) }
    g <- rgamma(3, conc * p0); p <- g / sum(g)
    el <- efflen[paste0(gid[i], "_", c("A", "B", "C"))]; w <- p * el; w <- w / sum(w)
    cnt <- c(cnt, as.vector(rmultinom(1, rnbinom(1, mu = gene_mu[i] * lib[j], size = 30), w)))
  }
  rpk <- cnt / efflen; d <- file.path(out, "salmon_quant", ids[j]); dir.create(d)
  write.table(data.frame(Name = tx_ids, Length = tlen, EffectiveLength = efflen, TPM = rpk / sum(rpk) * 1e6, NumReads = cnt), file.path(d, "quant.sf"), sep = "\t", quote = FALSE, row.names = FALSE)
}
meta <- data.frame(sample_id = ids, condition = cond); meta <- meta[sample(n), ]
write.table(meta, file.path(out, "sample_metadata.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
tg <- data.frame(gene_id = gid, type = type, is_het = is_het, true_switch = type %in% c("poison_switch", "skip_switch"))
write.table(tg, file.path(out, "truth_genes.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat("SYNTHETIC het set:", out, "| seed", seed, "|", nC, "v", nT, "| planted", planted, "| het genes", sum(is_het), "| ids", idstyle, "\n")
