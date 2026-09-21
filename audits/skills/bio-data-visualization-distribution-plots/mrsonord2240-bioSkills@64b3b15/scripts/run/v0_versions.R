for (p in c("ggplot2","ggbeeswarm","ggdist","gghalves","lvplot","introdataviz","dplyr","ALL","Biobase")) {
  r <- try(suppressMessages(library(p, character.only=TRUE)), silent=TRUE)
  cat(p, if (inherits(r,"try-error")) paste("FAIL:", conditionMessage(attr(r,"condition"))) else as.character(packageVersion(p)), "\n")
}
