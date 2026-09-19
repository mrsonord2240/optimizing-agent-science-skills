"""
Re-auditor: 'Refine a Tree Under Severe Homoplasy with Startle' SKILL.md
snippet, run on the re-auditor's OWN new/harder dataset (data2, 80 cells,
20 sites, 2 independent homoplasy events) -- not the fixer's original
60-cell/16-site matrix. Builds a seed tree with VanillaGreedySolver, exports
priors + character matrix + newick, then calls the Startle CLI.
"""
import cassiopeia as cas
import pandas as pd

char_matrix = pd.read_csv('../data2/character_matrix2.csv', index_col=0)
cell_meta = pd.read_csv('../data2/cell_metadata2.csv', index_col=0)

tree = cas.data.CassiopeiaTree(character_matrix=char_matrix, cell_meta=cell_meta)
solver = cas.solver.VanillaGreedySolver()
solver.solve(tree, collapse_mutationless_edges=True)
with open('seed_tree2.newick', 'w') as f:
    f.write(tree.get_newick())
print('seed tree written, newick len =', len(tree.get_newick()))

rows = []
for c in char_matrix.columns:
    col = char_matrix[c]
    edited = col[(col != 0) & (col != -1)]
    for state, p in edited.value_counts(normalize=True).items():
        rows.append({'character': c, 'state': int(state), 'probability': float(p)})
pd.DataFrame(rows).to_csv('startle_priors2.csv', index=False)
char_matrix.to_csv('startle_char_matrix2.csv')
print('priors and char matrix written for Startle')
