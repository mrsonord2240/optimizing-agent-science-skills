# Input 4 (Variant B): "Sample macrocycle conformers for a 14-membered
# cyclic ketone using macrocycle-aware ETKDGv3 settings."
# Following SKILL.md "Macrocycle Handling" section verbatim (macrocycle_conformers).

from rdkit import Chem
from rdkit.Chem import AllChem

def macrocycle_conformers(smiles, n_conf=200, seed=42):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f'Invalid SMILES: {smiles!r}')
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    params.useRandomCoords = True
    params.useMacrocycleTorsions = True
    params.useSmallRingTorsions = True
    params.maxIterations = 5000
    ids = list(AllChem.EmbedMultipleConfs(mol, numConfs=n_conf, params=params))
    if not ids:
        raise RuntimeError(f'No macrocycle conformers embedded for {smiles!r}')
    return mol, ids

# 14-membered carbocyclic ketone (cyclotetradecanone) -- a genuine macrocycle
# (>=12-atom ring), used here as a stand-in for a drug-like macrocycle so the
# ring-size claim can be verified directly rather than trusted from memory.
smiles = 'O=C1CCCCCCCCCCCCC1'
mol_check = Chem.MolFromSmiles(smiles)
ring_sizes = [len(r) for r in mol_check.GetRingInfo().AtomRings()]
print(f'Parsed ring sizes: {ring_sizes} (macrocycle threshold is >=12 atoms)')

mol, ids = macrocycle_conformers(smiles, n_conf=50, seed=42)
print(f'Macrocycle conformers embedded: {len(ids)} (requested 50)')

# Optimize + report energy spread, as the workflow implies downstream use
mmff_props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant='MMFF94s')
energies = []
converged_flags = []
for cid in ids:
    ff = AllChem.MMFFGetMoleculeForceField(mol, mmff_props, confId=cid)
    status = ff.Minimize(maxIts=1000)
    energies.append(ff.CalcEnergy())
    converged_flags.append(status == 0)
print(f'Optimized: {len(energies)}, converged: {sum(converged_flags)}/{len(converged_flags)}')
print(f'Energy range: {min(energies):.4f} to {max(energies):.4f} kcal/mol')
print(f'Unique energies (rounded 2dp): {len(set(round(e,2) for e in energies))} '
      f'(macrocycle should show real conformational diversity, unlike rigid aspirin)')

# Compare against non-macrocycle-aware settings on the same molecule
params_default = AllChem.ETKDGv3()
params_default.randomSeed = 42
params_default.useRandomCoords = True
params_default.maxIterations = 5000
mol2 = Chem.AddHs(Chem.MolFromSmiles(smiles))
ids2 = list(AllChem.EmbedMultipleConfs(mol2, numConfs=50, params=params_default))
print(f'Default (non-macrocycle-aware) embedding: {len(ids2)}/50 succeeded')
