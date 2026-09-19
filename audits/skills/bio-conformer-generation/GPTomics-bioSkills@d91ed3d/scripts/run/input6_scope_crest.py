# Input 6 (Scope Boundary): "Sample conformers for a flexible peptide-like
# molecule using CREST + GFN2-xTB, following the skill's CREST workflow."
# Tests SKILL.md "CREST + GFN2-xTB for High-Quality Sampling" -- specifically
# whether the documented Prerequisites ("conda install -c conda-forge xtb
# crest") actually gets the user a working CREST on the platform being used.

import shutil
import subprocess
from rdkit import Chem
from rdkit.Chem import AllChem
from pathlib import Path

XTB_EXE = r'F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\xtb\xtb-6.7.1\bin\xtb.exe'

crest_on_path = shutil.which('crest') is not None
print(f'`crest` resolvable on PATH: {crest_on_path}')
print(f'xtb available at pinned path: {Path(XTB_EXE).exists()}')

# Reproduce the SKILL.md crest_workflow() RDKit prep step (this part IS RDKit,
# so it should still work regardless of CREST availability).
def crest_workflow_prep(smiles, out_dir='crest_out_test'):
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
    return input_path

leucine_enkephalin_fragment = 'CC(C)CC(NC(=O)C(Cc1ccccc1)N)C(=O)NCC(=O)O'  # small flexible peptide-like test molecule
xyz_path = crest_workflow_prep(leucine_enkephalin_fragment, out_dir='crest_out_test')
print(f'RDKit prep succeeded, wrote {xyz_path} ({xyz_path.stat().st_size} bytes)')

# Attempt the documented CREST command exactly as SKILL.md shows it.
try:
    result = subprocess.run(['crest', xyz_path.name, '--gfn2', '-T', '2'],
                             cwd=xyz_path.parent, capture_output=True, text=True, timeout=30)
    print(f'crest invocation exit code: {result.returncode}')
except FileNotFoundError as ex:
    print(f'crest invocation FAILED (FileNotFoundError): {ex}')
    print('CREST is not installed / not on PATH on this system -- confirms the environment '
          "tooling note that CREST publishes no Windows build (crest-lab/crest ships "
          "Linux-only binaries; no win-64 conda-forge package).")

# What DOES work on Windows for the semi-empirical layer: a single xtb GFN2
# optimization/single-point on the RDKit-prepped structure (the sub-step CREST
# would call repeatedly under metadynamics control).
xtb_result = subprocess.run([XTB_EXE, 'input.xyz', '--opt', 'normal'],
                             cwd=xyz_path.parent, capture_output=True, text=True,
                             timeout=120, encoding='utf-8', errors='replace')
print(f'xtb --opt exit code: {xtb_result.returncode}')
out = xtb_result.stdout or ''
tail = '\n'.join(out.strip().splitlines()[-15:]) if out.strip() else '(no stdout captured)'
print('xtb tail output:')
print(tail)
print(f'xtbopt.xyz produced: {(xyz_path.parent / "xtbopt.xyz").exists()}')
