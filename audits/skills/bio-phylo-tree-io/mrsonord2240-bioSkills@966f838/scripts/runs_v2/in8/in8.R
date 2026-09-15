# Input 8 (NEW): does the Skill's stripped topology load in strict R readers, and what does ape do with the [&R] prefix
# and with Bio.Phylo's escaped comments? Files from runs_v2/in1 (SYNTHETIC mcc6.tree).
suppressPackageStartupMessages(library(ape))
for (f in c('../in1/topology.nwk', '../in1/phylo_convert.nwk')) {
  r <- tryCatch({ t <- read.tree(f); sprintf('tips %d, node.label %s', Ntip(t), paste(head(t$node.label, 2), collapse = ' | ')) },
                error = function(e) paste('ERROR', conditionMessage(e)), warning = function(w) paste('WARNING', conditionMessage(w)))
  cat(f, '->', r, '\n')
}
writeLines(paste0('[&R] ', readLines('../in1/topology.nwk')), 'with_R_prefix.nwk')
r <- tryCatch({ t <- read.tree('with_R_prefix.nwk'); sprintf('tips %d', Ntip(t)) }, error = function(e) paste('ERROR', conditionMessage(e)))
cat('same topology with a leading [&R] ->', r, '\n')
