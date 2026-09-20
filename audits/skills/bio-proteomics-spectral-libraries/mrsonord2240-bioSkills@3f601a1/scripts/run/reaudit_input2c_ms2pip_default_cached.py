import time
from psm_utils import PSM, PSMList
import ms2pip

psms = PSMList(psm_list=[
    PSM(peptidoform="LGGNEQVTR/2", spectrum_id="1"),
])
t0 = time.time()
result = ms2pip.predict_batch(psms, model="HCD")
t1 = time.time()
print(f"Elapsed with cached HCD2021 model: {t1-t0:.1f}s")
print(len(result), "results")
