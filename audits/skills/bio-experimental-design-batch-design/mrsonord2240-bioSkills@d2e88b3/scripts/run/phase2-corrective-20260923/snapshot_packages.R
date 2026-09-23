lib <- "/mnt/openscience/audit-envs/crispr-screen-analyst/tools/designit-linux-runtime/runtime-r-lib-20260923"
ip <- installed.packages(lib.loc = lib)
write.csv(data.frame(Package = ip[, "Package"], Version = ip[, "Version"], row.names = NULL),
          "isolated_runtime_packages_before.csv", row.names = FALSE)
cat("PASS: snapshotted ", nrow(ip), " packages in the private runtime.\n", sep = "")
