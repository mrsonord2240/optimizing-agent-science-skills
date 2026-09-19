import sys
print("starting ms2pip test", flush=True)
from psm_utils import PSM, PSMList
import ms2pip
print("imports ok", flush=True)
psms = PSMList(psm_list=[PSM(peptidoform="LGGNEQVTR/2", spectrum_id="s1")])
print("calling predict_batch", flush=True)
results = ms2pip.predict_batch(psms, model="HCD")
print("done, n results:", len(results), flush=True)
for r in results:
    print(r.psm.peptidoform, r.theoretical_mz, r.predicted_intensity)
