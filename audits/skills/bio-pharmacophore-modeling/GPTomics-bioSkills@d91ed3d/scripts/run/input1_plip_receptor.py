# Input 1 (Canonical) -- receptor-based pharmacophore via PLIP on a real co-crystal.
# Follows SKILL.md's "Receptor-Based Pharmacophore (apo2ph4 workflow)" PLIP snippet verbatim,
# run against PDB 1HSG (HIV-1 protease + indinavir precursor MK-639, ligand code MK1).
# Run with the plip-venv interpreter (F:\OpenScience\audit-envs\...\tools\plip-venv\Scripts\python.exe)
from plip.structure.preparation import PDBComplex

# Environment workaround (not a Skill defect): this plip-venv's openbabel-wheel build
# ships no InChI writer at all (confirmed in cheminformatics-hit-triage-analyst/TOOLS.md
# note 5 -- "No InChI in either Open Babel build"). PLIP's Ligand.__init__ unconditionally
# calls molecule.write(format='inchikey') to populate an identifier field that interaction
# detection itself never reads. Patch pybel.Molecule.write to no-op only for that one format
# so the real interaction analysis can run; every other write path is untouched.
from openbabel import pybel
_orig_write = pybel.Molecule.write
def _write_patched(self, format='smi', *a, **kw):
    if format == 'inchikey':
        return ''
    return _orig_write(self, format, *a, **kw)
pybel.Molecule.write = _write_patched

mol_complex = PDBComplex()
mol_complex.load_pdb('data/1hsg.pdb')
mol_complex.analyze()

print("Binding sites found:", list(mol_complex.interaction_sets.keys()))

for site_name, site in mol_complex.interaction_sets.items():
    print(f"\n=== Site: {site_name} ===")
    for itype_name in ['hbonds_ldon', 'hbonds_pdon', 'hydrophobic_contacts',
                        'pistacking', 'pication_laro', 'pication_paro',
                        'saltbridge_lneg', 'saltbridge_pneg', 'halogen_bonds',
                        'water_bridges', 'metal_complexes']:
        interactions = getattr(site, itype_name, [])
        if interactions:
            print(f"-- {itype_name}: {len(interactions)}")
            for i, inter in enumerate(interactions):
                cls = type(inter).__name__
                # Inspect documented fields per interaction class, as the Skill directs
                fields = {}
                for attr in ['distance', 'distance_ad', 'distance_aw', 'distance_dw',
                             'restype', 'resnr', 'reschain', 'restype_l', 'resnr_l',
                             'reschain_l', 'sidechain', 'don_orig_idx', 'acc_orig_idx',
                             'water_orig_idx']:
                    if hasattr(inter, attr):
                        fields[attr] = getattr(inter, attr)
                print(f"   [{i}] {cls} {fields}")

    # Also dump the generic all_itypes union used in SKILL.md's example
    all_types = site.all_itypes
    print(f"-- all_itypes total: {len(all_types)}")
    type_counts = {}
    for inter in all_types:
        cls = type(inter).__name__
        type_counts[cls] = type_counts.get(cls, 0) + 1
    print("   class counts:", type_counts)
