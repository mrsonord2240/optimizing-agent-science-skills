import time
from psm_utils import PSM, PSMList
import ms2pip

psms = PSMList(psm_list=[
    PSM(peptidoform="SAMPLEPEPTIDEK/2", spectrum_id="1"),
    PSM(peptidoform="ANALYTICALPEPTK/2", spectrum_id="2"),
])

t0 = time.time()
result = ms2pip.predict_batch(psms, model="HCD2019", model_dir="ms2pip_fresh_model_dir2")
t1 = time.time()
print(f"Elapsed: {t1 - t0:.1f}s")
for r in result:
    print("peptidoform:", r.psm.peptidoform if hasattr(r, 'psm') else '?')
    print("  n fragment predictions:", len(r.theoretical_mz) if hasattr(r, 'theoretical_mz') else 'n/a')
    print("  sample predicted intensities:", (r.predicted_intensity[:5] if hasattr(r, 'predicted_intensity') else r))
