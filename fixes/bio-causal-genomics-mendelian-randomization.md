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
