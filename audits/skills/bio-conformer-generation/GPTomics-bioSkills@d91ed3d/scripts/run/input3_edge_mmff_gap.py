# Input 3 (Edge): "Generate a 3D conformer for phenylboronic acid (a boron-
# containing building block). Optimize it with MMFF94, falling back to UFF
# if needed." Tests the SKILL.md "MMFF94 -- parameter missing" failure mode:
# MMFF94 only covers H, C, N, O, F, Si, P, S, Cl, Br, I + select cations --
# boron is not in that list.

from rdkit import Chem
from rdkit.Chem import AllChem

def gen_conformer_ensemble(smiles, n_conf=10, seed=42, optimize=True):
    '''Reproduces examples/gen_conformers.py gen_conformer_ensemble verbatim.'''
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, []
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    params.useRandomCoords = True
    params.maxIterations = 1000
    ids = AllChem.EmbedMultipleConfs(mol, numConfs=n_conf, params=params)
    if not optimize:
        return mol, [(int(cid), None) for cid in ids]
    conf_data = []
    mmff_props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant='MMFF94s')
    use_uff = mmff_props is None
    print(f'MMFFGetMoleculeProperties returned None (MMFF94 cannot parameterize): {use_uff}')
    if use_uff and not AllChem.UFFHasAllMoleculeParams(mol):
        raise ValueError('Neither MMFF94s nor UFF covers this molecule')
    for cid in ids:
        ff = (AllChem.UFFGetMoleculeForceField(mol, confId=cid) if use_uff else
              AllChem.MMFFGetMoleculeForceField(mol, mmff_props, confId=cid))
        if ff is None:
            raise ValueError(f'Could not construct force field for conformer {cid}')
        status = ff.Minimize(maxIts=1000)
        if status != 0:
            raise RuntimeError(f'Optimization did not converge for conformer {cid}')
        conf_data.append((int(cid), float(ff.CalcEnergy())))
    return mol, conf_data

phenylboronic_acid = 'OB(O)c1ccccc1'
mol, conf_data = gen_conformer_ensemble(phenylboronic_acid, n_conf=10)
print(f'Molecule parsed: {mol is not None}, atoms (with Hs): {mol.GetNumAtoms() if mol else None}')
print(f'Conformers generated: {len(conf_data)}')
energies = [e for _, e in conf_data]
print(f'Force field actually used (per code path): {"UFF" if AllChem.MMFFGetMoleculeProperties(mol, mmffVariant="MMFF94s") is None else "MMFF94s"}')
print(f'Energy range: {min(energies):.4f} to {max(energies):.4f}')
