import pandas as pd
import numpy as np

df = pd.read_csv("HAP1_TKOv3_reads.txt", sep="\t")
genes = df['GENE'].unique()
rng = np.random.default_rng(202609)  # different seed from the fix log's own subset
sub_genes = set(rng.choice(genes, size=1500, replace=False))
sub = df[df['GENE'].isin(sub_genes)].copy()
sub = sub.rename(columns={'SEQUENCE': 'sgRNA'})
sub = sub[['sgRNA', 'GENE', 'HAP1_T0', 'HAP1_T18A', 'HAP1_T18B', 'HAP1_T18C']]
sub.to_csv("r2_new1_HAP1_subset1500.txt", sep="\t", index=False)
print(sub.shape, sub['GENE'].nunique(), "genes")
