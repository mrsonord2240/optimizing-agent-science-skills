# Input 9 (NEW) -- "My sphingolipid names are a mix of old-style (d18:1) and
# new LIPID MAPS 2020 (;O2) notation from different tools -- get them into
# lipidr without silently dropping any."
#
# This is a NEW input (not in the pre-fix audit): tests the fix's
# to_lipidr_sphingoid() conversion snippet against all three O-levels
# (;O1/m, ;O2/d, ;O3/t) across multiple sphingolipid classes (Cer, HexCer,
# SM), plus a name that is ALREADY in the old prefix style (must pass through
# unchanged) and a non-sphingoid name (must be unaffected).
suppressMessages(library(lipidr))

to_lipidr_sphingoid <- function(x) {
  x <- sub("(\\d+:\\d+);O1\\b", "m\\1", x)
  x <- sub("(\\d+:\\d+);O2\\b", "d\\1", x)
  x <- sub("(\\d+:\\d+);O3\\b", "t\\1", x)
  x
}

names_in <- c(
  "Cer 18:1;O2/16:0",     # new-style, O2 -> d
  "Cer 18:0;O1/16:0",     # new-style, O1 -> m
  "Cer 18:1;O3/16:0",     # new-style, O3 -> t
  "HexCer 18:1;O2/16:0",  # different class, O2
  "SM 18:1;O2/16:0",      # different class, O2
  "Cer d18:0/18:0"        # already old-style, distinct from the O2 case's target -- must pass through unchanged
)
names_out <- to_lipidr_sphingoid(names_in)
cat("=== Conversion ===\n")
for (i in seq_along(names_in)) cat(sprintf("%-22s -> %s\n", names_in[i], names_out[i]))

expected <- c(
  "Cer d18:1/16:0", "Cer m18:0/16:0", "Cer t18:1/16:0",
  "HexCer d18:1/16:0", "SM d18:1/16:0",
  "Cer d18:0/18:0"
)
stopifnot(all(names_out == expected))
cat("\nPASS: all conversions match expected old-style prefixes (m/d/t), pass-through case unchanged\n\n")
# Non-sphingoid case checked separately (not mixed into the LipidomicsExperiment
# import below, to avoid an unrelated duplicate-rowname collision):
stopifnot(to_lipidr_sphingoid("PC 34:1") == "PC 34:1")
cat("PASS: non-sphingoid name (PC 34:1) unaffected by the conversion\n\n")

# Now confirm the fix actually matters: import unconverted vs. converted
# names into real LipidomicsExperiments and compare Class. Each name is
# tested alongside a fixed, already-valid anchor row (PC 34:1) in its OWN
# 2-row experiment -- as_lipidomics_experiment() hard-errors ("does not
# contain valid lipid names") once the majority of a batch fails to parse,
# so batching all 6 test names together would trip that whole-dataframe
# rejection and obscure the PER-NAME parsing behavior actually under test.
class_of <- function(molecule) {
  d <- suppressWarnings(as_lipidomics_experiment(
    data.frame(Molecule = c("PC 34:1", molecule), S1 = 1, S2 = 1, check.names = FALSE)
  ))
  rowData(d)$Class[rownames(d) == molecule]
}

cat("=== Class assignment: unconverted ';O#' names (each vs PC 34:1 anchor) ===\n")
class_unconverted <- vapply(names_in, function(m) as.character(class_of(m)), character(1))
print(data.frame(Molecule = names_in, Class = class_unconverted, row.names = NULL))

cat("\n=== Class assignment: converted (m/d/t prefix) names ===\n")
class_converted <- vapply(names_out, function(m) as.character(class_of(m)), character(1))
print(data.frame(Molecule = names_out, Class = class_converted, row.names = NULL))

n_na_unconverted <- sum(is.na(class_unconverted) | class_unconverted == "NA")
n_na_converted <- sum(is.na(class_converted) | class_converted == "NA")
cat("\nNA classes, unconverted:", n_na_unconverted, "/", length(names_in), "\n")
cat("NA classes, converted:  ", n_na_converted, "/", length(names_out), "\n")

# The 5 genuinely ';O#'-suffixed names (indices 1-5) should be NA before,
# non-NA after; index 6 (already old-style) should be non-NA both times.
stopifnot(n_na_unconverted == 5)
stopifnot(n_na_converted == 0)
stopifnot(!(is.na(class_unconverted[6]) || class_unconverted[6] == "NA"))  # old-style name unaffected even pre-conversion
cat("PASS: ';O#' sphingoid names that import as Class=NA unconverted correctly resolve to a real Class after conversion\n")
