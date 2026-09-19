"""Input 5 (Stress, regression): imatinib, full pipeline embed->optimize->prune->filter->Boltzmann."""
from rdkit import Chem
from rdkit.Chem import AllChem
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
    results = []
    mmff_props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant='MMFF94s')
    for cid in conf_ids:
        ff = AllChem.MMFFGetMoleculeForceField(mol, mmff_props, confId=cid)
        status = ff.Minimize(maxIts=1000)
        results.append({'conf_id': cid, 'energy': ff.CalcEnergy(), 'converged': status == 0})
    return results


def prune_conformers_rmsd(mol, conf_ids, rmsd_cutoff=0.5):
    keep = []
    for cid in conf_ids:
        is_unique = True
        for kept_cid in keep:
            rmsd = AllChem.GetBestRMS(mol, mol, cid, kept_cid)
            if rmsd < rmsd_cutoff:
                is_unique = False
                break
        if is_unique:
            keep.append(cid)
    return keep


def filter_by_energy(conf_ids, energies_by_id, window_kcal=10.0):
    min_e = min(energies_by_id.values())
    return [cid for cid in conf_ids if energies_by_id[cid] - min_e <= window_kcal]


def boltzmann_average(values, energies, T=300.0):
    energies = np.array(energies)
    kt = 0.001987 * T
    rel = energies - energies.min()
    w = np.exp(-rel / kt)
    w = w / w.sum()
    return float(np.sum(np.array(values) * w))


imatinib = 'Cc1ccc(NC(=O)c2ccc(CN3CCN(C)CC3)cc2)cc1Nc1nccc(-c2cccnc2)n1'
mol_check = Chem.MolFromSmiles(imatinib)
n_rot = AllChem.CalcNumRotatableBonds(mol_check)
n_conf = max(10, 5 * n_rot + 10)
print(f'Rotatable bonds: {n_rot}, n_conf heuristic: {n_conf}')

mol, ids = gen_conformers(imatinib, n_conf=n_conf)
print(f'Embedded: {len(ids)}/{n_conf}')
results = optimize_conformers(mol, ids)
converged = sum(1 for r in results if r['converged'])
print(f'Converged: {converged}/{len(results)}')
energies_by_id = {r['conf_id']: r['energy'] for r in results}

pruned = prune_conformers_rmsd(mol, ids, rmsd_cutoff=0.5)
print(f'After RMSD pruning (0.5A): {len(pruned)}')

windowed = filter_by_energy(pruned, energies_by_id, window_kcal=10.0)
print(f'After energy window (10 kcal/mol): {len(windowed)}')

from rdkit.Chem import Descriptors3D
asphericities = []
final_energies = []
for cid in windowed:
    Chem.rdMolTransforms.CanonicalizeConformer(mol.GetConformer(cid))
    asph = Descriptors3D.Asphericity(mol, confId=cid)
    asphericities.append(asph)
    final_energies.append(energies_by_id[cid])

boltz_avg = boltzmann_average(asphericities, final_energies)
simple_mean = float(np.mean(asphericities))
print(f'Boltzmann-avg asphericity: {boltz_avg:.4f}')
print(f'Simple mean asphericity: {simple_mean:.4f}')
