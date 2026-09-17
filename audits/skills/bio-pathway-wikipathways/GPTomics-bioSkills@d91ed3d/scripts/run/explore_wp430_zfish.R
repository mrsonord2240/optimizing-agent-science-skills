suppressMessages(library(rWikiPathways))
g430 <- getXrefList('WP430', 'L')
cat("WP430 n genes:", length(g430), "\n")
print(g430)

cat("\n--- zebrafish organism check ---\n")
zorgs <- get_wp_organisms()
cat("Danio rerio in list:", "Danio rerio" %in% zorgs, "\n")

zpaths <- listPathways('Danio rerio')
cat("n zebrafish pathways:", nrow(zpaths), "\n")
print(head(zpaths, 15))
