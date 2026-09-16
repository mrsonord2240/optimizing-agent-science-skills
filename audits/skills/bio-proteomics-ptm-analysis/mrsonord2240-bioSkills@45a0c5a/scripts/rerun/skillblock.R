# Re-audit 2026-09-15: pull the fork's SKILL.md ```r blocks programmatically (no retyping).
skill_r_blocks <- function() {
  txt <- paste(readLines('F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/ptm-analysis/SKILL.md', encoding = 'UTF-8', warn = FALSE), collapse = '\n')
  m <- regmatches(txt, gregexpr('(?s)```r\\n.*?```', txt, perl = TRUE))[[1]]
  sub('```$', '', sub('^```r\\n', '', m))
}
ptm_block <- function() { b <- skill_r_blocks(); b[grepl('groupComparisonPTM', b)][1] }
ksea_block <- function() { b <- skill_r_blocks(); b[grepl('KSEA.Scores', b)][1] }
truth_table <- function(adjusted_like, truth_file, label) {
  truth <- read.csv(truth_file)
  called <- adjusted_like$Protein[!is.na(adjusted_like$adj.pvalue) & adjusted_like$adj.pvalue < 0.05]
  tested <- adjusted_like$Protein
  out <- do.call(rbind, lapply(split(truth, truth$class), function(d)
    data.frame(class = d$class[1], n = nrow(d), tested = sum(d$site %in% tested), called = sum(d$site %in% called))))
  cat('--', label, '--\n'); print(out, row.names = FALSE)
  invisible(out)
}
