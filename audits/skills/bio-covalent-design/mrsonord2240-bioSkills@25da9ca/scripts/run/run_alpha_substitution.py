"""Exercise the shipped alpha-substitution helper as SKILL.md invokes it."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HELPER = ROOT / "skill_copy" / "scripts" / "acrylamide_alpha_substitution.py"
spec = spec_from_file_location("alpha_helper", HELPER)
module = module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

cases = {
    "unsubstituted": ("C=CC(=O)N1CCCCC1", 0),
    "alpha_methyl": ("C=C(C)C(=O)N1CCCCC1", 1),
    "alpha_chloro": ("C=C(Cl)C(=O)NC", 1),
    "no_acrylamide": ("CCO", None),
    "invalid": ("not-a-smiles", None),
}
for label, (smiles, expected) in cases.items():
    actual = module.acrylamide_alpha_substitution_count(smiles)
    assert actual == expected, f"{label}: {actual} != {expected}"
    print(f"{label}: {smiles}\t{actual}")
print("Input 2 alpha-substitution regression passed; values are structural counts only.")
