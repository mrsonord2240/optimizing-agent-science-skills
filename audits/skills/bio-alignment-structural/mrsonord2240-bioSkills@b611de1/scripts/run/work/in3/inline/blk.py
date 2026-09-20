from Bio.PDB import PDBParser, Superimposer

parser = PDBParser(QUIET=True)
mobile = parser.get_structure('mobile', 'mobile.pdb')
reference = parser.get_structure('ref', 'reference.pdb')

def ca_by_residue(structure):
    return {(c.id, r.id[1], r.id[2]): r['CA'] for c in structure[0] for r in c
            if r.id[0] == ' ' and 'CA' in r}     # ' ' = standard residue: no waters, ions, ligands

ca_m, ca_r = ca_by_residue(mobile), ca_by_residue(reference)
keys = sorted(set(ca_m) & set(ca_r))
assert keys, 'no shared (chain, number, icode): not co-numbered; use TMalign / USalign'
sup = Superimposer()
sup.set_atoms([ca_r[k] for k in keys], [ca_m[k] for k in keys])
sup.apply(list(mobile.get_atoms()))
print(f'RMSD: {sup.rms:.3f} A over {len(keys)} CA pairs')
