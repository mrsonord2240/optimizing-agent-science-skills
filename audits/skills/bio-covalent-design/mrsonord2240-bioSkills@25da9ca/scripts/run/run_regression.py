"""Run the prior report's classifier inputs from an isolated source copy."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLASSIFIER = ROOT / "skill_copy" / "examples" / "warhead_classifier.py"
spec = spec_from_file_location("warhead_classifier", CLASSIFIER)
module = module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def names(smiles):
    result = module.classify_warheads(smiles)
    return set() if result is None else set(result)


def require(smiles, expected, label):
    actual = names(smiles)
    assert expected <= actual, f"{label}: expected {expected}, got {actual}"
    print(f"{label}: {smiles} -> {sorted(actual)}")
    return actual


print("Input 1: canonical library")
canonical = {
    "acrylamide": "C=CC(=O)N1CCCCC1",
    "chloroacetamide": "O=C(CCl)NCc1ccccc1",
    "paracetamol_negative": "CC(=O)NC1=CC=C(O)C=C1",
}
for label, smiles in canonical.items():
    actual = names(smiles)
    print(f"{label}: {sorted(actual)}")
assert "acrylamide" in names(canonical["acrylamide"])
assert "chloroacetamide" in names(canonical["chloroacetamide"])
assert not names(canonical["paracetamol_negative"])

print("Input 3: invalid/no-warhead/overlap edge cases")
assert module.classify_warheads("not-a-smiles") is None
assert module.classify_warheads("") == {}
assert names("CC(=O)c1ccccc1") == set()
overlap = require("C=C(C)C(=O)N1CCCCC1", {"acrylamide", "alpha_substituted_acrylamide", "methacrylamide"}, "methacrylamide overlap")
assert overlap == {"acrylamide", "alpha_substituted_acrylamide", "methacrylamide"}

print("Input 4: residue-directed warheads")
sulfonyl = module.classify_warheads("CS(=O)(=O)F")
fluorosulfate = module.classify_warheads("COS(=O)(=O)F")
aldehyde = module.classify_warheads("O=CC1=CC=CC=C1")
assert sulfonyl["sulfonyl_fluoride"]["targets"] == ["Lys", "Tyr", "Ser"]
assert fluorosulfate["fluorosulfate_sufex"]["targets"] == ["Tyr", "Lys"]
assert aldehyde["aldehyde"]["reactivity_tier"] == "reversible"
print(f"sulfonyl fluoride: {sulfonyl}")
print(f"fluorosulfate: {fluorosulfate}")
print(f"aldehyde: {aldehyde}")

print("Input 5: independent positives, negatives, and non-contamination")
for label, smiles, expected in [
    ("4-bromophenacyl bromide", "BrCC(=O)c1ccc(Br)cc1", {"alpha_haloketone"}),
    ("1-chloro-2-propanone", "CC(=O)CCl", {"alpha_haloketone"}),
    ("benzalacetone", "CC(=O)/C=C/c1ccccc1", {"alpha_beta_unsaturated_ketone"}),
    ("cyclohex-2-enone", "O=C1CCCC=C1", {"alpha_beta_unsaturated_ketone"}),
]:
    require(smiles, expected, label)
for label, smiles in [("acetophenone", "CC(=O)c1ccccc1"), ("cyclohexanone", "O=C1CCCCC1")]:
    assert not names(smiles), label
    print(f"{label}: correctly negative")
for label, smiles in [
    ("chloroacetamide", "O=C(CCl)NC"),
    ("bromoacetamide", "O=C(CBr)NC"),
    ("acrylamide", "C=CC(=O)NC"),
    ("methacrylamide", "C=C(C)C(=O)NC"),
]:
    actual = names(smiles)
    assert "alpha_haloketone" not in actual and "alpha_beta_unsaturated_ketone" not in actual, (label, actual)
    print(f"{label}: no ketone-pattern contamination")

print("Input 8: multi-warhead detection")
multi = module.classify_warheads("C=CC(=O)Nc1ccc(cc1)C(=O)CCl")
assert {"acrylamide", "alpha_haloketone"} <= set(multi)
assert multi["acrylamide"]["reactivity_tier"] == "moderate"
assert multi["alpha_haloketone"]["reactivity_tier"] == "very_high"
print(f"multi-warhead: {multi}")

print("Input 9: iodoacetamide Decision-Tree regression")
for label, smiles in [("iodoacetamide", "NC(=O)CI"), ("N-benzyl iodoacetamide", "O=C(CI)NCc1ccccc1")]:
    actual = module.classify_warheads(smiles)
    assert "iodoacetamide" in actual, (label, actual)
    assert "chloroacetamide" not in actual, (label, actual)
    assert actual["iodoacetamide"]["targets"] == ["Cys"]
    print(f"{label}: {actual}")

print("All prior classifier inputs passed.")
