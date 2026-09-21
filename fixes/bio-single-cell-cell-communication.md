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

---

## 2026-09-21 fix pass (re-audit of 6d96d9c)

Fixer for `single-cell/cell-communication`. Worktree `F:\OpenScience\wt\single-cell-cell-communication`, branch
`fix/single-cell-cell-communication`. Env: `liana-venv` (cellphonedb 5.0.1, liana 1.10.0), real PBMC 1k v3 audit data.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| CellPhoneDB determinism verified only at threads=1, but the documented block used threads=4 (82/120,375 flags flipped across two seeded runs) | P1 | Documented call now `threads=1`; code comment and the `debug_seed` row of the rationale table say seeding is bit-reproducible only at threads=1 and use `threads>1` for exploration only | ran | Two runs of the exact block (iterations=100, threads=1, debug_seed=1337): p-value frames `equals` True, shape (535, 238). Chose the audit's option 1 (threads=1) plus the caveat, so the block and the table agree |
| Condition Comparison had no sampling-noise warning or stability check (null split gave 27.6% gained/lost) | P1 | Added a "Stability check" paragraph and code: permute condition labels within cell type, repeat the comparison 10 times, report real gained+lost against the null range, flag pairs gained/lost in >=50% of null splits as noise-prone | ran | Own script on the audit's data with a stratified-random (true null) condition column: "real" 282 gained+lost vs null splits 290, 259 (inside the range, as it must be); 214/282 pairs noise-prone. The exact SKILL.md block was also extracted and run unchanged with 2 null repeats: real 282 vs null 279-294, no errors |
| usage-guide.md Related Skills duplicated SKILL.md verbatim | P2 | Replaced by a one-line pointer to SKILL.md | read | |
| SKILL.md was 308 lines after the fixes | length rule | Split into `references/cellphonedb.md`, `references/cellchat.md`, `references/nichenet.md` (the three method sections, verbatim); SKILL.md 234 lines, gets a Reference Files index and pointers from the three Method Decision Table rows | ran | Compared non-blank lines before/after: only the three decision-table rows changed (pointer added). Moved fences: python `ast.parse` OK; both R fences `parse()` OK via `rs.sh` (R 4.4.3) |

### Redundancy pass

- `usage-guide.md` Related Skills (8 lines) deleted; the list lives in SKILL.md Related Skills. Nothing unique.
- No other repetition found: the Overview, Quick Start and Example Prompts are guide-only content.

### Left unfixed

None of the 2 P1s or the P2 left unfixed. Not run: the CellChat and NicheNet blocks (moved verbatim, parse-checked only)
because CellChat and nichenetr are GitHub-only and not installed here (`TOOLS.md`); no defect was reported in them.

