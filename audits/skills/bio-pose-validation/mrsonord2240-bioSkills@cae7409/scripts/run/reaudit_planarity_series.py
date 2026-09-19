"""
Independent re-auditor check on aromatic_planarity() cutoff claim.
Deliberately different from both the original auditor's puck_*.sdf series
(displaced ring atom 0, steps 0.6/1.0/1.5/2.0A along the ring SVD normal)
and the fixer's bisection. Here: displace a DIFFERENT ring atom (index 2 of
the aromatic ring, not index 0), using a finer step series that brackets
the documented 0.25A cutoff and the fixer's claimed 0.29-0.45A window:
0.15, 0.22, 0.30, 0.38, 0.46 A.
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
assert aromatic_ring is not None

ring_coords = coords0[list(aromatic_ring)]
centroid = ring_coords.mean(axis=0)
centered = ring_coords - centroid
_, _, vh = np.linalg.svd(centered)
normal = vh[-1]

puck_atom = aromatic_ring[2]  # different atom than fixer/auditor (idx 0)

bust_mol = PoseBusters(config='mol')

steps = [0.15, 0.22, 0.30, 0.38, 0.46]
print(f"Displacing ring atom idx {puck_atom} (of ring {aromatic_ring}) along SVD normal")
print(f"{'step_A':>8} {'skill_formula_A':>16} {'bust_aromatic_ring_flatness':>28}")
for step in steps:
    mol = Chem.Mol(base)
    c = mol.GetConformer()
    for i in range(mol.GetNumAtoms()):
        c.SetAtomPosition(i, coords0[i].tolist())
    p = coords0[puck_atom] + normal * step
    c.SetAtomPosition(puck_atom, p.tolist())

    skill_dev = aromatic_planarity(mol)

    path = f'../data/reaudit_puck_{step:.2f}.sdf'
    w = Chem.SDWriter(path)
    w.write(mol)
    w.close()

    r = bust_mol.bust(mol_pred=path)
    flat = bool(r['aromatic_ring_flatness'].iloc[0])
    print(f"{step:8.2f} {skill_dev:16.4f} {str(flat):>28}")
