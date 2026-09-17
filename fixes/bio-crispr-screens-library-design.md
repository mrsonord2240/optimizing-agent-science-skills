# Fix log: bio-crispr-screens-library-design (2026-09-16)

Branch `fix/r2-crispr-b` @ `F:\OpenScience\wt\crispr-b`, commit `829444b`.
Scope: Sam's 2026-09-16 override — fix every P0/P1/P2 in the report, plus the
two defects AUDIT.md names as "what keeps it at 81": the missing guide-spacing
filter and the SKILL.md/usage-guide.md Azimuth contradiction.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| No minimum-spacing/independence filter on candidate guides — `find_sgrna_candidates` filters composition only; a short/GC-tied region can select near-duplicate guides that both count toward the per-gene quota | P1 | Added `select_independent_guides()` (greedy, `min_spacing=5`) to SKILL.md's "Score and Rank sgRNAs" section, wired into the Approach text and a new Quantitative-Thresholds row | ran — real TP53 CDS (NM_000546.6, fetched live via NCBI efetch `fasta_cds_na`), not synthetic. Naive top-12-by-score selection returned a pair 1nt apart (19/20nt shared sequence, min pairwise distance 1nt); `select_independent_guides(min_spacing=5)` on the same candidate pool raised the guaranteed minimum pairwise distance to 5nt while still filling all 12 slots from the next-best candidates. Script + output kept in this session's scratchpad (`verify_spacing_filter.py`) | This was the audit's own primary "what would flip it to 85+" item |
| SKILL.md vs usage-guide.md contradiction on Azimuth 2.0 usability | P1 | Rewrote SKILL.md's Version Compatibility section: states plainly Azimuth 2.0 (the `azimuth` PyPI package) must not be called, names the confirmed failure, and gives an ordered recommendation (1. this Skill's own GC heuristic, always available; 2. Broad CRISPick or R `crisprScore::getAzimuthScores()` for real Rule Set 2). Also fixed the "sgRNA Library Design" tool-list bullet that still named the broken `azimuth` package | ran — `import azimuth.model_comparison` reproduced live on this machine (Python 3.12, shared venv): `SyntaxError: Missing parentheses in call to 'print'`, matching TOOLS.md §3 and the audit's own live reproduction. CRISPick/crisprScore were **not** installed/run here (crisprScore isn't in TOOLS.md's installed-R-packages table) — flagged as unverified-in-this-env in the new text rather than presented as confirmed | Resolved in favor of usage-guide.md's version (Azimuth unusable), which matched what TOOLS.md and the audit both independently confirmed |
| Shipped `examples/design_library.py` implements a different, simpler algorithm (random sequences + GC heuristic) than the documented CDS/TSS method | P2 | Rewrote the script to call `find_sgrna_candidates`/`annotate_exon_position`/`select_independent_guides` against a synthetic per-gene CDS, same functions SKILL.md documents | ran — exit 0, 142 rows, 0 NaN in `sequence`, all 20 genes at the 4-guide quota, all spacers 20nt; independently re-checked with `pandas.read_csv` + `value_counts` | Kept the synthetic-CDS approach (not a real Ensembl pull) to keep the example runnable offline, same as before |
| Demo control-guide proportions (43.7%) don't match the ~1% NTC genome-scale target and carry no caveat | P2 | Added an inline comment ahead of the controls section and in the control-fraction print line, pointing at SKILL.md's Control Guides table | ran — comment appears in stdout and in the script; not a functional change | |
| No explicit stop-and-ask escape hatch for missing required inputs | P2 | Added step 0 to usage-guide.md's "What the Agent Will Do": stop and confirm gene list / genome / chemistry / TSS-or-exon source before designing | docs — text-only change, no code to run | |
| (unticketed, evidenced by Input 3) Neither doc warns the 75bp Calabrese CRISPRa window can undersupply the 6-guide quota | — | Added a caveat to `crispra_window()`'s docstring | docs — matches the audit's own Input-3 finding (2/4 synthetic TFs undersupplied) | Cheap, bundled in since already touching that function's neighborhood |

## Left unfixed

Nothing from `recommendations[]` or AUDIT.md's library-design section was left
unfixed. Two related-but-broader gaps were noted and deliberately left alone
per the brief's "keep diffs minimal, no broader coverage" rule:
- `crisprScore` (R) was not installed/smoke-tested in this pass — TOOLS.md
  didn't cover it, and installing it belongs to a tooling pass, not this fix.
  The new SKILL.md text says so explicitly rather than presenting it as
  verified.
- Non-ACGT input validation (static-score dock, not in `recommendations[]`)
  was left alone — no crash observed, out of the ticketed scope.

## Verification method notes

- All three changed files: `design_library.py` (`py_compile`, then executed
  from its actual worktree location), `SKILL.md`'s three python code blocks
  (extracted by regex, `py_compile`'d individually), `usage-guide.md` (prose
  only, no code).
- `select_independent_guides()` was verified twice: once against the
  synthetic-CDS example script (end-to-end run) and once standalone against
  a real gene's CDS (TP53, NM_000546.6) pulled live from NCBI's public,
  unauthenticated E-utilities — not just import-checked.
- Nothing installed into the shared venv or R library; no version changes.
