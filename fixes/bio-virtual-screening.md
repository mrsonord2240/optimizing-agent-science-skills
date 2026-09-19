# bio-virtual-screening fixes (2026-09-19)

Worktree `F:\OpenScience\wt\cg-vscreen`, branch `fix/cg-vscreen` off fork `main`
(`eba37f4`). Runtime: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\`
(pdb2pqr 3.7.1, meeko 0.8.0, AutoDock Vina 1.2.7 CLI). Data: audit fixture
`F:\OpenScience\audits\bio-virtual-screening\data\rec.pdb` / `lig_benzamidine.pdbqt`
(PDB 3PTB, trypsin + benzamidine), copied to scratchpad before use.

## Verification re-run (scratchpad `vscreen_verify/`)

```
pdb2pqr --ff=AMBER --with-ph=7.4 --pdb-output rec_pH7.4.pdb rec.pdb rec_pH7.4.pqr   # exit 0
mk_prepare_receptor --read_pdb rec_pH7.4.pdb -o receptor -p                        # exit 0, receptor.pdbqt (162,891 bytes)
vina --receptor receptor.pdbqt --ligand lig_benzamidine.pdbqt \
     --center_x -1.52 --center_y 14.47 --center_z 17.47 \
     --size_x 20 --size_y 20 --size_z 20 \
     --exhaustiveness 8 --num_modes 9 --seed 42 --out out_seed42.pdbqt
# best mode -5.978 kcal/mol (9 modes, all negative this run)
```
Same target, structure, and insertion-code residues (184A etc.) as the audit's own
run. `mk_prepare_receptor` (no `.py`) and the `--pdb-output`/`--read_pdb` route both
confirmed by direct execution, not by inspection.

## Findings

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `mk_prepare_receptor.py` is not the installed command name | P1 | `SKILL.md` `prepare_receptor()` and `examples/virtual_screen.py` `prepare_receptor()`: `mk_prepare_receptor.py` -> `mk_prepare_receptor`; note added to Version Compatibility and Common Errors | ran | |
| `--read_pqr` route crashes on insertion-code residues (e.g. trypsin/chymotrypsin numbering) | P1 | `SKILL.md` `prepare_receptor()` switched to `pdb2pqr --pdb-output <pdb>` + `mk_prepare_receptor --read_pdb <pdb>`; pitfall note + Common Errors row added; `examples/virtual_screen.py`'s `prepare_receptor()` docstring now states the input must come from `--pdb-output` | ran (see re-run above, same 3PTB insertion codes) | `examples/virtual_screen.py` already used `--read_pdb`, just had the `.py` bug; unified both call sites on the same working route |
| No seed/determinism guidance for Vina (pose ranks 2+ vary run-to-run) | P1 | `dock_single()`/`virtual_screen()` in both `SKILL.md` and `examples/virtual_screen.py` gained a `seed=42` parameter (`Vina(seed=seed)` / CLI `--seed`); new "Seed and reproducibility" note | ran (`--seed 42` accepted by Vina CLI 1.2.7); `Vina.__init__(seed=...)` per official AutoDock-Vina Python bindings source -- not executable here (no Windows wheel, pre-existing P2) | Python-API `seed` kwarg checked against docs only, flagged below |
| `from vina import Vina` has no Windows wheel | P2 | One-line platform note added next to the existing version-based CLI-fallback comment in "Vina Docking (Single Ligand)" and in Version Compatibility | docs (pip build error already recorded in `TOOLS.md`; unbuildable here, matches audit) | |
| Docked poses not sanity-filtered (positive-energy outlier mode) | P2 | `dock_single()` now filters `affinity >= 0` modes before returning; `virtual_screen()`'s per-ligand loop does the same; new "Sanity-filter reported poses" note | ran the docking step; filter logic itself is a straightforward comparison, not separately exercised against a positive-energy mode (none appeared in this re-run) | |
| PDBQT->SDF handoff loses formal bond order/charge for charged ligands | P2 | "Handoff caveat" paragraph added after the pose-validation cross-reference, recommending carrying the original RDKit `Mol` alongside the PDBQT instead of reconstructing bonds from the pose | docs/reasoning (RDKit sanitization failure on PDBQT->SDF round-trip is the audit's own finding, Input 5); no clean programmatic fix exists -- documented as a known limitation, as the brief allows | |

## Redundancy pass (mandatory every fix, not audit-flagged)

`usage-guide.md`'s Tips section restated four points already in `SKILL.md`
(exhaustiveness default, box-from-ligand sizing, centering-on-co-crystal, and the
waters/cofactors/metals review) -- deleted, Tips now points at the `SKILL.md`
sections by name. Two Tips had no `SKILL.md` home and were agent-relevant, not
human-only, so they moved rather than being deleted:
- "benchmark any GPU port of Vina before adopting it" -> merged into the "GPU mode
  slow" row of `SKILL.md`'s Common Errors table.
- "Vina 1.1.2 vs 1.2 may give different poses" -> appended to `SKILL.md`'s Version
  Compatibility paragraph.

## Unfixed

- None of the 6 recommendations were left unfixed. The `vina` Python-API `seed`
  kwarg is verified against documentation only (package cannot build on this
  Windows machine at all, a pre-existing constraint, not introduced by this fix).
