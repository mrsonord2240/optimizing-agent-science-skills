"""Input 6 (Scope boundary, regression): CREST + GFN2-xTB workflow, exactly as documented, on Windows.
Re-verifies the P1 fix: does the new SKILL.md caveat correctly predict what happens, and does the
documented fallback (RDKit macrocycle embedding + standalone xtb --opt) actually work?"""
import shutil
import subprocess
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem

print('--- Step 1: is crest on PATH? ---')
crest_path = shutil.which('crest')
print(f'shutil.which("crest") = {crest_path}')

print('\n--- Step 2: run the crest_workflow() from SKILL.md verbatim, expect FileNotFoundError ---')


def crest_workflow(smiles, out_dir='crest_out'):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f'Invalid SMILES: {smiles!r}')
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.useRandomCoords = True
    if AllChem.EmbedMolecule(mol, params) == -1:
        raise RuntimeError(f'Initial 3D embedding failed for {smiles!r}')
    if not AllChem.MMFFHasAllMoleculeParams(mol):
        raise ValueError(f'MMFF parameters are unavailable for {smiles!r}')
    status = AllChem.MMFFOptimizeMolecule(mol, mmffVariant='MMFF94s', maxIters=1000)
    if status != 0:
        raise RuntimeError(f'Initial MMFF optimization did not converge (status {status})')
    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    input_path = out_dir / 'input.xyz'
    input_path.write_text(Chem.MolToXYZBlock(mol))
    subprocess.run(['crest', input_path.name, '--gfn2', '-T', '12'], cwd=out_dir, check=True)
    output_path = out_dir / 'crest_conformers.xyz'
    if not output_path.exists():
        raise FileNotFoundError(f'CREST did not produce {output_path}')
    return output_path


try:
    crest_workflow('c1ccccc1O')
    print('UNEXPECTED: crest_workflow succeeded')
except FileNotFoundError as e:
    print(f'Got expected FileNotFoundError: {e}')
except Exception as e:
    print(f'Got a DIFFERENT exception than expected: {type(e).__name__}: {e}')

print('\n--- Step 3: does the documented fallback actually work? ---')
print('Fallback per SKILL.md Installation + CREST sections: "skip CREST and use RDKit ETKDGv3 '
      'macrocycle-aware embedding plus a standalone xtb --opt semi-empirical refinement"')

XTB_EXE = r'F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\xtb\xtb-6.7.1\bin\xtb.exe'
import os
os.environ['XTBPATH'] = r'F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\xtb\xtb-6.7.1\share\xtb'

# a genuinely flexible/macrocyclic test molecule for the fallback path: 12-membered lactone-like ring
smiles = 'O=C1CCCCCCCCCCC1'  # cyclododecanone, a real macrocycle-adjacent test case
mol = Chem.MolFromSmiles(smiles)
mol = Chem.AddHs(mol)
params = AllChem.ETKDGv3()
params.randomSeed = 42
params.useRandomCoords = True
params.useMacrocycleTorsions = True
params.useSmallRingTorsions = True
params.maxIterations = 5000
ids = list(AllChem.EmbedMultipleConfs(mol, numConfs=10, params=params))
print(f'RDKit macrocycle-aware embed: {len(ids)}/10 conformers')

mmff_props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant='MMFF94s')
ff = AllChem.MMFFGetMoleculeForceField(mol, mmff_props, confId=ids[0])
ff.Minimize(maxIts=1000)
print(f'MMFF94s pre-relax energy: {ff.CalcEnergy():.4f} kcal/mol')

out_dir = Path('xtb_fallback_out').resolve()
out_dir.mkdir(exist_ok=True)
xyz_path = out_dir / 'mol.xyz'
xyz_path.write_text(Chem.MolToXYZBlock(mol, confId=ids[0]))

result = subprocess.run([XTB_EXE, 'mol.xyz', '--opt'], cwd=out_dir,
                         capture_output=True, text=True, timeout=120,
                         encoding='utf-8', errors='replace')
print(f'xtb --opt returncode: {result.returncode}')
success = 'normal termination of xtb' in result.stdout
print(f'"normal termination of xtb" in stdout: {success}')
opt_file = out_dir / 'xtbopt.xyz'
print(f'xtbopt.xyz produced: {opt_file.exists()}')
if opt_file.exists():
    lines = opt_file.read_text().splitlines()
    print(f'xtbopt.xyz atom count line: {lines[0].strip()}')
