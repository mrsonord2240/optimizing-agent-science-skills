"""Regression of prior scope input: real 3PTB with documented PLIP workaround."""
from pathlib import Path
from openbabel import pybel
from plip.structure.preparation import PDBComplex

original_write = pybel.Molecule.write
def patched_write(self, format="smi", filename=None, overwrite=False, opt=None):
    if format == "inchikey": return ""
    return original_write(self, format=format, filename=filename, overwrite=overwrite, opt=opt)
pybel.Molecule.write = patched_write
complex_ = PDBComplex()
complex_.load_pdb(str(Path(__file__).parents[1] / "data" / "3ptb.pdb"))
complex_.analyze()
classes = []
for site in complex_.interaction_sets.values():
    classes.extend(type(x).__name__ for x in site.all_itypes)
print("N_INTERACTIONS", len(classes), "CLASSES", sorted(set(classes)))
assert len(classes) == 9 and {"hbond", "hydroph_interaction", "metal_complex"}.issubset(classes)
print("ASSERT 3PTB gives real typed interactions after documented workaround: PASS")
