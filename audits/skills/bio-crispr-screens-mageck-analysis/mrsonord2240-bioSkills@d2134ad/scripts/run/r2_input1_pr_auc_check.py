import pandas as pd
from sklearn.metrics import average_precision_score

gs = pd.read_csv("r2_input1_canonical.gene_summary.txt", sep="\t")
ceg = set(pd.read_csv("CEGv2_core_essentials.txt", sep="\t")['GENE'])
neg = set(pd.read_csv("NEGv1_nonessentials.txt", sep="\t")['GENE'])
sub = gs[gs['id'].isin(ceg | neg)].copy()
sub['y_true'] = sub['id'].isin(ceg)
print("n scored:", len(sub), "CEG:", sub['y_true'].sum(), "NEG:", (~sub['y_true']).sum())
print("PR-AUC (neg|score):", average_precision_score(sub['y_true'], -sub['neg|score']))
print("PR-AUC (neg|lfc):", average_precision_score(sub['y_true'], -sub['neg|lfc']))
