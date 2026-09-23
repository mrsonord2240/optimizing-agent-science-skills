set.seed(2026092311)
n <- 4L
treatments <- sample(LETTERS[1:n])
latin <- outer(0:(n - 1), 0:(n - 1), function(i, j) treatments[(i + j) %% n + 1])
stopifnot(all(apply(latin, 1, function(x) length(unique(x)) == n)), all(apply(latin, 2, function(x) length(unique(x)) == n)))
cat("latin_square_rows_and_columns_each_contain_all_4_treatments=PASS\n")
print(latin)
