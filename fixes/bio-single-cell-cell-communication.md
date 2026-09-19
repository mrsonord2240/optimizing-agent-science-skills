# Fix log: bio-single-cell-cell-communication

2026-09-19. Fixer for `single-cell/cell-communication` (audit score 86, Limited Release, deployable,
no open P0). Worktree `F:\OpenScience\wt\sc-cellcomm`, branch `fix/sc-cell-communication`, commit
`6d96d9c`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| SKILL.md's CellPhoneDB code block crashes with a multiprocessing `RuntimeError` on Windows under `score_interactions=True` | P1 | Wrapped the documented `cpdb_statistical_analysis_method.call(...)` in `def main(): ... / if __name__ == '__main__':` | ran | `liana-venv` (cellphonedb 5.0.1), guarded call with `score_interactions=True, threads=4` completed with no crash |
| CellPhoneDB permutation p-values non-deterministic (`debug_seed` defaults to `-1`, never set in the documented call) | P1 | Added `debug_seed=1337` to the documented call; added a row to the Threshold and Permutation Rationale table | ran | Two identical guarded runs (iterations=100, threads=1, real PBMC 1k v3 data) with `debug_seed=1337`: 0/120,375 significance flags flipped, p-value columns bit-identical (`(p1==p2).all()` True). Audit's unseeded baseline flipped 252/120,375 |
| Frontmatter promises "comparing communication across conditions" but no method has runnable code for it | P1 | Wrote a new "Condition Comparison" SKILL.md section: per-condition LIANA `rank_aggregate` runs, diffed on robust (magnitude+specificity) sets to get gained/lost pairs; points to Tensor-cell2cell for the many-condition case (already named in Method Decision Table) | ran + py_compile | Ran end-to-end on real PBMC 1k v3 data with a synthetic 50/50 condition split (control 779 robust pairs / stimulated 1,118 / 409 gained / 70 lost / 709 shared), no errors. Chose "write it" over "install it" (Tensor-cell2cell not installed, out of scope to add) or "delete the claim" (LIANA alone, already confirmed working, covers the two-condition case cleanly) |
| SKILL.md says a single `groupby` group "yields only autocrine self-edges" | P2 | Corrected the sentence: a single group raises a `ValueError` (log2FC has no comparison group), not a silent autocrine-only result | docs (audit's own Input 3 run, `run/04_liana_single_group_edge.py`) | Text-only correction, no code changed, no re-run needed |

## Redundancy pass (mandatory every fix, not audit-flagged)

- `usage-guide.md`'s "Prerequisites" section (pip/R install commands) existed only in the guide but is
  agent-actionable -- moved into SKILL.md as its own `## Prerequisites` section, right after Version
  Compatibility. Not deleted, relocated.
- `usage-guide.md`'s "What the Agent Will Do" (7 steps) and "Tips" (9 bullets) sections deleted in full:
  every point in both restated a fact already stated in SKILL.md (Governing Principle, Confounds table,
  Common Errors table, or a method section's own prose) -- consensus-over-single-method, resource
  sensitivity, magnitude vs specificity axes, ambient RNA decontamination, abundance/depth confounds,
  dissociation-stress genes, NicheNet's gene-set dependency, membrane-bound-ligand contact requirement,
  mouse-data routing, and orthogonal validation are all already in SKILL.md. Checked each bullet
  individually against SKILL.md before deleting; nothing unique was found, so nothing else needed to
  move.
- `usage-guide.md` now holds only Overview, Quick Start, Example Prompts, and Related Skills.

## Left unfixed

None of the three P1s or the P2 were left unfixed.

## Notes for re-auditor

- `examples/` ships `liana_analysis.py` and `cellchat_analysis.R` only; there was no shipped CellPhoneDB
  example script to fix alongside SKILL.md's inline block.
- CellChat and nichenetr remain out of live-execution scope on this Windows box (GitHub-only packages,
  per `TOOLS.md`); their sections were not touched (audit found no defect in them beyond the P1 already
  covered by nichenetr's static review).
