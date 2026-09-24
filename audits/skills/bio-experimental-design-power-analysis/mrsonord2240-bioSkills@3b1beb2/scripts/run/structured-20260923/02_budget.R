source_path <- "F:/OpenScience/wt/p2-reaudit-bio-power-analysis/experimental-design/power-analysis/examples/rnaseq_power.R"
lines <- readLines(source_path, warn = FALSE)
marker <- grep("^# ---------------------------------------------------------------------------$", lines)[1]
eval(parse(text = lines[1:(marker - 1)]))
p4 <- checked_rnapower(depth = 2, n = 4, cv = .3, effect = 1.5, alpha = .05)
p8 <- checked_rnapower(depth = 1, n = 8, cv = .3, effect = 1.5, alpha = .05)
stopifnot(p8 > p4)
cat(sprintf("n4=%.6f n8=%.6f\nBUDGET=PASS\n", p4, p8))
