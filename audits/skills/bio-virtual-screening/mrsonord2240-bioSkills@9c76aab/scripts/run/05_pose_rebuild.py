from pathlib import Path

from meeko import PDBQTMolecule, RDKitMolCreate

root = Path(r"F:\OpenScience\audits\bio-virtual-screening\data")
poses = root / "fresh1" / "poses.pdbqt"
out = root / "poses_rebuilt.sdf"
pdbqt_mol = PDBQTMolecule.from_file(str(poses), skip_typing=True)
mols = RDKitMolCreate.from_pdbqt_mol(pdbqt_mol)
assert mols and mols[0] is not None
assert mols[0].GetNumConformers() > 0
from rdkit import Chem
writer = Chem.SDWriter(str(out))
for mol in mols:
    if mol is not None:
        writer.write(mol)
writer.close()
assert out.exists() and out.stat().st_size > 0
print(f"POSE_REBUILD=PASS mols={len(mols)} conformers={mols[0].GetNumConformers()}")
