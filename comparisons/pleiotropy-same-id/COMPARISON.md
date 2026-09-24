# Comparison: bio-causal-genomics-pleiotropy-detection (same id, two sides) - 2026-09-21

**Theirs**: Open Science / AIPOCH (`aipoch/medical-research-skills` d924410), 4 files: SKILL.md (302 lines), usage-guide.md, POLISH_CHANGELOG.md, an eval JSON. No scripts, no examples.
**Ours**: shelf, audited/fixed/re-audited, SKILL.md (475 lines), usage-guide.md, 5 runnable `examples/*.R`.

## What each claims
- **Theirs**: for someone validating an MR result. MR-PRESSO (global/outlier/distortion), MR-Egger intercept + I^2, Steiger filtering, a `run_sensitivity()` function, STROBE-MR list. Prose plus code blocks. Only one caveat set: Egger low power (<10 SNPs), I^2 < 0.9, PRESSO >= 1000 draws.
- **Ours**: the same UHP battery, plus the UHP-vs-CHP split, a 4-step decision flow (LDSC rg gate, battery, CAUSE/LHC-MR escalation, triangulate), a per-method "fails when" table and failure-mode sections (Egger NOME, PRESSO majority-outlier and CHP false negative, Steiger inversion, CAUSE power), MR-RAPS/MR-Mix/conmix/MR-Clust/CAUSE/LHC-MR/LCV, reconciliation table, practice boundary.

## Provenance (Q1: is theirs an earlier snapshot of the GPTomics Skill?)
- **Cannot establish by history.** `external/GPTomics__bioSkills` is a **shallow clone with one commit** (`d91ed3d`, "archive repo", 2026-08-15; `git rev-parse --is-shallow-repository` = true). `git log`/`show` for the path returns only that commit; the staging repo `mrsonord2240__bioSkills` also begins at `d91ed3d` and never contains the string "MRAPS CRAN package was archived" (`git log -S`). No pre-`d91ed3d` version is available anywhere on disk.
- **By content: not a copy of `d91ed3d`.** Only 23 of 227 non-blank SKILL.md lines (10%) and 11 of 49 in usage-guide.md occur in upstream, and those are frontmatter `name`, headings, code fences and `library()` lines (`run/92_prov.py` output). The body is a different, much shorter text.
- **What is consistent with (not proof of) an earlier version:** same `name`, same MIT licence, same "Goal:/Approach:" block convention and "Comprehensive Sensitivity Framework" shape that bioSkills uses; AIPOCH's polish is dated 2026-06-15, two months before the `d91ed3d` archive. Theirs carries `author: AIPOCH` and a Source link to aipoch, and no GPTomics credit inside the files. Conclusion: plausible ancestor, unverified; do not state it as fact.

## Shared data and requests
Synthetic summary statistics, 60 SNPs, mean F = 66.8, true theta = 0.30 except D (`run/00_gen_data.R`, `run/data/*.csv`). Synthetic because truth must be known; fair because both sides get the identical harmonised CSV, identical gamma/SE/noise, only the planted alpha differs. **A** balanced pleiotropy (alpha ~ N(0, .015)); **B** directional (alpha ~ N(+0.02, .008), InSIDE holds); **C** six planted outliers (rs7, 19, 28, 36, 47, 55); **D** correlated pleiotropy alpha = 0.5*gamma, true theta = **0**.
Requests: **R1** "is there directional pleiotropy; IVW vs Egger?" (A, B). **R2** "find outlier instruments with MR-PRESSO and correct the estimate" (C). **R3** "run the full sensitivity battery; can I trust this effect?" (D).
Each side's own code was run: theirs = SKILL.md blocks verbatim (`run/theirs_run.R`); ours = the SKILL.md battery block verbatim (`run/ours_run.R`) and the shipped `examples/sensitivity_battery.R` with its simulation block replaced by the CSV load (`run/ours_example_adapted.R`). Harness change, same for both: MR-PRESSO NbDistribution = 2000 (their text says 5000, ours 10000; both state 1000 as the floor; 5000+ was too slow on a shared machine). Logs `run/out/*.log`, assertions `run/out/assert.txt` (from `run/90_assert.R`).

## Results (request x side)
| Req (data) | Side | executed | Key output vs truth (source) |
|---|---|---|---|
| R1 (A) | both | true | IVW 0.310 (truth 0.30); Egger intercept 0.0052 p=0.50 (truth 0: correctly not flagged); Egger slope 0.249 (`assert.txt`) |
| R1 (B) | both | true | IVW **0.534** (biased, truth 0.30); Egger intercept 0.0164 p=0.013 (planted +0.02: flagged); Egger slope 0.344 se 0.078 (covers 0.30) |
| R2 (C) | both | true | PRESSO global p<5e-4; outliers 19,28,36,47,55 = **5/6 planted, 0 false**, missed rs7 (p=0.09); raw 0.318 -> corrected 0.310 (truth 0.30) |
| R3 (D) | theirs | true, one block errored | IVW 0.485, Egger 0.528 (p=1.8e-11), median 0.429, mode 0.378, PRESSO global p=0.39, Egger intercept p=0.47, Q p=0.145. All clean, all wrong (truth 0). Its summary prints "Consistent estimates across methods: Evidence strengthened" (`theirs_D_chp.log`) |
| R3 (D) | ours | true | Identical numbers (`ours_D_chp.log`). Adapted example adds conmix 0.499, RAPS 0.483 (warns "overdispersion very small"), prints "UHP-method agreement alone is INSUFFICIENT under CHP; run CAUSE or LHC-MR" (`oursex_D_chp.log`) |

Executed: theirs 3/3 requests (RAPS block errored 4/4 datasets); ours 3/3 (plus the example battery 4/4, 0 errors). Not run on either side: CAUSE/LHC-MR/LCV (need genome-wide sumstats, not in an instrument-level table; ours only) and SIMEX (I^2_GX = 0.863 < 0.9 on all sets; ours' rule says apply it).

## What only one side does
- **Same numbers on the UHP core** (IVW/Egger/median/mode/PRESSO/Steiger identical to 4 s.f. in `assert.txt`). On the core, either serves.
- **Ours only:** CHP regime and the rule that the IVW/Egger/PRESSO triple is blind to it (Morrison 2020); rg gate and escalation triggers; NOME tiers with SIMEX; PRESSO majority-outlier and Steiger-inversion warnings; working RAPS/conmix/CAUSE/MR-Clust calls; F-statistics; reconciliation table. On D, only ours tells the reader the clean battery does not clear the effect.
- **Theirs only:** a filter-then-rerun Steiger snippet, a multivariable MR stub, and the input-validation refusal boilerplate. Nothing statistical that ours lacks.
- **Neither can detect D from these numbers.** Ours' own numeric triggers (Egger/median/mode gap > 2 SE) did not fire (0.528 vs 0.429, ~1.6 SE); only the rg gate would, and it needs LDSC data.

## Verdict: **partial** (overlap on the UHP core; ours is a strict superset in guidance)
Prefer **ours** for any real MR validation, especially with high rg, weak instruments or a polygenic exposure. Theirs is usable only as a minimal PRESSO+Egger recipe, and its "Egger valid even with directional pleiotropy (InSIDE)" line has no CHP caveat: on D the Egger slope is 0.528 against a true 0.

## Defects hit (one line each)
- Theirs: `mr_raps(mr_input)` after `library(MendelianRandomization)` errors ("argument b_out is missing"): that package has no `mr_raps` (4/4 runs).
- Theirs: the line labelled `mr_conmix` actually runs `mr(dat, method_list='mr_raps')`, so no contamination mixture is ever run.
- Theirs: `summarize_sensitivity()` prints "Significant Egger intercept: Directional pleiotropy present" and the other verdict lines unconditionally, including on D where p=0.47.
- Theirs and ours: when PRESSO finds no outliers (B, D) the corrected estimate is silently NA; ours' example then prints "All methods agree on direction: NA" (`all()` over an NA), a silently uninformative line.
- Environment: OpenGWAS is gated, so `extract_instruments('ieu-a-300')` in theirs' multivariable stub was not run.
- My harness: first parallel launches were killed and rerun at NbDistribution 2000; logs in `run/out` are from the final run only.
