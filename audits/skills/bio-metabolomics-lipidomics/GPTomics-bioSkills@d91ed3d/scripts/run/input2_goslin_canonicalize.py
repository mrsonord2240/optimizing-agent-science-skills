# Input 2 (Variant A) -- "Canonicalize these lipid names through Goslin and
# report the structural-resolution level each one actually claims; downgrade
# any sn-position claim that CID-only data cannot support."
# Follows SKILL.md's "Honest Annotation-Level Assignment (Goslin)" pattern.
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
print(f"{'Input name':<22} {'Claimed level':<20} {'Honest (molecular species)':<28} {'Sum composition'}")
for n in names:
    try:
        lipid = parser.parse(n)
        claimed_level = lipid.lipid.info.level
        honest = lipid.get_lipid_string(LipidLevel.MOLECULAR_SPECIES)
        summed = lipid.get_lipid_string(LipidLevel.SPECIES)
        print(f"{n:<22} {str(claimed_level):<20} {honest:<28} {summed}")
    except Exception as e:
        print(f"{n:<22} PARSE ERROR: {type(e).__name__}: {e}")
