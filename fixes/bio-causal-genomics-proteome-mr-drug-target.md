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


---

# 2026-09-21 fix pass (Sonnet 5)

Worktree `F:\OpenScience\wt\causal-genomics-proteome-mr-drug-target`, branch `fix/causal-genomics-proteome-mr-drug-target`, commit `66192a6` (based on staging `431aa55`). Env: `mendelian-randomization-analyst` via `r.sh`; R 4.4.3, MendelianRandomization 0.10.0, TwoSampleMR 0.7.9, coloc 5.2.3. The 2026-09-17 plan above was executed except where noted.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `TwoSampleMR::mr_ivw` masks `MendelianRandomization::mr_ivw` | P1 | `MendelianRandomization::mr_ivw()` in both SKILL.md blocks, line-35 bullet, `examples/cis_pqtl_mr.R`; API caveat rewritten; Common Errors row added | ran: bare call after `library(MR); library(TwoSampleMR)` -> `unused arguments`; namespaced call works in both attach orders; robust+penalized runs | `environmentName(environment(mr_ivw))` gives `TwoSampleMR` when it is attached last |
| phewas example loops `id[1:200]` | P1 | loops full `outcomes_filt$id`; comment says a partial scan is a debug shortcut | ran: example text with stubbed `available_outcomes`/`extract_outcome_data`/`ld_clump` (OpenGWAS is gated), 250 of 250 outcomes scanned | audit's own Input 4 used the same stub approach |
| code passed `correl = TRUE` and `corr =` while prose said not to | P2 (internal contradiction) | code uses `correlation =` and no `correl`; line 35, method-table label, decision-tree row, related-skills line updated | ran: estimate 0.4925, SE 0.0945 identical for `correl` TRUE/FALSE/absent with matrix; `correl=TRUE` without a matrix errors; `corr=` and `correlation=` give identical slots | old claim "inconsistent across versions" unsupported by the run, removed |
| no path to a local LD panel | P2 | `1kg.v3.tgz` recipe in Tool Installation Notes (curl, tar, mv into `1kg_EUR/`) | URL 200, 1.57 GB, per ieugwasr local-LD vignette; tar listing shows `EUR.*` at archive root (first entry `AFR.bed`). Not downloaded | plink2-from-VCF variant not added (no plink2 here to verify) |
| neighbour-gene coloc threshold 0.7 (symptom, reconciliation row) vs 0.5 (fix, thresholds, rule) | P2 | 0.5 everywhere | read | operational drop rule kept |
| `ld_matrix(exposure_dat$SNP)` fed to vectors from `dat` | P2 | `ld_matrix(dat$SNP)`; sign-alignment bullet added; comment in example | docs (ieugwasr `ld_matrix` help; package's own runtime warning seen in the run) | sign-flip procedure not run (no plink reference) |
| `examples/cis_pqtl_mr.R` end to end | check | none needed | ran on the audit's synthetic data with stubbed `ld_clump`/`ld_matrix`: IVW 0.430, PP.H4 ~1.0, PAV-excluded 23 SNPs | both examples also parse |

## Redundancy pass (deleted passage -> where the content lives)

| deleted | now |
|---|---|
| usage-guide "Tips" (14 bullets) | SKILL.md failure modes, Cis-MR taxonomy, thresholds. Unique facts moved: r2<0.1 vs r2<0.001 contrast -> thresholds row; complement/immunoglobulin PAV caveat -> PAV failure mode |
| usage-guide Tips "PP.H4 >= 0.5 exploratory" | dropped: contradicted SKILL.md's audited 3-tier ladder (lowest 0.7) |
| usage-guide "Prerequisites" install blocks and source list | SKILL.md Tool Installation Notes; deCODE URL, UniProt-ID note and FinnGen DF12 portal added to its data-acquisition paragraph |
| usage-guide "What the Agent Will Do" (16 steps) | replaced by a two-line pointer; workflow is in SKILL.md; the step-16 report contents moved into Triangulation Requirement |
| SKILL.md "Anticipated Reviewer Pushback" (9 rows) | all restated other sections; the one unique fact (Patel 2023 preferred when LD reference is ancestry-mismatched) moved to the correlated-IV decision rule; 1 Mb rationale into Window section |
| SKILL.md Common Errors: trans-pQTL, PAV, neighbour-gene, sample-overlap, Olink/SomaScan rows; "SE explodes" row | failure-mode sections (numerical caveat kept for the explosion) |
| SKILL.md thresholds: three PP.H4 rows, cis-window row | PP.H4 ladder at top (Mountjoy source added there); Window section |
| SKILL.md "Operational rule for publication" (restated ladder) | shortened to pointer + downgrade sentence |

## Left unfixed

- **P2 references/ split**: declined. The redundancy rule governs duplication, not length; a split is a restructure the brief does not allow.
- **P2 bundled synthetic data for the examples**: declined. `ld_clump`/`ld_matrix` still need a real plink + 1000G bfile, so bundling the audit's TSVs would not make either example runnable; the LD recipe covers the missing piece. The examples were verified here with stubbed LD.
- Not run: the `1kg.v3.tgz` download, real plink clumping, sign-flip of `ld_matrix` output.
