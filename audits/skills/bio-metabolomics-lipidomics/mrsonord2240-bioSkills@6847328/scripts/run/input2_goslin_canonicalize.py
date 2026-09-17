# Input 2 (Variant A, REGRESSION) -- "Canonicalize these lipid names through
# Goslin and report the structural-resolution level each one actually claims:
# PC 34:1, PC 16:0_18:1, PC 16:0/18:1, TG 52:3, Cer 18:1;O2/16:0, PC O-34:1,
# PC P-34:1."
#
# Pre-fix: 4/7 of these (any name parsed at or below SPECIES, plus both
# ether/plasmalogen sum names) crashed with an unhandled pygoslin
# RuntimeException when the code asked for MOLECULAR_SPECIES.
# Post-fix: SKILL.md's "Honest Annotation-Level Assignment (Goslin)" section
# now caps target_level = min(MOLECULAR_SPECIES, claimed_level) before
# calling get_lipid_string(). This re-runs the exact same 7 names.
from pygoslin.parser.Parser import LipidParser
from pygoslin.domain.LipidLevel import LipidLevel

names = [
    "PC 34:1",              # sum composition
    "PC 16:0_18:1",         # molecular species (chains known, sn unresolved)
    "PC 16:0/18:1",         # sn-claimed from a tool export, CID-only data (over-claim)
    "TG 52:3",
    "Cer 18:1;O2/16:0",     # sphingoid hydroxyl notation
    "PC O-34:1",            # ether
    "PC P-34:1",            # plasmalogen (mass-degenerate with O-34:2)
]

parser = LipidParser()
n_crash = 0
print(f"{'Input name':<22} {'Claimed level':<20} {'Honest (capped)':<28} {'Sum composition'}")
for n in names:
    try:
        lipid = parser.parse(n)
        claimed_level = lipid.lipid.info.level
        # GUARD (post-fix, verbatim from SKILL.md): never request a target level
        # more specific than what was actually parsed.
        target_level = min(LipidLevel.MOLECULAR_SPECIES, claimed_level, key=lambda l: l.value)
        honest = lipid.get_lipid_string(target_level)
        summed = lipid.get_lipid_string(LipidLevel.SPECIES) if claimed_level.value >= LipidLevel.SPECIES.value else honest
        print(f"{n:<22} {str(claimed_level):<20} {honest:<28} {summed}")
    except Exception as e:
        n_crash += 1
        print(f"{n:<22} PARSE ERROR: {type(e).__name__}: {e}")

print(f"\nCrashes: {n_crash}/{len(names)} (pre-fix baseline was 4/7)")
assert n_crash == 0, f"REGRESSION FAILED: {n_crash} names still crash post-fix"
print("PASS: 0/7 crash post-fix")

# Sanity: the honest string for the sum-composition-only names must be
# UNCHANGED (no chains to invent), and PC 16:0/18:1's SKILL.md worked example
# must still reproduce exactly.
worked_example = parser.parse("PC 16:0/18:1")
we_claimed = worked_example.lipid.info.level
we_target = min(LipidLevel.MOLECULAR_SPECIES, we_claimed, key=lambda l: l.value)
we_honest = worked_example.get_lipid_string(we_target)
assert we_honest == "PC 16:0_18:1", f"worked example regressed: got {we_honest!r}"
print("PASS: SKILL.md's own worked example (PC 16:0/18:1 -> PC 16:0_18:1) still reproduces exactly")

# The ether/plasmalogen mass-degeneracy point the fix log claims as a side
# effect: PC P-34:1's sum composition should equal PC O-34:2's.
p_lipid = parser.parse("PC P-34:1")
o_lipid = parser.parse("PC O-34:2")
p_sum = p_lipid.get_lipid_string(LipidLevel.SPECIES)
o_sum = o_lipid.get_lipid_string(LipidLevel.SPECIES)
print(f"\nMass-degeneracy check: PC P-34:1 sum-composes to {p_sum!r}; PC O-34:2 sum-composes to {o_sum!r}")
assert p_sum == o_sum, "expected P-34:1 and O-34:2 to be mass-degenerate at sum-composition level"
print("PASS: ether/plasmalogen mass-degeneracy confirmed (matches fix log's claim)")
