"""New Phase-2 input: make the first-match behavior explicit and reproducible."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from rdkit import Chem

ROOT = Path(__file__).resolve().parent
HELPER = ROOT / "skill_copy" / "scripts" / "acrylamide_alpha_substitution.py"
spec = spec_from_file_location("alpha_helper", HELPER)
module = module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

smiles = "C=CC(=O)NCCNC(=O)C(C)=C"
pattern = Chem.MolFromSmarts("[CX3:1](=[OX1:2])([NX3:3])[CX3:4]=[CX3:5]")
mol = Chem.MolFromSmiles(smiles)
matches = mol.GetSubstructMatches(pattern, uniquify=True)
assert len(matches) == 2, matches
reported = module.acrylamide_alpha_substitution_count(smiles)
assert reported == 0, reported
print(f"multi-acrylamide: {smiles}")
print(f"matched_acrylamides={len(matches)}; helper_first_match_count={reported}")
print("The shipped helper intentionally reports only the first match; use per-site analysis for multi-warhead compounds.")
