# Input 7 -- Adversarial: exercise the harmonise() function that the redundancy pass
# moved from usage-guide.md into SKILL.md's "Allele Harmonisation (Critical Pre-Step)"
# section, verifying it still works correctly after the move (flip + palindromic +
# drop-mismatched-SNP logic) and testing an adversarial case: a SNP that matches
# neither 'same' nor 'flip' coding (should be dropped, not silently mis-flipped).

harmonise <- function(df1, df2) {
    m <- merge(df1, df2, by='SNP', suffixes=c('.1','.2'))
    same <- m$A1.1 == m$A1.2 & m$A2.1 == m$A2.2
    flip <- m$A1.1 == m$A2.2 & m$A2.1 == m$A1.2
    palindromic <- (m$A1.1 %in% c('A','T') & m$A2.1 %in% c('A','T')) |
                   (m$A1.1 %in% c('C','G') & m$A2.1 %in% c('C','G'))
    m$BETA.2[flip] <- -m$BETA.2[flip]
    m$MAF.2[flip] <- 1 - m$MAF.2[flip]
    keep <- (same | flip) & !(palindromic & m$MAF.1 > 0.42)
    m[keep, ]
}

df1 <- data.frame(
  SNP  = c('rs1', 'rs2', 'rs3', 'rs4', 'rs5', 'rs6'),
  A1   = c('A',   'A',   'A',   'A',   'C',   'T'),
  A2   = c('G',   'G',   'G',   'G',   'G',   'A'),
  BETA = c(0.5,  -0.3,   0.2,   0.4,   0.10,  0.15),
  MAF  = c(0.30,  0.20,  0.25,  0.35,  0.45,  0.10)
)
df2 <- data.frame(
  SNP  = c('rs1', 'rs2', 'rs3', 'rs4', 'rs5', 'rs6'),
  A1   = c('A',   'G',   'C',   'T',   'C',   'A'),   # rs1 same-coded; rs2 flip-coded (A/G<->G/A);
  A2   = c('G',   'A',   'T',   'C',   'G',   'T'),   # rs3 mismatched (A/G vs C/T, no overlap at all);
  BETA = c(0.55, -0.28,  0.10,  0.42,  0.11,  0.16),  # rs4 STRAND-FLIP not order-swap (A/G complement is T/C);
  MAF  = c(0.31,  0.79,  0.40,  0.66,  0.44,  0.09)   # rs5 palindromic C/G at MAF>0.42 (drop); rs6 palindromic A/T, MAF<=0.42 (keep, flip)
)

res <- harmonise(df1, df2)
cat('Harmonised rows kept:', paste(res$SNP, collapse=', '), '\n')
print(res[, c('SNP','A1.1','A2.1','A1.2','A2.2','BETA.1','BETA.2')])

# rs4 (A/G in df1, complement-strand T/C in df2) is NEITHER a literal order-swap
# (flip: A1.1==A2.2 & A2.1==A1.2 -> 'A'=='C' & 'G'=='T' -> FALSE) NOR same-coded,
# so the documented harmonise() correctly drops it under its own definition of
# 'flip' -- but this exposes a real, previously-unflagged gap: harmonise() has no
# strand-complement-flip branch, so any genuinely strand-mismatched (non-palindromic)
# SNP pair is silently dropped as if it were a hard allele mismatch, and none of the
# "Harmonisation pitfalls to watch for" bullets warn about this specific case (they
# cover build mismatch and palindromic-at-high-MAF, not general non-palindromic
# strand mismatch). Expectation corrected to match the function's actual documented
# logic, not an assumption that it does full strand-complement resolution.
expect_kept   <- c('rs1', 'rs2', 'rs6')
expect_dropped <- c('rs3', 'rs4', 'rs5')
cat('\nExpect kept:  ', paste(expect_kept, collapse=', '), '\n')
cat('Expect dropped:', paste(expect_dropped, collapse=', '), '\n')
ok_kept <- setequal(res$SNP, expect_kept)
cat(sprintf('\nASSERTION [kept set matches expectation]: %s\n', ifelse(ok_kept, 'PASS', 'FAIL')))

# rs2 should have been flipped: original df2 BETA.2 = -0.28 -> should become +0.28 after flip
rs2_row <- res[res$SNP == 'rs2', ]
flip_ok <- isTRUE(all.equal(rs2_row$BETA.2, 0.28))
cat(sprintf('ASSERTION [rs2 flip-coded SNP has beta sign correctly negated, -0.28 -> 0.28]: %s (got %.3f)\n',
            ifelse(flip_ok, 'PASS', 'FAIL'), rs2_row$BETA.2))

# rs6 (palindromic A/T, MAF<=0.42) should be KEPT and flip-corrected (A1.1='T' vs A1.2='A' is a flip)
rs6_row <- res[res$SNP == 'rs6', ]
rs6_ok <- nrow(rs6_row) == 1 && isTRUE(all.equal(rs6_row$BETA.2, -0.16))
cat(sprintf('ASSERTION [rs6 palindromic-but-low-MAF SNP kept and flip-corrected]: %s\n', ifelse(rs6_ok, 'PASS', 'FAIL')))

# rs3 (df1 = A/G, df2 = C/T, no A1/A2 overlap at all) must be dropped, not silently mis-flipped
rs3_dropped <- !('rs3' %in% res$SNP)
cat(sprintf('ASSERTION [rs3, allele-mismatched SNP with no A1/A2 overlap, is dropped not silently mis-flipped]: %s\n',
            ifelse(rs3_dropped, 'PASS', 'FAIL')))

# rs4 (df1 = A/G, df2 = T/C, i.e. the COMPLEMENT strand of A/G, non-palindromic) is dropped
# by harmonise()'s literal same/flip logic -- confirming a real, previously-unflagged limitation:
# no strand-complement resolution branch, and no pitfall bullet warns about it.
rs4_dropped <- !('rs4' %in% res$SNP)
cat(sprintf('FINDING [rs4, non-palindromic strand-complement mismatch (A/G vs T/C), silently dropped -- no strand-flip resolution, no pitfall callout]: %s\n',
            ifelse(rs4_dropped, 'CONFIRMED', 'NOT REPRODUCED')))
