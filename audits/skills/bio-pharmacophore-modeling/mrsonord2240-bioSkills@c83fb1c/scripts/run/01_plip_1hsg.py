"""Regression of the prior canonical PLIP input on real PDB 1HSG."""
from pathlib import Path
from openbabel import pybel
from plip.structure.preparation import PDBComplex

original_write = pybel.Molecule.write

def patched_write(self, format="smi", filename=None, overwrite=False, opt=None):
    if format == "inchikey":
        return ""
    return original_write(self, format=format, filename=filename,
                          overwrite=overwrite, opt=opt)

pybel.Molecule.write = patched_write
complex_ = PDBComplex()
complex_.load_pdb(str(Path(__file__).parents[1] / "data" / "1hsg.pdb"))
complex_.analyze()
counts = {"hbond": 0, "hydroph_interaction": 0, "saltbridge": 0, "waterbridge": 0}
for site in complex_.interaction_sets.values():
    for interaction in site.all_itypes:
        name = type(interaction).__name__
        if name in counts:
            counts[name] += 1
print("COUNTS", counts)
assert counts == {"hbond": 6, "hydroph_interaction": 15, "saltbridge": 2, "waterbridge": 4}, counts
print("ASSERT 1HSG documented workaround and interaction counts: PASS")
