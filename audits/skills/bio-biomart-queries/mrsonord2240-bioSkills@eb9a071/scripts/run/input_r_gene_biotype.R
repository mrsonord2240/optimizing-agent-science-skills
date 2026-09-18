# R attempt to verify the P1 gene_biotype fix live via biomaRt (block_7, SKILL.md's
# R pattern, extended with the coordinate-table attributes so it also exercises
# gene_biotype directly, matching the Python-side Input 2 test). The fixer's own log
# says this could not be confirmed live in 3 attempts and was verified by schema
# equivalence instead -- this re-audit tries again independently rather than accepting
# that claim on faith.
suppressMessages(library(biomaRt))
cat("biomaRt version:", as.character(packageVersion("biomaRt")), "\n")

try_query <- function(label, expr) {
  cat("\n---", label, "---\n")
  val <- tryCatch(expr, error = function(e) {
    cat("FAILED:", conditionMessage(e), "\n")
    NULL
  })
  if (!is.null(val)) {
    cat("SUCCESS (class:", paste(class(val), collapse=","), ")\n")
    # Only try to preview data-frame-like results; an S4 Mart object isn't
    # subsettable via head() and that must not be mistaken for a failure.
    if (is.data.frame(val)) {
      print(head(val))
    }
  }
  val
}

ensembl <- try_query("useEnsembl(version=110)", {
  useEnsembl(biomart = "genes", dataset = "hsapiens_gene_ensembl", version = 110)
})

if (is.null(ensembl)) {
  ensembl <- try_query("useEnsembl() current release, no version pin", {
    useEnsembl(biomart = "genes", dataset = "hsapiens_gene_ensembl")
  })
}

if (is.null(ensembl)) {
  ensembl <- try_query("useMart() archive host directly", {
    useMart("ENSEMBL_MART_ENSEMBL", dataset = "hsapiens_gene_ensembl",
            host = "https://jun2026.archive.ensembl.org")
  })
}

if (!is.null(ensembl)) {
  coord_df <- try_query("getBM gene_biotype attribute, chr17 protein_coding (block_7-style)", {
    getBM(
      attributes = c("ensembl_gene_id", "external_gene_name", "chromosome_name", "gene_biotype"),
      filters = c("chromosome_name", "biotype"),
      values = list("17", "protein_coding"),
      mart = ensembl
    )
  })
  if (!is.null(coord_df)) {
    cat("\nRows:", nrow(coord_df), "\n")
    cat("gene_biotype values seen:", paste(unique(coord_df$gene_biotype), collapse=", "), "\n")
  }
} else {
  cat("\nALL useEnsembl/useMart CONNECTION ATTEMPTS FAILED -- cannot test gene_biotype live from R this session.\n")
}
