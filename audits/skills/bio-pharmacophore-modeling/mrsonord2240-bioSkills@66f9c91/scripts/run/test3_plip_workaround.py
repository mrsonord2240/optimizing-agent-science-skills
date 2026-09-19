"""
New input A (Variant, not in the original 7): verify the SKILL.md Common
Errors table's *documented fix* actually works, not just that the error
occurs. Uses PDB 3PTB (trypsin + benzamidine) -- a real structure not used
in the original audit's PLIP test (which used 1HSG).

SKILL.md's new row says: "Use a conda-forge Open Babel build with InChI
support, or monkeypatch pybel.Molecule.write to no-op for format='inchikey'."
This applies exactly that second workaround and confirms PLIP completes
analyze() and reports real interactions.
"""
import sys
from openbabel import pybel
from plip.structure.preparation import PDBComplex

# Documented workaround: monkeypatch pybel.Molecule.write to no-op for inchikey
_orig_write = pybel.Molecule.write
def _patched_write(self, format='smi', filename=None, overwrite=False, opt=None):
    if format == 'inchikey':
        return ''
    return _orig_write(self, format=format, filename=filename, overwrite=overwrite, opt=opt)
pybel.Molecule.write = _patched_write

mol_complex = PDBComplex()
mol_complex.load_pdb('../../../audit-envs/cheminformatics-hit-triage-analyst/smoke/dock/3ptb.pdb')
mol_complex.analyze()

n_interactions = 0
types_seen = set()
for site_key, site in mol_complex.interaction_sets.items():
    for interaction in site.all_itypes:
        n_interactions += 1
        types_seen.add(type(interaction).__name__)

print('PDB 3PTB (trypsin + benzamidine) -- real structure, not used in original audit')
print('analyze() completed without raising after documented monkeypatch workaround')
print('total interaction records:', n_interactions)
print('interaction classes seen:', sorted(types_seen))
