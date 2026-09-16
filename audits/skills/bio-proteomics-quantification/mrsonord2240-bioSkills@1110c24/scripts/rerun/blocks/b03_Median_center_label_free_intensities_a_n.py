import numpy as np
import pandas as pd

log_int = np.log2(intensities.replace(0, np.nan))    # MaxQuant writes 0 for missing; log2(0) = -inf
sample_medians = log_int.median(axis=0)
normalized = log_int - sample_medians + sample_medians.median()
