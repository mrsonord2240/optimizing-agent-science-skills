import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'skill', 'examples'))
import pharmacophore as ph

nelfinavir = "CC1CCCCN1C(=O)C(CSc1ccccc1)NC(=O)C(O)C(Cc1ccccc1)NC(=O)C1CC2CCCCC2CN1C"
amprenavir = "CC(C)CN(CC(O)C(Cc1ccccc1)NC(=O)OC1CCOC1)S(=O)(=O)c1ccc(N)cc1"

library = [
    "CC(C)C1=NC(=CS1)CN(C)C(=O)NC(C(C)C)C(=O)NC(CC1=CC=CC=C1)CC(C(CC1=CC=CC=C1)NC(=O)OCC1=CN=CS1)O",
    "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
    "CN(C)C(=N)NC(=N)N",
    "CC(=O)OC1=CC=CC=C1C(=O)O",
    "CC(=O)NC1=CC=C(C=C1)O",
    "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
    "CN1CCC[C@H]1c1cccnc1",
    "OC(=O)c1ccccc1O",
    "CC(C)NCC(O)COc1cccc2[nH]ccc12",
    "CC12CCC3C(CCC4=CC(=O)CCC34C)C1CCC2O",
]

hits = ph.feature_family_prefilter([nelfinavir, amprenavir], library)
print("HITS:", hits)
print("N_LIBRARY:", len(library))
print("N_HITS:", len(hits))
