# Pass-5: does the match() fix actually protect against a shuffled annotation, and would the
# pre-fix `%in%` subset have produced a wrong answer on the same input? SYNTHETIC.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
blk <- list.files(file.path(PP,'pass5','blocks'), pattern='^b01', full.names=TRUE)
src <- readLines(blk)
cat('fixed block uses match():', any(grepl('sample_info[match(colnames(normalized)', src, fixed=TRUE)),
    '| carries the stopifnot:', any(grepl('stopifnot(!any(is.na(sample_info$sample)))', src, fixed=TRUE)), '\n')

run <- function(dir, prefix_version) {
  txt <- src
  if (prefix_version) {   # revert exactly the one line the fix changed
    i <- grep('sample_info[match(colnames(normalized), sample_info$sample), ]', txt, fixed=TRUE)
    txt[i] <- "sample_info <- sample_info[sample_info$sample %in% colnames(normalized), ]"
    j <- grep('stopifnot(!any(is.na(sample_info$sample)))', txt, fixed=TRUE)
    txt <- txt[-j]
  }
  f <- tempfile(fileext='.R'); writeLines(txt, f)
  e <- new.env(parent=globalenv()); owd <- getwd(); setwd(file.path(PP,'pass5',dir))
  r <- tryCatch({ suppressWarnings(sys.source(f, envir=e)); 'OK' },
                error=function(x) paste('ERROR:', conditionMessage(x)))
  setwd(owd)
  if (r != 'OK') return(list(status=r))
  res <- get('results', envir=e); si <- get('sample_info', envir=e); nm <- get('normalized', envir=e)
  list(status='OK', n=sum(res$significant),
       up=sum(res$significant & res$logFC>0), down=sum(res$significant & res$logFC<0),
       aligned=identical(as.character(si$sample), colnames(nm)),
       order=paste(si$sample, collapse=','), res=res)
}
a <- run('work1', FALSE); b <- run('work1_shuf', FALSE); c <- run('work1_shuf', TRUE)
cat('\nFIXED, annotation in file order   : sig', a$n, '(up', a$up, 'down', a$down, ') aligned', a$aligned, '\n')
cat('FIXED, annotation SHUFFLED        : sig', b$n, '(up', b$up, 'down', b$down, ') aligned', b$aligned, '\n')
cat('  order after subset:', b$order, '\n')
cat('PRE-FIX %in%, annotation SHUFFLED : sig', c$n, '(up', c$up, 'down', c$down, ') aligned', c$aligned, '\n')
cat('  order after subset:', c$order, '\n')
if (!is.null(a$res) && !is.null(b$res))
  cat('\nfixed shuffled == fixed unshuffled, protein-for-protein:',
      identical(a$res$significant[order(a$res$protein)], b$res$significant[order(b$res$protein)]), '\n')
if (!is.null(a$res) && !is.null(c$res)) {
  m <- merge(a$res[,c('protein','significant','logFC')], c$res[,c('protein','significant','logFC')], by='protein')
  cat('pre-fix shuffled vs fixed: calls differing:', sum(m$significant.x != m$significant.y),
      '| max |logFC| difference:', round(max(abs(m$logFC.x - m$logFC.y), na.rm=TRUE), 3), '\n')
}
