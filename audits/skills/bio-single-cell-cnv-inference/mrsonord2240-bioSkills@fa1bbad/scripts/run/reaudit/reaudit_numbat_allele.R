# RE-AUDIT (2026-09-19): independently verify the Numbat df_allele column
# fix. Build a df_allele with EXACTLY the 7 columns the PRE-FIX SKILL.md
# documented (cell, snp_id, CHROM, POS, AD, DP, GT) -- deliberately omitting
# cM, REF, ALT -- and pass it to numbat's own internal validator,
# check_allele_df(), to see whether the real error text names those three
# columns as required, matching what the fix now documents.
suppressMessages(library(numbat))

set.seed(20260919)
n <- 20
df_allele_incomplete <- data.frame(
    cell   = paste0("cell_", rep(1:5, each = 4)),
    snp_id = paste0("snp_", 1:n),
    CHROM  = rep(1:5, each = 4),
    POS    = sample(1e6:2e6, n),
    AD     = sample(0:10, n, replace = TRUE),
    DP     = sample(10:30, n, replace = TRUE),
    GT     = sample(c("0|1", "1|0", "1|1"), n, replace = TRUE)
)

cat("=== columns in the deliberately-incomplete df_allele (pre-fix docs' 7) ===\n")
print(colnames(df_allele_incomplete))

cat("\n=== calling numbat:::check_allele_df() on it ===\n")
result <- tryCatch({
    numbat:::check_allele_df(df_allele_incomplete)
    "NO ERROR (validation passed)"
}, error = function(e) {
    paste("ERROR:", conditionMessage(e))
})
cat(result, "\n")

# Now build the FULL 10-column df_allele (post-fix docs) and confirm it
# clears the same check.
df_allele_complete <- df_allele_incomplete
df_allele_complete$cM  <- runif(n, 0, 50)
df_allele_complete$REF <- sample(c("A", "C", "G", "T"), n, replace = TRUE)
df_allele_complete$ALT <- sample(c("A", "C", "G", "T"), n, replace = TRUE)

cat("\n=== calling numbat:::check_allele_df() on the FULL 10-column version ===\n")
result2 <- tryCatch({
    numbat:::check_allele_df(df_allele_complete)
    "NO ERROR (validation passed)"
}, error = function(e) {
    paste("ERROR:", conditionMessage(e))
})
cat(result2, "\n")

cat("\nDONE: reaudit Numbat df_allele verification complete\n")
