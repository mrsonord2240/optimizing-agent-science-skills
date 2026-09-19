"""
Re-auditor: 'Group Clones from mtDNA Heteroplasmy' SKILL.md snippet, verbatim,
run on (1) the original audit's 40-cell/4-clone/1-hotspot data (regression)
and (2) the re-auditor's own 50-cell/5-clone/2-hotspot data (harder: two
independent recurrent hotspots must both be blacklisted).
"""
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
from sklearn.metrics import silhouette_score
from sklearn.metrics import adjusted_rand_score

for label, path, truth_col in [
    ('R1-regression(original 40-cell/1-hotspot)', '../data/mtdna_heteroplasmy.csv', 'ground_truth_clone'),
    ('R2-new(reauditor 50-cell/2-hotspot)', '../data2/mtdna_heteroplasmy2.csv', 'ground_truth_clone'),
]:
    print(f'=== {label} ===')
    het_full = pd.read_csv(path, index_col=0)
    truth = het_full[truth_col]
    het = het_full.drop(columns=[truth_col])

    prevalence = (het > 0.1).mean(axis=0)
    dropped = list(prevalence[prevalence > 0.8].index)
    het_f = het.loc[:, prevalence <= 0.8]
    print('variants dropped as hotspot/NUMT:', dropped)

    dist = pdist(het_f.values, metric='correlation')
    Z = linkage(dist, method='average')

    best_k, best_score, best_labels = None, -1, None
    for k in range(2, 8):
        labels = fcluster(Z, t=k, criterion='maxclust')
        if len(set(labels)) < 2:
            continue
        score = silhouette_score(het_f.values, labels, metric='correlation')
        if score > best_score:
            best_k, best_score, best_labels = k, score, labels

    clones = pd.Series(best_labels, index=het.index, name='mtdna_clone')
    ari = adjusted_rand_score(truth.values, clones.values)
    print(f'chosen k={best_k}, silhouette={best_score:.3f}, ARI vs ground truth={ari:.4f}')
    print()
