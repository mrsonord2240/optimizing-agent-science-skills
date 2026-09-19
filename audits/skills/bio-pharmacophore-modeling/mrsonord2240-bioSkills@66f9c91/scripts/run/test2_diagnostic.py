"""
Re-auditor verification test 2.

Independently reproduces the fixer's claim: feature_family_prefilter now
prints, for a real rejected molecule, which query feature(s) it is missing.
Uses real drug SMILES (indinavir, saquinavir as queries; ritonavir, caffeine,
metformin, aspirin, acetaminophen as library) -- an independent molecule
selection from the fixer's own verification (not copy-pasted from the fix
log), to avoid confirming only the exact case the fixer already checked.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'skill', 'examples'))
import pharmacophore as ph

indinavir = 'CC(C)(C)NC(=O)C1CN(Cc2cccnc2)CCN1CC(O)CC(Cc1ccccc1)C(=O)NC1c2ccccc2CC1O'
saquinavir = 'CC(C)(C)NC(=O)C1CC2CCCCC2CN1CC(O)C(Cc1ccccc1)NC(=O)C(CC(N)=O)NC(=O)c1ccc2ccccc2n1'
ritonavir = 'CC(C)C1=NC(=CS1)CN(C)C(=O)NC(C(C)C)C(=O)NC(CC1=CC=CC=C1)CC(C(CC1=CC=CC=C1)NC(=O)OCC1=CN=CS1)O'
caffeine = 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C'
metformin = 'CN(C)C(=N)NC(=N)N'
aspirin = 'CC(=O)OC1=CC=CC=C1C(=O)O'
acetaminophen = 'CC(=O)NC1=CC=C(C=C1)O'

queries = [indinavir, saquinavir]
library = [ritonavir, caffeine, metformin, aspirin, acetaminophen]

hits = ph.feature_family_prefilter(queries, library)
print('QUERIES: indinavir, saquinavir (real HIV-1 protease inhibitors)')
print('LIBRARY: ritonavir (real HIV-1 PI, same class), caffeine, metformin, aspirin, acetaminophen (real unrelated drugs)')
print('HITS:', hits)
print('ritonavir in hits:', ritonavir in hits)
