# bio-causal-genomics-proteome-mr-drug-target fixes (2026-09-17)

Worktree `F:\OpenScience\wt\cg-pmr`, branch `fix/cg-proteome-mr`, based on `main` @ `558aea5`.
Fixer: Claude Sonnet 5. Runtime intended: R 4.4.3 via
`F:\OpenScience\audit-envs\mendelian-randomization-analyst\r.sh` (TwoSampleMR 0.7.9,
MendelianRandomization 0.10.0, coloc 5.2.3 already installed there per `TOOLS.md`).

**Session stopped on coordinator wind-down before any edit was made.** No file in the worktree was
touched, no commit created, no install-lock taken. `git status --short` in the worktree is empty.
Nothing to revert.

## Research completed this session

Read `SKILL.md`, `usage-guide.md`, both `examples/*.R`, the audit's `eval_report_*.json`,
`eval_viewer_*.md`, and `run/debug_mrivw*.R`, and the candidate env's `TOOLS.md`. Confirmed the plan
below but did not execute it.

| finding | priority | planned change | planned verification |
|---|---|---|---|
| `TwoSampleMR::mr_ivw` shadows `MendelianRandomization::mr_ivw` depending on load order; SKILL.md's documented `mr_ivw(mr_obj, model='default', correl=TRUE)` throws `unused arguments` | P1 | Namespace both call sites in SKILL.md ("Cis-IVW with Correlated Instruments", "Robust/Penalized cis-IVW") and `examples/cis_pqtl_mr.R` line 86 as `MendelianRandomization::mr_ivw(...)`; extend the existing "API caveat" paragraph with the shadowing mechanism; add one Common Errors row | Re-run `run/debug_mrivw2.R`-style probe with both load orders via `r.sh`, confirm explicit-namespace call succeeds regardless of order |
| Shipped `examples/phewas_drug_target_mr.R` line 65 runs `lapply(outcomes_filt$id[1:200], scan_one_outcome)` — the exact `[1:200]` shortcut SKILL.md's own prose disclaims | P1 | Drop the `[1:200]` slice, loop over the full `outcomes_filt$id` | Local synthetic outcome-catalogue stub (no live OpenGWAS, matching the audit's own Input 4 workaround) confirming no truncation remains |
| No concrete path to a local LD reference panel when OpenGWAS/`genetics.binaRies` are unavailable | P2 (cheap) | Add a short `plink2 --make-bed` recipe from public 1000G phase 3 VCFs to SKILL.md's Tool Installation Notes | docs only |
| SKILL.md carries the full methodological corpus inline, no `references/` split | P2 | Planned to **decline**: the redundancy rule in scope this pass governs SKILL.md<->usage-guide.md duplication, not SKILL.md's internal length; a full `references/` split is a restructure beyond "correction," and out of the brief's "still not in scope: broader coverage... restyling" carve-out | n/a |
| Example scripts not runnable out of the box (hardcoded paths, no bundled data) | P2 | Planned: copy the audit's 3 synthetic `data/*.tsv` fixtures into `examples/data/`, repoint `cis_pqtl_mr.R`'s default file variables at them (the `ld_clump`/`ld_matrix` steps still need a real plink+1000G bfile per the P2 above; documented, not worked around) | Run the bundled-data path through `format_data`/`harmonise_data`/`mr()`/`coloc.abf` via `r.sh` |
| Redundancy pass (mandatory, every fixer pass) | — | Planned: delete `usage-guide.md`'s "Tips" section (near-total restatement of SKILL.md's failure-mode/threshold sections, plus one internally-inconsistent PP.H4 exploratory-tier claim of ">=0.5" that disagrees with SKILL.md's audited ladder of ">=0.7"); fold its two facts with no SKILL.md home (r2<0.1 vs r2<0.001 polygenic-clumping contrast; complement-factor/immunoglobulin PAV-heavy caveat) into SKILL.md; collapse "Prerequisites"' duplicate install block to a pointer, moving its one unique fact (FinnGen-PPP DF12 source URL) into SKILL.md's data-acquisition paragraph | n/a |

## Left unfixed: not reached this session

All five items above (2 P1, 3 P2) plus the mandatory redundancy pass — identified and planned, none
applied. No lock was held on the shared R env; nothing needs releasing.

Nothing needs Sam yet. A follow-up session should pick up this plan directly; the P1 fixes are small,
targeted, and already have a verification method identified (the audit's own `debug_mrivw2.R` pattern
and a local synthetic-catalogue stub for the phewas truncation).
