"""Input 3 (Edge, regression): phenylboronic acid, MMFF94-parameter-missing -> UFF fallback."""
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
                results.append({'conf_id': cid, 'energy': ff.CalcEnergy(),
                                'converged': status == 0, 'force_field': 'MMFF94s'})
            return results
        force_field = 'uff'
        print('MMFF94 unavailable -> falling back to UFF')
    if force_field == 'uff':
        if not AllChem.UFFHasAllMoleculeParams(mol):
            raise ValueError('Neither MMFF94s nor UFF covers this molecule')
        for cid in conf_ids:
            ff = AllChem.UFFGetMoleculeForceField(mol, confId=cid)
            status = ff.Minimize(maxIts=1000)
            results.append({'conf_id': cid, 'energy': ff.CalcEnergy(),
                            'converged': status == 0, 'force_field': 'UFF'})
        return results
    raise ValueError(f'Unsupported force field: {force_field}')


phenylboronic_acid = 'OB(O)c1ccccc1'
mol, ids = gen_conformers(phenylboronic_acid, n_conf=10)
print(f'Embedded: {len(ids)}/10')
mmff_props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant='MMFF94s')
print(f'MMFF94 properties None (expected for boron): {mmff_props is None}')
results = optimize_conformers(mol, ids)
energies = [r['energy'] for r in results]
print(f'Force field used: {results[0]["force_field"]}')
print(f'Energy range: {min(energies):.4f} - {max(energies):.4f} kcal/mol')
