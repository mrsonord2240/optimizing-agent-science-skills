import pandas as pd
from sklearn.metrics import average_precision_score

gs = pd.read_csv("input1_canonical.gene_summary.txt", sep="\t")
ceg = set(x.strip() for x in open("CEGv2_core_essentials.txt").read().splitlines()[1:])
ceg = set(l.split("\t")[0] for l in open("CEGv2_core_essentials.txt").read().splitlines()[1:])
neg = set(l.split("\t")[0] for l in open("NEGv1_nonessentials.txt").read().splitlines()[1:])

sub = gs[gs['id'].isin(ceg | neg)].copy()
sub['y_true'] = sub['id'].isin(ceg).astype(int)
# score: more negative neg|score = more essential -> use -neg|score as "essentiality score"
sub['essentiality_score'] = -sub['neg|score']
pr_auc = average_precision_score(sub['y_true'], sub['essentiality_score'])
print(f"n genes scored (CEG+NEG present in gene_summary): {len(sub)}")
print(f"n CEG present: {sub['y_true'].sum()}, n NEG present: {(1-sub['y_true']).sum()}")
print(f"PR-AUC (neg|score ranking) vs CEGv2/NEGv1: {pr_auc:.3f}")

# also check using neg|lfc
sub['neg_lfc_score'] = -sub['neg|lfc']
pr_auc2 = average_precision_score(sub['y_true'], sub['neg_lfc_score'])
print(f"PR-AUC (neg|lfc ranking): {pr_auc2:.3f}")
