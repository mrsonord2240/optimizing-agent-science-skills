"""
Input 2 (Variant A): solver panel + Robinson-Foulds + triplets-correct, following
SKILL.md 'Compare Solvers and Score Tree Robustness'.
Also runs the T3 Skill-Veto determinism check: run the SAME solver on the SAME
character matrix twice and diff the newick strings / RF distance.
"""
import cassiopeia as cas
import pandas as pd
import numpy as np

char_matrix = pd.read_csv('../data/character_matrix.csv', index_col=0)
cell_meta = pd.read_csv('../data/cell_metadata.csv', index_col=0)

def build_tree():
    return cas.data.CassiopeiaTree(character_matrix=char_matrix, cell_meta=cell_meta)

# --- Solver panel: VanillaGreedy, HybridSolver, NeighborJoining ---
tree_vg = build_tree()
cas.solver.VanillaGreedySolver().solve(tree_vg, collapse_mutationless_edges=True)

tree_hybrid = build_tree()
hybrid = cas.solver.HybridSolver(
    top_solver=cas.solver.VanillaGreedySolver(),
    bottom_solver=cas.solver.VanillaGreedySolver(),  # ILPSolver needs Gurobi license -- not available here
    cell_cutoff=200,
)
hybrid.solve(tree_hybrid, collapse_mutationless_edges=True)

tree_nj = build_tree()
# NOTE (audit finding): SKILL.md's example calls NeighborJoiningSolver(...).solve(tree) with no
# root handling. Running that exactly as documented raises:
#   cassiopeia.mixins.errors.DistanceSolverError: Please specify an explicit root sample in the
#   Cassiopeia Tree or specify the solver to add an implicit root
# add_root=True is required and is undocumented in the Skill.
cas.solver.NeighborJoiningSolver(
    dissimilarity_function=cas.solver.dissimilarity_functions.weighted_hamming_distance,
    add_root=True,
).solve(tree_nj)

rf_vg_nj, rf_max = cas.critique.robinson_foulds(tree_vg, tree_nj)
triplet_vg_nj = cas.critique.triplets_correct(tree_vg, tree_nj)
print(f'RF(VanillaGreedy, NJ) = {rf_vg_nj}/{rf_max}')
print('triplets-correct(VanillaGreedy, NJ) (depth-stratified):', triplet_vg_nj)

rf_vg_hy, rf_max2 = cas.critique.robinson_foulds(tree_vg, tree_hybrid)
print(f'RF(VanillaGreedy, Hybrid[greedy/greedy since no Gurobi]) = {rf_vg_hy}/{rf_max2}')

# --- T3 determinism check: same solver, same input, run twice ---
tree_run1 = build_tree()
cas.solver.VanillaGreedySolver().solve(tree_run1, collapse_mutationless_edges=True)
newick_run1 = tree_run1.get_newick()

tree_run2 = build_tree()
cas.solver.VanillaGreedySolver().solve(tree_run2, collapse_mutationless_edges=True)
newick_run2 = tree_run2.get_newick()

print('VanillaGreedy determinism check: identical newick across 2 runs?', newick_run1 == newick_run2)

rf_repeat, rf_repeat_max = cas.critique.robinson_foulds(tree_run1, tree_run2)
print(f'RF(run1, run2) same-solver-same-data = {rf_repeat}/{rf_repeat_max}  (0 = fully deterministic)')

# NJ determinism check too
tree_nj_run1 = build_tree()
cas.solver.NeighborJoiningSolver(dissimilarity_function=cas.solver.dissimilarity_functions.weighted_hamming_distance, add_root=True).solve(tree_nj_run1)
tree_nj_run2 = build_tree()
cas.solver.NeighborJoiningSolver(dissimilarity_function=cas.solver.dissimilarity_functions.weighted_hamming_distance, add_root=True).solve(tree_nj_run2)
print('NJ determinism check: identical newick across 2 runs?', tree_nj_run1.get_newick() == tree_nj_run2.get_newick())
