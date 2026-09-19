# Input 5 (Stress): "For imatinib, generate an ETKDGv3 ensemble sized by the
# skill's own rotatable-bond heuristic, MMFF94-optimize, RMSD-prune at 0.5 A,
# filter to a 10 kcal/mol energy window, then report the Boltzmann-averaged
# asphericity across the surviving ensemble."
# Chains: ETKDGv3 embed -> Force-Field Optimization -> RMSD Pruning ->
# Energy Window Filtering -> Boltzmann Averaging of Properties, all per SKILL.md.

from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors3D
import numpy as np

def gen_conformers(smiles, n_conf, seed=42):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f'Invalid SMILES: {smiles!r}')
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    params.useRandomCoords = True
    params.maxIterations = 1000
    ids = AllChem.EmbedMultipleConfs(mol, numConfs=n_conf, params=params)
    return mol, list(ids)

def optimize_conformers(mol, conf_ids):
    mmff_props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant='MMFF94s')
    conf_data = []
    for cid in conf_ids:
        ff = AllChem.MMFFGetMoleculeForceField(mol, mmff_props, confId=cid)
        status = ff.Minimize(maxIts=1000)
        conf_data.append((cid, ff.CalcEnergy(), status == 0))
    return conf_data

def prune_rmsd(mol, conf_data, rmsd_cutoff=0.5):
    keep = []
    for cid, e, conv in conf_data:
        is_unique = True
        for kept_cid, _, _ in keep:
            rmsd = AllChem.GetBestRMS(mol, mol, cid, kept_cid)
            if rmsd < rmsd_cutoff:
                is_unique = False
                break
        if is_unique:
            keep.append((cid, e, conv))
    return keep

def filter_energy_window(conf_data, window_kcal=10.0):
    min_e = min(e for _, e, _ in conf_data)
    return [(cid, e, conv) for cid, e, conv in conf_data if (e - min_e) <= window_kcal]

def boltzmann_average(values, energies, T=300.0):
    energies = np.array(energies)
    kt = 0.001987 * T
    rel = energies - energies.min()
    w = np.exp(-rel / kt)
    w = w / w.sum()
    return float(np.sum(np.array(values) * w))

imatinib = 'Cc1ccc(NC(=O)c2ccc(CN3CCN(C)CC3)cc2)cc1Nc1nccc(-c2cccnc2)n1'
mol_flat = Chem.MolFromSmiles(imatinib)
n_rot = Chem.rdMolDescriptors.CalcNumRotatableBonds(mol_flat)
n_conf = max(10, 5 * n_rot + 10)  # SKILL.md "Conformer ensemble too small" heuristic
print(f'Imatinib rotatable bonds: {n_rot} -> n_conf heuristic = {n_conf}')

mol, ids = gen_conformers(imatinib, n_conf=n_conf, seed=42)
print(f'Embedded: {len(ids)}/{n_conf}')

conf_data = optimize_conformers(mol, ids)
n_converged = sum(1 for _, _, c in conf_data if c)
print(f'Optimized: {len(conf_data)}, converged: {n_converged}/{len(conf_data)}')

pruned = prune_rmsd(mol, conf_data, rmsd_cutoff=0.5)
print(f'After RMSD pruning (0.5 A): {len(pruned)}/{len(conf_data)} survive')

windowed = filter_energy_window(pruned, window_kcal=10.0)
print(f'After 10 kcal/mol energy window: {len(windowed)}/{len(pruned)} survive')

# Boltzmann-averaged asphericity across the surviving ensemble
asphericities = []
for cid, e, conv in windowed:
    val = Descriptors3D.Asphericity(mol, confId=cid)
    asphericities.append(val)
energies_kept = [e for _, e, _ in windowed]
avg_asph = boltzmann_average(asphericities, energies_kept)
print(f'Per-conformer asphericity range: {min(asphericities):.4f} to {max(asphericities):.4f}')
print(f'Boltzmann-averaged asphericity: {avg_asph:.4f}')
print(f'Simple mean asphericity (for comparison): {np.mean(asphericities):.4f}')
