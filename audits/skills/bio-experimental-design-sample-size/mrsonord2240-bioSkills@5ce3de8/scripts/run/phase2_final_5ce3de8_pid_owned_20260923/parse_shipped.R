root <- "/mnt/openscience/audits/bio-experimental-design-sample-size/run/phase2_final_5ce3de8_pid_owned_20260923/source_copy/sample-size"
files <- c(file.path(root, "examples", "sample_size_estimation.R"),
           file.path(root, "scripts", "proper_power.R"),
           file.path(root, "scripts", "pseudobulk_donor_ssize.R"))
for (path in files) parse(path)
cat(sprintf("OK parse %d shipped R files\n", length(files)))
