# Input 4 (Variant B) -- direct test of the Skill's own documented failure mode:
# "PLIP -- water bridge absent from output ... the required crystallographic water must be
# present in the input and satisfy its geometric criteria."
# Compare PLIP's water_bridges on 1HSG as deposited (with crystallographic waters, including
# the famous Ile50/Ile50' "flap water" that bridges the two protease flaps to the ligand) vs
# the same structure with every HOH HETATM record stripped.
from openbabel import pybel
_orig_write = pybel.Molecule.write
def _write_patched(self, format='smi', *a, **kw):
    if format == 'inchikey':
        return ''
    return _orig_write(self, format, *a, **kw)
pybel.Molecule.write = _write_patched

from plip.structure.preparation import PDBComplex

for label, path in [("WITH crystallographic waters", "data/1hsg.pdb"),
                     ("water-stripped", "data/1hsg_nowater.pdb")]:
    mc = PDBComplex()
    mc.load_pdb(path)
    mc.analyze()
    print(f"\n=== {label} ({path}) ===")
    for site_name, site in mc.interaction_sets.items():
        wb = getattr(site, 'water_bridges', [])
        print(f"Site {site_name}: {len(wb)} water bridges")
        for w in wb:
            print(f"   {w.restype}{w.resnr}{w.reschain} <-> ligand, "
                  f"d(acceptor-water)={w.distance_aw:.2f} A, d(donor-water)={w.distance_dw:.2f} A, "
                  f"water_atom_idx={w.water_orig_idx}")
