"""Input 9 (NEW, edge case): RMSD pruning and energy-window filtering on degenerate inputs --
empty conformer list, single conformer, and all-identical energies (Boltzmann weighting div check).
None of the original 7 audit inputs exercised these helper functions in isolation on boundary data."""
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np


def prune_conformers_rmsd(mol, conf_ids, rmsd_cutoff=0.5):
    n = len(conf_ids)
    keep = []
    for i, cid in enumerate(conf_ids):
        is_unique = True
        for kept_cid in keep:
            rmsd = AllChem.GetBestRMS(mol, mol, cid, kept_cid)
            if rmsd < rmsd_cutoff:
                is_unique = False
                break
        if is_unique:
            keep.append(cid)
    return keep


def filter_by_energy(mol, conf_ids, energies, window_kcal=10.0):
    min_e = min(energies)
    keep = []
    for cid, e in zip(conf_ids, energies):
        if e - min_e <= window_kcal:
            keep.append(cid)
    return keep


def boltzmann_weights(energies, T=300.0):
    energies = np.array(energies)
    kt = 0.001987 * T
    rel = energies - energies.min()
    w = np.exp(-rel / kt)
    return w / w.sum()


phenol = 'c1ccccc1O'
mol = Chem.AddHs(Chem.MolFromSmiles(phenol))
params = AllChem.ETKDGv3()
params.randomSeed = 42
ids = list(AllChem.EmbedMultipleConfs(mol, numConfs=3, params=params))

print('--- Case A: empty conformer list ---')
print(f'prune_conformers_rmsd(mol, []) = {prune_conformers_rmsd(mol, [])}')
try:
    print(f'filter_by_energy(mol, [], []) = {filter_by_energy(mol, [], [])}')
except ValueError as e:
    print(f'filter_by_energy on empty list raised: {e} (min() of empty sequence -- undocumented failure mode)')

print('\n--- Case B: single conformer ---')
single_id = ids[:1]
print(f'prune_conformers_rmsd single: {prune_conformers_rmsd(mol, single_id)}')
print(f'filter_by_energy single: {filter_by_energy(mol, single_id, [5.0])}')

print('\n--- Case C: all-identical energies (Boltzmann weights should be uniform, no div-by-zero) ---')
identical_energies = [10.0, 10.0, 10.0]
w = boltzmann_weights(identical_energies)
print(f'Weights: {w}')
print(f'Sum to 1.0: {np.isclose(w.sum(), 1.0)}')
print(f'All equal (uniform weighting when no energy difference): {np.allclose(w, w[0])}')
