"""Fresh calibration threshold guard test for the inline fit_irt_to_rt workflow."""
import json
import numpy as np
from scipy import stats

R2_MIN = 0.95
def fit_irt_to_rt(anchor_irt, observed_rt):
    slope, intercept, r, _, _ = stats.linregress(anchor_irt, observed_rt)
    if r ** 2 < R2_MIN:
        raise ValueError(f"iRT fit R^2={r**2:.3f} < {R2_MIN}; gradient may be nonlinear, use LOWESS")
    return lambda irt: slope * irt + intercept

x = np.arange(11, dtype=float)
good = 4 + 0.2 * x
predict = fit_irt_to_rt(x, good)
assert abs(float(predict(10)) - 6.0) < 1e-10
bad = np.array([5, 13, 8, 21, 7, 24, 10, 20, 9, 23, 6], dtype=float)
try:
    fit_irt_to_rt(x, bad)
except ValueError as error:
    message = str(error)
else:
    raise AssertionError("low-R2 calibration was accepted")
assert "use LOWESS" in message
print(json.dumps({"good_prediction_at_irt10": round(float(predict(10)), 4), "low_r2_guard": message}))
