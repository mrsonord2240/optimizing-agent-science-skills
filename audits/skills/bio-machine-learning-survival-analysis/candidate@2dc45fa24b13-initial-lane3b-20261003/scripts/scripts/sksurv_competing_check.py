"""SKILL.md model taxonomy says Random Survival Forest handles competing risks ('Yes (per-cause CIF)'). Check the scikit-survival
RandomSurvivalForest the Skill uses: does it expose any cause-specific / cumulative-incidence interface, or accept a multi-cause target?"""
import numpy as np, warnings
import sksurv
from sksurv.ensemble import RandomSurvivalForest, GradientBoostingSurvivalAnalysis
from sksurv.util import Surv
import sksurv.metrics as sm
names = [n for n in dir(RandomSurvivalForest) if any(k in n.lower() for k in ('cif', 'incidence', 'cause', 'compet'))]
print("scikit-survival", sksurv.__version__, "| RSF attributes mentioning cif/incidence/cause/competing:", names)
print("sksurv.metrics competing-risk functions:", [n for n in dir(sm) if any(k in n.lower() for k in ('cif', 'incidence', 'compet', 'cause'))])
print("sksurv.metrics public:", [n for n in dir(sm) if not n.startswith('_')])
rng = np.random.default_rng(0); X = rng.normal(size=(200, 3)); cause = rng.integers(0, 3, 200); t = rng.exponential(1, 200)
try:
    RandomSurvivalForest(n_estimators=10).fit(X, np.rec.fromarrays([cause, t], names=['event', 'time']))
    print("accepted a 3-valued cause column silently")
except Exception as e:
    print("multi-cause target rejected:", type(e).__name__, str(e)[:120])
