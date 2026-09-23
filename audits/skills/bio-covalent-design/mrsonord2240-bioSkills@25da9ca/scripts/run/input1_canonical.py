# Input 1 (Canonical): "Identify acrylamide and chloroacetamide candidates in library.smi.
# Report alpha substitution as a structural feature and flag compounds for matched
# GSH-reactivity measurements." (verbatim example prompt from usage-guide.md "Cysteine targeting")
#
# Synthetic candidate library (5 compounds), representative of real covalent-inhibitor chemotypes:
#  - N-phenylacrylamide (unsubstituted acrylamide, Cys-directed, cf. AMG 510 fragment-like warhead)
#  - N-phenyl chloroacetamide (ABPP-style probe)
#  - N-phenyl methacrylamide (alpha-methyl substituted, attenuated electrophile)
#  - a vinyl sulfone (Cys-directed)
#  - a molecule with no recognized warhead (paracetamol, negative control)
from warhead_classifier import classify_warheads
from alpha_sub import acrylamide_alpha_substitution_count

library = {
    'cand_01_acrylamide': 'C=CC(=O)Nc1ccccc1',
    'cand_02_chloroacetamide': 'ClCC(=O)Nc1ccccc1',
    'cand_03_methacrylamide': 'C=C(C)C(=O)Nc1ccccc1',
    'cand_04_vinylsulfone': 'C=CS(=O)(=O)c1ccccc1',
    'cand_05_paracetamol_negctrl': 'CC(=O)Nc1ccc(O)cc1',
}

print(f"{'compound':30s} {'warheads':45s} {'alpha_subs':10s} {'flag_for_GSH_testing'}")
for name, smi in library.items():
    matches = classify_warheads(smi)
    alpha = acrylamide_alpha_substitution_count(smi)
    warhead_str = ', '.join(
        f"{k}(tier={v['reactivity_tier']},targets={v['targets']})"
        for k, v in (matches or {}).items()
    ) or 'none'
    # A compound is flagged for matched GSH-reactivity measurement if it carries ANY
    # catalogued electrophilic warhead -- per SKILL.md "measure intrinsic reactivity" guidance.
    flag = 'YES - measure GSH t1/2 (no tier substitutes for a measured rate)' if matches else 'no recognized warhead'
    print(f"{name:30s} {warhead_str:45s} {str(alpha):10s} {flag}")
