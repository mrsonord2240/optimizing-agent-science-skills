# Isolate the post-output exit behaviour without changing the shared R library.
cat('base R reached\n')
if (identical(Sys.getenv('PROBE_PKG'), 'MSnbase')) suppressPackageStartupMessages(library(MSnbase))
if (identical(Sys.getenv('PROBE_PKG'), 'MSstats')) suppressPackageStartupMessages(library(MSstats))
if (identical(Sys.getenv('PROBE_PKG'), 'arrow')) suppressPackageStartupMessages(library(arrow))
cat('package probe reached:', Sys.getenv('PROBE_PKG'), '\n')
