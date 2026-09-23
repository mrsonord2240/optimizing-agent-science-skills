# bio-causal-genomics-pleiotropy-detection fixes (2026-09-17)

Worktree `F:\OpenScience\wt\mr-pleio`, branch `fix/mr-pleiotropy`, based on `openscience-fixes` @
`558aea5`. Fixer: Claude Sonnet 5. Runtime: R 4.4.3 via
`F:\OpenScience\audit-envs\mendelian-randomization-analyst\r.sh`; TwoSampleMR 0.7.9, simex 1.8,
MendelianRandomization 0.10.0, MRMix 0.1.0, mr.raps 0.4.3 already installed there (candidate
`mendelian-randomization-analyst`, no version changes made). Three commits: `9b5403f` (P0, both
P1s that need code/table changes, practice boundary, two P2s -- made in an earlier, interrupted
run of this same task), `d7f4589` (the third P2, dedupe), `9b18931` (MR-RAPS calling convention,
found while re-verifying). Verification scripts: scratchpad `mr-pleio/` (`test_simex_original.R`,
`test_simex_fixed.R`, `test_simex_band.R`, `run_shipped_simex2.R`, `test_mrmix_n18.R`,
`test_raps_weak.R`/`test_raps_weak2.R`, `check_raps_sig.R`, `verify_raps_snippet.R`), independent
of the audit's own scripts in `F:\OpenScience\audits\...\run\`, plus a fresh `git clone` of
`lukejoconnor/LCV` to check `RunLCV.R`'s real field names.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| SIMEX example crashes as shipped | P0 | `examples/simex_egger_correction.R`: precompute `w <- 1 / dat$se.outcome^2` before `lm()`, pass `weights = w` instead of the in-formula `1 / se.outcome^2` | ran | Reproduced the crash independently (`test_simex_original.R`: `ERROR: object 'se.outcome' not found`), confirmed the fix runs (`test_simex_fixed.R`), then ran the actual shipped file end-to-end via `source()` (`run_shipped_simex2.R`, B=1000, planted true effect 0.3, I^2_GX=0.607): SIMEX-corrected slope 0.340 vs naive 0.298 -- no crash, recovers a checkable value, not just exit 0 |
| LCV usage snippet references a field name that doesn't exist | P1 | SKILL.md: `res_lcv$gcp` -> `res_lcv$gcp.pm` in the code comment | docs | `git clone`d `lukejoconnor/LCV` fresh into scratchpad and read `RunLCV.R`'s own header/return list directly: fields are `zscore, pval.gcpzero.2tailed, gcp.pm, gcp.pse, rho.est, rho.err` -- no `gcp` field exists |
| MR-Mix / contamination mixture don't fail the way Common Errors says | P1 | SKILL.md Common Errors row rewritten: describes the actual behavior (confident point estimate below the 20-SNP minimum, not NA) and adds a pre-flight n-check recommendation | ran | Own script (`test_mrmix_n18.R`), n=18 (below documented minimum): `MRMix()` returned theta=0.34, p=4e-7 (not NA); `mr_conmix()` returned a non-NA estimate with a finite CI -- independent of the audit's Input 7, same conclusion |
| No practice-boundary scaffolding for individual-level requests | P1 | Added a "Practice boundary" paragraph after SKILL.md's opening method list: decline personal treatment/diagnostic requests, name the population-vs-individual gap, redirect to a physician | docs (matches the pattern used in `causal-genomics/mediation-analysis`'s own fix) | |
| MR-RAPS weak-instrument claim didn't hold under stress | P2 | Algorithmic Taxonomy row and a new Common Errors row: qualify "weak-IV robust" with an extreme-weak-IV caveat (mean F well below 10) naming the actual degenerate-overdispersion warning text | ran | Own script (`test_raps_weak2.R`), mean F=2.6 (independent dataset/seed from the audit's Input 4): RAPS(huber) error 0.212, RAPS(tukey) error 0.217, both worse than IVW's 0.041; tukey printed "another finite root" warnings; huber printed "overdispersion parameter is very small" / "Cannot find solution with finite over.dispersion" |
| SKILL.md/usage-guide.md duplicate content | P2 | usage-guide.md's "Operational Decision Flow" section trimmed to a one-line pointer at SKILL.md's canonical 4-step version; header kept so nothing links to a vanished section | docs | Checked sibling Skills in the same folder (`colocalization-analysis`, `genetic-correlation`): neither repeats SKILL.md's decision logic in usage-guide.md, confirming this was the outlier, not the house style |
| No seed guidance for MR-PRESSO | P2 | `set.seed(42)` added immediately before SKILL.md's inline `mr_presso()` call, with a one-line Monte-Carlo note | docs (examples/*.R already seed; only the inline block was missing it) | |
| (Found while fixing) MR-RAPS bullets imply `over.dispersion=`/`loss.function=` are passed directly to `TwoSampleMR::mr_raps()` | not in `recommendations[]` | Added a code block to the MR-RAPS section showing the real nested form: `parameters = list(over.dispersion = TRUE, loss.function = 'huber', shrinkage = FALSE)`, with a one-line note that bare top-level arguments throw `unused arguments` | ran | `TwoSampleMR::mr_raps()`'s real signature is `function(b_exp, b_out, se_exp, se_out, parameters = default_parameters())` (`args()`); confirmed the bare-argument form errors and the `parameters = list(...)` form succeeds (`verify_raps_snippet.R`) |
| Pre-audit lead: contamination-mixture snippet allegedly calls `mr_raps` | not a `recommendations[]` item | Checked and refuted -- `examples/sensitivity_battery.R` lines 111-119 correctly call `mr_conmix()` | ran/read | No change made |

All 7 `recommendations[]` entries fixed (1 P0, 3 P1, 3 P2), plus one additional defect found while
fixing (MR-RAPS calling-convention bullets). Nothing left unfixed.

Three commits total on `fix/mr-pleiotropy`: `9b5403f`, `d7f4589`, `9b18931` (`9b5403f` was made in
an earlier, apparently interrupted run of this exact task -- this session independently
re-verified every claim in it before treating it as done, then added the dedupe fix that commit
had declined, then the MR-RAPS calling-convention fix found during that re-verification).

Nothing needs Sam.

## Redundancy pass (2026-09-17)

Fixer: Claude Sonnet 5. Same worktree/branch, on top of `9b18931` (both prior commits kept intact).
Commit: `refactor(causal-genomics/pleiotropy-detection): state each fact once across SKILL.md and
usage-guide.md`. Scope: `SKILL.md` and `usage-guide.md` only, per the brief's 2026-09-17 "Remove
redundancy, every pass" rule. Lines: SKILL.md 452 -> 473 (net +21: absorbed usage-guide.md's install
commands, input-format note, LCV gcp table, and three Tips-only details); usage-guide.md 142 -> 79
(net -63).

**Deleted passage -> new home** (every deletion verified present at destination by grep before commit):

| Deleted from usage-guide.md | New home in SKILL.md | Note |
|---|---|---|
| Overview's UHP/CHP bullet list + InSIDE definition + rg>=0.3 sentence | "UHP vs CHP: The Central Postdoc-Grade Distinction" (already there) | Overview now a 2-sentence pointer |
| "LCV gcp Interpretation" table + "LCV uses ALL genome-wide SNPs..." sentence | "LCV (Latent Causal Variable)" section | SKILL.md previously said "Full gcp interpretation table is in usage-guide.md" -- table moved in, pointer removed; Quantitative Thresholds' matching pointer line changed to "...tabulated in the LCV section above" |
| "Prerequisites" install code block (`remotes::install_github(...)` x6 + LCV clone note) | "Version Compatibility" section | Byte-identical code block, moved verbatim |
| "Prerequisites" input-format paragraph (harmonized TwoSampleMR data.frame / LHC-MR / LCV / CAUSE input shapes) | "Version Compatibility" section | |
| "What the Agent Will Do" 11-step list | "Operational Decision Flow (4 Steps)" + "Standard Sensitivity Battery (Working Reference)" (already there) | Replaced with a 1-line pointer to both sections |
| Tips: "UHP vs CHP" (PRESSO blind to CHP) | "MR-PRESSO false negative under CHP" failure mode (already there) | Deleted, no unique content |
| Tips: "NbDistribution" ("5000 minimum") | Quantitative Thresholds row "MR-PRESSO NbDistribution" (already there, unchanged) | **Disagreement resolved**: Tips framed 5000 as a hard minimum, contradicting SKILL.md's own tiered "1000 exploratory; >=5000 publication; >=10000 stringent" (also matches Operational Decision Flow step 2 and the Standard Sensitivity Battery code, which use 10000). Kept SKILL.md's tiered version since it's the one the code/decision-flow/battery sections already agree on; deleted the Tip |
| Tips: "Egger NOME" | "MR-Egger NOME violation" + I^2_GX rows in Quantitative Thresholds (already there) | Deleted, no unique content |
| Tips: "Few-SNP Egger" | "MR-Egger underpowered with few SNPs" (already there) | Deleted, no unique content |
| Tips: "CAUSE sample overlap" | CAUSE section's `est_cause_params`/rho text (already there) | Deleted, no unique content |
| Tips: "CAUSE underpowered regime" | "CAUSE underpowered with few significant SNPs" (already there) | Deleted, no unique content |
| Tips: "Steiger interpretation" | "Steiger filter inverted by exposure measurement error" (already there) | Deleted, no unique content |
| Tips: "MR-PRESSO majority assumption" | "MR-PRESSO majority-outlier breakdown" (already there) | Deleted, no unique content |
| Tips: "MR-RAPS install" | Common Errors row `MR-RAPS package not found...` | Row already covered the GitHub install + `TwoSampleMR::mr_raps()` wrapper; appended the Tip's unique detail ("or `mr.raps::mr.raps()` directly") to the row |
| Tips: "MR-Clust biology" | MR-Clust section's closing paragraph | Appended the Tip's unique clause ("Pure statistical clustering without a biological story is weak evidence") |
| Tips: "LHC-MR runtime" | LHC-MR Workflow section + Common Errors "LHC-MR runtime > 24h" row (already there) | Deleted, no unique content |
| Tips: "LCV vs MR" | LCV section's opening paragraph | Its "genome-wide SNPs not just significant instruments" detail folded into the LCV paragraph (already largely said via "complement to, not a replacement for, MR") |
| Tips: "STROBE-MR" | STROBE-MR Reporting section's closing paragraph (already there) | Deleted, no unique content |
| Tips: "Reproducibility" (pin versions) | Version Compatibility section, appended to the closing sentence | Only Tip with genuinely unique content and no existing SKILL.md home |
| "Related Skills" full 7-line list | SKILL.md's "Related Skills" (already there, identical) | usage-guide.md's copy replaced with "See SKILL.md's Related Skills section." |

Untouched (already collapsed by the prior session's `d7f4589`): usage-guide.md's "Operational
Decision Flow" section was already a 1-line pointer before this pass. No SKILL.md-internal
repetition found beyond the intentional narrative-section / Quantitative-Thresholds-lookup-table
pattern (a threshold stated once in prose, then summarized as one row in the aggregate table) --
left alone since collapsing it would break the table's one-stop-lookup purpose and wasn't itself a
named item in the dispatch.

No code changed (moves only, code blocks byte-identical); no R execution required for this pass.


## Fix pass on the 3 open P2s, split and scripts (2026-09-21)

Fixer: Claude Sonnet 5. Worktree `F:\OpenScience\wt\causal-genomics-pleiotropy-detection`, branch
`fix/causal-genomics-pleiotropy-detection`, from staging `main` @ `431aa55`. Audit: upstream `d91ed3d`
fork audit, 3 P2 findings, none already fixed by the earlier fix (all three are gaps that fix left).
Runtime: R 4.4.3 via the `mendelian-randomization-analyst` `r.sh`, TwoSampleMR 0.7.9, MRPRESSO 1.0.
Commits: fix `6484938`, split `30c5cf4`, scripts step `8645346`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| SIMEX not flagged as able to land further from truth than naive | P2 | SKILL.md NOME failure mode: added a "Caveat" paragraph (report naive and SIMEX slopes side by side with CIs, read against IVW / median / mode); header comment in `examples/simex_egger_correction.R` says the same | docs plus the audit's run 5 (naive 0.666 -> SIMEX 0.854, truth 0.3, IVW 0.314, conmix 0.343) | The example already prints both slopes; no code change |
| `set.seed` covered only `mr_presso()` | P2 | Moved `set.seed(42)` ahead of `mr()` in the Standard Sensitivity Battery, comment names the weighted-median/mode bootstrap SEs | ran on the audit's `synth_simex.rds` (20 SNPs), block as in SKILL.md with `NbDistribution=500` for speed: two seeded runs identical (median/mode SE 0.0963 / 0.1249, PRESSO global p 0.962); two unseeded runs differ (0.0917 / 0.1293, p 0.958 vs 0.0910 / 0.1209, p 0.974) | `examples/sensitivity_battery.R` already seeds at line 15, before `mr()` |
| No `references/` split | P2 | Split, see below | line-multiset diff, R fences parsed | SKILL.md 476 -> 251 lines |

All 3 P2s fixed. Nothing left unfixed.

**Split (own commit `30c5cf4`).** Verbatim moves, no non-blank line lost (only the 5 edited pointer
lines differ), all 7 R fences parse. The audit suggested one `references/pleiotropy-methods.md` with the
taxonomy and threshold tables; those stay in SKILL.md because every request needs them (scope, decision
tree, thresholds), and the method-specific blocks moved instead, per FIX_BRIEF.

| SKILL.md section (old) | New home |
|---|---|
| Per-Method Failure Modes (all 7 subsections) | `references/failure-modes.md` |
| CAUSE for CHP-Aware Estimation | `references/cause.md` |
| MR-RAPS Loss Function and Overdispersion; MR-Clust for Mechanism Heterogeneity | `references/mr-raps-mr-clust.md` |
| LHC-MR Workflow (with the CAUSE vs LHC-MR table) | `references/lhc-mr.md` |
| LCV (Latent Causal Variable) incl. gcp table | `references/lcv.md` |
| Required Supplementary Tables; Anticipated Reviewer Pushback; STROBE-MR Reporting | `references/reporting.md` |

Stayed in SKILL.md: install/version, UHP vs CHP, decision flow, taxonomy, decision tree (rows now point at
the reference files), thresholds, sensitivity battery, bidirectional MR, reconciliation, Common Errors,
references, related skills. New "Reference Files" index.

**Redundancy:** already done on 2026-09-17 (section above); no new duplication found.

**Scripts step (commit `8645346`).** No `scripts/` file was created. The only inline block over 15 lines, SKILL.md's
Standard Sensitivity Battery (26 lines), is a strict subset of `examples/sensitivity_battery.R`, so per the
brief the copy is deleted and SKILL.md points at the example (seed-once and NbDistribution notes kept).
Every other block (CAUSE 4, MR-RAPS 5, MR-Clust 8, LHC-MR 3, LCV 3, install 9 lines) is under 15 and stays inline.

| old location | new home |
|---|---|
| SKILL.md "Standard Sensitivity Battery" R block | `examples/sensitivity_battery.R` (pointer) |

Found while verifying the pointer target, fixed in the same commit:

| finding | change | verified |
|---|---|---|
| `examples/sensitivity_battery.R` crashed at `directionality_test()` (simulated data had no `pval.exposure` / `pval.outcome`) | added both columns | ran the whole example, R 4.4.3, TwoSampleMR 0.7.9, NbDistribution 5000: Steiger 29/30 pass, IVW 0.379 vs planted 0.35, weighted median 0.344, mode 0.332, conmix 0.359 |
| "All methods agree on direction" printed NA when the PRESSO-corrected row is NA (no outliers) | `na.rm = TRUE` | checked on the run's estimates, file parses |
| SKILL.md said the example includes SIMEX; it does not | text points at `examples/simex_egger_correction.R` | docs |

SKILL.md 476 -> 251 (split) -> 223 (battery block replaced by pointer).

## Final-pass Phase 1 (2026-09-21)

Fixer: Claude Sonnet 5. Same worktree `F:\OpenScience\wt\causal-genomics-pleiotropy-detection`,
branch `fix/causal-genomics-pleiotropy-detection`, on top of `8645346`. Commit `5c1c030`. No revisit-list
row named this Skill; walked every runnable block per `FINAL_PASS_BRIEF.md`, not just what earlier
passes touched.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `examples/cause_analysis.R` crashes 100% of the time as shipped: only ~55-60 of the intended 150 "significant" SNPs actually cleared p<5e-8; `cause()` crashed hard on the resulting <100-SNP fit (`Error in -1 * comp[2, 1] : non-numeric argument to binary operator` in `in_sample_elpd_loo`) rather than the graceful wide-CI degradation the script's own WARNING implies | P1 (shipped example crashes) | Fixed the synthetic data so all 150 planted SNPs deterministically clear p<5e-8 (`sample(c(-1,1),...) * runif(n_sig, 0.035, 0.07)`, se 0.006; min |z|=5.83 > the ~5.45 threshold for p=5e-8) | ran | No prior audit or fix pass had ever run `cause()` itself (TOOLS.md only had a `library()` load check) |
| Deeper defect found underneath the above: installed `cause` 1.2.0.335 (jean997/cause GitHub HEAD) itself crashes against `loo` >=2.6 (env had 2.10.1) -- `loo_compare()`'s return layout changed (leading `model` column, rownames `model1`/`model2` -> `1`/`2`), and `cause`'s `in_sample_elpd_loo()` reads the old layout by position | not a Skill-code bug -- env/dependency incompatibility | Built a side R library `R-lib-cause-loo` (loo 2.5.1, CRAN archive, pure R) + `r_cause.sh` wrapper in the shared env, same pattern as its existing GenomicSEM/lavaan side-library fix; documented in the env's `TOOLS.md`, `SKILL.md` Common Errors, and `references/cause.md` | ran / confirmed by direct `loo_compare()` inspection | No install-lock needed (new, unshared directory); no existing package version changed |
| `examples/mr_presso_analysis.R` crashes 100% of the time as shipped, on its own hardcoded `set.seed(42)`: 0 outliers detected -> Distortion Test `Pvalue` is `NULL`, not a scalar `NA` -> `if (!is.na(distortion_p) && distortion_p < 0.05)` throws "missing value where TRUE/FALSE needed" | P1 (shipped example crashes) | Guarded the length-zero case (`length(distortion_p) > 0 && ...`) | ran | Reproduced independently first (`debug_presso_distortion.R`) before fixing |
| `references/lcv.md`'s `RunLCV()` snippet crashes at call time (`cannot open file 'MomentFunctions.R'`): `RunLCV()`'s own internal `source()` is relative to the R session's cwd, not `RunLCV.R`'s location, and the snippet never cwd'd into the clone's `R/` folder; the default `ldsc.intercept=1` also silently mis-estimates without real `n.1`/`n.2`, never shown in the snippet | P1 (shipped snippet crashes) | Added `setwd('LCV/R')` before the call and explicit `n.1 = n_exposure, n.2 = n_outcome` args | ran | Re-ran the corrected snippet and LCV's own upstream `ExampleSimulationScript.R`; both recover planted gcp=1 as gcp.pm 0.87-0.89, p<2.22e-16. This also resolves the env's own prior "SimulateLCV() zero-length output" note in `TOOLS.md` -- that was the earlier session's own test script, not a package defect |
| `examples/bidirectional_mr.R`, never run by any prior audit or fix pass | not a defect | none needed | ran | Built realistic harmonized TwoSampleMR forward/reverse instrument sets and sourced the file unmodified: forward IVW 0.326 vs planted 0.35 (p=1.1e-9), reverse IVW 0.018 vs planted 0 (p=0.73, correctly null), correct interpretation printed |
| `examples/simex_egger_correction.R`, re-verification | not a defect | none needed | ran | Built a harmonized `dat` with I^2_GX=0.655 (SIMEX-triggering band): SIMEX 0.387 vs naive 0.289 vs planted 0.3; prior pass's weights-precompute fix still holds |
| `examples/sensitivity_battery.R`, re-verification | not a defect | none needed | ran | Ran as shipped (self-contained data): IVW 0.379, RAPS 0.368, weighted median 0.344 vs planted 0.35; matches the audit's own recorded numbers |

Nothing left unfixed. Nothing needs Sam. Checkpoint:
`F:\OpenScience\audits\_final_pass\bio-causal-genomics-pleiotropy-detection\CHECKPOINT.md`.
