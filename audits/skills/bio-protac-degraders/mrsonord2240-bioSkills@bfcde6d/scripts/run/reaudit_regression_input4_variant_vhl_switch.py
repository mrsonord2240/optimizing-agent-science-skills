"""
Input 4 (Variant B) — "Switch from CRBN to VHL E3. Adjust linker to maintain
ternary geometry. Re-predict ternary complex." (verbatim usage-guide.md
example prompt, "VHL alternative design")

Exercises the Skill's E3-ligase table (VHL / VL-269-class ligand) and the
Decision Tree row "Reduce recruiter-specific liabilities -> compare
alternative E3 recruiters and linker geometries". Re-runs the same target
fragment from Input 1 against a VHL fragment instead of CRBN, and reports
how the property profile shifts across the linker series -- this is the
kind of A/B E3-swap comparison the Skill instructs the agent to produce.
"""
import sys
sys.path.insert(0, r"F:\OpenScience\audits\bio-protac-degraders\skill_copy\examples")
from protac_enumerate import enumerate_linkers, compute_protac_size

target_fragment = "[*]c1cc(Nc2ncc(-c3ccccc3)nc2N2CCNCC2)ccn1"  # same as Input 1

# VHL E3 recruiter fragment (hydroxyproline-based VHL ligand class, exit
# vector off the terminal amide, illustrative of the VL-269 series).
vhl_fragment = "[*]NC(=O)C1CC(O)CN1C(=O)C(NC(C)=O)c1ccc(-c2csc(C)n2)cc1"

crbn_fragment = "[*]c1ccc2c(c1)C(=O)N(C1CCC(=O)NC1=O)C2=O"

for label, e3 in (("VHL", vhl_fragment), ("CRBN (baseline from Input 1)", crbn_fragment)):
    results = enumerate_linkers(target_fragment, e3)
    print(f"--- E3 = {label} ---")
    for name in ("short_alkyl", "piperazine_short", "triazole"):
        smi = results[name]
        props = compute_protac_size(smi)
        print(f"  {name:<18} MolWt={props['MolWt']:.1f}  TPSA={props['TPSA']:.1f}  "
              f"LogP={props['LogP']:.2f}  RotBonds={props['RotBonds']}")
    print()

print("Note: switching E3 recruiter changes MolWt/TPSA/LogP substantially "
      "(VHL ligand is larger and more polar than the CRBN glutarimide). "
      "A structural ternary hypothesis (e.g. PRosettaC) would be needed to "
      "confirm which E3/linker combination supports a productive geometry; "
      "this script only reports 2D composition, consistent with the Skill's "
      "statement that an attachment-point distance does not map uniquely to "
      "a linker choice.")
