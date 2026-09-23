# Follow-up test: does SetMetabolomeFilter(mSet, TRUE) alone (exactly as documented in
# SKILL.md's ORA code block) actually restrict the background, or is it a silent no-op
# without the undocumented companion call Setup.KEGGReferenceMetabolome()?
suppressMessages(library(MetaboAnalystR))

run_ora <- function(use_filter, call_reference_setup) {
  mSet <- InitDataObjects('conc', 'pathora', FALSE)
  mSet <- SetOrganism(mSet, 'hsa')
  compounds <- c('Pyruvate','L-Lactate','Citrate','Succinate','Fumarate','L-Alanine',
                 'L-Glutamate','L-Glutamine','Malate','Isocitrate','Oxaloacetate','Acetyl-CoA')
  mSet <- Setup.MapData(mSet, compounds)
  mSet <- CrossReferencing(mSet, 'name')
  mSet <- CreateMappingResultTable(mSet)
  mSet <- SetKEGG.PathLib(mSet, 'hsa', 'current')
  mSet <- SetMetabolomeFilter(mSet, use_filter)
  if (call_reference_setup) {
    mSet <- Setup.KEGGReferenceMetabolome(mSet, "../../data/input1_reference_metabolome_synthetic.txt")
  }
  mSet <- CalculateOraScore(mSet, 'rbc', 'hyperg')
  as.data.frame(mSet$analSet$ora.mat)
}

cat("=== A: SetMetabolomeFilter(mSet, FALSE) -- SKILL.md's 'inflated default' path ===\n")
ora_false <- run_ora(FALSE, FALSE)
print(ora_false[order(rownames(ora_false)), c("Raw p","FDR")])

cat("\n=== B: SetMetabolomeFilter(mSet, TRUE) alone -- exactly what SKILL.md's code block shows ===\n")
ora_true_alone <- run_ora(TRUE, FALSE)
print(ora_true_alone[order(rownames(ora_true_alone)), c("Raw p","FDR")])

cat("\n=== C: SetMetabolomeFilter(mSet, TRUE) + Setup.KEGGReferenceMetabolome() (undocumented in SKILL.md) ===\n")
ora_true_ref <- run_ora(TRUE, TRUE)
print(ora_true_ref[order(rownames(ora_true_ref)), c("Raw p","FDR")])

cat("\n=== Comparison: is B identical to A (i.e. is the documented call alone a silent no-op)? ===\n")
common <- intersect(rownames(ora_false), rownames(ora_true_alone))
cat("Identical Raw p between A and B for", sum(abs(ora_false[common,"Raw p"] - ora_true_alone[common,"Raw p"]) < 1e-12), "of", length(common), "shared pathways\n")

cat("\n=== Comparison: does C (real reference call) differ from A/B? ===\n")
common2 <- intersect(rownames(ora_false), rownames(ora_true_ref))
cat("Identical Raw p between A and C for", sum(abs(ora_false[common2,"Raw p"] - ora_true_ref[common2,"Raw p"]) < 1e-12), "of", length(common2), "shared pathways\n")
