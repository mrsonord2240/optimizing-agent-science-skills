from splice_parsers import build_concordance
T = build_concordance('input.vcf', spliceai_vcf='output.vcf', pangolin_vcf='pangolin_output.vcf',
                      mmsplice_csv='mmsplice_predictions.csv')
print(T[['spliceai_delta', 'pangolin_score', 'delta_logit_psi', 'n_scored', 'n_above', 'concordance']])
