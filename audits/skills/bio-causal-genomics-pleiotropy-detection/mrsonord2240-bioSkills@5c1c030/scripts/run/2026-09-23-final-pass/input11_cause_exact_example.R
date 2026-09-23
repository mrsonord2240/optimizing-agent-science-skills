# Fresh independent final-pass input: run the exact audited CAUSE example.
source_path <- 'F:/OpenScience/wt/causal-genomics-pleiotropy-detection/causal-genomics/pleiotropy-detection/examples/cause_analysis.R'
cat('FINAL_PASS_INPUT=11\n')
cat('SOURCE=', source_path, '\n', sep='')
source(source_path, echo = FALSE)
cat('ASSERTION: exact CAUSE example completed after its 150-signature-SNP gate and model comparison.\n')
