> **Audit record for `bio-machine-learning-omics-classifiers`**
> - Audited working candidate `906900fae480655dca3808442d858f84b17aace68513ed281607842a0151276f`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/omics-classifiers), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-machine-learning-omics-classifiers`**
> - Audited working candidate `906900fae480655dca3808442d858f84b17aace68513ed281607842a0151276f`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/omics-classifiers), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer: bio-machine-learning-omics-classifiers

Generated: 2026-10-03  
Phase: final re-audit 2, full mode (lane 3a-2), independent of the fixers, the initial auditor and the first re-auditor  
Exact candidate: `906900fae480655dca3808442d858f84b17aace68513ed281607842a0151276f` (files=7, bytes=50806; `tools/skill_preflight.py --offline` PASS before and after)

## Outcome

**Candidate-ready.** Score 88/100, grade Production Ready (static 88, execution average 87.9, Layer 1 average 35.1/40, Layer 2 average 52.7/60, assertions 31/33 = 93.9%). Both veto gates pass, no open P0 or P1. All eleven earlier findings (OC-001 to OC-011) hold on the exact bytes. One new text-only P2 (OC-012): several quoted figures are single-setup values.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 35 | 51 | 86 | 4/5 | ✅ |
| 2 | Variant A | 36 | 54 | 90 | 5/5 | ✅ |
| 3 | Variant B | 35 | 53 | 88 | 4/4 | ✅ |
| 4 | Edge | 35 | 53 | 88 | 5/5 | ✅ |
| 5 | Scope Boundary | 33 | 50 | 83 | 3/4 | ✅ |
| 6 | Adversarial | 36 | 54 | 90 | 5/5 | ✅ |
| 7 | Stress | 36 | 54 | 90 | 5/5 | ✅ |

**Execution average:** 87.9/100  
**Assertion pass rate:** 31/33 (93.9%)  
**Static score:** 88/100  
**Final:** 35.2 + 52.7 = 88 (Production Ready)

## Veto gates

Skill veto: PASS (stability, contract, determinism, security). Research veto (Data Analysis): PASS (scientific integrity, practice boundaries, methodological ground, code usability).

## Finding verdicts

| ID | Verdict | Measured on the current bytes |
|---|---|---|
| OC-001 | resolved | Calibration guidance is the same in SKILL.md, usage-guide, failure-modes and code constants; shipped demo 1 gives 0.988x unweighted, 4.193x balanced, 1.106x recalibrated |
| OC-002 | resolved | Planted batch-only signal: per-batch leave-one-batch-out mean 0.48-0.51 vs random-split 0.60-0.67; real signal survives at 0.77 / 0.81 / 0.85; one-class batches listed |
| OC-003 | resolved | Dense neg_log_loss fit 2000/2000 non-zero on two own Golub splits; lasso + 1-SE uses training data only (held-out perturbation leaves c_1se and the support identical) |
| OC-004 | resolved | Isotonic only at n >= 1,000 and >= 100 rarer-class events (999, and 1000 with 52 events, give sigmoid); degenerate calibrator warns |
| OC-005 | resolved | Three-way split; test-split replaced by noise leaves best round, validation score and train/validation predictions bit-identical |
| OC-006 | resolved | Script captions and usage-guide agree with measured output; script numbers match prose |
| OC-007 | resolved | Logistic AUC 0.910 vs 0.907 and 0.824 vs 0.823; RF 0.876 vs 0.891 and 0.821 vs 0.836, higher in 6 of 6 seeds in both setups; RF risk ratio 1.06x to 1.80x and 1.06x to 1.54x; every place in the text is scoped |
| OC-008 | resolved | Relative path from the Skill directory rc 0; foreign cwd relative fails as the comment says; foreign cwd absolute path rc 0 |
| OC-009 | resolved | SKILL.md line 35 and usage-guide line 63 label LightGBM, CatBoost, linear SVM and DLDA as not executed |
| OC-010 | resolved | Test-split perturbation changes no round, loss or train/validation prediction; learning rate 0.03 / 0.1 / 0.3 gives validation logloss 0.588 / 0.597 / 0.610; warning fires at n=300 (round 0); two runs identical. Caveat in OC-012 |
| OC-011 | resolved | usage-guide carries the 100-rarer-class condition; noise caution covers 2, 3, 6 batches; RF Brier 0.1985 raw / 0.2089 sigmoid / 0.2356 isotonic at n=20 reproduced; saga snippets set random_state |

## New findings (P2, text-only)

- **OC-012 Quoted demo and 1-SE figures are setup-specific.** The XGBoost round in the demo is 160 / 133 / 397 / 223 for n_jobs 1 / 2 / 4 / default (test AUC 0.828-0.840); SKILL.md and the script comment quote 223 and 0.577 / 0.601 / 0.632 (n_jobs=4). Golub lasso + 1-SE counts were 369 and 273 on two further splits (quoted 45 / 142 / 60). The 0.09-0.10 leave-one-batch-out spread names no setup (0.07-0.11 on an independent generator). None contradicts a conclusion; state the variability or the setup.

## Inputs

### Input 1 (Canonical): Core Workflow and lasso + 1-SE on real Golub (own splits 31, 32)
Dense fit 2000/2000 non-zero; lasso + 1-SE 369 and 273 of 2,000, held-out AUC 0.97 and 1.00; held-out perturbation leaves selection identical. One assertion fails: the quoted 45 / 142 / 60 do not convey the range (OC-012).

### Input 2 (Variant A): OC-007 per-family reweighting, own generators A and B, 6 seeds each
Logistic: scale moves (1.01x to 1.89x, 1.00x to 1.36x), AUC unchanged. RF: AUC up in 12 of 12 seed runs. All text locations scoped correctly.

### Input 3 (Variant B): SMOTE placement and effect
Noise labels AUC 0.898 before CV vs 0.472 in the imblearn Pipeline; real signal AUC change -0.0076; risk 3.56x vs 0.99x.

### Input 4 (Edge): recalibrate() boundaries, degenerate warning, n=20 recalibration
Boundaries and warning verified through the shipped code; Brier 0.1985 / 0.2089 / 0.2356 reproduced.

### Input 5 (Scope Boundary): bundled XGBoost demo
Test-split independence by construction and perturbation; warning fires at n=300; runs identical; round and loss depend on thread count (one assertion fails, OC-012).

### Input 6 (Adversarial): planted batch effect and noise caution
Batch-only signal collapses, real signal survives, pooled AUC less honest than the per-batch mean; spread 0.07-0.11 at 2, 3, 6 batches.

### Input 7 (Stress): all scripts and blocks under -W error::FutureWarning
Four scripts rc 0; 7/7 SKILL.md blocks on Golub and synthetic data with no warning; cwd handling and not-executed labels verified.

## Coverage and evidence

Reused unchanged evidence: `batch_checks.py`, `calibration_check.py`, `logistic_regression.py` have the same hashes as the first re-audit; all three were re-executed here anyway. Not executed (labelled in the Skill): LightGBM, CatBoost, linear SVM, DLDA. Standing caveats: the sample-size rule comes from synthetic RF/XGBoost bases; no public multi-batch cohort exists, so batch behaviour is checked on synthetic data; Golub is near-separable and shows sparsity and executability only. The preflight no-Skill-root-LICENSE warning is expected (frontmatter `license: MIT` plus repository licence evidence).
