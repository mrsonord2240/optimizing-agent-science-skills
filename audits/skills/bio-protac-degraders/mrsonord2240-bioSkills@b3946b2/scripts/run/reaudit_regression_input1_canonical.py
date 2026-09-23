"""
Input 1 (Canonical) — "Design an exploratory PROTAC series for kinase target X
(PDB 5XYZ-like ATP-site ligand with a known solvent-exposed exit vector) using
CRBN as the E3 recruiter. Vary linker composition/rigidity and report
connected SMILES with computed properties as structural hypotheses, not final
candidates."

Follows the Skill's "Quick Start" / "CRBN PROTAC design" example prompt and
the SKILL.md pseudo-code workflow: build a target ligand fragment with an
exit vector, a CRBN (glutarimide) E3 fragment, enumerate the built-in linker
library, and report MolWt/TPSA/LogP/RotBonds as hypotheses (the Skill is
explicit that these are not acceptance criteria).
"""
import sys
sys.path.insert(0, r"F:\OpenScience\audits\bio-protac-degraders\skill_copy\examples")
from protac_enumerate import enumerate_linkers, compute_protac_size

# Target ligand: a generic solvent-exposed aminopyrimidine kinase hinge binder
# with an exit vector off a piperazine (synthetic/illustrative fragment).
target_fragment = "[*]c1cc(Nc2ncc(-c3ccccc3)nc2N2CCNCC2)ccn1"

# CRBN E3 recruiter: glutarimide (pomalidomide-like) fragment with exit vector
# off the aryl ring, as used in published CRBN-recruiting PROTACs.
e3_fragment = "[*]c1ccc2c(c1)C(=O)N(C1CCC(=O)NC1=O)C2=O"

results = enumerate_linkers(target_fragment, e3_fragment)

print(f"{'linker':<20}{'MolWt':>8}{'TPSA':>8}{'LogP':>8}{'RotBonds':>10}  SMILES")
for name, smi in results.items():
    props = compute_protac_size(smi)
    print(f"{name:<20}{props['MolWt']:>8.1f}{props['TPSA']:>8.1f}{props['LogP']:>8.2f}{props['RotBonds']:>10d}  {smi}")

print(f"\nTotal linkers enumerated: {len(results)}")
