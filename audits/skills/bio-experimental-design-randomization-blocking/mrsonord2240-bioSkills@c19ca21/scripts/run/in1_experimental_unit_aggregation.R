set.seed(20260923)
library(dplyr)
cells <- expand.grid(donor = sprintf("D%02d", 1:8), cell = 1:50,
                     KEEP.OUT.ATTRS = FALSE)
cells$condition <- ifelse(as.integer(sub("D", "", cells$donor)) <= 4, "ctrl", "treat")
donor_shift <- setNames(rnorm(8, 0, 0.7), sprintf("D%02d", 1:8))
cells$measurement <- donor_shift[cells$donor] + ifelse(cells$condition == "treat", 0.8, 0) + rnorm(nrow(cells), 0, 0.35)
eu_level <- cells |> group_by(donor, condition) |> summarise(value = mean(measurement), .groups = "drop")
stopifnot(nrow(cells) == 400L, nrow(eu_level) == 8L,
          all(table(eu_level$condition) == c(ctrl = 4L, treat = 4L)))
cat("cells=", nrow(cells), " eu_rows=", nrow(eu_level), " n_by_condition=", paste(table(eu_level$condition), collapse = "/"), "\n", sep = "")
