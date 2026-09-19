# Verification: does the SKILL.md's OWN shown LinDA code snippet crash on a real phyloseq
# object? SKILL.md's "LinDA" section shows exactly:
#   otu <- as.data.frame(otu_table(ps)); if (!taxa_are_rows(ps)) otu <- t(otu)
#   meta <- as.data.frame(sample_data(ps))
#   fit <- linda(feature.dat = otu, meta.dat = meta, formula = '~ Group + Age + (1 | SubjectID)', ...)
# TOOLS.md §6 warns as.data.frame(sample_data(ps)) silently keeps class "sample_data" and
# crashes MicrobiomeStat::linda() deep inside its internals. Testing the SKILL.md code VERBATIM.
suppressMessages({
  library(phyloseq)
  library(MicrobiomeStat)
})
ps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/phyloseq_object.rds')

# EXACT code as shown in SKILL.md's LinDA section
otu <- as.data.frame(otu_table(ps)); if (!taxa_are_rows(ps)) otu <- t(otu)
meta <- as.data.frame(sample_data(ps))
cat('class(meta) after SKILL.md-shown as.data.frame(sample_data(ps)):', paste(class(meta), collapse=','), '\n')

result <- tryCatch({
  fit <- linda(feature.dat = otu, meta.dat = meta,
               formula = '~ Group + Age + (1 | SubjectID)',
               feature.dat.type = 'count', prev.filter = 0.10, alpha = 0.05)
  'SUCCEEDED'
}, error = function(e) paste('CRASHED:', conditionMessage(e)))
cat('\nResult of running SKILL.md\'s own verbatim LinDA code block:', result, '\n')
