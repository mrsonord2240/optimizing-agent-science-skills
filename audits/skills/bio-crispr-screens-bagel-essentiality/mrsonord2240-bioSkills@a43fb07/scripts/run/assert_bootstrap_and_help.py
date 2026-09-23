import pandas as pd

for name, flags in {'fc_help.txt': ['-i', '-o', '-c'], 'bf_help.txt': ['-i', '-e', '-n', '-c', '-r'], 'pr_help.txt': ['-i', '-e', '-n']}.items():
    text = open(name, encoding='utf-8').read()
    assert all(flag in text for flag in flags), (name, flags)
bf = pd.read_csv('bootstrap_50.txt', sep='\t')
assert list(bf.columns) == ['GENE', 'BF', 'STD', 'NumObs'], bf.columns.tolist()
assert len(bf) == 18053 and bf['STD'].notna().all() and (bf['NumObs'] >= 1).all()
print(f'PASS fresh bootstrap: {len(bf)} genes and bootstrap-only STD/NumObs columns; documented flags present')
