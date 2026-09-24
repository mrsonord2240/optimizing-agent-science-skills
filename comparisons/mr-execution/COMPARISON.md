# Comparison: mr-execution (2026-09-21)

**Theirs** (Open Science marketplace, `aipoch/medical-research-skills@d924410`): `two-sample-mr-exposure-screening-reference-grounded` and `mendelian-randomization-protocol-designer`. **Ours** (shelf): `bio-causal-genomics-mendelian-randomization`. Env: `mendelian-randomization-analyst` via `r.sh` (TwoSampleMR 0.7.9, MRPRESSO 1.0).

## What each side claims (read in full before running)
- **Theirs, both:** "Generate a complete, structured research design, not a literature summary, not a tool list." Fixed A-J / A-L output: Lite/Standard/Advanced/Publication+ configs, one recommended plan, workflow, evidence tiers, claim boundaries, figure plan, verified-reference discipline. Files: SKILL.md + 8 reference `.md` files + an eval JSON. **No scripts, no code, no call signatures.** Input-validation section redirects anything outside plan design.
- **Ours:** "Estimate causal effects... implements IVW, Egger, weighted median/mode, MR-RAPS, CAUSE, MR-PRESSO, MVMR..." SKILL.md (regime decision tree, per-method failure modes, thresholds, reconciliation table) + 4 runnable R examples.

## Shared data (synthetic, `run/01_simulate.R`, seeds fixed)
Why fair: neither side ships data; planted truth is the only way to test recovery; both sides' tooling is TwoSampleMR/MRPRESSO, so no format favors one. 400 SNPs, exposure N=200k, outcome N=100k, 100 real instruments, **30 planted invalid (directional pleiotropy, alpha~N(0.02,0.005), independent of gamma)**, 60/52 SNPs allele-swapped in the outcome file to force harmonisation. Scenario A: true beta = 0.30. Scenario B: true beta = **0** (pleiotropy only; a false-positive trap). Truth: `data_A/truth.txt`, `data_B/truth.txt`.

## Requests
- **R1** (data A): "Estimate the causal effect of X on Y; how far can I trust it?"
- **R2** (data B): "IVW says X causes Y. Is that real, or pleiotropy?"
- **R3** (no data): "Write me the study protocol for this MR question."

## Results

| Req | Side | executed | Key output (file) | Asserted |
|---|---|---|---|---|
| R1 | Ours | **true** | IVW 0.397 [0.358,0.435]; Egger 0.348 [0.246,0.450]; WM 0.336 [0.301,0.371]; mode 0.305 [0.230,0.381]; RAPS 0.389; Q p=8e-57; PRESSO global p<3.3e-4; I2_GX 0.996 (`run/out_ours_A.txt`) | truth 0.30 inside CI: Egger, mode only; IVW, WM, RAPS miss (biased +0.04 to +0.10) |
| R1 | Theirs as written | **false** | protocol only; zero data-derived numbers (`run/04_theirs_protocol_output.md`, `run/out_theirs_protocol_check.txt`) | no estimate, no Q, no F, no instrument count |
| R1 | Theirs, ceiling (only the stack in their `method-library.md`, my code) | true | IVW 0.397, WM 0.336, Egger 0.348; PRESSO global p<0.001; their tier rule -> "DOWNGRADED" (`run/out_theirs_A.txt`) | same estimates as ours; flags pleiotropy via PRESSO |
| R2 | Ours | **true** | IVW 0.0995 p=2.4e-6 (false positive); WM 0.053 p=0.006; RAPS 0.089 p=4.9e-5; Egger 0.024 p=0.72; mode -0.006 p=0.82; Q p=1e-47; PRESSO global p<3.3e-4, outlier-corrected still 0.070 p=1.5e-4; Egger intercept p=0.24 (`run/out_ours_B.txt`) | truth 0: 3 of 5 estimators falsely significant; global-pleiotropy flags fire |
| R2 | Theirs as written | **false** | cannot say whether 0.0995 is real | none possible |
| R2 | Theirs, ceiling | true | IVW 0.0995, WM 0.053, Egger 0.024; tier "DOWNGRADED" (`run/out_theirs_B.txt`) | downgrade fired only because their "PRESSO when justified" step was run |
| R3 | Ours | prose | regime tree, thresholds, STROBE-MR pointer; no Lite/Standard/Advanced structure, no figure plan (by reading) | n/a |
| R3 | Theirs | prose | full A-L protocol, 4 configs, claim-boundary language, evidence tiers (by reading; `run/04_...md`) | n/a |

Executed: ours 2/2 code requests; theirs 0/2 as written (2/2 only if an agent ignores the prose and runs the tools their method-library merely names).

## What only one side can do
- **Ours only:** produce an estimate from files; report F (mean 280/226) and I2_GX (0.996, so Egger is valid); mode, MR-RAPS; Steiger (TRUE, p~0) with a guard for its silent NULL; explicit `NbDistribution` >= 10000 rule (theirs, run at the default 1000, got MRPRESSO's "Outlier test unstable" warning with no guidance: `run/out_theirs_A.txt`); overlap/winner's-curse (MRlap), MVMR conditional F, cis-MR + coloc.
- **Theirs only:** the deliverable a grant/protocol reader wants: four workload tiers, reference-verification discipline, claim-boundary and downgrade language, sparse-IV fallback, ancestry/overlap/phenotype checklist, "anti-overdesign" rule. Ours has none of this scaffolding.
- Their pleiotropy warning is real but **generic**: it names Egger/PRESSO/Q and downgrade triggers, and cannot tell you these data are pleiotropic. Their tier rule is direction-based (IVW, WM, Egger all positive in B, `sens_qual_direction_only = TRUE`); only the PRESSO/intercept trigger prevents a "sensitivity-qualified" label.

## Verdict: **distinct** (partial at the margin)
The premise is true. Theirs are planners; you cannot get a number out of them. Ours runs the estimators and, in this test, the ceiling of their named stack reproduces ours to the digit, so the estimator content overlaps but their Skills never execute it. Prefer ours to analyse data; prefer theirs to write the protocol/paper plan first, then execute with ours. On the demonstrated difference: on data B, only running code shows that IVW/WM/RAPS all say "causal, p<0.006" for a true null while Egger and mode do not.

## Defects hit (one line each)
- **Ours:** SKILL.md MR-PRESSO snippet `which(Pvalue < 0.05 / nrow(dat))` double-Bonferroni-corrects (MRPRESSO's outlier P is already multiplied by n): it flagged 0 outliers on both datasets while PRESSO's own rule flagged 11 (9 true) on A and 8 (8 true) on B (`run/out_presso_outliers_{A,B}.txt`; source check `run/out_presso_source_check.txt`). Silent under-detection.
- **Ours:** reconciliation row "IVW sig, WM sig, mode null -> trust IVW + median" would endorse the false positive in data B; only the publication rule (needs non-significant PRESSO global) and Q catch it.
- **Ours:** `NbDistribution = 10000` (as instructed) did not finish in 40 min here on a shared CPU; I killed it (my PIDs) and used 3000 (`02_ours.R` arg). Not a defect per se; cost note.
- **Theirs:** no code, no data path, no NbDistribution or F/Isq guidance; "pleiotropy review: explicit test or justified omission" allows omission.
- **Theirs:** eval JSONs mark code usability "N/A ... Mode A skill", consistent with the finding.
- Machine was shared with another comparer's ~20 R workers; wall-clock only.

Scripts: `F:\OpenScience\comparisons\mr-execution\run\` (01 simulate, 02 ours, 03 theirs ceiling, 04-05 theirs prose + checker, 06-07 PRESSO checks).
