# bio-causal-genomics-mendelian-randomization fixes (2026-09-17)

Worktree `F:\OpenScience\wt\mr-mr`, branch `fix/mr-mendelian-randomization`, based on
`openscience-fixes` @ `558aea5`. Fixer: Claude Sonnet 5. Runtime: R 4.4.3 via
`F:\OpenScience\audit-envs\mendelian-randomization-analyst\r.sh`; TwoSampleMR 0.7.9,
MendelianRandomization 0.10.0, MRPRESSO 1.0, coloc 5.2.3, simex 1.8 already installed there
(candidate `mendelian-randomization-analyst`), no version changes made, nothing new installed.
Verification scripts: scratchpad `mr-mr/` (`verify_p0_realdata.R`/`verify_p0_realdata_fast.R`
(real GIANT-BMI15 x PGC-MDD18 data, background — MR-PRESSO's 10000/1000-draw bootstrap on 95 real
SNPs did not finish inside this session's turn budget under shared-machine load, same as the
audit's own note), `verify_p0_unit.R` (deterministic unit-check of the exact defensive expression
against the exact character value the audit's Input 1 confirmed MRPRESSO returns on this real
dataset), `verify_simex.R`, `test_coloc_ld.R`/`test_coloc_ld2.R`/`test_coloc_ld3.R` (parameter
search), `rundir/cis_mr_drug_target.R` (full patched file re-run end to end).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `examples/two_sample_mr.R`'s MR-PRESSO reporting line crashes on real pleiotropic data | P0 | `signif(...Global Test$Pvalue, 3)` -> check `is.numeric()` first, print the raw string otherwise; same guard added to the Distortion-test line; `set.seed(42)` added before the call | ran | Root cause: MRPRESSO's own source coerces `Pvalue` from numeric to a character string (e.g. `"<2e-04"`) whenever the bootstrap p rounds to 0. Re-ran the real-data harmonisation (GIANT-BMI15 x PGC-MDD18, 95 SNPs after dropping 1 palindromic SNP -- exact match to the audit's Input 1 numbers). The full MR-PRESSO bootstrap (10000, then 1000 draws) did not finish inside this session's background-check window under concurrent machine load, so verification closed the loop a second, faster way: `verify_p0_unit.R` reproduces the *exact* pre-patch crash (`signif("<2e-04", 3)` -> `"non-numeric argument to mathematical function"`, matching the audit's error text verbatim) and confirms the patched `is.numeric()` branch prints `"<2e-04"` without crashing, plus confirms no regression on an ordinary numeric p-value (`0.00612` unchanged) |
| Decision Tree / Operational rule name MR-RAPS as the fix for one-sample-equivalent designs generally | P1 | Decision Tree row, Operational rule paragraph, and the "Sample-overlap correction ignored" Common Errors row all now state MR-RAPS corrects weak-instrument bias only, not sample-overlap/confounding bias, and point to MRlap/Burgess-2016 for the latter | docs, backed by a run | Audit's Input 7 (UKB-on-UKB, planted true effect 0, mean F=44.6, well above the one-sample F>=20 floor): naive IVW b=0.180, MR-RAPS b=0.196 -- MR-RAPS was no better, because the bias source was sample-overlap confounding, not weak instruments, which MR-RAPS does not address |
| SIMEX correction was prose-only in SKILL.md; the natural in-formula weighting pattern crashes | P1 | Added a runnable code block under "NOME violation invalidating Egger": precompute `w <- 1 / dat$se.outcome^2` before `lm()`, pass `weights = w, data = dat`, then `simex()`; IVW section's duplicate prose trimmed to point here instead of repeating it | ran | `verify_simex.R`: NOME-violated synthetic data (I^2_GX = 0, true slope 0.4) -- naive Egger recovered 0.395 (checkable, close to truth); SIMEX ran to completion without the `object 'se.outcome' not found` crash the in-formula form produces. Same verified pattern as the sibling `pleiotropy-detection` fix (`fix/mr-pleiotropy`), independently re-run here rather than copied |
| `examples/cis_mr_drug_target.R`'s synthetic data cannot demonstrate its own PP.H4 >= 0.7 threshold | P1 | Rewrote the data-generating step: one causal SNP plus an LD-tag-decay vector (`r_tag <- exp(-|distance|/250000)`), exposure effect = `beta_causal_exp * r_tag` + noise, outcome effect = that same tagged signal x `true_beta_xy` + noise, so both traits' association profiles peak at the same SNP instead of being drawn independently | ran | Root cause (confirmed by the audit's own Input 2 re-run, which used the same independent-per-SNP pattern and got the same failure): with every SNP's effect drawn independently, coloc.abf can't localize a single shared causal SNP and spreads posterior mass onto PP.H1/PP.H3 even when a true shared beta_XY is planted. Parameter search (`test_coloc_ld2.R`/`ld3.R`) confirmed the LD-decay approach across several decay/effect-size settings; the shipped file's own `set.seed(7)` reproducibly gives PP.H4 = 1.00 (11 of 40 SNPs pass genome-wide significance + F>=10, IVW b=0.613 vs true 0.5) -- re-ran the actual patched file end-to-end in a scratch working directory, not just the isolated test |
| No seed before SKILL.md's own inline Monte-Carlo `mr_presso()` call | P2 | `set.seed(42)` added immediately before the call, matching the fix already applied to `examples/two_sample_mr.R` | docs (examples/*.R already needed the same seed added as part of the P0 fix) | |
| SKILL.md / usage-guide.md duplicate content | P2 | See redundancy-pass table below | docs | |

All 6 dispatched findings fixed (1 P0, 3 P1, 2 P2). Nothing left unfixed.

## Redundancy pass (2026-09-17)

Scope: `SKILL.md` and `usage-guide.md` only, per the brief's "Remove redundancy, every pass" rule.
Lines: SKILL.md 414 -> 439 (net +25: absorbed usage-guide.md's missing `simex` install entry and
the plink2/1KG URLs, plus the new SIMEX code block and MR-RAPS/seed fixes above).
usage-guide.md 125 -> 78 (net -47).

**Deleted passage -> new home** (every deletion verified present at destination before commit):

| Deleted from usage-guide.md | New home in SKILL.md | Note |
|---|---|---|
| "Prerequisites" R install block (`install.packages(...)` + 8 `remotes::install_github(...)` lines) | "Tool Installation Notes" (already there) | **Gap found and closed**: usage-guide.md's copy included `simex` in the CRAN-stable list; SKILL.md's own copy did not, even though SKILL.md now ships runnable SIMEX code that needs it. Added `simex` to SKILL.md's `install.packages()` line rather than just deleting the usage-guide.md copy |
| "Prerequisites" OpenGWAS JWT paragraph | "Common Errors" row `Unauthorized / 403 from OpenGWAS` (already there, identical content) | Deleted, no unique content |
| "Prerequisites" bash comment block (plink2 + 1KG bfile URLs) | "Tool Installation Notes" closing sentence | URLs (`cog-genomics.org/plink/2.0`, `mrcieu.github.io/ieugwasr`) were nowhere in SKILL.md; folded into its existing local-clumping sentence |
| "What the Agent Will Do" 12-step list | Decision Tree + TwoSampleMR Standard Workflow + MR-PRESSO/CAUSE/MVMR/Steiger/STROBE-MR sections (already there) | Replaced with a 4-line pointer naming the sections |
| Tips (17 bullets: F-stat-from-exposure, MR-RAPS install, OpenGWAS auth, UKB-on-UKB bias direction, palindromic handling, Egger NOME, CAUSE SNP floor, MVMR conditional F, CAUSE/CHP, Bonferroni, STROBE-MR, Steiger confounding, MRlap, non-linear MR, one-sample F floor, binary-outcome non-collapsibility, qhet_mvmr fallback) | Common Errors table, Per-Method Failure Modes, Statistical Model Taxonomy, Decision Tree, Quantitative Thresholds, MVMR section, Binary-outcomes section, MRlap section, STROBE-MR Reporting section (each already present) | Checked every one individually: all 17 were verbatim or near-verbatim restatements of content SKILL.md already had in its own agent-facing sections; none carried a fact absent from SKILL.md. Deleted the whole section rather than a partial trim -- Tips is not one of the three categories (overview / example prompts / related Skills) the brief keeps in usage-guide.md |

Untouched: "Overview", "Quick Start", "Example Prompts", "Related Skills" -- all within the brief's
allowed usage-guide.md categories, no restatement of SKILL.md agent-facing material found in them.

Left unfixed: none. Nothing needs Sam.

---

# Round 2 (2026-09-17) — re-audit P2s

Worktree `F:\OpenScience\wt\mr-mr-p2`, branch `fix/mr-mr-p2`, based on staging `main` @ `978ae4a`
(already contains round 1 above). Commit `dfecae6`. Fixer: Claude Sonnet 5. Runtime: R 4.4.3 via
`F:\OpenScience\audit-envs\mendelian-randomization-analyst\r.sh`; MVMR 0.4.8, TwoSampleMR 0.7.9
already installed, no version changes, nothing new installed. Evidence: re-audit at
`F:\OpenScience\audits\bio-causal-genomics-mendelian-randomization\` (score 87, Production Ready).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Below conditional F < 1, `qhet_mvmr` flips the sign of an exposure's estimate; SKILL.md called it "robust to weak conditional instruments" with no floor | P2 | Added `if (any(condF < 1)) stop(...)` to the "MVMR with Conditional F" code block, plus a caveat paragraph with the reproduced numbers; softened the "robust to weak conditional instruments" claim | ran | Reproduced the re-audit's own Input 4 (`run/input4_mvmr.R`) verbatim: condF = 0.87/0.78, MVMR-IVW = 0.298/-0.099 (true 0.30/-0.10, close), `qhet_mvmr` = 0.236/**+0.049** (true -0.10 — sign flip). Confirmed the new guard fires at condF = 0.87/0.78 and does *not* fire on an independent-instrument synthetic case at condF = 1.22/1.21 |
| Under SKILL.md's own inline code ("TwoSampleMR Standard Workflow" and "Bidirectional and Steiger"), `directionality_test()` returns `NULL` with no error | P2 | Added `samplesize_col = 'N'` to both `read_exposure_data()`/`read_outcome_data()` calls in the Standard Workflow block (matching the already-correct `examples/two_sample_mr.R` pattern); added an `is.null()` guard with `stop()` at both call sites | ran | Root cause: `TwoSampleMR::directionality_test()` needs `pval.exposure`/`pval.outcome`/`samplesize.exposure`/`samplesize.outcome` (or precomputed `r.exposure`/`r.outcome`); without them it prints a message and returns `NULL` — no error. Reproduced the NULL on synthetic planted-direction data using SKILL.md's code exactly as written pre-fix; confirmed the fix returns `correct_causal_direction = TRUE`, `steiger_pval = 7.85e-180` (planted direction is exposure -> outcome); confirmed the new guard fires with a clear message when `samplesize_col` is omitted |

2/2 dispatched P2s fixed. All 7 R code blocks in the updated SKILL.md re-verified to parse
(`Rscript -e "parse(...)"`).

**Out of scope, not fixed:** CAUSE crashing against `loo` 2.10.1 (`in_sample_elpd_loo` -> `loo_compare()`
shape mismatch). This is a package-version defect in the environment (`cause` 1.2.0.335 x `loo`
2.10.1), not in any file this Skill ships — SKILL.md's own CAUSE section is prose plus a pointer to
the sibling `pleiotropy-detection` Skill, not runnable code here. Per the re-audit's own note, it
does not affect the veto or the grade.

Left unfixed: none of the two dispatched findings. Nothing needs Sam.

---

# Round 3 (2026-09-21) -- comparison defect + open P2s + split

Worktree `F:\OpenScience\wt\causal-genomics-mendelian-randomization`, branch
`fix/causal-genomics-mendelian-randomization`. Commits: `4bcf657` (fixes), `10e2381` (split). Fixer: Claude Sonnet 5.
Evidence: `F:\OpenScience\comparisons\mr-execution\COMPARISON.md` and its `run\` scripts; the re-audit's two open P2s.
Runtime: R 4.4.3 via `r.sh`, TwoSampleMR 0.7.9, MRPRESSO 1.0; nothing installed. Verification script: scratchpad `v/verify_presso.R`
(comparison's harmonisation on `data_A`, `data_B`, NbDistribution 3000, seed 42).

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| SKILL.md MR-PRESSO outlier rule `Pvalue < 0.05 / nrow(dat)` double-corrects (MRPRESSO's outlier P is already x n) | P1 (silent under-detection) | Rule now `adjusted P <= SignifThreshold`; string P (`"<3e-04"`) parsed; NULL `Outlier Test` guarded; rows returned by `dat_p[rownames(ot)[...], 'SNP']`; `mr_presso` run on `dat[dat$mr_keep, ]` | ran | Old rule flagged 0 on A and B. New rule: A 11 flagged, 9 planted (of 29 in set); B 8 flagged, 8 planted (of 30). Both identical (`setequal`) to MR-PRESSO's own `Distortion Test$Outliers Indices`; source lines checked with `deparse(mr_presso)` (`refOutlier <- which(OutlierTest$Pvalue <= SignifThreshold)`) |
| `examples/two_sample_mr.R` STROBE summary line still `signif()` on the string PRESSO p (the 2026-09-17 P0 guard missed this second call) | P1 (crash on pleiotropic data) | Uses `presso_p_fmt`; added outlier-SNP extraction with the same rule and the `mr_keep` filter | ran (whole example end to end, NbDistribution 1000) + parsed | Found while fixing the rule; the crash path fires only when the bootstrap p is exactly 0 |
| Reconciliation row "IVW sig, WM sig, mode null -> trust IVW + median" endorses the false positive on the null-effect data | P2 | Row conditioned on non-significant Cochran Q and PRESSO global; new row for "IVW, WM and RAPS sig, Egger and mode null, Q and PRESSO global sig -> do not report a causal effect", with the comparison's planted-null numbers | ran (comparison `out_ours_B.txt`, my rerun of PRESSO on B: outlier-corrected IVW 0.070, p 1.5e-4) | |
| `NbDistribution = 10000` cost undocumented; the "Outlier test unstable" warning had no guidance | P2 | Floor `NbDistribution > nrow(dat)/SignifThreshold` and the 40-minute/shared-CPU cost stated; run in background, 3000-5000 to explore; Common Errors rows updated (new row for the double-correction symptom) | ran (warning text read from MRPRESSO source; comparison `out_theirs_A.txt` shows it at 1000 draws) | My own 3000-draw runs took >20 min each on a loaded machine |
| Re-audit P2: qhet_mvmr imprecise between conditional F 1 and 10 | P2 | CI caveat added to the existing guard paragraph with the audit's numbers | docs (audit run `input10`) | |
| Re-audit P2: CAUSE crashes against loo 2.10.1 | P2 | Version note in the CAUSE section | docs (audit Input 8; cause 1.2.0.335 x loo 2.10.1) | Note only; a package mismatch, no Skill file to fix |
| SKILL.md > 300 lines | structure | Split into `references/`: mr-presso, mvmr-conditional-f, mrlap-overlap-correction, simex-egger-nome, bidirectional-steiger, cis-mr-and-binary-outcomes, bibliography; "Reference Files" index + pointers on 7 decision-tree rows | ran (line diff, 7 R fences `parse()`) | 470 -> 331 lines. No non-blank line lost; 7 table rows only gained a pointer. Still over 300 because what every request needs (taxonomy, decision tree, failure modes, thresholds, standard workflow, common errors, install) stays |

No usage-guide.md change: it restates none of the edited text.

## Left unfixed

- **`cause()` crash under `loo` 2.10.1** (re-audit P2, comparison did not touch it): the fault is inside the installed `cause` package against a newer `loo`; fixing it means installing or pinning a different `loo`/`cause` in the shared env, which the brief forbids. Documented as a version note only.
- **qhet_mvmr precision (P2)** documented, not "fixed": it is a property of the estimator.
- **SKILL.md still 331 lines** (> 300): the remaining sections are the ones every request needs; moving them would remove what the brief says must stay.
- **`I^2_GX` = 0.996 reading / other comparison remarks** (theirs-side gaps, protocol scaffolding Theirs has and ours lacks: tiers, claim-boundary language): out of the Skill's scope (broader coverage the brief excludes).
- **Comparison note: IVW/WM/RAPS biased +0.04 to +0.10 on data A with 30% invalid IVs**: a property of the estimators on the planted data, not a Skill defect; the corrected reconciliation row and the Egger/mode guidance already cover it.
- **`examples/` synthetic data use random `A1`/`A2` (can be identical) and no LD clumping**: not hit in any run and not in the audit or comparison findings; judged not a correction.

---

# 2026-09-21 (structure)

Worktree `F:\OpenScience\wt\causal-genomics-mendelian-randomization`, branch `fix/causal-genomics-mendelian-randomization`, on top of `10e2381`. Commits: `189f3b4` (split), `9fde5b0` (scripts). Fixer: Claude Sonnet 5. No behaviour or claim changed; the MR-PRESSO outlier rule (adjusted P <= SignifThreshold, string P parsed, NULL guarded, `mr_keep` filter) is unchanged.

## Split: SKILL.md 331 -> 302 lines (extends the existing 7 files; 9 now)

| Moved from SKILL.md | To | Left in SKILL.md |
|---|---|---|
| Cohort Gotchas + Anticipated Reviewer Pushback (18 lines) | `references/cohorts-and-reviewer-pushback.md` (new) | heading + 1-line pointer |
| Tool Installation Notes (install block and mr.raps/plink note) | `references/tool-installation.md` (new) | heading + 1-line pointer |
| Winner's curse Mechanism + Fix | appended to `references/mrlap-overlap-correction.md` (its Read-when line updated) | heading, Trigger, Symptom, 1-line pointer |

Two new rows in the Reference Files index. Check: line set of the old SKILL.md against new SKILL.md plus references: only the edited index row differs. R fences `parse()` OK.

## Scripts: SKILL.md 302 -> 260 lines

| Old location | Script | How run |
|---|---|---|
| SKILL.md "TwoSampleMR Standard Workflow" R block (48 lines) | `scripts/twosample_workflow.R` (args `--exposure --outcome --outdir --bfile --plink --no-clump`; writes primary/heterogeneity/pleiotropy/leaveoneout/steiger/harmonised TSVs) | `r.sh` on `F:\OpenScience\comparisons\mr-execution\data_A` and `data_B` (the data the round-3 fix used) with `--no-clump`: 97/95 instruments, IVW/Egger/median/mode and `directionality_test()` all returned; numbers match round 3 (B: IVW p 2e-6, Egger p 0.72, mode p 0.82; A: IVW 0.397, planted 0.3). Missing `--bfile` without `--no-clump` stops with a clear error (checked) |
| `references/mr-presso.md` R block (27 lines) | `scripts/mr_presso_outliers.R` (`--dat --nb --seed --signif --out`) | `r.sh`, `--nb 1000 --seed 42`, on a 40-SNP subset of data_B's harmonised output (14 planted invalid): outliers = MRPRESSO's own `Outliers Indices` (6 SNPs, `setequal`), all 6 planted. Full 95 SNPs at 3000-10000 draws exceeds 20-40 min on this loaded machine, so the subset was used; the rule is the round-3 one, unchanged |
| `references/mvmr-conditional-f.md` R block (22 lines) | `scripts/mvmr_conditional_f.R` (`--dat --exposures --gencov`) | `r.sh` on the audit's Input 4 generator (seed 21): conditional F 0.87/0.78, guard stops with the message (checked); an independent-instrument case gave conditional F 22.6/25.7, MVMR-IVW 0.342/-0.119 (planted 0.30/-0.10), Q_A p 0.66 |
| `references/simex-egger-nome.md` R block (20 lines) | `scripts/simex_egger.R` (`--dat --B --seed`) | `r.sh` on the audit's Input 5 generator (seed 33, I^2_GX < 0.9): runs without the `se.outcome` crash; SIMEX slope 1.007 vs naive 0.339 (the audit's own run gave 1.020 at true slope 0.40, so the SIMEX extrapolation instability at I^2_GX ~ 0 is pre-existing, not new); on data_B harmonised: 0.1004 vs naive 0.0995 |

The load-bearing code comments (outlier-rule reasoning, simex weights workaround, NbDistribution cost) are kept in the script headers and as prose in the reference files. The three scripts that read data take the harmonised TSV from `twosample_workflow.R`.

Differences from the inline blocks, all mechanical: hard-coded file names and constants became arguments; `--no-clump` added because plink and a 1KG reference do not exist on this machine (default still clumps); MVMR generalised from `x1,x2` to a list of exposures (default unchanged); `--seed` on SIMEX optional.

## Stayed inline

- `references/bidirectional-steiger.md` block (13 lines) and `references/mrlap-overlap-correction.md` block (13 lines): under the 15-line threshold; MRlap also needs LDSC reference files that do not exist here.
- `references/tool-installation.md` install block: install commands, not analysis code.
- `examples/*.R` untouched; no block duplicated an example (the examples simulate their own data, the workflow reads user files).

## Left unfixed / not run

- **LD clumping path** (`ld_clump()` with plink + 1KG bfile) of `twosample_workflow.R`: no plink, `genetics.binaRies` or reference panel on this machine and the brief forbids installing; the code is verbatim from the inline block and only guarded by the `--bfile` check.
- **SKILL.md is now 260 lines**, under 300; nothing further to split.
