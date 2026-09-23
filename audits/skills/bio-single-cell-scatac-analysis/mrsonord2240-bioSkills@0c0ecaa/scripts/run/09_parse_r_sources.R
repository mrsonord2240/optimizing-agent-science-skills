# Purpose: Parse-check all R source files without loading their dependencies.
# Usage: r.sh 09_parse_r_sources.R
files <- c(
  'F:/OpenScience/wt/single-cell-scatac-analysis/single-cell/scatac-analysis/scripts/run_chromvar.R',
  'F:/OpenScience/wt/single-cell-scatac-analysis/single-cell/scatac-analysis/examples/signac_workflow.R'
)
for (f in files) { parse(f); cat('parse=PASS ', f, '\n', sep='') }
