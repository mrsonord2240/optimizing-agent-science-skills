make_layout <- function() {
  set.seed(20260528)
  u <- data.frame(id = sprintf("S%02d", 1:24), block = rep(c("day1", "day2", "day3"), each = 8))
  u$treatment <- ave(u$id, u$block, FUN = function(ids) sample(rep(c("ctrl", "treat"), length.out = length(ids))))
  u$run_order <- sample(nrow(u))
  u
}
a <- make_layout(); b <- make_layout()
stopifnot(identical(a, b))
cat("identical_seeded_layouts=TRUE checksum=", sum(utf8ToInt(paste(a$treatment, collapse = ""))), "\n", sep = "")
