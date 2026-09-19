# Input 5 (Stress): "Classify all 20 compounds in this mixed covalent-fragment library
# (mix of Cys-, Lys-, Ser/Thr-, Tyr-directed warheads plus decoys), rank by reactivity tier,
# and flag every compound that needs matched GSH-reactivity measurement before further
# progression." -- multi-part, larger batch, full ranked report.
from warhead_classifier import classify_warheads, REACTIVITY_TIER

library = {
    'f01_acrylamide':            'C=CC(=O)Nc1ccccc1',
    'f02_chloroacetamide':       'ClCC(=O)Nc1ccccc1',
    'f03_bromoacetamide':        'BrCC(=O)Nc1ccccc1',
    'f04_methacrylamide':        'C=C(C)C(=O)Nc1ccccc1',
    'f05_vinylsulfone':          'C=CS(=O)(=O)c1ccccc1',
    'f06_sulfonylfluoride':      'O=S(=O)(F)c1ccccc1',
    'f07_fluorosulfate':         'O=S(=O)(F)Oc1ccccc1',
    'f08_aldehyde':              'O=Cc1ccccc1',
    'f09_boronate':              'OB(O)c1ccccc1',
    'f10_nitrile':               'N#Cc1ccccc1',
    'f11_epoxide':                'C1OC1c1ccccc1',
    'f12_aziridine':              'C1NC1c1ccccc1',
    'f13_maleimide':              'O=C1C=CC(=O)N1c1ccccc1',
    'f14_isothiocyanate':         'S=C=Nc1ccccc1',
    'f15_isocyanate':             'O=C=Nc1ccccc1',
    'f16_alpha_sub_acrylamide':  'C=C(c1ccccc1)C(=O)Nc1ccccc1',
    'f17_decoy_benzene':          'c1ccccc1',
    'f18_decoy_ibuprofen':        'CC(C)Cc1ccc(cc1)C(C)C(=O)O',
    'f19_double_warhead':         'C=CC(=O)NCCCC(=O)CCl',   # acrylamide + chloroketone-like
    'f20_decoy_caffeine':         'Cn1cnc2c1c(=O)n(C)c(=O)n2C',
    # SKILL.md's own "Warhead Chemistry" table documents these two classes explicitly
    # (alpha-haloketone: "Very high" reactivity, Cys-selective "Yes (but reactive)";
    # alpha,beta-unsaturated ketone: "Moderate" reactivity, Cys-selective) -- included here
    # to check whether the shipped classifier actually recognizes what SKILL.md documents.
    'f21_alpha_haloketone_phenacylCl': 'O=C(c1ccccc1)CCl',
    'f22_alpha_beta_unsat_ketone':     'O=C(c1ccccc1)C=Cc1ccccc1',
}

TIER_RANK = {'very_high': 5, 'high': 4, 'moderate': 3, 'context_dependent': 2.5,
             'reversible': 2, 'low': 1, 'unknown': 0}

rows = []
for name, smi in library.items():
    matches = classify_warheads(smi)
    if not matches:
        rows.append((name, 'NONE', 0, []))
        continue
    # rank by the single highest-tier warhead found in the molecule
    best = max(matches.items(), key=lambda kv: TIER_RANK.get(kv[1]['reactivity_tier'], 0))
    max_rank = TIER_RANK.get(best[1]['reactivity_tier'], 0)
    rows.append((name, best[0], max_rank, list(matches.keys())))

rows.sort(key=lambda r: -r[2])

print(f"{'compound':28s} {'top_warhead':22s} {'rank':6s} {'all_warheads_matched'}")
for name, top, rank, allw in rows:
    flag = 'FLAG: measure GSH t1/2' if top != 'NONE' else 'no warhead - no flag'
    print(f"{name:28s} {top:22s} {rank!s:6s} {allw}  [{flag}]")

n_flagged = sum(1 for r in rows if r[1] != 'NONE')
print(f"\n{n_flagged}/{len(rows)} compounds carry a catalogued warhead and are flagged for GSH measurement.")
