# Input 4 -- Variant B: regression + extension test of flag_excluded_region()
# (P1 fix: MHC/chr8-inversion exclusion enforced only by prose before this fix)
# Extracted verbatim from SKILL.md's "Standard coloc.abf Pipeline" code block.

flag_excluded_region <- function(chr, pos_bp, build = 'hg38') {
  if (build != 'hg38') stop('flag_excluded_region: liftover to hg38 first -- this Skill only documents hg38 MHC / chr8 inversion boundaries')
  chr <- gsub('^chr', '', as.character(chr))
  if (chr == '6' && pos_bp >= 25000000 && pos_bp <= 35000000) return('MHC')
  if (chr == '8' && pos_bp >= 8100000  && pos_bp <= 11900000) return('chr8_inversion')
  NA_character_
}

cases <- list(
  list(label = "chr6:30450000 (fixer's own MHC test locus)",           chr = 6,    pos = 30450000, build = 'hg38', expect = 'MHC'),
  list(label = "chr8:9000000 (fixer's own inversion test locus)",       chr = 8,    pos = 9000000,  build = 'hg38', expect = 'chr8_inversion'),
  list(label = "chr1:1000000 (fixer's own negative control)",           chr = 1,    pos = 1000000,  build = 'hg38', expect = NA_character_),
  list(label = "chr6:24000000 (fixer's own just-outside-MHC case)",     chr = 6,    pos = 24000000, build = 'hg38', expect = NA_character_),
  # New cases not in the fix log -- boundary edges and chr-prefix / string-vs-numeric robustness
  list(label = "chr6:25000000 (exact MHC lower boundary, inclusive)",   chr = 6,    pos = 25000000, build = 'hg38', expect = 'MHC'),
  list(label = "chr6:35000000 (exact MHC upper boundary, inclusive)",   chr = 6,    pos = 35000000, build = 'hg38', expect = 'MHC'),
  list(label = "chr6:35000001 (one bp past MHC upper boundary)",        chr = 6,    pos = 35000001, build = 'hg38', expect = NA_character_),
  list(label = "'chr8':8100000 (chr given with 'chr' prefix, lower bound of inversion)", chr = 'chr8', pos = 8100000, build = 'hg38', expect = 'chr8_inversion'),
  list(label = "chr8:11900001 (one bp past inversion upper boundary)",  chr = 8,    pos = 11900001, build = 'hg38', expect = NA_character_)
)

for (cs in cases) {
  got <- flag_excluded_region(chr = cs$chr, pos_bp = cs$pos, build = cs$build)
  ok <- identical(got, cs$expect) || (is.na(got) && is.na(cs$expect))
  cat(sprintf('%-70s -> got=%-16s expect=%-16s %s\n',
              cs$label, ifelse(is.na(got), 'NA', got), ifelse(is.na(cs$expect), 'NA', cs$expect),
              ifelse(ok, 'PASS', 'FAIL')))
}

# hg19 build case: must stop() per the function's own documented behavior
cat('\nTesting build="hg19" (should stop() with a liftover message):\n')
result <- tryCatch({
  flag_excluded_region(chr = 6, pos_bp = 30450000, build = 'hg19')
  'NO ERROR -- FAIL (should have stopped)'
}, error = function(e) paste('Correctly stopped:', conditionMessage(e)))
cat(result, '\n')

# Integration check: does the gate actually abort the pipeline (stop()) as SKILL.md says,
# not just return a flag that could be silently ignored?
cat('\nTesting full gate block (region_flag + stop()) as it appears in SKILL.md:\n')
gwas_df <- data.frame(CHR = 6, POS = 30450000, P = 1e-20)
result2 <- tryCatch({
  region_flag <- flag_excluded_region(chr = gwas_df$CHR[1], pos_bp = gwas_df$POS[which.min(gwas_df$P)])
  if (!is.na(region_flag)) {
    stop(sprintf(
      'Locus is in the %s exclusion zone -- standard coloc PP.H4 is not interpretable here. Use HLA-coloc (Butler-Laporte 2024) for MHC, or pre-condition on inversion genotype for chr8; do not report a naive coloc.abf/coloc.susie result.',
      region_flag))
  }
  'NO ERROR -- FAIL (should have stopped for MHC locus)'
}, error = function(e) paste('Correctly stopped pipeline:', conditionMessage(e)))
cat(result2, '\n')
