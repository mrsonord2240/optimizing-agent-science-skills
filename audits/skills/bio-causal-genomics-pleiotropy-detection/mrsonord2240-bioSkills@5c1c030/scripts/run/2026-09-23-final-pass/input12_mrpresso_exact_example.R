# Fresh independent final-pass input: run the exact audited MR-PRESSO example.
source_path <- 'F:/OpenScience/wt/causal-genomics-pleiotropy-detection/causal-genomics/pleiotropy-detection/examples/mr_presso_analysis.R'
cat('FINAL_PASS_INPUT=12\n')
cat('SOURCE=', source_path, '\n', sep='')
source(source_path, echo = FALSE)
cat('ASSERTION: exact MR-PRESSO example completed, including the zero-length distortion-test guard.\n')
