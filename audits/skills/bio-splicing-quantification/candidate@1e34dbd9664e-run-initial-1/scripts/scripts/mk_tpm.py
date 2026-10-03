import sys, pandas as pd
R, out = sys.argv[1], sys.argv[2]
cols = {}
for s in ['ERR188383', 'ERR188428', 'ERR188454', 'ERR204916']:
    cols[s] = pd.read_csv(f'{R}/salmon/{s}/quant.sf', sep='\t', index_col=0)['TPM']
m = pd.DataFrame(cols)
with open(f'{out}/chrX_tpm.tsv', 'w', newline='\n') as f:   # SUPPA2 header has no index-name cell
    f.write('\t'.join(m.columns) + '\n')
    m.to_csv(f, sep='\t', header=False, lineterminator='\n')
print('tpm', m.shape)
