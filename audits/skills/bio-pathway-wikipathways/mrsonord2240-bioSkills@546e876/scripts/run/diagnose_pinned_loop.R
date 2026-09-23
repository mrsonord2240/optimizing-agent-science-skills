suppressMessages({library(rWikiPathways); library(clusterProfiler); library(tidyr)})
for (archive_date in unique(format(Sys.Date() - seq(60, 330, by = 30), '%Y%m10'))) {
  gmt <- tryCatch(suppressWarnings(downloadPathwayArchive(date = archive_date, organism = 'Homo sapiens', format = 'gmt', destpath = tempdir())), error = function(e) { cat('error=', conditionMessage(e), '\n', sep=''); NULL })
  cat(sprintf('date=%s result=%s exists=%s joined=%s temp=%s\n', archive_date, paste(gmt, collapse='|'), !is.null(gmt) && file.exists(gmt), !is.null(gmt) && file.exists(file.path(tempdir(), gmt)), tempdir()))
}
