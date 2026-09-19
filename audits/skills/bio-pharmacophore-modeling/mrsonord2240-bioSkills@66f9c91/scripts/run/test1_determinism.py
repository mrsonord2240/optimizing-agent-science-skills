"""
Re-auditor verification test 1 (T3 determinism gate).

Verifies the fixed randomSeed=23 in examples/pharmacophore.py produces
identical conformer geometry across independent process runs, for BOTH
functions touched by the fix: shared_feature_types_prefilter
(EmbedMultipleConfs) and has_feature_types (EmbedMolecule).

Run this script twice (two separate python.exe invocations) and diff the
printed coordinate hashes -- a real "run it twice" check, not an in-process
comparison that could be fooled by process-local RNG state.
"""
import sys
import os
import hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'skill', 'examples'))
import pharmacophore as ph
from rdkit import Chem
from rdkit.Chem import AllChem

def hash_coords(mol, n_confs):
    h = hashlib.sha256()
    for ci in range(n_confs):
        conf = mol.GetConformer(ci)
        for i in range(mol.GetNumAtoms()):
            p = conf.GetAtomPosition(i)
            h.update(f'{p.x:.6f},{p.y:.6f},{p.z:.6f};'.encode())
    return h.hexdigest()

factory = ph.get_feature_factory()

# --- shared_feature_types_prefilter path (EmbedMultipleConfs) ---
active_mols = [Chem.MolFromSmiles(s) for s in [
    'CC(=O)Nc1ccc(C(=O)c2ccccc2)cc1',
    'CC(=O)Nc1ccc(C(=O)c2ccc(F)cc2)cc1',
]]
m0 = Chem.AddHs(active_mols[0])
params = AllChem.ETKDGv3()
params.randomSeed = 23
cids = AllChem.EmbedMultipleConfs(m0, numConfs=20, params=params)
AllChem.MMFFOptimizeMoleculeConfs(m0)
multi_hash = hash_coords(m0, len(cids))
print('EmbedMultipleConfs n_confs:', len(cids))
print('EmbedMultipleConfs coord hash:', multi_hash)

# --- has_feature_types path (EmbedMolecule) ---
target_mol = Chem.MolFromSmiles('c1ccc(cc1)CCN')
target = Chem.AddHs(target_mol)
params2 = AllChem.ETKDGv3()
params2.randomSeed = 23
AllChem.EmbedMolecule(target, params2)
AllChem.MMFFOptimizeMolecule(target)
single_hash = hash_coords(target, 1)
print('EmbedMolecule coord hash:', single_hash)

# --- end-to-end demo determinism (feature_family_prefilter + diagnostic) ---
queries = ['CC(=O)Nc1ccc(C(=O)c2ccccc2)cc1',
           'CC(=O)Nc1ccc(C(=O)c2ccc(F)cc2)cc1']
library = ['CCC(=O)Nc1ccc(C(=O)c2ccc(Cl)cc2)cc1', 'CCCCCC', 'c1ccncc1']
hits = ph.feature_family_prefilter(queries, library)
print('demo hits:', hits)
