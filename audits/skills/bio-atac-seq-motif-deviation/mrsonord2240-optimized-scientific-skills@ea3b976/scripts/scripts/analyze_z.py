import pandas as pd
a=pd.read_csv('F:/OpenScience/audits/bio-atac-seq-motif-deviation/reaudit-run/bulk_A/chromvar_deviations.csv',index_col=0)
print('max|z| %.2f'%a.abs().values.max(), 'n motifs with max|z|>9:', int((a.abs().max(axis=1)>9).sum()))
