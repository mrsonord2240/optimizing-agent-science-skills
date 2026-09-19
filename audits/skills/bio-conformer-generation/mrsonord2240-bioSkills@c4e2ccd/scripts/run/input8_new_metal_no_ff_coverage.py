"""Input 8 (NEW, adversarial): organometallic molecule where NEITHER MMFF94 nor UFF has full
coverage. SKILL.md's Common Errors table says 'Fall back to UFF; or for metals, use GFN2-xTB' --
verify the documented optimize_conformers() actually raises a clear ValueError rather than
crashing or silently returning nonsense, per the fixed-pattern code."""
from rdkit import Chem
from rdkit.Chem import AllChem


def gen_conformers(smiles, n_conf=10, seed=42):
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


def optimize_conformers(mol, conf_ids, force_field='mmff94'):
    results = []
    if force_field == 'mmff94':
        mmff_props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant='MMFF94s')
        if mmff_props is not None:
            for cid in conf_ids:
                ff = AllChem.MMFFGetMoleculeForceField(mol, mmff_props, confId=cid)
                status = ff.Minimize(maxIts=1000)
                results.append({'conf_id': cid, 'energy': ff.CalcEnergy(), 'converged': status == 0})
            return results
        force_field = 'uff'
    if force_field == 'uff':
        if not AllChem.UFFHasAllMoleculeParams(mol):
            raise ValueError('Neither MMFF94s nor UFF covers this molecule')
        for cid in conf_ids:
            ff = AllChem.UFFGetMoleculeForceField(mol, confId=cid)
            status = ff.Minimize(maxIts=1000)
            results.append({'conf_id': cid, 'energy': ff.CalcEnergy(), 'converged': status == 0})
        return results
    raise ValueError(f'Unsupported force field: {force_field}')


# ferrocene: organometallic, neither MMFF94 nor UFF fully parameterizes Fe sandwich bonding well;
# choose a molecule known to be genuinely outside typical MMFF/UFF coverage
metal_complex = '[Fe+2].c1cc[cH-]c1.c1cc[cH-]c1'  # ferrocene as ion pair SMILES

mol = Chem.MolFromSmiles(metal_complex)
print(f'Parsed: {mol is not None}')
if mol is not None:
    mol_h, ids = gen_conformers(metal_complex, n_conf=5)
    print(f'Embedded: {len(ids)}/5 (may be 0 if distance geometry cannot place disconnected ion pair)')
    mmff_props = AllChem.MMFFGetMoleculeProperties(mol_h, mmffVariant='MMFF94s')
    print(f'MMFF94 properties None (expected for Fe): {mmff_props is None}')
    uff_ok = AllChem.UFFHasAllMoleculeParams(mol_h)
    print(f'UFF has all params: {uff_ok}')
    try:
        if ids:
            optimize_conformers(mol_h, ids)
            print('Optimization ran without raising (UFF must have covered it)')
        else:
            print('No conformers embedded -- cannot test optimize_conformers on this input; '
                  'this itself is a real failure mode (embedding failure) not documented '
                  'for disconnected/ionic organometallics.')
    except ValueError as e:
        print(f'Got expected ValueError: {e}')
