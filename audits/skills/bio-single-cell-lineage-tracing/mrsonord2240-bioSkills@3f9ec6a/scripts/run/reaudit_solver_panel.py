"""
Re-auditor Input R3: solver panel + the two undocumented-API fixes the fixer
claims (NeighborJoiningSolver add_root=True, ILPSolver Gurobi requirement),
run on the re-auditor's OWN independent dataset (data2), not the fixer's.
Also re-confirms determinism (T3 veto) on this new data.
"""
import cassiopeia as cas
import pandas as pd

char_matrix = pd.read_csv('../data2/character_matrix2.csv', index_col=0)
cell_meta = pd.read_csv('../data2/cell_metadata2.csv', index_col=0)


def build_tree():
    return cas.data.CassiopeiaTree(character_matrix=char_matrix, cell_meta=cell_meta)


# 1) NJ WITHOUT add_root -- confirm it still throws DistanceSolverError as the
#    fixer claims (i.e. the fix note is accurate, not just documentation theater)
print('--- NJ without add_root (expect DistanceSolverError) ---')
try:
    tree_bad = build_tree()
    cas.solver.NeighborJoiningSolver(
        dissimilarity_function=cas.solver.dissimilarity_functions.weighted_hamming_distance,
    ).solve(tree_bad)
    print('UNEXPECTED: no error raised')
except Exception as e:
    print(f'Confirmed raises: {type(e).__name__}: {e}')

# 2) NJ WITH add_root=True -- confirm the documented fix works
print('--- NJ with add_root=True ---')
tree_nj = build_tree()
cas.solver.NeighborJoiningSolver(
    dissimilarity_function=cas.solver.dissimilarity_functions.weighted_hamming_distance,
    add_root=True,
).solve(tree_nj)
print('NJ solved OK, newick len =', len(tree_nj.get_newick()))

# 3) ILPSolver without gurobipy -- confirm it still fails as documented
print('--- ILPSolver without gurobipy (expect failure) ---')
try:
    tree_ilp = build_tree()
    cas.solver.ILPSolver().solve(tree_ilp)
    print('UNEXPECTED: no error raised')
except Exception as e:
    print(f'Confirmed raises: {type(e).__name__}: {e}')

# 4) HybridSolver with greedy/greedy fallback (license-free, as documented)
print('--- HybridSolver(greedy/greedy) ---')
tree_hybrid = build_tree()
hybrid = cas.solver.HybridSolver(
    top_solver=cas.solver.VanillaGreedySolver(),
    bottom_solver=cas.solver.VanillaGreedySolver(),
    cell_cutoff=200,
)
hybrid.solve(tree_hybrid, collapse_mutationless_edges=True)
print('Hybrid greedy/greedy solved OK, newick len =', len(tree_hybrid.get_newick()))

# 5) VanillaGreedy for RF/triplets comparison
tree_vg = build_tree()
cas.solver.VanillaGreedySolver().solve(tree_vg, collapse_mutationless_edges=True)
rf, rf_max = cas.critique.robinson_foulds(tree_vg, tree_nj)
print(f'RF(VanillaGreedy, NJ) on NEW data = {rf}/{rf_max}')
triplet = cas.critique.triplets_correct(tree_vg, tree_nj)
print('triplets-correct (depth-stratified):', {k: v for k, v in list(triplet[0].items())[:3]} if isinstance(triplet, tuple) else 'see raw', )

# 6) Determinism (T3) on the new dataset: same solver, same data, twice
tree_a = build_tree(); cas.solver.VanillaGreedySolver().solve(tree_a, collapse_mutationless_edges=True)
tree_b = build_tree(); cas.solver.VanillaGreedySolver().solve(tree_b, collapse_mutationless_edges=True)
print('Determinism (VanillaGreedy) on NEW data: identical newick?', tree_a.get_newick() == tree_b.get_newick())
rf_rep, rf_rep_max = cas.critique.robinson_foulds(tree_a, tree_b)
print(f'RF(run1,run2) = {rf_rep}/{rf_rep_max} (0 = deterministic)')
