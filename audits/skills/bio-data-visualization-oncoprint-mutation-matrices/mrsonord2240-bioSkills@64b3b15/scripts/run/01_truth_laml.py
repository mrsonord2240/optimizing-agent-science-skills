import pandas as pd, gzip, json
maf = pd.read_csv(r'F:\OpenScience\audit-envs\data-visualization\public-data\mutations\tcga_laml.maf.gz', sep='\t', comment='#', low_memory=False)
print(maf.shape); print(list(maf.columns)[:20])
print(maf.Variant_Classification.value_counts())
print("samples", maf.Tumor_Sample_Barcode.nunique())
# per-gene: samples with >=1 mutation, and variant count
g = maf.groupby('Hugo_Symbol').agg(n_var=('Tumor_Sample_Barcode','size'), n_samp=('Tumor_Sample_Barcode','nunique')).sort_values(['n_samp','n_var'],ascending=False)
print(g.head(25))
print(g.sort_values(['n_var','n_samp'],ascending=False).head(25).index.tolist())
# multi-hit: sample-gene pairs with >1 variants, and with >1 distinct classes
sg = maf.groupby(['Hugo_Symbol','Tumor_Sample_Barcode']).Variant_Classification.agg(['size','nunique'])
print("multi-hit pairs", (sg['size']>1).sum(), "multi-class pairs", (sg['nunique']>1).sum())
print(sg[sg['nunique']>1].head())
# TMB per sample
tmb = maf.groupby('Tumor_Sample_Barcode').size()
print(tmb.describe())
