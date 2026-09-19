# Input 4 (Variant B): "Suggest warheads for a lysine-selective covalent inhibitor, and separately
# a tyrosine-selective one; classify these three candidate structures and report their target
# residue compatibility." -- exercises the non-Cys rows of the Reactive Residue Taxonomy /
# Warhead Chemistry tables (sulfonyl fluoride -> Lys/Tyr/Ser, fluorosulfate/SuFEx -> Tyr/Lys,
# aldehyde -> Cys/Lys/Ser reversible imine).
from warhead_classifier import classify_warheads

candidates = {
    'lys_sulfonylfluoride': 'O=S(=O)(F)c1ccc(cc1)C(=O)Nc1ccccc1',
    'tyr_fluorosulfate_sufex': 'O=S(=O)(F)Oc1ccc(cc1)C(=O)Nc1ccccc1',
    'lys_aldehyde_reversible': 'O=CCCNC(=O)c1ccccc1',
}

for name, smi in candidates.items():
    matches = classify_warheads(smi)
    print(f"{name}: {matches}")
