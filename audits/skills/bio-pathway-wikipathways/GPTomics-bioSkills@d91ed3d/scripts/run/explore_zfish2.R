suppressMessages(library(rWikiPathways))
zpaths <- listPathways('Danio rerio')
cat("n zebrafish pathways:", nrow(zpaths), "\n")
print(head(zpaths, 20))
