# Input 3 (Edge): boundary/robustness cases for the Skill's own classify_warheads /
# acrylamide_alpha_substitution_count functions.
#  a) invalid SMILES string
#  b) empty string
#  c) a molecule with NO catalogued warhead (aspirin)
#  d) a molecule that matches MULTIPLE overlapping SMARTS patterns at once
#     (a methacrylamide matches both 'acrylamide' [CX3](=[OX1])([NX3])[CX3]=[CX3] --
#     since that pattern has no atomic constraint excluding substitution -- AND
#     'alpha_substituted_acrylamide' AND 'methacrylamide' simultaneously)
#  e) a charged / zwitterionic acrylamide (protonated amine) to test SMARTS robustness to charge
from warhead_classifier import classify_warheads
from alpha_sub import acrylamide_alpha_substitution_count

cases = {
    'invalid_smiles': 'not_a_smiles(((',
    'empty_string': '',
    'no_warhead_aspirin': 'CC(=O)Oc1ccccc1C(=O)O',
    'overlapping_methacrylamide': 'C=C(C)C(=O)Nc1ccccc1',
    'charged_acrylamide_ammonium': 'C=CC(=O)NCC[NH3+]',
}

for name, smi in cases.items():
    print(f"--- {name} (SMILES: {smi!r}) ---")
    try:
        matches = classify_warheads(smi)
        alpha = acrylamide_alpha_substitution_count(smi)
        print(f"  classify_warheads -> {matches}")
        print(f"  acrylamide_alpha_substitution_count -> {alpha}")
    except Exception as e:
        print(f"  RAISED: {type(e).__name__}: {e}")
