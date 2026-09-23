# Copied verbatim from SKILL.md "Reactivity Surrogates" section (chemoinformatics/covalent-design)
from rdkit import Chem


def acrylamide_alpha_substitution_count(smi):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None
    acryl_pat = Chem.MolFromSmarts(
        '[CX3:1](=[OX1:2])([NX3:3])[CX3:4]=[CX3:5]'
    )
    matches = mol.GetSubstructMatches(acryl_pat, uniquify=True)
    if not matches:
        return None
    alpha_query_idx = next(
        atom.GetIdx() for atom in acryl_pat.GetAtoms()
        if atom.GetAtomMapNum() == 4
    )
    alpha_c = mol.GetAtomWithIdx(matches[0][alpha_query_idx])
    n_subs = len([n for n in alpha_c.GetNeighbors() if n.GetIdx() not in matches[0]])
    return n_subs
