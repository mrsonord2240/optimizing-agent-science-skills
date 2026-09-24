# mediation-same-id: `bio-causal-genomics-mediation-analysis` (theirs, AIPOCH) vs ours (shelf)

Compared 2026-09-21 by execution. Env: `mendelian-randomization-analyst` via `r.sh` (mediation 4.5.1, HIMA 2.3.4, CMAverse 0.1.0, EValue). Scripts in `run/`, logs in `out/`, data in `data/`.

## What each side claims
- **Theirs** (`_theirs/.../SKILL.md`, 10 KB, `author: AIPOCH`, polish changelog dated 2026-06-15): "using the `mediation` R package". Prose only, no scripts. Single-mediator `mediate`, an eQTL multi-gene loop, a methylation-chain sketch, HIMA (old 2.2 API), `medsens`. Says sequential ignorability is untestable and to run sensitivity.
- **Ours** (shelf, 40 KB SKILL.md + 4 example scripts): adds a method taxonomy, VanderWeele 4-way (CMAverse), HIMA 2.3 formula API, BAMA, two-step/MVMR mediation, medDML, mediational E-value, reporting checklist, decision tree, reviewer pushback, error table.

## Provenance (question 1)
- **Cannot establish by git.** The clone has one commit: `git rev-list --all --count` = 1 (`d91ed3d`, 2026-08-15, "archive repo"). `git log`/`show` on the path has no earlier version to match.
- **By content:** none of theirs' distinctive strings (`plot_mediation_diagram`, `run_eqtl_mediation`, "Multi-Omics Mediation", the description sentence, the Quick Start prompts) occur anywhere in the d91ed3d tree (`git grep`, 0 hits). But theirs uses the GPTomics template: `## Version Compatibility` block (562 `.md` files in the clone have that heading), Goal/Approach blocks, the same usage-guide section list, GPTomics-style Related Skills paths, and the HIMA 2.2 call the upstream text describes as the pre-2.3 API. Theirs never names GPTomics.
- **Supported, not proven:** theirs is very likely an earlier, shorter GPTomics text (pre-expansion) re-badged by AIPOCH (polished 2026-06-15, before the 2026-08-15 snapshot). Exact source commit unknown; independent authorship not strictly excluded.

## Shared data (synthetic, so the truth is known; identical files given to both)
`data/A_planted.csv` (n=1500, genotype -> expression -> disease/y_cont, ACME 0.30, ADE 0.20, prob-scale ACME 0.106 from `data/truth.rds`); `B_confounded.csv` (latent U, expression does NOT cause y: true ACME 0, planted rho 0.237); `C_*.csv` (n=800, 100 mediators, M1/M2 true, M3/M4 decoys); `D_interaction.csv` (G x M interaction: CDE 0.2, INTmed 0.2, PIE 0.3, TE 0.7). Fair to both: both sides' canonical example is genotype -> expression -> disease with age/sex/PCs.

## Requests x side
| Request | Side | Executed | Key output (file) | Asserted |
|---|---|---|---|---|
| R1 planted mediation, binary disease + continuous | theirs | yes | ACME 0.105 [0.087,0.126], PM 0.59; continuous 0.314 [0.266,0.370] (`out/theirs_r1.log`). `medsens` as written: error "only valid for the probit link"; text gives no fix | CI covers 0.106 and 0.30: pass |
| | ours | yes | ACME 0.106 [0.088,0.127] (bca, 5000 sims); continuous 0.314 [0.267,0.368] (`out/ours_r1.log`). Same `medsens` error on our main snippet; our Common Errors row says refit probit; then rho_crit 0.30 | pass |
| R2 SI violated (dataset B) | theirs | yes | ACME 0.103 [0.074,0.139], PM 0.82, truth ACME 0; medsens rho_crit 0.2 vs planted 0.237 (`out/theirs_r2.log`) | naive CI excludes true 0 (wrong); rho within 0.08: pass |
| | ours | yes | same ACME; rho_crit 0.2; E-value 1.39 (<1.5 "fragile") (`out/ours_r2.log`, `out/evalue_check.log`). Our E-value snippet as written errors (`hi=NULL`) | pass |
| R3 100 mediators, binary outcome | theirs | as written no; adapted yes | `hima(X=,Y=,...)` -> "argument formula is missing"; adapted to `hima_classic`: M1, M2 only (`out/theirs_r3.log`) | truth recovered after adapting: pass |
| | ours | yes | `hima(formula,...)` as written: M1, M2, no decoys (`out/ours_r3.log`) | pass |
| R4 4-gene eQTL loop + BH | theirs | as written no; adapted yes | error "object med_formula not found" inside `mediate` bootstrap; adapted: M1,M2 FDR 0, decoys FDR 0.81 (`out/theirs_r4.log`) | pass after fix |
| | ours | as written no; adapted yes | same error in shipped `examples/eqtl_mediation.R` (`out/ours_example_eqtl_mediation.log`, `out/ours_r4.log`); same fix: M1,M2 found, decoys not | pass after fix |
| R5 exposure-mediator interaction (D) | theirs | yes, wrong | ACME 0.414, ADE 0.42, total 0.834 vs true TE 0.70; no interaction term, no split (`out/theirs_r5.log`) | total within 0.1: **fail** |
| | ours | yes | `cmest` EMint: cde 0.212, intmed 0.190, pnie 0.299, te 0.707 (`out/ours_r5.log`) | all within tolerance: pass |

Executed with a result: theirs 5/5, ours 5/5. Correct on assertion: theirs 4/5, ours 5/5. Ran as written without repair: theirs 2/5 (R2, R5-wrong), ours 3/5 (R2, R3, R5).

## What only one side does
- **Only ours:** 4-way decomposition (R5 above), HIMA on the installed 2.3.4 API, mediational E-value, MVMR/two-step MR mediation (example ran, `out/ours_example_mvmr_mediation.log`), exposure-induced-confounder handling, a rule that a single-method claim is "exploratory" unless rho_crit/E-value and MR agree, and warnings on rare-outcome ORs and unstable proportion mediated.
- **Only theirs:** nothing functional. Its "PM > 0.8: mediator explains most of the effect" reading, applied to R2, reports strong mediation of a true-null effect (PM 0.82).
- **Both are blind to violated sequential ignorability:** the bootstrap CI excluded the true 0 on both sides (R2). Only the medsens rho (0.2) hints at it; rho_crit was 0.45 on unconfounded data A (`out/evalue_check.log`).

## Verdict: **partial**, close to superset
Ours contains everything theirs does, works with current packages, and adds the assumption and decomposition machinery. Use ours for any request. Theirs suffices only for a plain single-mediator `mediate` + `medsens` run on a continuous or probit outcome, and even then it omits the probit requirement.

## Defects hit
- Theirs: HIMA call is the 2.2 API and fails on 2.3.4; `BH.FDR` column does not exist; `medsens` logit failure undocumented; eQTL loop scoping error.
- Ours: main single-mediator snippet uses a logit outcome then `medsens` (errors; fix only in Common Errors); `evalues.RR(..., hi=NULL)` errors (use `NA`); `examples/eqtl_mediation.R` multi-gene section fails (`med_form` scoping).
