# Fix log — bio-conformer-generation

2026-09-19. Fixer for `chemoinformatics/conformer-generation` (skill-id `bio-conformer-generation`,
audited at 86/100, Limited Release, deployable, no open P0).

Worktree `F:\OpenScience\wt\cg-conf`, branch `fix/cg-conformer-generation`, commit `c4e2ccd`.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| CREST + GFN2-xTB escalation path has no Windows caveat despite CREST publishing no Windows build anywhere upstream | P1 | Added an "Installation" section to SKILL.md (moved from usage-guide.md's Prerequisites) stating CREST is Linux/macOS-only, `conda install crest` will not resolve on Windows, invoking it raises `FileNotFoundError`, and pointing to WSL or the RDKit macrocycle-aware + standalone `xtb --opt` fallback; added a one-line pointer to it in the CREST section itself | checked against docs/tooling record | Matches `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\TOOLS.md`'s own finding: crest has "Linux binaries only... no Windows build, no conda-forge win-64 package"; xtb 6.7.1 confirmed working standalone (real GFN2 run) |
| SKILL.md's `gen_conformers()` omits the `mol is None` guard present in `macrocycle_conformers()` and `crest_workflow()` in the same file | P1 | Added `if mol is None: raise ValueError(f'Invalid SMILES: {smiles!r}')` immediately after `Chem.MolFromSmiles(smiles)`, matching the existing pattern | ran | Live-ran the fixed function against a malformed SMILES (`C1CC(not_a_smiles`): now raises `ValueError: Invalid SMILES: 'C1CC(not_a_smiles'` instead of the opaque boost.python `ArgumentError` from `Chem.AddHs(None)`; a valid SMILES (`c1ccccc1O`) still embeds 5/5 conformers unchanged. Ran against the shared RDKit 2026.03.6 venv in `cheminformatics-hit-triage-analyst`. |
| Function names diverge between SKILL.md (`gen_conformers`/`prune_conformers_rmsd`/`filter_by_energy`) and `examples/gen_conformers.py` (`gen_conformer_ensemble`/`prune_rmsd`/`filter_energy_window`) with no cross-reference | P2 | Added a one-line note after `gen_conformers()` naming all three name pairs and pointing to `examples/gen_conformers.py` | checked (prose only, no runnable change) | Picked the note over renaming — renaming either file touches many more call sites for no functional gain; smaller diff |
| Mandatory redundancy pass | — | Moved usage-guide.md's Prerequisites (install commands) into SKILL.md's new Installation section (install notes are content the agent acts on). Deleted usage-guide.md's "What the Agent Will Do" and "Tips" sections — both fully restated SKILL.md's Decision Tree, Macrocycle Handling, and Common Errors content — replaced with a one-line pointer to SKILL.md. usage-guide.md now holds only Overview, Prerequisites (pointer), Quick Start, Example Prompts, Related Skills. | — | Nothing deleted was unique; every fact now lives once, in SKILL.md. |

## Left unfixed

- P2 "macrocycle-aware embedding's claimed benefit has no worked before/after example" (observed in
  input 4) — not in this dispatch's scope (only the two P1s and the function-naming P2 were named);
  left for a future pass since it would require a new worked example (new content), not a correction.

## Verification method

`py_compile` on all 8 Python code blocks extracted from the fixed SKILL.md (individually and
combined into one file) plus `examples/gen_conformers.py` (unchanged) — all pass. Live-ran the fixed
`gen_conformers()` guard against both a malformed and a valid SMILES via
`F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe` (RDKit 2026.03.6).
The Windows/CREST claim was checked against the audit env's own `TOOLS.md` tooling record rather than
re-run, since CREST cannot execute on this machine by definition of the defect being fixed.
