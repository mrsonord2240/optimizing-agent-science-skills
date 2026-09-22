# bio-pose-validation — fix log

2026-09-19. Fixer for `chemoinformatics/pose-validation` (skill-id `bio-pose-validation`). Audit: 89/100,
Limited Release, deployable, no open P0. Worktree `F:\OpenScience\wt\cg-pose`, branch
`fix/cg-pose-validation`, commit `cae7409`.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| SKILL.md's `dock` config table claimed "all checks except RMSD reference" | P1 | Rewrote the `dock` row to name all 4 reference-dependent checks it drops (molecular formula, molecular bonds, double-bond stereo, chirality) plus RMSD; added a caveat line under the main check table stating stereo/chirality checks need `mol_true` | ran — `bust(config='dock')` vs `bust(config='redock', mol_true=...)` against a real Vina redock of benzamidine into 3PTB (reused audit fixtures `mode1_fixed.sdf`/`ben_ref.sdf`/`receptor.pdb`): dock=22 bool columns, redock=28; diff = `rmsd_<=_2å`, `mol_true_loaded`, `molecular_formula`, `molecular_bonds`, `double_bond_stereochemistry`, `tetrahedral_chirality` | Audit counted 27 (excluding the `mol_true_loaded` status column, a loading-status column analogous to `mol_pred_loaded`/`mol_cond_loaded`, not a check); the 5 real checks match the audit's finding exactly |
| Standalone `aromatic_planarity()` snippet claimed a 0.25 Å cutoff | P1 | Replaced the fixed-cutoff prose with the empirically verified pass/fail bracket (0.29 Å passes, 0.45 Å fails) and a note to treat `bust()`'s own `aromatic_ring_flatness` column as authoritative, not this reimplementation | ran — bisected a 4-point ring-displacement series (`puck_0.6/1.0/1.5/2.0.sdf`, reused from audit data) through both the Skill's SVD formula and installed `bust(config='mol')`: 0.6→0.2888 Å (bust passes), 1.0→0.4524 Å (bust fails), 1.5→0.5926 Å (fails), 2.0→0.6575 Å (fails) | Confirms the audit's 0.29–0.45 Å bracket exactly |
| `examples/validate_poses.py` shipped no test fixtures; `__main__` was a no-op print | P2 | Bundled a small public-domain fixture pair (RCSB PDB 3PTB, CC0, receptor + a real AutoDock Vina-redocked benzamidine pose — both reused from the audit's own data) under `examples/fixtures/`; wired `__main__` to run `pose_qc_pipeline` against them with an assertion | ran — `python examples/validate_poses.py` → `pb_valid=True`, `strain_kcal=4.162648`, matching the audit's independent run of the same code on the same input | Cheap fix per FIX_BRIEF; not scope creep since the code already existed and only needed a real input to execute |
| Redundancy pass (mandatory every fix, not audit-flagged) | — | `usage-guide.md`'s Prerequisites (pip install) moved into `SKILL.md`'s Version Compatibility section (install notes belong there); its Quick Start bullets folded into Example Prompts (no content lost — one entry, "identify chirality-inverted poses," was Quick-Start-only and is now an Example Prompt); its What-the-Agent-Will-Do narrative and 4 of 5 Tips deleted as restatements of SKILL.md's When-to-Apply table, Strain Energy section, Reconciliation table, and Common Errors table; the 5th tip ("use PoseBusters as a filter, not an absolute reject") existed only in usage-guide.md and is agent-actionable, so it moved into SKILL.md's Common Errors table as a new row instead of being deleted. `usage-guide.md` now holds only Overview, Example Prompts, Related Skills | ran — diffed old vs new usage-guide.md by hand; py_compile clean on the changed .py | — |

## Unfixed

None. Both P1s and the flagged P2 were fixed.

## Environment

`F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe` — PoseBusters 0.6.5, RDKit
2026.03.6, pandas 3.0.5 (per that env's `TOOLS.md`). `PYTHONIOENCODING=utf-8` needed for the `≤` character
in PoseBusters' RMSD column name on this Windows console. No packages installed or changed.

## 2026-09-21

Fixer for the Production Ready P2 batch. Worktree `F:\OpenScience\wt\chemoinformatics-pose-validation`, branch
`fix/chemoinformatics-pose-validation` from staging `431aa55`. Commits: `66bc056` (fix), `e4fa0a7` (scripts).
No split: SKILL.md was 300 lines (not over threshold) and is 177 after the scripts move.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `mol` config row claims "stereo" among its checks | P2 | Row now lists what `mol` returns (sanitization, bond lengths/angles, internal clash, ring and double-bond flatness, energy) and says stereo/chirality need `mol_true` | ran: `PoseBusters(config='mol').bust()` on the bundled fixture, PoseBusters 0.6.5: 12 boolean columns, asserted none contain "stereo" or "chiral" | Audit's suggested wording said "double-bond geometry"; the real column is `double_bond_flatness`, so the row names that |
| Redundancy pass | - | `dock` row no longer restates the four reference-dependent checks already listed under the check table. `usage-guide.md` was already deduplicated on 2026-09-19 | grep of SKILL.md | - |

### Runnable code moved (old location -> new home)

| old location (SKILL.md) | new home | ran |
| --- | --- | --- |
| `aromatic_planarity()` block | `scripts/aromatic_planarity.py` (SDF argument) | puck_0.6 -> 0.2888 A, puck_1.0 -> 0.4524 A, matching the 2026-09-19 bracket |
| Integration into VS Pipeline `pose_qc_pipeline()` | `scripts/pose_qc_batch.py` (receptor + SDFs arguments) | fixture + a copy: 2/2 files with a PB-valid pose |
| Strain Energy `ligand_strain()` (65 lines) | deleted, duplicate of `examples/validate_poses.py` `ligand_strain_mmff` | ran from the example: `strain_kcal` 4.162648, note `ok` |
| Python Library API block | deleted, duplicate of `run_posebusters` in the example | ran: `pb_valid` True |

Also: Common Errors row "Reduce `n_ref`" now says `n_ref_conf`, the example's parameter name. Found while doing the pipeline script: the `rank` column in `pose_qc_pipeline` is a running count of valid poses per file, not a score rank; kept verbatim, left as is.

### Left unfixed

None.

Env: `cheminformatics-hit-triage-analyst` Python, PoseBusters 0.6.5, RDKit 2026.03.6, pandas 3.0.5. No installs.
