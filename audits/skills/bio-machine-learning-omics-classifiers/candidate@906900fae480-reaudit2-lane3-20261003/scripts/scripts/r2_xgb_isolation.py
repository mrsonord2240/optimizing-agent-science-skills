"""OC-010: test split plays no part in choosing rounds / learning rate; warning fires at best round 0; determinism.
Executes the shipped rf_xgboost_classifier.py source via exec with controlled edits (copies of the text, Skill bytes untouched).
Usage: python r2_xgb_isolation.py <Skill dir> <case>   case: base | perturb | n300 | lr"""
import sys, io, contextlib, warnings, hashlib, numpy as np
skill, case = sys.argv[1], sys.argv[2]
warnings.simplefilter('error', FutureWarning)
src = open(skill + '/scripts/rf_xgboost_classifier.py', encoding='utf-8').read()
split_end = "X_tr, X_val, y_tr, y_val = train_test_split(X_dev, y_dev, test_size=0.3, stratify=y_dev, random_state=0)"
assert split_end in src
if case == 'perturb':      # destroy the test split completely after the split: random features and shuffled labels
    src = src.replace(split_end, split_end + "\nX_te = np.random.default_rng(99).normal(size=X_te.shape) * 5; y_te = np.random.default_rng(98).permutation(y_te)")
if case == 'n300':
    assert "n, p, k = 600, 1500, 25" in src; src = src.replace("n, p, k = 600, 1500, 25", "n, p, k = 300, 1500, 25")
if case == 'lr':           # learning-rate choice on validation logloss only (no test split involved)
    from xgboost import XGBClassifier
    ns = {}; head = src.split("models = {")[0]
    exec(head, ns)
    for lr in (0.03, 0.1, 0.3):
        m = XGBClassifier(n_estimators=2000, learning_rate=lr, max_depth=4, subsample=0.8, colsample_bytree=0.5, early_stopping_rounds=50, eval_metric='logloss', random_state=0)
        m.fit(ns['X_tr'], ns['y_tr'], eval_set=[(ns['X_val'], ns['y_val'])], verbose=False)
        print(f'lr {lr}: best round {m.best_iteration}, validation logloss {m.best_score:.3f}')
    sys.exit()
ns = {'__name__': '__main__'}; buf = io.StringIO()
with contextlib.redirect_stdout(buf): exec(compile(src, 'rf_xgboost_classifier.py', 'exec'), ns)
out = buf.getvalue(); print(out)
x = ns['models']['xgboost']; pv = x.predict_proba(ns['X_val'])[:, 1]; ptr = x.predict_proba(ns['X_tr'])[:, 1]
print(f'CASE {case}: best_iteration {x.best_iteration} best_score {x.best_score:.6f} val-pred sha {hashlib.sha256(pv.tobytes()).hexdigest()[:16]} train-pred sha {hashlib.sha256(ptr.tobytes()).hexdigest()[:16]} warning_line_present {"WARNING: best round is 0" in out}')
