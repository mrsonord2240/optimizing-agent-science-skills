# Smoke: chromVAR deviations equal a hand computation; motifmatchr recovers a planted motif; JASPAR2024 loads.
suppressPackageStartupMessages({
  library(chromVAR); library(motifmatchr); library(SummarizedExperiment); library(GenomicRanges)
  library(TFBSTools); library(JASPAR2024); library(RSQLite); library(BSgenome.Hsapiens.UCSC.hg38); library(Matrix)
})
chk <- function(name, ok, val) { cat(sprintf("%s %-52s %s\n", if (ok) "PASS" else "FAIL", name, val)); if (!ok) quit(status = 1) }

# ---- 1. chromVAR: computeDeviations vs hand computation --------------------------------------
set.seed(1)
np <- 40; ns <- 6
counts <- matrix(rpois(np * ns, lambda = 30), np, ns, dimnames = list(paste0("p", 1:np), paste0("s", 1:ns)))
counts[1:5, 4:6] <- counts[1:5, 4:6] + 60L      # planted: annotation peaks 1:5 open up in samples 4-6
rr <- GRanges("chr1", IRanges(start = seq(1000, by = 1000, length.out = np), width = 500))
se <- SummarizedExperiment(assays = list(counts = counts), rowRanges = rr)
ann <- matrix(FALSE, np, 1, dimnames = list(NULL, "planted")); ann[1:5, 1] <- TRUE
annSE <- SummarizedExperiment(assays = list(motifMatches = Matrix(ann, sparse = TRUE)), rowRanges = rr)
# 3 fixed background sets (5 peaks each; no sampling, so the result is exactly checkable)
bg <- cbind(1:np, 1:np, 1:np)                    # background_peaks is peaks x iterations (row i = substitutes for peak i)
bg[1:5, ] <- cbind(6:10, 11:15, 16:20)          # so background sets for annotation peaks 1:5 are 6:10, 11:15, 16:20
dev <- computeDeviations(object = se, annotations = annSE, background_peaks = bg)
z <- assay(dev, "z"); d <- assay(dev, "deviations")
raw <- function(idx) {                     # (observed - expected)/expected as in Schep 2017
  cij <- counts; expct <- (rowSums(cij) / sum(cij)) %o% colSums(cij)
  (colSums(cij[idx, , drop = FALSE]) - colSums(expct[idx, , drop = FALSE])) / colSums(expct[idx, , drop = FALSE])
}
r_obs <- raw(1:5); r_bg <- sapply(1:3, function(k) raw(bg[1:5, k]))       # samples x 3
d_hand <- r_obs - rowMeans(r_bg)
z_hand <- d_hand / apply(r_bg, 1, sd)
chk("chromVAR deviations == hand computation (1e-8)", isTRUE(all.equal(as.numeric(d), as.numeric(d_hand), tolerance = 1e-8)),
    sprintf("max|diff| = %.2e", max(abs(as.numeric(d) - d_hand))))
chk("chromVAR z-scores == hand computation (1e-8)", isTRUE(all.equal(as.numeric(z), as.numeric(z_hand), tolerance = 1e-8)),
    sprintf("z(s1)=%.4f z(s4)=%.4f", z[1, 1], z[1, 4]))
chk("planted signal: mean z(s4-6) > mean z(s1-3) by > 3", mean(z[1, 4:6]) - mean(z[1, 1:3]) > 3, sprintf("%.2f", mean(z[1, 4:6]) - mean(z[1, 1:3])))
cat(sprintf("INFO chromVAR %s, motifmatchr %s\n", packageVersion("chromVAR"), packageVersion("motifmatchr")))

# ---- 2. motifmatchr: planted CTCF motif is found -----------------------------------------------
jaspar <- JASPAR2024()
sq <- dbConnect(SQLite(), db(jaspar))
pfm <- getMatrixSet(sq, opts = list(collection = "CORE", tax_group = "vertebrates", matrixtype = "PFM"))
chk("JASPAR2024 CORE vertebrates PFMs loaded (>=879)", length(pfm) >= 879, length(pfm))
ctcf <- getMatrixSet(sq, opts = list(ID = "MA0139.1"))
pm <- TFBSTools::Matrix(ctcf[[1]])     # TFBSTools::Matrix, not Matrix::Matrix (masked by library(Matrix))
cons <- paste(sapply(1:ncol(pm), function(i) c("A", "C", "G", "T")[which.max(pm[, i])]), collapse = "")
cat("INFO MA0139.1 consensus:", cons, "\n")
genome <- BSgenome.Hsapiens.UCSC.hg38
peaks <- GRanges("chr1", IRanges(c(1e6, 2e6, 3e6), width = 300))
seqs <- getSeq(genome, peaks)
ins <- DNAStringSet(c(paste0(as.character(subseq(seqs[[1]], 1, 100)), cons, as.character(subseq(seqs[[1]], 100 + nchar(cons) + 1, 300))),
                      as.character(seqs[[2]]), as.character(seqs[[3]])))
mm <- matchMotifs(ctcf, ins, out = "matches", p.cutoff = 1e-5)
hit <- as.matrix(motifMatches(mm))
chk("motifmatchr finds planted CTCF consensus in seq 1", hit[1, 1], paste(hit[, 1], collapse = ","))
cat("R smoke chromVAR/motifmatchr: ALL PASS\n")
