"""Input 4, corrected data generation: real theoretical y-ion m/z via pyteomics
instead of placeholder fragment masses, which is what let OpenSwathDecoyGenerator
succeed (see run/input4_format_conversion.py for the first, failing attempt).
"""
import pandas as pd
import numpy as np
from pyteomics import mass


def y_ion_mz(seq, i, charge=1):
    frag = seq[-i:]
    return mass.fast_mass(frag, ion_type='y', charge=charge)


rows = []
rng = np.random.default_rng(3)


def add_peptide(seq, charge, protein):
    prec_mz = mass.fast_mass(seq, charge=charge)
    for i in range(1, 7):
        rows.append({
            'PrecursorMz': prec_mz, 'ProductMz': y_ion_mz(seq, i, 1),
            'Tr_recalibrated': 25.0 + rng.uniform(-1, 1),
            'transition_name': f'{seq}_{charge}_y{i}', 'CE': 30,
            'LibraryIntensity': rng.uniform(1000, 10000),
            'transition_group_id': f'{seq}_{charge}', 'decoy': 0,
            'PeptideSequence': seq, 'ProteinName': protein,
            'FullUniModPeptideName': seq, 'PrecursorCharge': charge,
            'FragmentType': 'y', 'FragmentSeriesNumber': i, 'FragmentCharge': 1,
            'Annotation': f'y{i}^1',
        })


add_peptide('LGGNEQVTR', 2, 'P1')
add_peptide('VEATFGVDESNAK', 2, 'P2')
df = pd.DataFrame(rows)
p = r'F:\OpenScience\audits\bio-proteomics-spectral-libraries\data\input4_library.tsv'
df.to_csv(p, sep='\t', index=False)
print(df[['PeptideSequence', 'PrecursorMz', 'ProductMz', 'Annotation']])
