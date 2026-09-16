import pandas as pd

src = r"F:\OpenScience\audit-envs\crispr-screen-analyst\public-data\HAP1_TKOv3_reads.txt"
df = pd.read_csv(src, sep='\t')
print(df.shape, df.columns.tolist())

# Build a mageck-style count table: sgRNA, Gene, samples...
# Use sequence prefix + row index as sgRNA ID (unique, mageck doesn't care about content)
df2 = df.copy()
df2.insert(0, 'sgRNA', ['sg%06d_%s' % (i, g) for i, g in enumerate(df2['GENE'])])
df2 = df2.drop(columns=['SEQUENCE'])
df2 = df2.rename(columns={'GENE': 'Gene', 'HAP1_T0': 'T0', 'HAP1_T18A': 'T18_A', 'HAP1_T18B': 'T18_B', 'HAP1_T18C': 'T18_C'})
# mageck requires integer counts
for c in ['T0', 'T18_A', 'T18_B', 'T18_C']:
    df2[c] = df2[c].round().astype(int)
df2.to_csv('experiment.count.txt', sep='\t', index=False)
print("wrote experiment.count.txt", df2.shape)
print(df2.head(3))
