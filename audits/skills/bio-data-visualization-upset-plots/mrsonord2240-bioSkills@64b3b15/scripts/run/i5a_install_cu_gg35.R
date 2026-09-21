# Private lib for THIS audit only: ComplexUpset built from source against ggplot2 3.5.2 (r-gg35.sh puts 3.5.2 first).
# Purpose: verify the Skill's "pin ggplot2 <= 3.5.2" advice. Nothing is written to any shared env lib.
lib <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/R-lib-cu-gg35_private"
cat("ggplot2 in use:", as.character(packageVersion("ggplot2")), " from", find.package("ggplot2"), "\n")
options(repos = c(CRAN = "https://cloud.r-project.org"))
install.packages("ComplexUpset", lib = lib, type = "source", dependencies = FALSE)
.libPaths(c(lib, .libPaths()))
library(ComplexUpset); cat("ComplexUpset", as.character(packageVersion("ComplexUpset")), "from", find.package("ComplexUpset"), "\n")
