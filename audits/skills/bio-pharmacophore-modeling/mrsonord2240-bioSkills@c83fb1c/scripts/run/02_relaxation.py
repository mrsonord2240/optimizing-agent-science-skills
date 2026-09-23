"""Regression plus new test of strict and relaxed shared-feature filtering."""
import sys
from pathlib import Path

skill_examples = Path(__file__).parents[3] / "wt" / "chemoinformatics-pharmacophore-modeling" / "chemoinformatics" / "pharmacophore-modeling" / "examples"
sys.path.insert(0, str(skill_examples))
import pharmacophore as ph

indinavir = "CC(C)(C)NC(=O)C1CN(Cc2cccnc2)CCN1CC(O)CC(Cc1ccccc1)C(=O)NC1c2ccccc2CC1O"
saquinavir = "CC(C)(C)NC(=O)C1CC2CCCCC2CN1CC(O)C(Cc1ccccc1)NC(=O)C(CC(N)=O)NC(=O)c1ccc2ccccc2n1"
ritonavir = "CC(C)C1=NC(=CS1)CN(C)C(=O)NC(C(C)C)C(=O)NC(CC1=CC=CC=C1)CC(C(CC1=CC=CC=C1)NC(=O)OCC1=CN=CS1)O"
caffeine = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
metformin = "CN(C)C(=N)NC(=N)N"
aspirin = "CC(=O)OC1=CC=CC=C1C(=O)O"
acetaminophen = "CC(=O)NC1=CC=C(C=C1)O"
library = [ritonavir, caffeine, metformin, aspirin, acetaminophen]
strict = ph.feature_family_prefilter([indinavir, saquinavir], library)
relaxed = ph.feature_family_prefilter([indinavir, saquinavir], library, min_shared_fraction=0.6)
print("STRICT", strict)
print("RELAXED", relaxed)
assert strict == []
assert ritonavir in relaxed and caffeine not in relaxed and metformin not in relaxed
print("ASSERT default strict is unchanged and 0.6 admits ritonavir only among the specified discriminants: PASS")
