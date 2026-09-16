suppressMessages(library(lipidr))
lipidr:::.data_internal("lipidnames_pattern")
p <- lipidr:::.myDataEnv$lipidnames_pattern
cat("istd regex:\n"); print(p$istd)
cat("istd_list sample:\n"); print(head(p$istd_list, 30))
