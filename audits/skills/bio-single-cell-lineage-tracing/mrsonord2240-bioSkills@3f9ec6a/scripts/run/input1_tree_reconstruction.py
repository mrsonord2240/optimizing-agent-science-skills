"""
Input 1 (Canonical) execution, following SKILL.md 'Build a Character Matrix and
Reconstruct a Tree' pattern verbatim against the synthetic character_matrix.csv.
"""
import cassiopeia as cas
import pandas as pd
import numpy as np

char_matrix = pd.read_csv('../data/character_matrix.csv', index_col=0)
cell_meta = pd.read_csv('../data/cell_metadata.csv', index_col=0)

tree = cas.data.CassiopeiaTree(character_matrix=char_matrix, cell_meta=cell_meta)
print(f'cells {tree.n_cell}  characters {tree.n_character}  missing {(char_matrix.values == -1).mean():.2%}')

solver = cas.solver.VanillaGreedySolver()
solver.solve(tree, collapse_mutationless_edges=True)
newick = tree.get_newick()
print('NEWICK (first 300 chars):', newick[:300])

tree.reconstruct_ancestral_characters()
print('Ancestral character reconstruction: OK, internal nodes =', len(tree.internal_nodes))
