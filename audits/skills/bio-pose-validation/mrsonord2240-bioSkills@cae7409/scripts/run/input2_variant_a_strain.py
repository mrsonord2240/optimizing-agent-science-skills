"""
Audit Input 2 (Variant A) — bio-pose-validation
Prompt: "Compute relative MMFF94 strain energy for the docked benzamidine pose
versus the lowest sampled reference conformer, and report whether it is an
outlier."
Runs the Skill's own `ligand_strain_mmff` function from examples/validate_poses.py
verbatim (copied below unmodified) against the real Vina mode-1 pose.
"""
import sys
sys.path.insert(0, '.')
from rdkit import Chem
from rdkit.Chem import AllChem
import pandas as pd


def ligand_strain_mmff(docked_sdf, n_ref_conf=20):
    '''Compute relative MMFF94 strain versus the lowest sampled conformer.'''
    suppl = Chem.SDMolSupplier(docked_sdf, removeHs=False, sanitize=True)
    rows = []
    for i, docked in enumerate(suppl):
        if docked is None:
            rows.append({'pose_idx': i, 'strain_kcal': None, 'note': 'parse_fail'})
            continue

        smi = Chem.MolToSmiles(docked)
        ref_mol = Chem.MolFromSmiles(smi)
        if ref_mol is None:
            rows.append({'pose_idx': i, 'strain_kcal': None, 'note': 'reference_parse_fail'})
            continue
        ref_mol = Chem.AddHs(ref_mol)

        mmff_props_ref = AllChem.MMFFGetMoleculeProperties(ref_mol)
        if mmff_props_ref is None:
            rows.append({'pose_idx': i, 'strain_kcal': None, 'note': 'no_mmff_params'})
            continue
        conf_ids = list(AllChem.EmbedMultipleConfs(
            ref_mol, numConfs=n_ref_conf, params=AllChem.ETKDGv3()
        ))
        if not conf_ids:
            rows.append({'pose_idx': i, 'strain_kcal': None, 'note': 'embedding_failed'})
            continue
        AllChem.MMFFOptimizeMoleculeConfs(ref_mol)

        ref_energies = []
        for c in conf_ids:
            ff = AllChem.MMFFGetMoleculeForceField(ref_mol, mmff_props_ref, confId=c)
            if ff is not None:
                ref_energies.append(ff.CalcEnergy())
        if not ref_energies:
            rows.append({'pose_idx': i, 'strain_kcal': None, 'note': 'reference_force_field_failed'})
            continue
        min_ref = min(ref_energies)

        docked_h = Chem.AddHs(Chem.Mol(docked), addCoords=True)
        if docked_h.GetNumAtoms() != ref_mol.GetNumAtoms():
            rows.append({'pose_idx': i, 'strain_kcal': None, 'note': 'atom_system_mismatch'})
            continue
        mmff_props_dock = AllChem.MMFFGetMoleculeProperties(docked_h)
        if mmff_props_dock is None:
            rows.append({'pose_idx': i, 'strain_kcal': None, 'note': 'no_dock_mmff_params'})
            continue
        ff_dock = AllChem.MMFFGetMoleculeForceField(docked_h, mmff_props_dock)
        if ff_dock is None:
            rows.append({'pose_idx': i, 'strain_kcal': None, 'note': 'dock_force_field_failed'})
            continue
        for atom in docked_h.GetAtoms():
            if atom.GetAtomicNum() != 1:
                ff_dock.AddFixedPoint(atom.GetIdx())
        ff_dock.Minimize(maxIts=200)
        docked_e = ff_dock.CalcEnergy()

        rows.append({
            'pose_idx': i,
            'strain_kcal': docked_e - min_ref,
            'note': 'ok',
        })
    return pd.DataFrame(rows)


if __name__ == '__main__':
    df = ligand_strain_mmff('../data/mode1_fixed.sdf')
    print(df.to_string())
