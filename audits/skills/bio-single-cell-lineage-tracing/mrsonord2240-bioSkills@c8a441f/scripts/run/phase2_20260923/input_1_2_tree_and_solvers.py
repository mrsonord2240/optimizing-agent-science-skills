"""Phase 2 Inputs 1-2: execute the current SKILL.md tree and solver patterns."""
import cassiopeia as cas
import numpy as np
import pandas as pd

rng = np.random.default_rng(20260923)
cells = [f"cell_{i:02d}" for i in range(36)]
clades = np.repeat(["A", "B", "C"], 12)
matrix = np.zeros((36, 12), dtype=int)
matrix[clades == "A", :4] = 1
matrix[clades == "B", 4:8] = 2
matrix[clades == "C", 8:] = 3
matrix[rng.random(matrix.shape) < 0.08] = -1
char_matrix = pd.DataFrame(matrix, index=cells, columns=[f"site_{i}" for i in range(12)])
cell_meta = pd.DataFrame({"ground_truth_clade": clades}, index=cells)
char_matrix.to_csv("../data/phase2_character_matrix.csv")
cell_meta.to_csv("../data/phase2_cell_metadata.csv")

# Literal current SKILL.md reconstruction block.
tree = cas.data.CassiopeiaTree(character_matrix=char_matrix, cell_meta=cell_meta)
print(f"cells {tree.n_cell} characters {tree.n_character} missing {(char_matrix.values == -1).mean():.2%}")
solver = cas.solver.VanillaGreedySolver()
solver.solve(tree, collapse_mutationless_edges=True)
newick = tree.get_newick()
tree.reconstruct_ancestral_characters()
assert newick.endswith(";") and len(tree.leaves) == 36
print("input1 PASS parseable Newick", len(newick), "internal_nodes", len(tree.internal_nodes))

def make_tree():
    return cas.data.CassiopeiaTree(character_matrix=char_matrix, cell_meta=cell_meta)

# The documented NJ branch must use add_root=True.
nj_tree = make_tree()
cas.solver.NeighborJoiningSolver(
    dissimilarity_function=cas.solver.dissimilarity_functions.weighted_hamming_distance,
    add_root=True,
).solve(nj_tree)
assert nj_tree.get_newick().endswith(";")
try:
    licensed = cas.solver.ILPSolver()
    licensed.solve(make_tree())
    ilp_note = "ILPSolver unexpectedly ran"
except Exception as exc:
    ilp_note = f"documented unlicensed ILPSolver failure: {type(exc).__name__}"

# Explicitly take the license-free option documented in the preceding source comment.
hybrid = cas.solver.HybridSolver(
    top_solver=cas.solver.VanillaGreedySolver(),
    bottom_solver=cas.solver.VanillaGreedySolver(),
    cell_cutoff=200,
)
hybrid_tree = make_tree()
hybrid.solve(hybrid_tree, collapse_mutationless_edges=True)
rf, rf_max = cas.critique.robinson_foulds(tree, nj_tree)
assert hybrid_tree.get_newick().endswith(";") and rf_max > 0
print("input2 PASS", ilp_note, f"RF={rf}/{rf_max}")
