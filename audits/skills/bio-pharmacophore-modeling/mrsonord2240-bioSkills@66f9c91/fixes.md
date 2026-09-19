# Fix log: bio-pharmacophore-modeling

2026-09-19 — fixer pass on `chemoinformatics/pharmacophore-modeling`, fork commit
`d89e84a0a8222123302b8633b1869613b0e3ebfc`, branch `fix/cg-pharm`, commit `66f9c91`.

Audited fresh at 86/Production Ready, deployable, no P0/P1. All 4 recommendations in
`F:\OpenScience\audits\bio-pharmacophore-modeling\eval_report_bio-pharmacophore-modeling_result.json`
were P2. Fixed all 4.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `shared_feature_types_prefilter`/`has_feature_types` conformer embedding has no fixed random seed (non-reproducible geometry across runs) | P2 | Set `params.randomSeed = 23` on both `EmbedMultipleConfs` (multi-active) and `EmbedMolecule` (single target) calls in `examples/pharmacophore.py`, matching SKILL.md's own `randomSeed=23` convention | ran | Extended beyond the recommendation's one named line to the analogous `EmbedMolecule` call in `has_feature_types`, which has the identical unset-seed defect — fixing one and not the other would have been an internal inconsistency |
| `feature_family_prefilter` silently rejects a true positive (ritonavir) with no diagnostic | P2 | `has_feature_types` now returns `(is_match, missing_feature_types)`; `feature_family_prefilter` prints, per rejected library molecule, which query feature(s) it lacks; docstring now points to SKILL.md's "Ligand-based -- diverse actives confound" failure-mode fix (cluster actives by scaffold first) | ran | Verified on real molecules (indinavir/saquinavir queries vs a real ritonavir-analog + caffeine/metformin/aspirin/acetaminophen library): the ritonavir-analog is now reported as missing exactly `('PosIonizable','BasicGroup')` and `('LumpedHydrophobe','tButyl')`, matching the audit's own root-cause debug (`run/debug_ritonavir.py`) |
| No troubleshooting row for PLIP's `ValueError: inchikey is not a recognised Open Babel format` on Windows (`openbabel-wheel` ships no InChI writer) | P2 | Added a row to SKILL.md's Common Errors table naming the cause and both documented workarounds (conda-forge openbabel build with InChI support, or monkeypatch `pybel.Molecule.write` to no-op for `format='inchikey'`) | docs | Sourced from `cheminformatics-hit-triage-analyst/TOOLS.md` note 5 and note 4/5 context; not independently re-run (TOOLS.md's own smoke test is the source of truth for this environment gap) |
| Ligand-based worked example's placeholder `query_features` carries no inline warning at its point of definition | P2 | Added `# PLACEHOLDER COORDINATES -- do not reuse without deriving from a validated workflow` directly above `query_features` in SKILL.md's Ligand-Based Pharmacophore snippet, naming the audit's own enrichment=0.5 result | docs | The enrichment=0.5 finding itself was independently reproduced by the audit (input 5), not re-run here; this is a documentation-only addition next to already-verified code |

## Redundancy (found while in there, not flagged by audit)

`usage-guide.md`'s Tips restated two of SKILL.md's caveats near-verbatim: the geometric-tolerance
"repository starting heuristic" language (SKILL.md's Pharmacophore Feature Types section) and the
enrichment ">5x is a repository starting heuristic" language (SKILL.md's Pharmacophore Quality
Validation section). Collapsed both Tips bullets into one line pointing at the two SKILL.md
sections by name. Nothing deleted was usage-guide-only content — both facts remain stated in full
in SKILL.md, so nothing the agent needs was lost.

## Unfixed

None — all 4 P2 recommendations addressed, plus the redundancy pass.

## Verification method

- `py_compile` on the modified `examples/pharmacophore.py`: passed.
- Ran the script's own `__main__` demo block: output unchanged from its originally documented
  hits (`['CCC(=O)Nc1ccc(C(=O)c2ccc(Cl)cc2)cc1']`), plus the new missing-feature diagnostic lines.
- Ran `feature_family_prefilter` twice on a second, independent real-molecule scenario (approximate
  indinavir/saquinavir/ritonavir SMILES plus real decoys) to confirm identical hit sets and
  identical diagnostics across runs (determinism fix).
- Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe`,
  RDKit 2026.03.6 (per that env's `TOOLS.md`).
