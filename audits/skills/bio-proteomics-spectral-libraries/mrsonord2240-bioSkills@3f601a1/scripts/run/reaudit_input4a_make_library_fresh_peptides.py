"""
Re-audit input: build a fresh transition list (different peptides from the fixer's
input4_library.tsv) to independently verify the OpenSwathDecoyGenerator fix.

Peptides chosen: two tryptic peptides NOT used in the original fix verification
(fixer used LGGNEQVTR-family peptides per the audit's input4). Using different
sequences here: AGGSSEPVTGLDAK-family swapped for a distinct pair.
"""
import sys
sys.path.insert(0, r"F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\Scripts")
from pyteomics import mass

peptides = ["YILAGVENSK", "TPVISGGPYEYR"]  # CiRT-style peptides, distinct from fixer's set
charge = 2

def y_ion_mz(seq, i, chg=1):
    return mass.fast_mass(seq[-i:], ion_type='y', charge=chg)

def precursor_mz(seq, chg):
    return mass.fast_mass(seq, charge=chg)

rows_placeholder = []
rows_real = []
for pep in peptides:
    prec_mz = precursor_mz(pep, charge)
    for i in [2, 3]:
        # placeholder version: fake round-number ProductMz, NO Annotation column value (blank)
        rows_placeholder.append({
            "PrecursorMz": prec_mz, "ProductMz": 500.0 + i, "Tr_recalibrated": 30.0,
            "PeptideSequence": pep, "ProteinName": f"PROT_{pep[:3]}",
            "LibraryIntensity": 10000, "transition_name": f"{pep}_{i}",
            "PrecursorCharge": charge, "FragmentType": "y", "FragmentCharge": 1,
            "FragmentSeriesNumber": i, "Annotation": "",
        })
        # real version: real theoretical y-ion m/z + literal Annotation
        rows_real.append({
            "PrecursorMz": prec_mz, "ProductMz": y_ion_mz(pep, i), "Tr_recalibrated": 30.0,
            "PeptideSequence": pep, "ProteinName": f"PROT_{pep[:3]}",
            "LibraryIntensity": 10000, "transition_name": f"{pep}_{i}",
            "PrecursorCharge": charge, "FragmentType": "y", "FragmentCharge": 1,
            "FragmentSeriesNumber": i, "Annotation": f"y{i}^1",
        })

import pandas as pd
cols = ["PrecursorMz", "ProductMz", "Tr_recalibrated", "PeptideSequence", "ProteinName",
        "LibraryIntensity", "transition_name", "PrecursorCharge", "FragmentType",
        "FragmentCharge", "FragmentSeriesNumber", "Annotation"]
pd.DataFrame(rows_placeholder)[cols].to_csv("placeholder_library.tsv", sep="\t", index=False)
pd.DataFrame(rows_real)[cols].to_csv("real_library.tsv", sep="\t", index=False)
print("wrote placeholder_library.tsv and real_library.tsv")
print(pd.DataFrame(rows_real)[cols])
