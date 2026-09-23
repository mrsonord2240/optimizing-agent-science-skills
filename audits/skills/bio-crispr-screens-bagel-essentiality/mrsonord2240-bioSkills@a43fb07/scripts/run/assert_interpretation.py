import pandas as pd

dropout = pd.read_csv('calls_dropout.tsv', sep='\t')
enrichment = pd.read_csv('calls_enrichment.tsv', sep='\t')
controls = {'LacZ', 'luciferase', 'EGFP'}
assert not (set(dropout.GENE) & controls)
assert (dropout['call'] == 'tumor_suppressor').sum() == 0
assert (dropout['call'] == 'essential').sum() > 1000
assert (enrichment['call'] == 'tumor_suppressor').sum() / len(enrichment) > 0.80
for gene in ['TSC1', 'TSC2']:
    assert enrichment.loc[enrichment.GENE == gene, 'call'].iat[0] == 'tumor_suppressor'
stderr = open('enrichment.stderr', encoding='utf-8').read()
assert 'implausibly high' in stderr
print(f'PASS interpretation: dropout TS=0; enrichment TS={(enrichment.call == "tumor_suppressor").sum()}/{len(enrichment)}; warning emitted')
