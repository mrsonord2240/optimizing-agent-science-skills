# bio-outlier-splicing-detection - fix log

## 2026-09-20 (fixer, branch `fix/as-outlier`, worktree `F:\OpenScience\wt\as-outlier`)

First audit: 67, Beta Only, not deployable, no veto/P0. Evidence: `F:\OpenScience\audits\bio-outlier-splicing-detection\`.
Checked on FRASER 2.2.0 + OUTRIDER 1.24.0 (Windows R 4.4.3 / Bioc 3.20, `r.sh`) and FRASER 2.6.1 + OUTRIDER 1.28.1 + DROP 1.6.1 (WSL `as-drop`, R 4.5.3 / Bioc 3.22); regtools 1.0.0, leafcutter 0.2.9, bcftools 1.24. No new env was needed (nothing installed anywhere). Scratch (cohort BAMs regenerated from `01_make_synth_cohort.py`, truth and gene counts byte-identical to the audit): `F:\OpenScience\as-outlier-scratch`.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| Main FRASER workflow + example crash (`colData = data.frame`) | P1 | `S4Vectors::DataFrame()` in SKILL.md block and `examples/fraser2_rare_disease.R`; example takes `bam_dir patient_id working_dir` args, stops if patient absent, warns n<20, prints junctions kept / q / calls, writes volcano to a PDF, no dplyr; also fixed a crash the run exposed (empty result -> `order(NULL)`) | ran (clean copy) on the planted 30-sample cohort on 2.2.0 and 2.6.1: 4/4 planted events flagged in the right sample/gene (2.6.1: skipping S05/g010 padj 2.8e-5, cryptic donor S12/g030 9.3e-3, retention S20/g050 9.1e-4, pseudoexon S25/g070 3.6e-3; 2.2.0: 4.1e-5, 1.1e-2, 1.1e-3, 5.2e-3), 0 non-planted calls, expression-only S15/S28 not called; n=8 and n=12 subsets now finish with 0 calls; 4 real chrX BAMs run to the end on both versions (232 / 262 junctions, 0 calls, n warning) | 2.2.0 has no `estimateBestQ`; example picks `optimHyperParams` there (`exists()` check) |
| `estimateBestQ` / `plotEncDimSearch` API drift (FRASER and OUTRIDER) | P1 | FRASER: `estimateBestQ(fds, 'jaccard', plot=FALSE)` + `bestQ()`; OUTRIDER: block handles number (1.24.0) or object (1.28.1); `max(q,2)` because OHT returned q=1 on the synthetic matrix and `OUTRIDER()` rejects q<=1 (found by running); `plotEncDimSearch` comment corrected: default shows OHT singular values and returns NULL after `useOHT=FALSE`, `plotType='auc'/'loss'` show the grid | ran: OUTRIDER block verbatim from SKILL.md on 1.24.0 (Windows) and 1.28.1 (as-drop), n=30 and n=100 synthetic counts, no crash; `plotEncDimSearch` on 2.6.1 (default -> NULL + warning, auc/loss -> ggplot) | Windows: `MulticoreParam` errors in OUTRIDER 1.24.0 (`mcparallel`), so the block picks `SerialParam()` on Windows |
| OUTRIDER cohort guidance too optimistic (0/57 at n=30) | P1 | New measured power table (OUTRIDER's simulator, 2000 genes, 3 seeds, both versions): n=20 0/107 both; n=30 0/156 (1.24.0), 5/156 (1.28.1); n=50 37% / 41%; n=60 48% / 56%; n=100 71% / 74%; n=200 71% / 77%; fixed q=2 or 4 does not rescue n=30 (0/156), q=2 at n=50 gave up to 39 false calls. Rule stated: OUTRIDER >=50 (useful power ~100); "acceptable at n=20-50" and the shared FRASER/OUTRIDER table removed; failure-mode symptom corrected to the silent `No significant events` | ran: `outrider_power.R` 6 sizes x 3 seeds x 2 versions, plus fixed-q runs | synthetic; false calls 0-2 per 3 seeds at padj<0.05 |
| No research-use caveat; PS3 / clinical report directive | P1 | New "Research Use and Licences" section; description reworded (no "clinical diagnostics"/"clinical samples"); usage-guide step 7 "clinical report with PS3 weight" deleted; the "strong PS3 ... converts PP3 to PS3" sentence and the "(PP3, not PS3)" pitfall replaced by: candidate for follow-up, classification/strength is a clinical-lab decision (ClinGen SVI, Walker 2023), not this Skill | read | |
| Licence misstated | P1 | Licence bullet: FRASER 2.6.1 / OUTRIDER 1.28.1 / DROP 1.6.1 CC BY-NC 4.0, FRASER 2.2.0 / OUTRIDER 1.24.0 MIT (LICENSE files read in both installs); frontmatter `license: MIT` untouched | ran (`packageDescription` + LICENSE files, both R libs; DROP notice printed by `drop init`) | |
| q=10 hard-coded, tuning advice unbacked | P1 | Example and SKILL call `estimateBestQ`; merged into one "Choosing q" section with measured sweep (PCA, n=30: q=1-3 4/4, 5-10 3/4, 15 1/4; OHT q=1 on 2.6.1, grid q=2 on 2.2.0, both 4/4); "q=8-15 usual, 5-8 for small" removed | ran (example on both versions; audit's q sweep quoted) | |
| DROP section: `drop init <name>`, config keys, MAE, `--use-conda`, PCA default | P1 | `mkdir && cd && drop init`; real keys (`run: true`, PCA, FRASER2, padjCutoff 0.1, expression autoencoder); `snakemake aberrantSplicing --cores N`; no `--use-conda` (0 rule files contain `conda:`); MAE is a negative-binomial test; demo took ~85 min on 10 cores and gave no significant outlier | ran: `drop init` in `as-drop` (error for the old form, config read, `conda:` grep = 0); demo numbers from the audit's run (not re-run: 63/70-step run with the results file written, results.tsv 258 rows, min padjust 1) | claim "v1.4+ uses FRASER 2.0" replaced by the observed `FRASER_version: "FRASER2"` default |
| Invented error messages; AE not reproducible | P1 | Common Errors table rebuilt from messages seen in runs (colData slot, BAM index, OHT `smaller than 2`, OUTRIDER q, `No significant events`, LeafcutterMD empty counts, `drop init`, silent chr join); the three invented ones deleted. Seed advice: the audit's suggested `set.seed()` does NOT work (9,165 of 20,010 p-values still differ); `SerialParam(RNGseed=1)` does (0 differ), no seed 9,841 differ | ran (`ae_seed.R`, FRASER 2.6.1, AE q=5, 4 fits) | |
| LeafcutterMD: outputs, correction, limits | P1 | Files named, script locations, XS/index requirement, BH snippet, junction-only limitation | ran: block on the 30-BAM cohort (regtools 1.0.0, leafcutter 0.2.9): 86x30 clusters, BH q<0.05 = 11 (S05 skipping q 6.4e-7, S12 cryptic donor q 2.0e-2, S29 mismatch sample 9, other 0); the R BH snippet reproduces 11; retention and pseudoexon events have no cluster p-value | |
| Tissue-mismatch symptom and detection | P2 | Symptom reworded (PCA 0 calls, AE 15, LeafcutterMD 9 on the shifted synthetic sample); calls-per-sample check added | ran: snippet on the fitted fds (2.2.0); mismatch numbers from the audit + my LeafcutterMD run | |
| Threshold inconsistencies (|z|>=2 vs 0; filter params; "autoencoder" wording) | P2 | zScoreCutoff 0 stated as OUTRIDER/DROP default; example uses FRASER's default variability filter (both gave 667 junctions on the cohort); PCA named as the default fit | ran | |
| Integration block (delta_max, chr naming, GTEx access) | P2 | `bcftools query` + R step derives `delta_max` from `SpliceAI` INFO (max of DS_*; `.` alleles ignored), chr prefix stripped, `stopifnot` on chromosome overlap; dbGaP note | ran on the real SpliceAI `examples/output.vcf` (multi-allelic, `.` entries; AIFM1 record -> 0.19) plus 3 synthetic chr21 hits: only the concordant 90190 joined the patient's junctions; `chr21` vs `21` handled | |
| Unbacked mentions (gnomAD splice constraint filter, ClinVar cross-reference, ComBat / batch covariate) | brief rule | deleted (no runnable code, needs external data); "filter against a disease-gene panel you supply" kept | read | chose delete over write: external databases / not verified with FRASER |
| Redundancy (SKILL vs usage-guide; q, cohort size, tissue, PS3 stated 3-5 times) | brief rule | see deletion list | read | |

## Findings left unfixed

- **P2 single-file layout / no `references/` split and no shipped test dataset**: a restructure and shipping synthetic BAMs is outside a minimal fix; the generator is `01_make_synth_cohort.py` in the audit's `run\scripts`.
- **DROP demo not re-run** (about 85 min): audit's completed run is cited; only `drop init` and config were re-run.
- **MAE / OUTRIDER modules of DROP** and `mamba create` not run (audit did not either).
- OUTRIDER power measured on OUTRIDER's own simulator and one synthetic matrix, not real cohorts.

## Deleted passages and where the content lives

| deleted (from) | now |
| --- | --- |
| usage-guide: Overview tool list, Prerequisites | shortened Overview; install line in SKILL.md "Version Compatibility" |
| usage-guide: "What the Agent Will Do" (7 steps incl. clinical report / PS3, ClinVar, gnomAD) | SKILL.md workflow sections; the report/PS3, ClinVar and gnomAD items are gone by design (Research Use section) |
| usage-guide: Tips (9 bullets: FRASER 2 defaults, cohort size, tissue, GTEx batch, q, PS3, LeafcutterMD, candidates) | SKILL.md: FRASER Workflow (defaults), Cohort Size and Power, Tissue Choice, Choosing q, LeafcutterMD, Common Pitfalls |
| SKILL: "FRASER 2.0 changes vs 1.x" bullets | one paragraph "Differences from FRASER 1.x" |
| SKILL: paragraph after FRASER block on q + "Hyperparameter Tuning" section + "FRASER 2.0: Q Hyperparameter Mistuning" failure mode + q pitfall | "Choosing q" |
| SKILL: "When to Use Outlier vs Differential" two-list section | one paragraph under the decision tree |
| SKILL: OUTRIDER "Few Controls" mechanism ("fails to fit", "convergence warnings") and Common Errors rows `cohort too small`, `convergence not reached`, `encoding-dim search slow` | measured symptom in the failure mode; real messages in Common Errors |
| SKILL: DROP "Cohort >=30 recommended" | Cohort Size and Power (FRASER >=20, OUTRIDER >=50) |
| SKILL: tissue-choice sentence repeated in Pitfalls, "Tissue match required" quality row, batch-effect ComBat text | Tissue Choice; Cohort Size and Power; pitfalls point to them |
| SKILL: quality row "OUTRIDER |z|>=2 conservative" | OUTRIDER block note on `zScoreCutoff` |

## 2026-09-20 post-re-audit patch (orchestrator)

Re-audit (82, Limited Release, no P0) found the AE reproducibility advice wrong: `SerialParam(RNGseed=1)` alone leaves
9,815 of 20,010 p-values differing (`set.seed(1)` alone 9,279); only both together give 0 (audit input 7). SKILL.md and the
example comment now say so. Text-only change; these bytes post-date the audit, so the Skill is promoted with `reaudit: needed`.
