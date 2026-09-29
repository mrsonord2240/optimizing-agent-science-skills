> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@72ba7e0](https://github.com/mrsonord2240/optimized-scientific-skills/tree/72ba7e0949bdeb61322a64248c429b378d42f97e/skills/bio-analytical-validation) match audited candidate `bd66239b9133b70a7522d0d99e3bc4ebbed1b8c1291c74fad26367dfa339b2ab` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-analytical-validation`**
> - Audited working candidate `bd66239b9133b70a7522d0d99e3bc4ebbed1b8c1291c74fad26367dfa339b2ab`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/liquid-biopsy/analytical-validation), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-analytical-validation

Generated: 2026-09-28  
Phase: independent re-audit  
Candidate identity: `bd66239b9133b70a7522d0d99e3bc4ebbed1b8c1291c74fad26367dfa339b2ab`

The re-auditor did not perform the initial audit, fix, or tooling delta. Full
machine output, commands, candidate manifest, and invalid-probe details are in
[`evidence/execution-summary.json`](evidence/execution-summary.json).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 40 | 58 | 98 | 5/5 PASS | ✅ |
| 2 | Variant A | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 3 | Edge | 40 | 58 | 98 | 5/5 PASS | ✅ |
| 4 | Variant B | 40 | 59 | 99 | 5/5 PASS | ✅ |
| 5 | Stress | 39 | 57 | 96 | 5/5 PASS | ✅ |

**Execution Average: 97.6 / 100**  
**Layer 1 Average: 39.6 / 40**  
**Layer 2 Average: 58.0 / 60**  
**Assertion Pass Rate: 25/25 (100%)**

## Veto Results

- Structural veto: PASS — stability, contract, determinism, and security all pass.
- Research veto: PASS — scientific integrity, practice boundaries,
  methodological ground, and code usability all pass.
- No accessible public surface was blocked, deferred, simulated in place of
  execution, or left uninspected.

## Detailed Outputs

### Input 1 — Sampling-only molecule-count calculation

**Prompt:** For 25 ng cfDNA and a 0.05% VAF single-locus variant,
compute haploid genome equivalents under the documented 3.3 pg convention,
expected mutant molecules, sampling-only presence probability, and the input
required for 95% template presence. Cross-check at least two fresh
probability/inversion cases and state what these calculations do not establish.

**Output:** The canonical case produced 7,575.75757576 GE, lambda
3.78787878788, and sampling probability 0.977356417213. The exact one-template
95% requirement at VAF 1e-4 was 29,957.3227355 GE. A fresh k=2 probability
was 0.176045779693, and a fresh k=2/80% inverse solve was 3,992.41112934 GE;
both matched independent SciPy roots. The CLI exited zero under
`PYTHONWARNINGS=error` and explicitly excluded recovery, background errors,
false positives, and assay-calling behavior.

**Scores:** Basic 40/40 | Specialized 58/60 | Total 98/100

**Assertions:**

- PASS — Default 303.03 GE/ng convention and explicit alternate convention.
- PASS — Canonical and fresh k=2 Poisson probabilities.
- PASS — Exact `-log(0.05)` inversion rather than a rounded lambda shortcut.
- PASS — Fresh k=2/80% continuous-root agreement.
- PASS — Sampling-only CLI interpretation boundary.

### Input 2 — Replicated LoB and LoD95 fits

**Prompt:** Re-run the bounded public aggregate pseudo-replicate smoke case,
then fit at least two fresh replicated binary dilution series. Inspect LoD95,
confidence intervals, slope, convergence, target bracketing, separation
rejection, and a non-bracketing failure. Treat all fixtures as computational
tests rather than clinical validation.

**Output:** The fresh blank LoB was 0.000242202728163 and matched the formula.
The inherited aggregate smoke case returned LoD95 0.00396833096549 with an
ordered 95% interval [0.00313605615849, 0.00502148235102] and no warning. Two
fresh replicated series returned LoD95 0.00334601956925 and 0.00459714452988;
both converged with positive slope, ordered intervals, and a reconstructed
target probability of 0.95. Separated data and data that failed to bracket
0.95 were refused with stable candidate-level errors. The CLI reported CI,
slope, convergence, sample count, level count, and bracketing with empty stderr.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**

- PASS — Independent LoB arithmetic.
- PASS — Public aggregate smoke fit with interval and no warning.
- PASS — Two fresh identified replicated fits.
- PASS — Separation and non-bracketing refusal.
- PASS — Complete CLI diagnostics under warnings-as-errors.

### Input 3 — Physical, shape, and fit-domain validation

**Prompt:** Probe every public calculator with invalid
finite/range/type/shape/replicate/binary/k-of-N/grid/target inputs. Each case
must stop with a stable actionable ValueError rather than NaN, infinity, a raw
dependency exception, or a misleading scientific result.

**Output:** Eighteen independent probes covered zero VAF, negative/nonfinite/
Boolean mass, invalid molecule count and target, blank count/shape, probit
length/binary/replicate/confidence contracts, impossible k-of-N, grid
dimension/order/ceiling, and simulation level/replicate constraints. All
eighteen raised the expected stable `ValueError` with zero warnings.

**Scores:** Basic 40/40 | Specialized 58/60 | Total 98/100

**Assertions:**

- PASS — Six finite/range/type probes.
- PASS — Two blank count/shape probes.
- PASS — Four probit-contract probes.
- PASS — Four panel/grid probes.
- PASS — Two simulation probes.

### Input 4 — Theoretical multi-locus sampling bounds

**Prompt:** For the inherited 30 ng two-of-N comparison and two fresh k-of-N
scenarios, compare the grid threshold with an independent continuous root,
check expected monotonic relationships, and verify every result and
command-line output carries the equal-VAF, independence, recovery, background,
and non-assay-LoD interpretation boundaries.

**Output:** The inherited N=16 and N=48 thresholds were 3.41849214618e-5 and
1.10307874488e-5. Their default-grid overestimates versus independent roots
were 1.4046% and 0.3952%. Fresh k=1 and k=3 scenarios had grid overestimates
of 0.3752% and 0.0177%. Every structured result carried the same four model
assumptions and the phrase `not an achieved assay LoD95`; both legacy
assay-looking API names were absent. The warnings-as-errors CLI output exposed
the same boundaries.

**Scores:** Basic 40/40 | Specialized 59/60 | Total 99/100

**Assertions:**

- PASS — Expected N=16/N=48 monotonicity.
- PASS — Two inherited thresholds versus independent roots.
- PASS — Two fresh thresholds versus independent roots.
- PASS — Structured assumptions and retired misleading API names.
- PASS — Complete CLI interpretation boundary.

### Input 5 — Simulation determinism, calibration, and sensitivity

**Prompt:** Run the complete worked example twice, then independently test the
teaching simulator with fresh seeds, two true-LoD values, and two slopes.
Verify deterministic replay, material parameter sensitivity, approximate 95%
calibration at the named true LoD, input rejection, and explicit
non-validation labeling.

**Output:** Two complete example runs were byte-identical and warning-free. A
same-seed replay reproduced the full arrays. Moving `true_lod_vaf` from 1e-3
to 5e-3 changed 833 of 2,400 outcomes and reduced positives from 2,135 to
1,514; changing slope changed 181 outcomes. A fresh 4,000-replicate check at
the named true LoD observed 0.9485 detection. The example labeled Poisson and
multi-locus values as theoretical and the simulation as contrived teaching,
not validation evidence.

**Scores:** Basic 39/40 | Specialized 57/60 | Total 96/100

**Assertions:**

- PASS — Complete-example determinism and warning-free execution.
- PASS — Exact seeded array replay.
- PASS — True-LoD and slope parameter sensitivity.
- PASS — Approximate 95% calibration at the named true LoD.
- PASS — Non-validation interpretation labels.

## Readiness Decision

Static score 94, execution average 97.6, Layer 1 average 39.6, Layer 2 average
58.0, assertions 100%, and both veto gates PASS. All production-readiness
floors are exceeded. The exact candidate is **candidate-ready**.

One non-blocking P2 remains: `ADV-006`, which should replace the unsupported
exact `130–170 bp` preparation range with the primary method's `110–190 bp`
size-selection range and average fragment length of about 165 bp, or cite a
primary source for the narrower range.
