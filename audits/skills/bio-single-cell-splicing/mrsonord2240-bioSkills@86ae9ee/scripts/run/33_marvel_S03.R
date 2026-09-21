# INPUT 4: SKILL.md block S03 (Preprocess_rMATS loop) run LITERALLY on the real chrX rMATS output, for (a) the Ensembl GTF as shipped and (b) the gene_type-renamed GTF.
# Block S03 reads 'annotation.gtf' and writes events_<TYPE>.txt in the working directory, so each variant gets its own directory.
suppressMessages({library(MARVEL); library(data.table)})
base <- 'F:/OpenScience/audits/bio-single-cell-splicing/run/out/in4_s03'
for (v in c('annotation.gtf', 'annotation_gencode.gtf')) {
  d <- file.path(base, paste0('var_', sub('[.]gtf$', '', v))); dir.create(d, showWarnings = FALSE); setwd(d)
  file.copy(file.path(base, v), 'annotation.gtf', overwrite = TRUE); dir.create('rmats_out', showWarnings = FALSE)
  file.copy(list.files(file.path(base, 'rmats_out'), pattern = '^fromGTF[.](SE|MXE|RI|A5SS|A3SS)[.]txt$', full.names = TRUE), 'rmats_out')
  cat('\n######## variant:', v, '\n')
  r <- tryCatch({ source('F:/OpenScience/audits/bio-single-cell-splicing/run/blocks/S03_r.R', echo = FALSE); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
  cat('block S03 status:', r, '\n')
  for (ev in c('SE', 'MXE', 'RI', 'A5SS', 'A3SS')) {
    f <- sprintf('events_%s.txt', ev); if (!file.exists(f)) { cat(ev, ': file missing\n'); next }
    t <- read.table(f, header = TRUE, sep = '\t'); raw <- read.table(sprintf('rmats_out/fromGTF.%s.txt', ev), header = TRUE, sep = '\t')
    cat(sprintf('%-5s rMATS events %4d -> MARVEL table %4d rows; cols: %s; gene_type NA: %d; distinct gene_type: %s\n', ev, nrow(raw), nrow(t), paste(colnames(t), collapse = ','), sum(is.na(t$gene_type)), paste(unique(t$gene_type)[1:3], collapse = '|')))
  }
  # hand-check one plus- and one minus-strand SE tran_id against the rMATS row (rMATS coords are 0-based start, 1-based end)
  se <- read.table('events_SE.txt', header = TRUE, sep = '\t'); raw <- read.table('rmats_out/fromGTF.SE.txt', header = TRUE, sep = '\t')
  for (st in c('+', '-')) {
    i <- which(raw$strand == st)[1]; r <- raw[i, ]
    exp_id <- if (st == '+') sprintf('chr%s:%d:%d:+@chr%s:%d:%d:+@chr%s:%d:%d', sub('^chr', '', r$chr), r$upstreamES + 1, r$upstreamEE, sub('^chr', '', r$chr), r$exonStart_0base + 1, r$exonEnd, sub('^chr', '', r$chr), r$downstreamES + 1, r$downstreamEE) else NA
    cat('strand', st, 'rMATS row', i, ': ', r$chr, r$upstreamES, r$upstreamEE, r$exonStart_0base, r$exonEnd, r$downstreamES, r$downstreamEE, '\n')
    hit <- if (!is.na(exp_id)) exp_id %in% se$tran_id else NA
    cat('   hand-built tran_id (+ only):', exp_id, ' found in MARVEL table:', hit, '\n')
    if (st == '-') { ex <- paste(r$chr, r$downstreamES + 1, sep = ':'); cat('   minus-strand: any tran_id starting', ex, ':', any(startsWith(se$tran_id, paste0(r$chr, ':', r$downstreamES + 1, ':'))), '\n') }
  }
}
