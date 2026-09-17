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
