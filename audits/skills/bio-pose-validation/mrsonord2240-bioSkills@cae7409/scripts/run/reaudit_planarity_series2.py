"""
Extend the independent displacement series further to actually locate the
bust() aromatic_ring_flatness pass/fail transition (previous run topped out
at 0.46A physical displacement / 0.2252A measured deviation, never failing).
Same distinct perturbation (ring atom idx 7, not the fixer/auditor's idx of
ring[0]) pushed to larger physical steps.
"""
import numpy as np
from rdkit import Chem
from posebusters import PoseBusters

def aromatic_planarity(mol):
    deviations = []
    for ring in mol.GetRingInfo().AtomRings():
        ring_atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if not all(a.GetIsAromatic() for a in ring_atoms):
            continue
        coords = np.array([mol.GetConformer().GetAtomPosition(i) for i in ring])
        centroid = coords.mean(axis=0)
        centered = coords - centroid
        _, s, vh = np.linalg.svd(centered)
        normal = vh[-1]
        deviation = np.abs(centered @ normal).max()
        deviations.append(deviation)
    return max(deviations) if deviations else 0

base = Chem.MolFromMolFile('../data/mode1_fixed.sdf', removeHs=False)
conf0 = base.GetConformer()
coords0 = np.array([list(conf0.GetAtomPosition(i)) for i in range(base.GetNumAtoms())])

ring_info = base.GetRingInfo()
aromatic_ring = None
for ring in ring_info.AtomRings():
    if all(base.GetAtomWithIdx(a).GetIsAromatic() for a in ring):
        aromatic_ring = ring
        break

ring_coords = coords0[list(aromatic_ring)]
centroid = ring_coords.mean(axis=0)
centered = ring_coords - centroid
_, _, vh = np.linalg.svd(centered)
normal = vh[-1]

puck_atom = aromatic_ring[2]
bust_mol = PoseBusters(config='mol')

steps = [0.6, 0.9, 1.2, 1.5, 1.8, 2.2]
print(f"Displacing ring atom idx {puck_atom} along SVD normal (independent series 2)")
print(f"{'step_A':>8} {'skill_formula_A':>16} {'bust_aromatic_ring_flatness':>28}")
last_pass = None
first_fail = None
for step in steps:
    mol = Chem.Mol(base)
    c = mol.GetConformer()
    for i in range(mol.GetNumAtoms()):
        c.SetAtomPosition(i, coords0[i].tolist())
    p = coords0[puck_atom] + normal * step
    c.SetAtomPosition(puck_atom, p.tolist())

    skill_dev = aromatic_planarity(mol)
    path = f'../data/reaudit_puck2_{step:.2f}.sdf'
    w = Chem.SDWriter(path)
    w.write(mol)
    w.close()

    r = bust_mol.bust(mol_pred=path)
    flat = bool(r['aromatic_ring_flatness'].iloc[0])
    print(f"{step:8.2f} {skill_dev:16.4f} {str(flat):>28}")
    if flat:
        last_pass = (step, skill_dev)
    elif first_fail is None:
        first_fail = (step, skill_dev)

print()
print("Last passing (physical, skill-formula):", last_pass)
print("First failing (physical, skill-formula):", first_fail)
