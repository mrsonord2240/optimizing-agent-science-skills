from splice_parsers import parse_spliceai_vcf, classify_delta, read_input_vcf, unscored_report

s = parse_spliceai_vcf('output.vcf')                       # one row per variant x ALT x gene
s['acmg_evidence'] = classify_delta(s['delta_max'])        # BP4 / inconclusive / PP3_supporting[_prec0.5|_prec0.8] / not_scored
print(unscored_report('input.vcf', s['key'], 'SpliceAI'))  # input records with no SpliceAI= tag
