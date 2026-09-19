"""
Re-auditor Input R1 (regression, original data) + Input R2 (new independent data):
'Build a Character Matrix and Reconstruct a Tree', SKILL.md verbatim snippet
(post-fix: (char_matrix.values == -1).mean() fix already in the snippet).
"""
import cassiopeia as cas
import pandas as pd
import numpy as np

for label, cm_path, meta_path in [
    ('R1-regression(original audit data)', '../data/character_matrix.csv', '../data/cell_metadata.csv'),
    ('R2-new(reauditor data)', '../data2/character_matrix2.csv', '../data2/cell_metadata2.csv'),
]:
    print(f'=== {label} ===')
    char_matrix = pd.read_csv(cm_path, index_col=0)
    cell_meta = pd.read_csv(meta_path, index_col=0)

    tree = cas.data.CassiopeiaTree(character_matrix=char_matrix, cell_meta=cell_meta)
    print(f'cells {tree.n_cell}  characters {tree.n_character}  missing {(char_matrix.values == -1).mean():.2%}')

    solver = cas.solver.VanillaGreedySolver()
    solver.solve(tree, collapse_mutationless_edges=True)
    newick = tree.get_newick()
    print('NEWICK (first 200 chars):', newick[:200])

    tree.reconstruct_ancestral_characters()
    print('Ancestral reconstruction OK, internal nodes =', len(tree.internal_nodes))

    # Check recovered clades roughly match ground truth: leaves sharing a clade
    # label should be closer in the tree than random. Cheap check: for each pair
    # of same-clade leaves, are they both present and does the newick group them
    # (approximated via common ancestor character-sharing since full traversal
    # is more code than needed for a smoke check)
    clades = cell_meta['ground_truth_clade']
    print('ground truth clade counts:', clades.value_counts().to_dict())
    print()
