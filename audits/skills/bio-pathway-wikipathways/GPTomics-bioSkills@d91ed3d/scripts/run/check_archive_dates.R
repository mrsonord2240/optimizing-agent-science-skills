res <- tryCatch({
  con <- url("https://data.wikipathways.org/current/gmt/", "r")
  readLines(con, n=50)
}, error=function(e) e)
if (inherits(res,'error')) cat("current/ index ERROR:", conditionMessage(res), "\n") else print(res)

cat("\n--- listing top-level archive index ---\n")
res2 <- tryCatch({
  con <- url("https://data.wikipathways.org/", "r")
  readLines(con)
}, error=function(e) e)
if (inherits(res2,'error')) cat("root index ERROR:", conditionMessage(res2), "\n") else print(tail(res2, 60))
