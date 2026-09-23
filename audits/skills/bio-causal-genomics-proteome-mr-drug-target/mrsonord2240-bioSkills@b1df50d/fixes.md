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

---

# 2026-09-21 (structure)

Worktree `F:\OpenScience\wt\causal-genomics-proteome-mr-drug-target`, branch `fix/causal-genomics-proteome-mr-drug-target`, on top of `66192a6`. Env `mendelian-randomization-analyst` via `r.sh`. Structure only; no behaviour or claim changed.

## Split (commit `ff22b0d`): SKILL.md 457 -> 294 lines (245 after the scripts commit)

Moved verbatim to `references/`, with a "Reference Files" index in SKILL.md and a pointer in each decision-tree row that needs one:

| SKILL.md section (old lines) | New file |
|---|---|
| Data Source Taxonomy + Platform and Cohort Versioning (40-62) | `references/pqtl-datasets.md` |
| Per-Method Failure Modes, six subsections (95-167) | `references/failure-modes.md` (SKILL.md keeps a one-paragraph stub naming the six) |
| Phenome-Wide Drug-Target MR (185-216) | `references/phewas.md` (stub in SKILL.md) |
| Cis-IVW with Correlated Instruments + Robust/Penalized (275-317) | `references/correlated-instruments.md` (stub in SKILL.md) |
| Drug Repurposing and Target Nomination (371-383) | `references/target-nomination.md` (stub in SKILL.md) |

Verified: every non-blank line of the old SKILL.md is in SKILL.md or a reference file, except seven decision-tree rows, the line-35 bullet and one Common-Errors row, which stayed and only gained a `references/...` pointer. All 4 R fences, the bash fences and the R install fence parse (`parse()` via `r.sh`, `bash -n`). Stayed inline: scope, PP.H4 ladder, methodological taxonomy, decision tree, Triangulation Requirement, Standard Workflow, PAV/VEP recipe, window width, thresholds, reconciliation table, Common Errors, install, references.

## Scripts (commit follows the split)

| old location | result | how run |
|---|---|---|
| SKILL.md "Phenome-Wide Drug-Target MR" R block (24 lines, then in `references/phewas.md`) | `scripts/phewas_curated_endpoints.R` (args: pqtl.tsv, endpoints.tsv, out.tsv, min sample size, population; body verbatim otherwise) | `Rscript` through `r.sh` on the audit's synthetic PCSK9 window (top 8 SNPs as instruments, 300-endpoint list); OpenGWAS is gated (401), so `available_outcomes()`/`extract_outcome_data()` stubbed in the calling session, script unchanged. Assertions: 285 of 300 endpoints returned results (10 below the sample-size floor, 5 with no SNPs), all IVW rows, `p_bonf == min(p * 300, 1)`, non-curated id excluded, output file written |
| SKILL.md "Cis-MR Standard Workflow" R block (50 lines) | deleted; SKILL.md points at `examples/cis_pqtl_mr.R`, which does every step of it and more (PAV flag, adaptive panel, correlated IVW, PAV-excluded rerun) | example run with `ld_clump`/`ld_matrix` and `genetics.binaRies::get_plink_binary()` stubbed (no 1000G bfile or plink here): IVW 0.426, PP.H4 ~1.0, 6 instruments, 5 after PAV exclusion, `triangulation_passed` TRUE |

Small edits made while moving: the script guards `is.null(outcome_dat)` before `nrow()` (the original errors when an outcome has none of the SNPs); `population` argument is named `pop_filter` internally because a variable called `population` would be masked by the column of the same name; it also prints the counts and writes the results table. Comment in `references/correlated-instruments.md` "dat comes from the Standard Workflow above" now says `examples/cis_pqtl_mr.R`; the install-note comment "in the code above" now names the example and reference file.

Stayed inline: the correlated-IVW blocks (10 and 6 lines, fragments that need `dat` and `ld`), the Steiger 5-line block, the VEP bash and install blocks (short, or need VEP/downloads).
Not run: `phewas_curated_endpoints.R` against the live catalogue (OpenGWAS needs a JWT token).

---

# 2026-09-21 final pass, phase 1 (Sonnet 5)

Worktree `F:\OpenScience\wt\causal-genomics-proteome-mr-drug-target`, branch `fix/causal-genomics-proteome-mr-drug-target`, commit `b1df50d`. Walked every runnable block in the Skill (not just what earlier passes touched), following `process/FINAL_PASS_BRIEF.md`. Checkpoint: `F:\OpenScience\audits\_final_pass\bio-causal-genomics-proteome-mr-drug-target\CHECKPOINT.md`.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `references/failure-modes.md` Reverse-causation snippet (`steiger_filtering()` -> `dat[dat$steiger_dir,]` -> `directionality_test()`) crashes `replacement has 0 rows, data has N` | P1 | added `dat$samplesize.exposure`/`dat$samplesize.outcome` before `steiger_filtering()`; one-line caveat for binary outcomes (need `ncase`/`ncontrol`/`prevalence` instead) | ran: crash reproduced on `dat` built exactly the way `examples/cis_pqtl_mr.R` builds it (no `samplesize_col` anywhere in this Skill's own `format_data()`/`read_outcome_data()` calls); literal fixed block re-run clean, `steiger_dir` all TRUE, `directionality_test` `correct_causal_direction=TRUE`, p=9.2e-31 | TwoSampleMR 0.7.9; root cause is `add_rsq()`'s internal `ind1` check silently going to zero rows and never creating `effective_n.<what>`, which the next step assumes exists |
| `references/correlated-instruments.md` `mr_ivw` namespace + sign-alignment recipe, previously only stub-verified | check | none needed | ran for real: `genetics.binaRies` (real plink 1.9) was already installed in this env's shared R-lib (not by me); ran `ld_clump()`/`ld_matrix()` against the real 957-individual/14389-SNP panel already cached at `...\tools\src\plink2R\data.bed` (8 real chr1 SNPs, PCSK9 +/-1Mb); deliberately swapped one SNP's A1/A2 and confirmed the `with_alleles=TRUE` row-name convention flags it, and realigning + re-running `mr_ivw` recovers the identical estimate (diff = 0) | converts the prior pass's "sign-flip not run (no plink reference)" line to verified; no doc text changed |
| `examples/cis_pqtl_mr.R` | check | none needed | regression: IVW 0.4264134 (p 1.3e-49), PP.H4 0.9999999, 6->5 instruments after PAV exclusion — identical to the last fix pass | no drift |
| `examples/phewas_drug_target_mr.R` full-outcome loop | check | none needed | regression with a corrected stub (previous stub had a fixed-allele bug that zeroed every outcome; fixed for this run only, not shipped): 151/151 filtered outcomes scanned, and for the first time the merge/Bonferroni/forest-input/`write.table` steps after the loop also ran clean | |
| `scripts/phewas_curated_endpoints.R` | check | none needed | regression: clean run, exit 0, real 131-row output file, against a fresh 300-endpoint synthetic catalogue + 8 real significant cis-pQTLs | still not run against the live catalogue (needs an OpenGWAS token) |
| SKILL.md R/bash blocks, package versions | check | none needed | R install block and both bash blocks parse (`parse()`, `bash -n`); MendelianRandomization 0.10.0, TwoSampleMR 0.7.9, coloc 5.2.3, ieugwasr 1.1.0.9000 all match every version claim in the Skill | |

## Left unfixed (checkpoint, needs a decision)

- `scripts/phewas_curated_endpoints.R` and `examples/phewas_drug_target_mr.R` against the live OpenGWAS catalogue — needs an OpenGWAS JWT token.
- `1kg.v3.tgz` 1000G EUR download (~1.5 GB) in SKILL.md's Tool Installation Notes — not downloaded this phase (judged not worth it); the plink/LD mechanism it supports is now independently verified against a different, already-cached real panel instead.
- Ensembl VEP (SKILL.md PAV Annotation section) — never run; not installed here (real GRCh38 cache is itself multi-GB); checked against VEP's own documented flags only.
