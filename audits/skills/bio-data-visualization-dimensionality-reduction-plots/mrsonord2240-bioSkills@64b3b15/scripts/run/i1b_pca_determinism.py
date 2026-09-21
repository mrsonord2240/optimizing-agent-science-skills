"""SKILL.md says PCA is 'deterministic'. Test sklearn PCA(n_components=10) (no random_state) on the wide synthetic bulk matrix."""
import numpy as np, pandas as pd
from sklearn.decomposition import PCA
from common import DATA
import os
counts = pd.read_csv(os.path.join(DATA,'bulk_counts.csv'), index_col=0); X = np.log2(counts.values+1)
a = PCA(n_components=10); b = PCA(n_components=10)
A = a.fit_transform(X); B = b.fit_transform(X)
print('solver:', a._fit_svd_solver, '| identical scores twice:', np.array_equal(A,B), '| max|score diff| %.3g' % np.abs(A-B).max(), '| max|ratio diff| %.3g' % np.abs(a.explained_variance_ratio_-b.explained_variance_ratio_).max())
c = PCA(n_components=10, svd_solver='full'); d = PCA(n_components=10, svd_solver='full')
print('svd_solver=full identical twice:', np.array_equal(c.fit_transform(X), d.fit_transform(X)))
c1 = PCA(n_components=10, random_state=42).fit_transform(X); c2 = PCA(n_components=10, random_state=42).fit_transform(X); print('random_state=42 identical twice:', np.array_equal(c1,c2))
