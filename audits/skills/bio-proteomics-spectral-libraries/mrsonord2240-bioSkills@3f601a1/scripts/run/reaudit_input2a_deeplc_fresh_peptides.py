"""
Independent re-audit run of the SKILL.md deeplc snippet (deeplc.predict_and_calibrate),
using CiRT peptides as calibration anchors -- a different peptide set from the fixer's
IRT_PEPTIDES-based verification -- and different held-out peptides to predict.
"""
from psm_utils import PSM, PSMList
import deeplc

# CiRT endogenous peptide set (subset), with plausible synthetic observed RT (minutes)
# distinct from the fixer's Biognosys IRT_PEPTIDES calibration set.
calibration_pairs = [
    ("TASEFDSAIAQDK", 22.4),
    ("SNAQLIVK", 8.1),
    ("VVDLMAHMASK", 25.9),
    ("EDAANNYARGHYTIGK", 30.2),
    ("GVLGYTEDAVVSSDFLGDSHSSIFDASAGIQLSPK", 44.8),
    ("SFANQPLEVVYSK", 26.7),
    ("ADTLDPALLRPGR", 21.1),
    ("YFPTQALNFAFK", 34.5),
    ("SAPSTGGVK", 5.9),
    ("HVFGQAAK", 6.3),
    ("VLDSVTLQLK", 20.6),
]

held_out = ["LGGNEQVTR", "GTFIIDPGGVIR", "DGLDAASYYAPVR"]  # distinct from calibration set

cal_psms = PSMList(psm_list=[
    PSM(peptidoform=seq + "/2", spectrum_id=str(i), retention_time=rt)
    for i, (seq, rt) in enumerate(calibration_pairs)
])
pred_psms = PSMList(psm_list=[
    PSM(peptidoform=seq + "/2", spectrum_id=str(i))
    for i, seq in enumerate(held_out)
])

result = deeplc.predict_and_calibrate(pred_psms, psm_list_reference=cal_psms)
print("Type of result:", type(result))
print(result)
for pep, rt in zip(held_out, result):
    print(f"{pep}: predicted/calibrated RT = {rt}")
