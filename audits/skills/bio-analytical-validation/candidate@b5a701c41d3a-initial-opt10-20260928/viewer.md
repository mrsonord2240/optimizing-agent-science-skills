> **Audit record for `bio-analytical-validation`**
> - Audited working candidate `b5a701c41d3afe697766a02a11b2954e12ff9d42`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/liquid-biopsy/analytical-validation), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-analytical-validation

Generated: 2026-09-28  
Phase: bounded diagnostic initial audit  
Exact candidate: `0bc0b31fc52742dbec1034f698103434cc9460c3` / `b5a701c41d3afe697766a02a11b2954e12ff9d42`

## Outcome

The exact candidate is **not ready**. Its diagnostic score is **59/100
(Reject)**, and a Methodological Ground research-veto failure independently
forces rejection. The decisive issue is not installation: all four shipped
Python entry points run. The decisive issue is that the panel calculator calls
a sampling-only independent-binomial lower bound an achieved
`panel_integrated_lod95` without modeling recovery, consensus depth,
background error, false positives, or empirical detection.

This is an initial diagnostic audit, not final certification. Route the five
open findings to `fix-scientific-skill`, then independently re-audit the fixed
bytes.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 33 | 45 | 78 | 3/4 | ✅ |
| 2 | Variant A | 29 | 34 | 63 | 3/4 | ⚠️ |
| 3 | Edge | 14 | 20 | 34 | 0/4 | ❌ |
| 4 | Variant B | 25 | 25 | 50 | 3/4 | ❌ |
| 5 | Stress | 31 | 38 | 69 | 3/4 | ⚠️ |

**Execution average:** 58.8/100  
**Assertion pass rate:** 12/20  
**Static score:** 59/100  
**Arithmetic:** 59 × 0.4 = 23.6; 58.8 × 0.6 = 35.3; 23.6 + 35.3 = 58.9 → **59/100**

## Veto gates

### Skill veto

| Gate | Result | Basis |
|---|---|---|
| Operational stability | PASS | Every entry point executed; no infinite loop or dependency conflict. |
| Structural contract | PASS | Valid frontmatter contains `name` and `description`; public surfaces are consistent Python modules. |
| Determinism | PASS | Seeded example output is byte-identical across two complete runs. |
| System security | PASS | No raw-code execution, shell interpolation, credentials, or destructive operations. |

### Research veto

| Gate | Result | Basis |
|---|---|---|
| Scientific integrity | PASS | No fabricated identifier, trial, p-value, sample size, or efficacy data in tested outputs. |
| Practice boundaries | PASS | Outputs remain technical analytical-method calculations, with no patient diagnosis or treatment advice. |
| Methodological ground | **FAIL** | Input 4 presents a sampling-only lower bound as assay LoD95; see ADV-001. |
| Code usability | PASS | All runnable files execute under the pinned environment; robustness findings do not meet the hard un-runnable-code trigger. |

## Static evaluation

| Category | Score | Rationale |
|---|---:|---|
| Functional suitability | 7/12 | Core sampling and LoB math works; confidence intervals, a complete LoD/LoQ workflow, and a defensible panel LoD are missing. |
| Reliability | 3/12 | Invalid cases produce NaN, zero, raw exceptions, or an unidentified fit estimate. |
| Performance/context | 6/8 | Compact primary file and short scripts; duplicated content and implementations create some drift. |
| Agent usability | 9/16 | Strong conceptual decision aids; weak input contracts, output schema, diagnostics, and stop rules. |
| Human usability | 5/8 | Natural prompts and examples; unsafe failure behavior undermines forgiveness. |
| Security | 8/12 | No secret or command risk; domain inputs are not validated. |
| Maintainability | 8/12 | Small modules, but duplicated logic, no regression suite, and an inert parameter. |
| Agent-specific | 13/20 | Precise trigger and deterministic tools; no structured composition contract or reliable escape hatches. |
| **Subtotal** | **59/100** | Sum verified. |

## Detailed executions

Full machine-readable values and direct-entry-point transcripts are in
[`evidence/execution-summary.json`](evidence/execution-summary.json). Prompts are
in [`inputs.json`](inputs.json), and the bounded harness is
[`run_cases.py`](run_cases.py).

### Input 1 — Canonical: single-locus Poisson sampling

**Prompt:** Given 25 ng of cfDNA, calculate the haploid genome-equivalent
count, expected mutant molecules, and sampling-only detection probability for
a 0.05% VAF single-locus variant. Also report the mass required for the
lambda=3 sampling threshold and state what this calculation does not prove.

**Executed surface:** `scripts/ge_and_poisson.py` plus imported public
functions.  
**Output:** 8,250 GE; lambda 4.125; sampling probability
0.9838365054118341; lambda=3 requires 6,000 GE or 18.1818 ng under the shipped
330 GE/ng convention. Direct CLI exit 0.

**Assertions:**

- PASS — GE and lambda are internally consistent.
- PASS — Probability matches `1 - exp(-lambda)`.
- PASS — Inversion returns 6,000 GE and 18.1818 ng.
- FAIL — Direct output does not say that recovery, consensus depth, background
  error, and calling behavior are excluded.

### Input 2 — Variant A: blank plus LoD95 fit

**Prompt:** Use a bounded analyte-free blank fixture and five published
aggregate sensitivity rows, retain the pseudo-replicate limitation, and report
fit warnings without making a clinical claim.

**Executed surface:** `scripts/lod95_probit.py` direct and imported.  
**Output:** LoB 0.000242202728163. The bounded aggregate smoke fit returns
LoD95 0.00396833096549 without warning. The shipped direct demo exits 0,
emits `PerfectSeparationWarning` three times, and nevertheless prints LoD95
0.000779 VAF.

**Assertions:**

- PASS — LoB equals mean + 1.645 sample SD.
- PASS — Aggregate smoke fit is finite and warning-free.
- FAIL — Separated direct demo does not refuse or suppress its estimate.
- PASS — Aggregate result remains explicitly smoke-only.

### Input 3 — Edge: invalid inputs

**Prompt:** Reject zero VAF, negative mass, a one-value blank, mismatched
probit arrays, and a positivity threshold larger than the panel.

**Executed surface:** public functions across all three scripts.  
**Output:** zero VAF exposes `ZeroDivisionError`; negative mass returns NaN;
one blank returns NaN with NumPy warnings; mismatched arrays expose a raw
statsmodels `ValueError`; three-of-two loci silently returns 0.0.

**Assertions:** 0/4 PASS. Every requested actionable domain rejection is
absent. This is ADV-002.

### Input 4 — Variant B: panel integration

**Prompt:** Compare two-of-16 and two-of-48 sampling thresholds at 30 ng,
check the grid against a continuous root, and state interpretation assumptions.

**Executed surface:** `scripts/panel_integrated_lod.py` direct and imported.  
**Output:** grid values 3.116982298e-5 and 1.029274772e-5; continuous roots
3.095629069e-5 and 1.008940565e-5. Grid overestimation is 0.69% and 2.02%.
The direct CLI prints these as panel-integrated LoD95 values without model
boundaries.

**Assertions:**

- PASS — 48-locus result is lower than 16-locus result.
- PASS — grid and continuous roots agree within one grid step.
- PASS — entry point exits zero and reports both sizes.
- FAIL — output omits independence, equal-VAF, recovery, and background-error
  assumptions. This supports ADV-001 and the research-veto failure.

### Input 5 — Stress: complete example and parameter sensitivity

**Prompt:** Run the complete example twice, then verify every public simulation
parameter controls the result, especially `true_lod_vaf`.

**Executed surface:** `examples/detection_limits.py` twice plus imported
`simulate_dilution_series`.  
**Output:** complete runs are byte-identical and warning-free. With seed 17,
changing `true_lod_vaf` from 1e-5 to 1e-2 yields identical 120-row arrays and
116 detections.

**Assertions:**

- PASS — repeated complete runs are byte-identical.
- PASS — direct example has no runtime warning or error.
- FAIL — `true_lod_vaf` has no effect. This is ADV-004.
- PASS — output labels the example as simulated and makes no patient claim.

## Ordered open findings

1. **ADV-001 / P0 — sampling floor mislabeled as panel LoD95.** Relabel it as
   a theoretical sampling lower bound or implement an empirical assay-detection
   model with recovery and background; state assumptions in every output.
2. **ADV-002 / P1 — public functions lack domain validation.** Add finite,
   range, shape, binary-outcome, replicate-count, and k-of-N checks with stable
   actionable errors.
3. **ADV-003 / P1 — probit demo reports an unidentified fit.** Replace the
   separated demo, detect fit failure, require bracketing, and return diagnostics
   and confidence intervals.
4. **ADV-004 / P1 — `true_lod_vaf` is inert.** Remove it or make it control a
   documented calibrated simulation and add a sensitivity regression.
5. **ADV-005 / P2 — conventions and provenance need precision.** Correct the
   330 GE/ng explanation and distinguish the HCC1395 truth set from fragmented
   SEQC2 Sample A-derived materials with stable identifiers.

The durable ledger is [`finding-ledger.md`](finding-ledger.md).

## Surface classification and deferrals

| Surface | Classification | Notes |
|---|---|---|
| `scripts/ge_and_poisson.py` | executed | Canonical formula and direct CLI both run. |
| `scripts/lod95_probit.py` | executed-with-product-warning | Stable aggregate API path plus separated shipped CLI. |
| `scripts/panel_integrated_lod.py` | executed-with-methodological-finding | Direct CLI, grid comparison, and continuous root. |
| `examples/detection_limits.py` | executed-with-interface-finding | Full run repeated and parameter sensitivity tested. |

Deferred executable surfaces: **none**.  
Blocked executable surfaces: **none**.  
Restricted-access items: **none**.  
Minor repairs: **none**; every open issue changes a method, claim, interface,
validation boundary, or provenance judgment.

## Identity, tooling, and safety

- Exact source identity and per-file hashes:
  [`source-identity.json`](source-identity.json).
- Tooling record:
  `F:\OpenScience\audit-envs\bio-analytical-validation\TOOLS.md`, SHA-256
  `fe7b0abec79899f81a33fc194a275f56ed7d29ce30d83fc2e734313d1d07dbb3`.
- Environment fingerprint SHA-256:
  `1827b29fb5f66fbac54fc681b345e57d06ccbb51cf30a4b47c63683b2ce81a8a`.
- WSL `science`, user `sci`, interop unset; Python 3.12.14, NumPy 1.26.4,
  SciPy 1.12.0, statsmodels 0.14.6.
- Candidate and origin trees are clean. No candidate byte changed and no
  `__pycache__` or `.pyc` remains.
- The first 30-second audit-harness timeout is explicitly classified as
  audit-local preflight evidence in
  [`evidence/harness-preflight-failure.txt`](evidence/harness-preflight-failure.txt);
  the 120-second rerun completed and is the scored run.
- No product/control commit, push, PR, release, publication, marketplace
  intake, or remote mutation occurred.

## Transition

Next role: **`fix-scientific-skill`**. A direct re-audit is not appropriate
because ADV-001 through ADV-005 remain open and ADV-001 fails a research veto.
