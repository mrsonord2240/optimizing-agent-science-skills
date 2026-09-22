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

## 2026-09-21 — P2 batch fixer pass

Worktree `F:\OpenScience\wt\chemoinformatics-shape-similarity`, branch `fix/chemoinformatics-shape-similarity`
(from staging `main` 431aa55). Commits: `ae992c0` fix, `5a7f03a` redundancy, `1622b1d` split, `2f8cee5` scripts.
Env `cheminformatics-hit-triage-analyst` (RDKit 2026.03.6, ShaEP 1.4.2, Open Babel 3.1.0).
Source audit: `F:\OpenScience\audits\bio-shape-similarity\` (1 P2).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `obabel --gen3D` prints "NaN in calculated coordinates" on fused-ring scaffolds while still writing a mol2 | P2 | ShaEP section now says so and gives an `awk` check of the mol2 `@<TRIPOS>ATOM` block (atoms / zero rows / duplicate rows) to run before trusting the score | ran: warning reproduced on the naphthalene target (`COc1ccc2cc(ccc2c1)C(C)C(=O)O`); check gives `zero=0 dup=0` on it and on the query; a zeroed copy gives `zero=31 dup=30`; ShaEP 1.4.2 then scored the pair (shape 0.607, ESP 0.594) | replaces the audit's prose suggestion with a runnable check |
| USRCAT snippet raised `NameError` (`Chem`/`AllChem` never imported, `desc1`/`desc2` undefined) | small defect, fixed inline | self-contained `usrcat()` helper + imports | ran: 60-D vectors, ethanol vs propanol 0.396, identical 1.0 | not in the audit |
| O3A snippet lacked `Chem`/`AllChem` imports | small defect, fixed inline | imports added | ran: RMSD 0.365, O3A 67.2, shape Tanimoto 0.610 | not in the audit |
| `scaffold_hop_candidates` called undefined `ecfp_tanimoto` | small defect, fixed inline | helper defined (Morgan r=2, 2048); later moved to the script | ran end to end on the toy set incl. a salt | not in the audit |
| ShaEP output-file wording | wording check | "with no `--output-file`, the last filename in the input list is the similarity output" | help: `shaep --help` | |

### Left unfixed

None. The audit's single P2 is fixed.

### Deleted passage -> new home (redundancy pass)

| deleted from `usage-guide.md` | now in `SKILL.md` |
| --- | --- |
| Prerequisites: `conda install -c conda-forge rdkit`, no `usrcat` package, ShaEP is a separate binary | Version Compatibility ("Install:" paragraph) |
| Prerequisites: ShaEP `-q`, positional output, `-s` syntax | "ESP Similarity" -> ShaEP (now `references/esp-similarity.md`) |
| Tip: Open3DAlign mutates probe coordinates | Open3DAlign section (`references/open3dalign.md`) |
| Tip: 20 conformers is a starting budget | conformer-ensemble "Critical" paragraph (`references/open3dalign.md`) |
| Tips: benchmark throughput; TanimotoCombo 0-2 vs raw O3A (twice); calibrate 0.7/0.5; validate by docking | already stated: USRCAT Speed, Tanimoto-Combo Scoring, Shape vs ECFP4 Complementarity, Common Errors (deleted, no move) |
| "What the Agent Will Do" (5 steps) | restated SKILL.md; replaced by a pointer line |

Each destination checked by grep.

### Split

`SKILL.md` 378 -> 231 lines (then 214 after the scripts move). Moved verbatim to `references/usrcat.md`,
`references/open3dalign.md` (Open3DAlign + conformer-ensemble search) and `references/esp-similarity.md`
(ShaEP + ESPSim); Reference Files index, decision-tree pointers added. Every non-blank line of the
pre-split file is present in SKILL.md or a reference file except six pointer-edited lines; python fences
`ast.parse`, the bash fence `bash -n`.

### Scripts

| old location | script |
| --- | --- |
| `references/open3dalign.md` `shape_search_ensemble` fence (48 lines); `SKILL.md` `ecfp_tanimoto` + `scaffold_hop_candidates` fence | `scripts/shape_search_ensemble.py` (argparse CLI; `seed` and `n_conf` parametrised, output deterministic) |

Ran both invocations exactly as written in SKILL.md / the reference on the toy set (analog, sulfonamide hop,
FeCl2 salt): shape 0.656 / 0.572, the salt reported as dropped, 1/20 and 4/20 MMFF-non-convergence warnings,
`--scaffold-hop` at 0.3/0.55 keeps only the sulfonamide (ECFP4 0.513); two runs byte-identical. USRCAT,
O3A and ESPSim fragments (under 15 lines) stay inline; `examples/shape_search.py` untouched.

## 2026-09-21 — final-pass phase 1 (verification only, no changes)

Worktree `F:\OpenScience\wt\chemoinformatics-shape-similarity`, branch
`fix/chemoinformatics-shape-similarity`, tip commit `2f8cee5` (unchanged). Env
`cheminformatics-hit-triage-analyst`. Checked the fix log's "left unfixed" (none, both prior
passes) and `fixes/README.md`'s Revisit list (no row for this Skill) — nothing was queued.

Independently re-ran every runnable block in the Skill (not just what a prior fixer touched):
USRCAT snippet, O3A snippet, both `scripts/shape_search_ensemble.py` invocations (plain and
`--scaffold-hop`) on a built 3-molecule library, `examples/shape_search.py` standalone, the
ShaEP `obabel`+`shaep.exe` pipeline, the ShaEP NaN-coordinate awk check (reproduced the
warning on a naphthalene SMILES and confirmed the check flags it), the ESPSim block, and
`shaep --help` for the output-file wording. All ran and produced correct, checkable output;
no new defects found. No installs were needed. Full detail:
`F:\OpenScience\audits\_final_pass\bio-shape-similarity\CHECKPOINT.md`. No commits this phase
(nothing to change).
