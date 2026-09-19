"""
Regression of original audit input 1 (PLIP receptor-based, PDB 1HSG),
re-run using the workaround now DOCUMENTED in SKILL.md's Common Errors
table (previously the auditor used an undocumented ad-hoc patch).
"""
from openbabel import pybel
from plip.structure.preparation import PDBComplex

_orig_write = pybel.Molecule.write
def _patched_write(self, format='smi', filename=None, overwrite=False, opt=None):
    if format == 'inchikey':
        return ''
    return _orig_write(self, format=format, filename=filename, overwrite=overwrite, opt=opt)
pybel.Molecule.write = _patched_write

mol_complex = PDBComplex()
mol_complex.load_pdb('../data/1hsg.pdb')
mol_complex.analyze()

hbonds, hydrophobic, saltbridge, waterbridge = 0, 0, 0, 0
for site in mol_complex.interaction_sets.values():
    for interaction in site.all_itypes:
        cn = type(interaction).__name__
        if cn == 'hbond':
            hbonds += 1
        elif cn == 'hydroph_interaction':
            hydrophobic += 1
        elif cn == 'saltbridge':
            saltbridge += 1
        elif cn == 'waterbridge':
            waterbridge += 1

print('h-bonds:', hbonds, '| hydrophobic:', hydrophobic, '| salt bridges:', saltbridge, '| water bridges:', waterbridge)
