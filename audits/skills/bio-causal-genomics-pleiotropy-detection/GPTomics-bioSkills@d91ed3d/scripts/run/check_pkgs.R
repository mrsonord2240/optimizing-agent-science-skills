for (p in c("mr.raps","mrclust")) {
  cat(p, ":", requireNamespace(p, quietly=TRUE), "\n")
}
