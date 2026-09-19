"""
Construct deliberately implausible poses from the real Vina mode-1 docked
pose, to check that PoseBusters (as the Skill directs) correctly flags them
as PB-invalid and identifies the right failed check.

1. clash_pose.sdf   — ligand translated ~2.5 A into the receptor's binding-site
                       wall, causing severe protein-ligand overlap.
2. stretched_bond.sdf — the N-C(amidinium) bond stretched from ~1.33 A to ~2.6 A
                         (2x), everything else identical.
3. puckered_ring.sdf  — one aromatic ring atom displaced 0.6 A out of the ring
                         plane (aromatic_ring_flatness cutoff is 0.25 A).
"""
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

mol = Chem.MolFromMolFile('../data/mode1_fixed.sdf', removeHs=False)
conf = mol.GetConformer()
coords = np.array([list(conf.GetAtomPosition(i)) for i in range(mol.GetNumAtoms())])

# --- 1. Clash pose: push the whole ligand toward the catalytic triad region.
# The 3PTB active site residues cluster near approx (-4, 15, 17) based on the
# benzamidine co-crystal position; shift the ligand centroid deep into the
# protein wall by translating toward a heavy-atom-dense direction.
clash = Chem.Mol(mol)
clash_conf = clash.GetConformer()
shift = np.array([3.0, -1.5, -2.0])  # into the pocket wall, not just off-site
for i in range(clash.GetNumAtoms()):
    p = coords[i] + shift
    clash_conf.SetAtomPosition(i, p.tolist())
w = Chem.SDWriter('../data/clash_pose.sdf')
w.write(clash)
w.close()
print('wrote clash_pose.sdf, centroid shift', shift)

# --- 2. Stretched bond: find the amidinium C=N bond (atom idx 1-2 template:
# N=C(=NH2+)... locate by symbol pattern) and pull atom along the bond vector.
stretched = Chem.Mol(mol)
sconf = stretched.GetConformer()
# find a N-C bond within the amidinium group (non-aromatic, non-ring)
target_bond = None
for b in mol.GetBonds():
    a1, a2 = b.GetBeginAtom(), b.GetEndAtom()
    if {a1.GetSymbol(), a2.GetSymbol()} == {'C', 'N'} and not b.GetIsAromatic() and not a1.GetIsAromatic() and not a2.GetIsAromatic():
        target_bond = (a1.GetIdx(), a2.GetIdx())
        break
assert target_bond is not None, "no amidinium C-N bond found"
i1, i2 = target_bond
p1 = np.array(list(sconf.GetAtomPosition(i1)))
p2 = np.array(list(sconf.GetAtomPosition(i2)))
direction = (p2 - p1)
orig_len = np.linalg.norm(direction)
direction_unit = direction / orig_len
new_len = orig_len * 2.0  # ~2.6 A, way outside 0.75-1.25x bounds
new_p2 = p1 + direction_unit * new_len
sconf.SetAtomPosition(i2, new_p2.tolist())
w = Chem.SDWriter('../data/stretched_bond.sdf')
w.write(stretched)
w.close()
print(f'wrote stretched_bond.sdf, bond {i1}-{i2} stretched {orig_len:.3f}A -> {new_len:.3f}A')

# --- 3. Puckered aromatic ring: displace one ring atom 0.6 A off-plane.
puckered = Chem.Mol(mol)
pconf = puckered.GetConformer()
ring_info = puckered.GetRingInfo()
aromatic_ring = None
for ring in ring_info.AtomRings():
    if all(puckered.GetAtomWithIdx(a).GetIsAromatic() for a in ring):
        aromatic_ring = ring
        break
assert aromatic_ring is not None, "no aromatic ring found"
ring_coords = np.array([list(pconf.GetAtomPosition(i)) for i in aromatic_ring])
centroid = ring_coords.mean(axis=0)
centered = ring_coords - centroid
_, _, vh = np.linalg.svd(centered)
normal = vh[-1]
puck_atom = aromatic_ring[0]
p = np.array(list(pconf.GetAtomPosition(puck_atom))) + normal * 0.6
pconf.SetAtomPosition(puck_atom, p.tolist())
w = Chem.SDWriter('../data/puckered_ring.sdf')
w.write(puckered)
w.close()
print(f'wrote puckered_ring.sdf, ring atom {puck_atom} displaced 0.6A off-plane')
