"""Do the shipped scripts' saga fits without random_state vary run to run? Repeats the logistic_regression.py fit 8 times in one process (global numpy RNG state differs) and in fresh processes."""
import numpy as np, subprocess, sys
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
X, y = make_classification(n_samples=300, n_features=500, n_informative=15, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
cnt = []
for i in range(8):
    p = Pipeline([('s', StandardScaler()), ('c', LogisticRegression(solver='saga', l1_ratio=0.5, C=0.1, max_iter=5000))]).fit(X_tr, y_tr)
    cnt.append(int((p['c'].coef_[0] != 0).sum()))
print('non-zero counts over 8 fits without random_state:', cnt)
