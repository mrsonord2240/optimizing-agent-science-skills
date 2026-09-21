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

---

# 2026-09-21 (Production Ready P2 batch)

Worktree `F:\OpenScience\wt\chemoinformatics-virtual-screening`, branch
`fix/chemoinformatics-virtual-screening` off staging `431aa55`. Commits: `745ffa9` (fix),
`2158b54` (split), `7dc9c5d` (scripts). Env `cheminformatics-hit-triage-analyst`: Vina 1.2.7 CLI,
meeko 0.8.0, RDKit 2026.03.6, PoseBusters 0.6.5, pdb2pqr 3.7.1. Data: audit fixture
`data\rec.pdb` / `lig_benzamidine.pdbqt` (PDB 3PTB), copied to scratchpad.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Insertion-code failure mode documented too narrowly | P2 | Pitfall note and Common Errors row now state the generic cause (any residue with a PDB insertion code; trypsin 3PTB and elastase 1EAI as examples) | ran: wording matches the audit's runs on 3PTB and 1EAI; the `--pdb-output` route re-ran on 3PTB (receptor PDBQT 162,891 bytes) | |
| PDBQT->SDF bond-order/charge loss left open | P2 | Replaced the "no clean fix" caveat with a working recipe: meeko `PDBQTMolecule.from_file(..., skip_typing=True)` + `RDKitMolCreate.from_pdbqt_mol` rebuilds the pose from the `REMARK SMILES` that Vina keeps in its output; new Common Errors row | ran: benzamidine docked to 3PTB, `obabel` route PoseBusters 3/12, meeko route 12/12 on all 5 poses; snippet extracted from SKILL.md and executed; also on a ligand freshly made by `examples/virtual_screen.py` | Needs a meeko-written ligand PDBQT (carries the SMILES); caveat says to carry the RDKit `Mol` otherwise. Contradicts the audit's "no clean fix exists": the audit converted with `obabel` only. |

## Redundancy pass

Already done in the 2026-09-19 pass (`usage-guide.md` Tips point at SKILL.md); nothing further
duplicated. The pointer to "Per-Tool Failure Modes" in `usage-guide.md` now names
`references/failure-modes.md`.

## Split (commit `2158b54`)

SKILL.md 419 -> 268 lines (405 originally; +14 from the fix). Verbatim moves; no non-blank line lost
(checked by multiset comparison; only the three decision-tree rows that gained pointers differ);
moved fences parse.

| old location | new home |
|---|---|
| "GNINA with CNN Scoring" section | `references/gnina.md` |
| "Virtual Screening Pipeline (Hierarchical)" and "Ultralarge Library Screening" | `references/ultralarge-screening.md` |
| "Per-Tool Failure Modes" and "Reconciliation: Vina vs GNINA" | `references/failure-modes.md` |

SKILL.md gained a "Reference Files" index and pointers in three decision-tree rows.

## Scripts (commit `7dc9c5d`)

SKILL.md 268 -> 214 lines.

| old location | script |
|---|---|
| `prepare_receptor()` block, Receptor Preparation | `scripts/prepare_receptor.py` (argparse CLI) |
| `dock_single()` block, Vina Docking | `scripts/dock_single.py` (Vina API; Vina CLI fallback where the `vina` wheel does not build; positive-energy filter; argparse CLI) |
| `prepare_ligand()` block, Ligand Preparation | not moved: duplicated `examples/virtual_screen.py`; block deleted, SKILL.md imports the example's function |

Ran as SKILL.md invokes them: `prepare_receptor.py` on 3PTB gave a 162,891-byte PDBQT (same as the
2026-09-19 run); `dock_single.py` (CLI path) best mode -5.978, byte-identical output over two runs at
seed 42, all 9 modes negative; the positive-energy filter was exercised with a fabricated +68 mode
(8 of 9 kept); a bad ligand path raises with Vina's own message. The `vina` Python-API branch is not
executable here (no Windows wheel) and is checked against the API docs only. `virtual_screen()` in the
example already carried its own copy of the filter.

## Left unfixed

- Nothing from the audit. The `vina` Python-API branch of `dock_single.py` and `examples/virtual_screen.py`
  stays unrun: `pip install vina` cannot build on this machine.
- Not fixed, noticed: `pose_validate`/`drug_like_filter`/`gnina_rescore` in
  `references/ultralarge-screening.md` remain `NotImplementedError` stubs (orchestrator skeleton, by design).
  GNINA has no Windows binary, so nothing there was run.
