"""
Input 3 (Edge/boundary) — "I have a target fragment with a double-bonded
exit-vector dummy atom, e.g. '[*]=C1CCC(=O)N1', and a CRBN fragment
'[*]CC(=O)N1CCC(=O)NC1=O'. Build the connected PROTAC SMILES with the
short_alkyl linker."

Tests usage-guide.md's explicit stated constraint: "The linker-enumeration
example requires each explicit dummy attachment to use a single bond;
reject other dummy-bond orders unless the intended connection chemistry has
a separately validated bond-order rule." This is a genuine edge case in the
shipped code (_connect_dummies raises ValueError on non-single dummy bonds).
Also tests a second edge: a fragment with zero or two dummy atoms (invalid
input) is rejected with a clear error rather than crashing uninformatively.
"""
import sys
sys.path.insert(0, r"F:\OpenScience\audits\bio-protac-degraders\skill_copy\examples")
from protac_enumerate import build_protac, LINKERS

target_double_bond = "[*]=C1CCC(=O)N1"
e3_fragment = "[*]CC(=O)N1CCC(=O)NC1=O"
linker = LINKERS["short_alkyl"]

print("Case A: double-bonded exit-vector dummy (should be rejected)")
try:
    smi = build_protac(target_double_bond, linker, e3_fragment)
    print("  UNEXPECTED SUCCESS:", smi)
except ValueError as e:
    print("  Correctly raised ValueError:", e)

print("\nCase B: target fragment with two dummy atoms (should be rejected)")
target_two_dummies = "[*]c1ccc([*])cc1"
try:
    smi = build_protac(target_two_dummies, linker, e3_fragment)
    print("  UNEXPECTED SUCCESS:", smi)
except ValueError as e:
    print("  Correctly raised ValueError:", e)

print("\nCase C: invalid SMILES for target (should be rejected)")
try:
    smi = build_protac("not_a_smiles(((", linker, e3_fragment)
    print("  UNEXPECTED SUCCESS:", smi)
except ValueError as e:
    print("  Correctly raised ValueError:", e)

print("\nCase D: valid single-bond exit vector (should succeed, control)")
target_ok = "[*]C1CCC(=O)N1"
smi = build_protac(target_ok, linker, e3_fragment)
print("  Success:", smi)
