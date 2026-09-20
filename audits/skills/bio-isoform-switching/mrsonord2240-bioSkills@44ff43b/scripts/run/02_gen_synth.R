# SYNTHETIC data generator (planted isoform-switch truth). Everything written here is synthetic.
# 300 genes x 3 isoforms (A canonical, B = +exon P (poison in 'poison' genes, coding in others), C = skip E3)
# 12 samples: 6 x ctrl, 6 x trt.  Salmon-format quant.sf per sample.  Truth in truth_genes.tsv / truth_isoforms.tsv
set.seed(20260920)
out <- "F:/OpenScience/audits/bio-isoform-switching/run/data/synth"
dir.create(out, recursive = TRUE, showWarnings = FALSE)

nt <- c("A","C","G","T")
rand_nt <- function(n, exclude_atg = TRUE) {
  s <- paste(sample(nt, n, replace = TRUE), collapse = "")
  s
}
sense <- setdiff(apply(expand.grid(nt, nt, nt), 1, paste, collapse = ""), c("TAA","TAG","TGA","ATG"))
codons <- function(k) paste(sample(sense, k, replace = TRUE), collapse = "")
utr5 <- function(n) { repeat { s <- rand_nt(n); if (!grepl("ATG", s)) return(s) } }
utr3 <- function(n) { repeat { s <- rand_nt(n); if (!grepl("ATG", s)) return(s) } }
ubq <- "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG"  # human ubiquitin, PF00240
# back-translate with a fixed codon per aa (no stops, no ATG except Met -> put Met as ATG only at ORF start; inside domain M -> use "CTG"(L) would change the domain: keep M via ATG is fine but creates in-frame ATG)
bt <- c(A="GCT",R="CGT",N="AAT",D="GAT",C="TGT",Q="CAA",E="GAA",G="GGT",H="CAT",I="ATT",L="CTG",K="AAA",M="ATG",F="TTT",P="CCT",S="TCT",T="ACT",W="TGG",Y="TAT",V="GTT")
ubq_nt <- paste(bt[strsplit(ubq, "")[[1]]], collapse = "")  # 228 nt, 76 codons

G <- 300
gid <- sprintf("GENE%03d", 1:G)
# roles
type <- rep("null", G)
type[1:10]    <- "poison_switch"   # B (poison exon isoform) rises: 0.10 -> 0.55
type[11:20]   <- "skip_switch"     # C (skip E3, loses ubiquitin domain in these genes) rises: 0.20 -> 0.60
type[21:30]   <- "small_switch"    # ~0.06 shift A->C: below dIF 0.1
type[31:35]   <- "dge_only"        # gene total x3 in trt, proportions unchanged (DTU decoy)
type[36:40]   <- "dte_like"        # isoform A x2, others same => both DTE and small DTU (A frac 0.6->0.75)
strand <- sample(c("+","-"), G, replace = TRUE)
has_dom <- type %in% c("skip_switch")   # ubiquitin domain in E3 of skip genes
# NB: gene 41..: null; also give ubiquitin to the null half of E3 so domain-loss only expected in switching skip genes? keep: only skip_switch genes carry it

# ---- build exons in transcript order (5'->3'), per gene
mk_gene <- function(i) {
  k1 <- sample(40:90, 1); k2 <- sample(40:90, 1); kP <- 20; k3 <- if (has_dom[i]) NA else sample(30:60, 1)
  ex <- list()
  e1 <- paste0(utr5(30), "ATG", codons(k1))                       # 5'UTR 30 + ATG + k1 codons (length mult of 3)
  e2 <- codons(k2)
  eP <- if (type[i] == "poison_switch") paste0("TAA", codons(kP - 1)) else codons(kP)
  e3 <- if (has_dom[i]) paste0(codons(5), ubq_nt, codons(5)) else codons(k3)
  e4 <- paste0(codons(sample(30:60, 1)), "TAA", utr3(sample(90:250, 1)))
  list(E1 = e1, E2 = e2, P = eP, E3 = e3, E4 = e4)
}
genes <- lapply(1:G, mk_gene)
# transcripts
tx_defs <- list(A = c("E1","E2","E3","E4"), B = c("E1","E2","P","E3","E4"), C = c("E1","E2","E4"))
tx_ids <- unlist(lapply(gid, function(g) paste0(g, "_", c("A","B","C"))))
tx_seq <- setNames(character(length(tx_ids)), tx_ids)
gtf <- character()
pos <- 1000L
for (i in 1:G) {
  ex <- genes[[i]]
  # genomic layout in transcript order: intron gaps of 400-900
  starts <- list(); cur <- pos
  ord <- c("E1","E2","P","E3","E4")
  coords <- list()
  for (e in ord) { L <- nchar(ex[[e]]); coords[[e]] <- c(cur, cur + L - 1L); cur <- cur + L + sample(400:900, 1) }
  pos <- cur + 2000L
  if (strand[i] == "-") {  # mirror: transcript-order exon1 at highest coordinate
    tot <- max(unlist(coords)) + min(unlist(coords))
    coords <- lapply(coords, function(cc) sort(tot - cc))
  }
  for (t in names(tx_defs)) {
    tid <- paste0(gid[i], "_", t)
    tx_seq[tid] <- paste(unlist(ex[tx_defs[[t]]]), collapse = "")
    for (e in tx_defs[[t]]) {
      cc <- coords[[e]]
      gtf <- c(gtf, sprintf('chr1\tsynth\texon\t%d\t%d\t.\t%s\t.\tgene_id "%s"; transcript_id "%s"; gene_name "%s";', cc[1], cc[2], strand[i], gid[i], tid, gid[i]))
    }
  }
}
# GTF must be sorted? ISAR doesn't require. write
writeLines(gtf, file.path(out, "annotation.gtf"))
fa <- unlist(lapply(tx_ids, function(t) c(paste0(">", t), tx_seq[[t]])))
writeLines(fa, file.path(out, "transcripts.fa"))
tlen <- nchar(tx_seq)

# ---- proportions per gene per condition
base <- t(sapply(1:G, function(i) { a <- rgamma(3, c(6, 1, 3)); a / sum(a) }))
colnames(base) <- c("A","B","C")
base[type == "poison_switch", ] <- matrix(c(0.60, 0.10, 0.30), sum(type == "poison_switch"), 3, byrow = TRUE)
base[type == "skip_switch", ]   <- matrix(c(0.60, 0.20, 0.20), sum(type == "skip_switch"), 3, byrow = TRUE)
base[type == "small_switch", ]  <- matrix(c(0.60, 0.10, 0.30), sum(type == "small_switch"), 3, byrow = TRUE)
base[type == "dte_like", ]      <- matrix(c(0.60, 0.10, 0.30), sum(type == "dte_like"), 3, byrow = TRUE)
alt <- base
alt[type == "poison_switch", ] <- matrix(c(0.25, 0.55, 0.20), sum(type == "poison_switch"), 3, byrow = TRUE)
alt[type == "skip_switch", ]   <- matrix(c(0.20, 0.20, 0.60), sum(type == "skip_switch"), 3, byrow = TRUE)
alt[type == "small_switch", ]  <- matrix(c(0.54, 0.10, 0.36), sum(type == "small_switch"), 3, byrow = TRUE)
alt[type == "dte_like", ]      <- matrix(c(0.75, 0.0833, 0.1667), sum(type == "dte_like"), 3, byrow = TRUE)
gene_mu <- exp(rnorm(G, 6.7, 0.5))   # ~ 800 mean reads per gene per 1x library
gene_mult_trt <- rep(1, G); gene_mult_trt[type == "dge_only"] <- 3; gene_mult_trt[type == "dte_like"] <- 1.25

samples <- data.frame(sampleID = sprintf("%s_%d", rep(c("ctrl","trt"), each = 6), rep(1:6, 2)),
                      condition = rep(c("control","treatment"), each = 6),
                      batch = rep(c("b1","b2"), 6))
lib <- exp(rnorm(12, 0, 0.15))
conc <- 60  # Dirichlet concentration (biological overdispersion)
rdirich <- function(a) { g <- rgamma(length(a), a); g / sum(g) }
cnt <- matrix(0, length(tx_ids), 12, dimnames = list(tx_ids, samples$sampleID))
for (j in 1:12) for (i in 1:G) {
  p0 <- if (samples$condition[j] == "treatment") alt[i, ] else base[i, ]
  mu <- gene_mu[i] * lib[j] * (if (samples$condition[j] == "treatment") gene_mult_trt[i] else 1)
  ptot <- rdirich(conc * p0)
  n <- rnbinom(1, mu = mu, size = 30)
  cnt[paste0(gid[i], "_", c("A","B","C")), j] <- as.vector(rmultinom(1, n, ptot))
}
# write Salmon-format quant.sf
efflen <- pmax(tlen - 74, 20)        # effective length ~ length - mean frag
dir.create(file.path(out, "salmon_quant"), showWarnings = FALSE)
for (j in 1:12) {
  d <- file.path(out, "salmon_quant", samples$sampleID[j]); dir.create(d, showWarnings = FALSE)
  n <- cnt[, j]; rpk <- n / efflen; tpm <- rpk / sum(rpk) * 1e6
  write.table(data.frame(Name = tx_ids, Length = tlen, EffectiveLength = efflen, TPM = tpm, NumReads = n),
              file.path(d, "quant.sf"), sep = "\t", quote = FALSE, row.names = FALSE)
}
write.table(samples, file.path(out, "samples.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
# truth
truth_g <- data.frame(gene_id = gid, type = type, strand = strand,
                      IF_A_ctrl = base[,1], IF_B_ctrl = base[,2], IF_C_ctrl = base[,3],
                      IF_A_trt = alt[,1], IF_B_trt = alt[,2], IF_C_trt = alt[,3])
truth_g$true_max_abs_dIF <- pmax(abs(alt[,1]-base[,1]), abs(alt[,2]-base[,2]), abs(alt[,3]-base[,3]))
truth_g$true_switch <- type %in% c("poison_switch","skip_switch")   # planted switches that must be called (dIF>=0.35)
write.table(truth_g, file.path(out, "truth_genes.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(data.frame(tx = tx_ids, length = tlen), file.path(out, "truth_isoforms.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat("SYNTHETIC data written:", out, "\n")
cat("transcripts:", length(tx_ids), " genes:", G, "\n")
print(table(type))
cat("gene-level counts range (sum over iso, ctrl_1):", range(tapply(cnt[,1], rep(gid, each = 3), sum)), "\n")
