import sys
print("starting deeplc test", flush=True)
from psm_utils import PSM, PSMList
import deeplc
print("imports ok", flush=True)
psms = PSMList(psm_list=[PSM(peptidoform="LGGNEQVTR/2", spectrum_id="s1"),
                          PSM(peptidoform="VEATFGVDESNAK/2", spectrum_id="s2")])
print("calling deeplc.predict", flush=True)
rt = deeplc.predict(psms)
print("done:", rt, flush=True)
