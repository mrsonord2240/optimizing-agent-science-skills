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

## 2026-09-21 -- P2 batch pass

Worktree `F:\OpenScience\wt\chemoinformatics-pharmacophore-modeling`, branch
`fix/chemoinformatics-pharmacophore-modeling` (from staging `431aa55`). Commits: `5720d85` (fix), `c83fb1c` (dedup).
Audit: `F:\OpenScienceuditsio-pharmacophore-modeling\eval_report_bio-pharmacophore-modeling_result.json` (88, 1 P2).
Env: `cheminformatics-hit-triage-analyst`, RDKit 2026.03.6.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `feature_family_prefilter` rejects a same-class active (ritonavir) under strict intersection | P2 | New `min_shared_fraction` parameter (default 1.0 = strict, unchanged); a library molecule passes when it carries at least that fraction of the shared query feature types. SKILL.md "Ligand-based -- diverse actives confound" Fix row (same line, no new line) names it and says it stays a coarse filter | ran: indinavir/saquinavir queries vs ritonavir, caffeine, metformin, aspirin, acetaminophen. Strict: no hits. 0.6: ritonavir admitted, caffeine and metformin still rejected. Default == explicit 1.0. Shipped `__main__` demo unchanged (`CCC(=O)Nc1ccc(C(=O)c2ccc(Cl)cc2)cc1`). `py_compile` ok | At 0.6, aspirin and acetaminophen also pass (they lack the same two types as ritonavir): the feature-family filter cannot separate them, so the docs say to follow with a 3D distance match. Default behaviour is unchanged |

### Left unfixed

- None of the audit's findings. Not moved to `scripts/` (judged illustrations, not runnable pipelines): the
  Ligand-Based Pharmacophore block (~33 lines, carries deliberately placeholder coordinates that must not be
  reused, so a script would invite reuse), the PLIP loop (~15 lines, API-shape illustration that prints objects),
  and `pharmacophore_enrichment` (14 lines, needs a caller-supplied matcher). `examples/pharmacophore.py` already exists.
- Split: not needed, SKILL.md stays 299 lines (before and after).

### Deleted passage -> new home (usage-guide.md redundancy)

| deleted | now lives in |
| --- | --- |
| "What the Agent Will Do" step 3 (ligand-based: align, derive, `EmbedPharmacophore` does not derive consensus) | SKILL.md "Ligand-Based Pharmacophore" Approach (line 72) |
| step 4 (tolerances from variability/uncertainty/validation) | SKILL.md "Pharmacophore Feature Types" (line 41) |
| step 5 (convert to search engine's query format) | SKILL.md "Receptor-Based" Approach (line 116) and "Pharmacophore Search" (line 141) |
| Tip: compare ligand- vs receptor-based, neither more reliable | SKILL.md "Reconciliation" (line 265) |
| Tip: use bioactive conformer | SKILL.md failure mode "single conformer bias" and Common Errors (lines 218, 275) |
| Tip: measure specificity/recall on the project dataset | SKILL.md "Pharmacophore Quality Validation" (line 169) |

## 2026-09-21 -- final pass, Phase 1 (verification only, no code changes)

Worktree `F:\OpenScience\wt\chemoinformatics-pharmacophore-modeling`, branch
`fix/chemoinformatics-pharmacophore-modeling`, tip `c83fb1c` (unchanged). Env:
`cheminformatics-hit-triage-analyst`. No entry in `fixes\README.md`'s Revisit list for this Skill, and
the prior pass's "left unfixed" was empty, so this phase was pure re-verification, not a fix.

Independently re-ran (fresh scripts, on real data) every runnable block in `SKILL.md` and
`examples/pharmacophore.py`: the `examples/pharmacophore.py` demo, the new `min_shared_fraction=0.6`
relaxation (matches the fix log's claim: admits ritonavir, still rejects caffeine/metformin), the
Ligand-Based `EmbedPharmacophore` block (`can_match=True`, 10/10 embeddings), `pharmacophore_enrichment`
on a fresh active/inactive set never used in any prior audit (enrichment=inf), and the Receptor-Based
PLIP block on both PDB 1HSG (27 interactions, matches the audit's 6/15/2/4 breakdown) and PDB 3PTB
(9 interactions, matches the audit's record). All passed. Full detail in
`F:\OpenScience\audits\_final_pass\bio-pharmacophore-modeling\CHECKPOINT.md`.

### Still blocked

None.
