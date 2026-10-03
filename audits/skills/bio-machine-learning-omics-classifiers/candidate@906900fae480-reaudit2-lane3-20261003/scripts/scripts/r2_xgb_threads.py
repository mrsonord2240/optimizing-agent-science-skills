"""Does the shipped demo's XGBoost best round depend on thread count? Executes the head of rf_xgboost_classifier.py (data+splits) then fits the script's XGB setting with n_jobs=1,2,4,default. Usage: python r2_xgb_threads.py <Skill dir>"""
import sys, os, numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
ns = {}; exec(open(sys.argv[1] + '/scripts/rf_xgboost_classifier.py', encoding='utf-8').read().split("models = {")[0], ns)
print('cpu_count', os.cpu_count())
for nj in (1, 2, 4, None):
    kw = {} if nj is None else {'n_jobs': nj}
    m = XGBClassifier(n_estimators=2000, learning_rate=0.03, max_depth=4, subsample=0.8, colsample_bytree=0.5, early_stopping_rounds=50, eval_metric='logloss', random_state=0, **kw)
    m.fit(ns['X_tr'], ns['y_tr'], eval_set=[(ns['X_val'], ns['y_val'])], verbose=False)
    print(f'n_jobs={nj}: best round {m.best_iteration}, val logloss {m.best_score:.3f}, test AUC {roc_auc_score(ns["y_te"], m.predict_proba(ns["X_te"])[:,1]):.3f}', flush=True)
