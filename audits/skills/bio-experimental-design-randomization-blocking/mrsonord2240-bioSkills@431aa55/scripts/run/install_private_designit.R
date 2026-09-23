install.packages("designit", repos = "https://cloud.r-project.org", lib = .libPaths()[1], dependencies = FALSE)
library(designit)
cat("designit=", as.character(packageVersion("designit")), "\n", sep = "")
