"""Phase 2 Input 6: prepare exact Startle inputs from the fresh scar matrix."""
import cassiopeia as cas
import pandas as pd

char_matrix = pd.read_csv("../data/phase2_character_matrix.csv", index_col=0)
tree = cas.data.CassiopeiaTree(character_matrix=char_matrix)
solver = cas.solver.VanillaGreedySolver()
solver.solve(tree, collapse_mutationless_edges=True)
with open("phase2_seed_tree.newick", "w", encoding="utf-8") as handle:
    handle.write(tree.get_newick())
rows = []
for c in char_matrix.columns:
    edited = char_matrix[c][(char_matrix[c] != 0) & (char_matrix[c] != -1)]
    for state, p in edited.value_counts(normalize=True).items():
        rows.append({"character": c, "state": int(state), "probability": float(p)})
pd.DataFrame(rows).to_csv("phase2_startle_priors.csv", index=False)
char_matrix.to_csv("phase2_startle_character_matrix.csv")
assert rows and tree.get_newick().endswith(";")
print("input6 preparation PASS", len(rows), "priors")
