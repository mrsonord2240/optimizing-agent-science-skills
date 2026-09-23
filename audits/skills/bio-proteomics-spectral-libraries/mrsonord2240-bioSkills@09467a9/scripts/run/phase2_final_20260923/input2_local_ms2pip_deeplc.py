"""Fresh local MS2PIP intensity and DeepLC calibrated-RT validation.

Usage: run with the isolated ms2pip-deeplc Python environment.
"""
import json
import deeplc
import ms2pip
from psm_utils import PSM, PSMList

anchors = [("LGGNEQVTR", 5.2), ("GAGSSEPVTGLDAK", 7.1), ("VEATFGVDESNAK", 9.3),
           ("YILAGVENSK", 11.5), ("TPVISGGPYEYR", 13.8), ("TPVITGAPYEYR", 15.0),
           ("DGLDAASYYAPVR", 16.9), ("ADVTPADFSEWSK", 18.6), ("GTFIIDPGGVIR", 21.1),
           ("GTFIIDPAAVIR", 23.4), ("LFLQFGAQGSPFLK", 26.7)]
cal = PSMList(psm_list=[PSM(peptidoform=s, spectrum_id=f"c{i}", retention_time=rt)
                        for i, (s, rt) in enumerate(anchors)])
targets = PSMList(psm_list=[PSM(peptidoform=s, spectrum_id=f"t{i}")
                            for i, s in enumerate(["ELGQSGVDTYLQTK", "DSTLIMQLLR"])])
rt = deeplc.predict_and_calibrate(targets, psm_list_reference=cal)
assert len(rt) == 2 and all(float(x) > 0 for x in rt)
psms = PSMList(psm_list=[PSM(peptidoform="LGGNEQVTR/2", spectrum_id="ms2pip")])
result = ms2pip.predict_batch(psms, model="HCD2019")
first = next(iter(result))
intensities = getattr(first, "predicted_intensity", None)
assert intensities is not None and len(intensities) > 0
print(json.dumps({"deeplc_module_api": hasattr(deeplc, "predict_and_calibrate"),
                  "deeplc_class_absent": not hasattr(deeplc, "DeepLC"), "calibrated_rt": [round(float(x), 4) for x in rt],
                  "ms2pip_result_type": type(first).__name__, "ms2pip_intensity_count": len(intensities)}))
