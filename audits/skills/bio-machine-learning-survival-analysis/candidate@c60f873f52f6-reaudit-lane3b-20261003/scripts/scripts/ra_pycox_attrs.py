import pycox, torch
from pycox.models import DeepHit, DeepHitSingle, CoxPH
print("pycox", pycox.__version__, "DeepHit.predict_cif:", hasattr(DeepHit, "predict_cif"), "CoxPH.compute_baseline_hazards:", hasattr(CoxPH, "compute_baseline_hazards"), "predict_surv_df:", hasattr(CoxPH, "predict_surv_df"))
