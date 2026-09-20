"""Input 4 (Variant B): convert the merged library (from build_library.py) into
an OpenSWATH-compatible transition TSV, then use the OpenMS CLI to convert to
TraML and generate decoys with OpenSwathDecoyGenerator -- exercising the
Skill's documented "format conversion ... generate decoys for OpenSWATH" step
and its warning that "DIA-NN and Spectronaut generate their own, so do not
supply both."
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(3)

def make_transitions(seq, charge, protein, n, base_prec_mz, base_frag_mz):
    return pd.DataFrame({
        'PrecursorMz': base_prec_mz,
        'ProductMz': base_frag_mz + np.arange(n) * 12.3,
        'Tr_recalibrated': 25.0 + rng.uniform(-1, 1),
        'transition_name': [f'{seq}_{charge}_y{i+1}' for i in range(n)],
        'CE': 30,
        'LibraryIntensity': rng.uniform(1000, 10000, n),
        'transition_group_id': f'{seq}_{charge}',
        'decoy': 0,
        'PeptideSequence': seq,
        'ProteinName': protein,
        'FullUniModPeptideName': seq,
        'PrecursorCharge': charge,
        'FragmentType': 'y',
        'FragmentSeriesNumber': np.arange(1, n + 1),
        'FragmentCharge': 1,
    })

lib = pd.concat([
    make_transitions('LGGNEQVTR', 2, 'P1', 6, 511.27, 175.12),
    make_transitions('VEATFGVDESNAK', 2, 'P2', 6, 683.83, 233.16),
], ignore_index=True)

out_tsv = r"F:\OpenScience\audits\bio-proteomics-spectral-libraries\data\input4_library.tsv"
lib.to_csv(out_tsv, sep='\t', index=False)
print('wrote', out_tsv, 'rows=', len(lib))
