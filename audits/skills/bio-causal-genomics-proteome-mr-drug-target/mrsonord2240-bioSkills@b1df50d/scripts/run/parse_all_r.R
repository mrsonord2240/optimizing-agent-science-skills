# Parse every R file that participates in this final-pass audit and every
# shipped R file in the audited snapshot. This is a syntax gate, not execution evidence.
audit_root <- "F:/OpenScience/audits/bio-causal-genomics-proteome-mr-drug-target/run"
files <- c(list.files(audit_root, pattern="\\.R$", full.names=TRUE),
           list.files(file.path(audit_root, "skill-copy"), pattern="\\.R$", recursive=TRUE, full.names=TRUE))
for (f in files) parse(f)
cat("Parsed", length(files), "R files successfully.\n")
