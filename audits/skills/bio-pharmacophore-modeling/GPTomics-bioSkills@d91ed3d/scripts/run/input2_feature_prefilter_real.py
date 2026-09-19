# Input 2 (Variant A) -- reuse the Skill's shipped feature_family_prefilter (examples/pharmacophore.py)
# with real actives and a real active/decoy library, to test whether the coarse feature-family
# prefilter genuinely discriminates HIV-1 protease inhibitors from unrelated drugs.
import sys, time
sys.path.insert(0, '.')
from pharmacophore_example import feature_family_prefilter

# Query actives: two real, structurally distinct HIV-1 protease inhibitors (ChEMBL canonical SMILES)
indinavir  = "CC(C)(C)NC(=O)[C@@H]1CN(Cc2cccnc2)CCN1C[C@@H](O)C[C@@H](Cc1ccccc1)C(=O)N[C@H]1c2ccccc2C[C@H]1O"
saquinavir = "CC(C)(C)NC(=O)[C@@H]1C[C@@H]2CCCC[C@@H]2CN1CC(O)[C@H](Cc1ccccc1)NC(=O)[C@@H](CC(N)=O)NC(=O)c1ccc2ccccc2n1"

queries = [indinavir, saquinavir]

# Library: one more real HIV-PR inhibitor (ritonavir, expected to match: has donor/acceptor/
# aromatic/hydrophobe families) plus four real, unrelated marketed drugs that plausibly lack
# the shared feature-family set (expected to fail the prefilter).
ritonavir    = "CC(C)c1nc(CN(C)C(=O)N[C@H](C(=O)N[C@H](CC[C@H](Cc2ccccc2)NC(=O)OCc2cncs2)Cc2ccccc2)C(C)C)cs1"
caffeine     = "Cn1c(=O)c2c(ncn2C)n(C)c1=O"
metformin    = "CN(C)C(=N)NC(=N)N"
aspirin      = "CC(=O)Oc1ccccc1C(=O)O"
acetaminophen = "CC(=O)Nc1ccc(O)cc1"

library = {
    "ritonavir (real active, expected MATCH)": ritonavir,
    "caffeine (decoy, expected reject)": caffeine,
    "metformin (decoy, expected reject)": metformin,
    "aspirin (decoy, expected reject)": aspirin,
    "acetaminophen (decoy, expected reject)": acetaminophen,
}

t0 = time.time()
hits = feature_family_prefilter(queries, list(library.values()))
print(f"Elapsed: {time.time()-t0:.1f}s")
print("Hits (raw SMILES):", hits)

for label, smi in library.items():
    status = "MATCH" if smi in hits else "reject"
    print(f"{label}: {status}")
