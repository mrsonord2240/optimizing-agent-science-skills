# Fix log: bio-shape-similarity

2026-09-19 — fixer pass on `fix/cg-shape` (worktree `F:\OpenScience\wt\cg-shape`),
commit `cb11853`, base `mrsonord2240/bioSkills@85ca33b`.
Source audit: `F:\OpenScience\audits\bio-shape-similarity\` (81/100, Limited Release,
deployable, no P0).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| SKILL.md's `shape_search_ensemble` discarded an entire library molecule if even 1 of n_conf MMFF-optimized conformers failed to converge, silently (2/3 molecules vanished in the audit's verbatim Input 4 run) | P1 | Replaced `if any(status != 0 ...): continue` with filtering converged conformer ids (`status == 0`) and scoring the survivors; a molecule is now dropped only when zero conformers converge, and every drop (embedding failure, missing MMFF params, disconnected fragments, all-conformers-non-convergent) is collected and printed with its SMILES and reason at the end of the run | ran | Re-ran the audit's exact Input 4 reproducer (query + lib_A/lib_B/lib_C SMILES, `n_conf=20`, seed 42) against the fixed function in `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst`: 3/3 molecules now score (was 1/3), with explicit `WARNING: ... 1/20 conformers failed ... scoring the remaining 19` / `4/20 ... remaining 16` lines. |
| Disconnected-fragment (salt) SMILES like `[Fe+2].[Cl-].[Cl-]` pass `MMFFHasAllMoleculeParams` trivially and generate meaningless conformers with no error | P1 | Added a `len(Chem.GetMolFrags(mol)) > 1` pre-check, in `shape_search_ensemble` (raises no exception there since it's a library loop -- logs a drop reason instead) and in `examples/shape_search.py`'s `prepare_mol_3d` (raises `ValueError`); added a new "Disconnected-fragment (salt) input" row to the Per-Tool Failure Modes table | ran | Same audit env: the salt case now produces 0 scores with an explicit `disconnected fragments (salt/multi-component); no single shape to compare` reason (previously silently "succeeded" with 10 meaningless conformers). `prepare_mol_3d('[Fe+2].[Cl-].[Cl-]')` now raises `ValueError`; a normal molecule (`CCO`) still embeds 20 conformers unaffected. |
| ShaEP example (`shaep -q query.mol2 target.mol2 ...`) assumes `.mol2` files already exist; RDKit has no Mol2 writer and the SMILES->mol2 step was never shown | P1 | Added the Open Babel `obabel -:"<SMILES>" -O out.mol2 --gen3D` conversion before the `shaep` call, with a pointer to `chemoinformatics/molecular-io` | ran | Real run in the audit env: `obabel` produced real 3D coordinates for query and target SMILES, then `shaep.exe` 1.4.2 (the version the Skill names) scored them -- `shape_similarity 0.999`, `ESP_similarity 0.824`. |
| ESPSim named in frontmatter/taxonomy as a supported method but had no code example anywhere in SKILL.md | P2 | Added a minimal `EmbedAlignScore` example under a new "ESPSim (RDKit-native, Python)" subsection, noting the default `metric='carbo'` is unbounded (not [0,1] like shape Tanimoto) and how to renormalize | ran | espsim was not installed in the candidate env (`TOOLS.md` had no entry). Installed espsim 0.0.1 (public/unauthenticated PyPI package, single release) into its own `tools\espsim-venv` per the env's isolation rule -- it pulls rdkit 2026.03.6 / numpy 2.5.3, identical to the shared venv's pinned versions, so no version was changed anywhere shared. Needed `setuptools<81` for `pkg_resources` (noted in TOOLS.md). Ran `EmbedAlignScore(target, [query], prbNumConfs=10, refNumConfs=10)` on two real acetanilide analogs: `shape_sim 0.922`, `esp_sim 0.815`. Recorded in `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\TOOLS.md`. |

## Unfixed

None. All 3 P1s and the 1 P2 from the audit's `recommendations[]` were fixed.

## Redundancy pass

No duplication found between SKILL.md and usage-guide.md for the sections touched (usage-guide.md
does not mention ESPSim or the ShaEP mol2 step at all; the new content added is agent-facing code/
failure-mode material that belongs in SKILL.md only, consistent with the existing split).

## Environment

Verified in `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\` (RDKit 2026.03.6, ShaEP
1.4.2, Open Babel 3.1.0, per its `TOOLS.md`). Only new install: espsim 0.0.1 into a fresh
`tools\espsim-venv` there (documented above); nothing in the shared venv was installed or changed.
