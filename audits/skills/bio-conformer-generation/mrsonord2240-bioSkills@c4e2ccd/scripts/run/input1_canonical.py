"""Input 1 (Canonical, regression): 20 ETKDGv3 conformers for aspirin, MMFF94-optimized.
Uses the FIXED SKILL.md gen_conformers()/optimize_conformers() verbatim (post-fix c4e2ccd)."""
from rdkit import Chem
from rdkit.Chem import AllChem


def gen_conformers(smiles, n_conf=20, seed=42):
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
                if ff is None:
                    results.append({'conf_id': cid, 'status': 'force_field_failed'})
                    continue
                status = ff.Minimize(maxIts=1000)
                results.append({'conf_id': cid, 'energy': ff.CalcEnergy(),
                                'converged': status == 0, 'force_field': 'MMFF94s'})
            return results
    raise ValueError(f'Unsupported force field: {force_field}')


aspirin = 'CC(=O)OC1=CC=CC=C1C(=O)O'
mol, ids = gen_conformers(aspirin, n_conf=20, seed=42)
print(f'Embedded: {len(ids)}/20')
results = optimize_conformers(mol, ids)
converged = sum(1 for r in results if r.get('converged'))
energies = sorted(r['energy'] for r in results if 'energy' in r)
print(f'Converged: {converged}/{len(results)}')
print(f'Energy range: {min(energies):.4f} - {max(energies):.4f} kcal/mol')
print(f'Unique energies (rounded to 2dp): {len(set(round(e, 2) for e in energies))}')
