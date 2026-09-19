# Input 1 (Canonical): "Generate 20 ETKDGv3 conformers for aspirin with MMFF94
# optimization. Report the conformer count and energies."
# Following SKILL.md "ETKDGv3 (Modern Default)" + "Force-Field Optimization" sections verbatim.

from rdkit import Chem
from rdkit.Chem import AllChem

def gen_conformers(smiles, n_conf=20, seed=42):
    mol = Chem.MolFromSmiles(smiles)
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
        force_field = 'uff'
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

aspirin = 'CC(=O)Oc1ccccc1C(=O)O'
mol, ids = gen_conformers(aspirin, n_conf=20, seed=42)
print(f'Embedded conformer IDs: {len(ids)} (requested 20)')

results = optimize_conformers(mol, ids, force_field='mmff94')
energies = [r['energy'] for r in results if 'energy' in r]
converged = [r['converged'] for r in results if 'converged' in r]
print(f'Optimized: {len(results)}')
print(f'All converged: {all(converged)} ({sum(converged)}/{len(converged)})')
print(f'Energy range (kcal/mol): min={min(energies):.4f} max={max(energies):.4f}')
print(f'Unique energy values (rounded 3dp): {len(set(round(e,3) for e in energies))}')
print('Sample energies:', [round(e, 4) for e in energies[:5]])
