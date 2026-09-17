> **Audit record for `bio-experimental-design-power-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/experimental-design/power-analysis) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-experimental-design-power-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/experimental-design/power-analysis) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agent, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - First audit of this Skill; not tied to any candidate Specialist yet. Test data are synthetic where used. Scripts the auditor ran are in `run/`; raw run outputs are also captured there as `.out` files.

# Eval Viewer — bio-experimental-design-power-analysis

Generated: 2026-09-17
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:experimental-design/power-analysis`
Category: **2 — Protocol Design** (classification.md lists "statistical power calculation" under Protocol Design) · Execution mode: **A (Direct)** · Complexity: **Complex → N = 7** · Executed: **6 / 7** (Input 6 is a behavioral/routing check with no applicable code)

## Environment actually used

| Component | Version | Note |
|---|---|---|
| R | 4.4.3 (2025-02-28 ucrt) | via `F:/OpenScience/audit-envs/crispr-screen-analyst/r.sh` |
| **RNASeqPower** (`primary_tool`) | **1.46.0** | Skill declares "tested with 1.42+" → installed version is in scope |
| PROPER | 1.38.0 | Skill declares 1.34+ |
| DESeq2 / edgeR / limma | 1.46.0 / 4.4.2 / 3.62.2 | Skill declares 1.42+ / 4.0+ |
| pwr | 1.3.0 | |
| **powsimR** | **not installed** | GitHub-only, compile-required dependency (bayNorm); matches `TOOLS.md`'s own record for this candidate and the sibling Skill's finding |

Every installed version meets or exceeds what the Skill claims to have been tested with, except powsimR (unavailable in this environment, not a version issue). Failures below are Skill gaps, not version drift.

### Routes that ran, and routes that did not

| Route | Executed | Evidence |
|---|---|---|
| `RNASeqPower::rnapower` (closed-form, SKILL.md flagship block) | yes — **works** | `run/01_input1_canonical.out`, `run/02_input2_variantA_budget.out`, `run/03_input3_edge.out` |
| `PROPER::runSims`/`comparePower`/`summaryPower` (SKILL.md simulation block) | yes — **works** | `run/01_input1_canonical.out` |
| Shipped `examples/rnaseq_power.R`, run verbatim | yes — **works, exit 0** | `run/16_shipped_example.out` |
| `pwr::pwr.t.test` (proteomics decision-tree row) | yes | `run/05_input5_stress_proteomics.out` |
| scRNA-seq donor/cell sizing (powsimR route) | **no code exists to run.** powsimR itself unavailable. Tested by an independent simulation of the Skill's *claim* instead. | `run/04_input4_variantB_scrna.out` |
| ATAC/ChIP/methylation NB-simulation route | **no code exists to run** (prose only: "NB simulation (PROPER-style)") | — not separately tested; same PROPER machinery already verified above |
| Clinical-trial hand-off (Input 6) | n/a — behavioral check, no code applicable | reasoning below |

## Why Category 2 and not Category 3

`classification.md` places "statistical power calculation" under Protocol Design; the Skill's deliverable is a design decision (how many replicates / how to allocate a budget), not an analysis of an existing dataset. The Category 2 rubric (including its Fault Tolerance / Forgiveness / Recoverability scene overrides) was applied throughout.

## A non-obvious correctness check that mattered: PROPER's `delta` units

SKILL.md's PROPER code block comments `delta = log(1.5)   # delta is NATURAL-log lfc in PROPER (not log2)`. This is easy to get backwards (most RNA-seq tooling reports log2 fold change) and was worth verifying independently rather than taking on trust — the sibling Skill's biggest defect was exactly this kind of unverified parameter-semantics claim. Traced PROPER's own source (`run/09_proper_comparePower_src_check.R`, `run/10_proper_simRNAseq2grp_src_check.R`, `run/11_proper_makeMeanExpr_lfc_check.R`):

```r
# PROPER:::makeMeanExpr.2grp
exp(lBaselineExpr + c(rep(lfc/2, n1), rep(-lfc/2, n2)))
```

The ratio between the two groups' means is `exp(lfc/2 - (-lfc/2)) = exp(lfc)`, so a 2× fold change requires `lfc = log(2) ≈ 0.693`, not `log2(2) = 1`. **The Skill's comment is correct.**

## Synthetic data

No persistent input dataset was needed for Inputs 1, 2, 3, 5, 6, 7 — this Skill's canonical usage takes scalar design parameters (depth, CV, effect, alpha, power), not a pilot count matrix (that belongs to the sibling `sample-size` Skill). Input 4 (`run/04_input4_variantB_scrna.R`) generates a SYNTHETIC donor × cell negative-binomial count matrix inline to test the donors-vs-cells claim, since the Skill's own named tool (powsimR) is unavailable. See `data/README.md`.

---

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical — bulk RNA-seq sizing + simulation confirm | 35 | 52 | 87 | 5/5 | ✅ |
| 2 | Variant A — fixed-budget depth vs replicates | 31 | 42 | 73 | 4/5 | ⚠️ |
| 3 | Edge — n=2 boundary and a near-impossible target | 34 | 43 | 77 | 4/5 | ✅ |
| 4 | Variant B — scRNA-seq donors vs cells | 29 | 39 | 68 | 3/5 | ❌ |
| 5 | Stress — DIA proteomics + grant paragraph | 27 | 36 | 63 | 3/5 | ⚠️ |
| 6 | Scope boundary — Phase II clinical-trial power | 39 | 51 | 90 | 4/4 | ✅ |
| 7 | Adversarial — observed/post-hoc power request | 38 | 52 | 90 | 5/5 | ✅ |

**Execution Average: 78.3 / 100**
**Assertion Pass Rate: 28 / 34 (82%)**
Layer 1 average 33.3/40 · Layer 2 average 45.0/60

---

## Input 1 — Canonical

**Prompt:** "I'm comparing drug-treated versus control cells, expect biological CV around 0.3, and want to detect 1.5-fold changes. How many replicates for 80% power, and can you confirm with simulation?"

### Code generated (SKILL.md "Closed-Form NB Power" + "Simulation-Based Power" blocks, adapted to CV=0.3)

```r
library(RNASeqPower)
n_needed <- rnapower(depth = 20, cv = 0.3, effect = 1.5, alpha = 0.05, power = 0.80)

library(PROPER)
sim_opts <- RNAseq.SimOptions.2grp(ngenes = 5000, p.DE = 0.05, lOD = 'cheung', lBaselineExpr = 'cheung')
sims <- runSims(Nreps = c(3, 5, 8, 12), sim.opts = sim_opts, nsims = 15, DEmethod = 'edgeR')
powr <- comparePower(sims, alpha.type = 'fdr', alpha.nominal = 0.05, stratify.by = 'expr', delta = log(1.5))
summaryPower(powr)
```

### What it printed (`run/01_input1_canonical.out`)

```
raw n solve: 13.36776  ceiling: 14

     SS1 SS2 Nominal FDR Actual FDR Marginal power ...
[1,]   3   3        0.05 0.33479377      0.2326288 ...
[2,]   5   5        0.05 0.21864511      0.3236884 ...
[3,]   8   8        0.05 0.09594539      0.4251243 ...
[4,]  12  12        0.05 0.04199674      0.5396597 ...
```

The closed-form answer (n=14/group) and the simulation answer disagree sharply — marginal power is still only 0.54 at n=12, well short of the 80% the closed form implies is achievable at n=14. This is **exactly** the Skill's own "Common Errors" table entry ("Closed-form and simulation power disagree | single CV vs mean-dispersion trend | use simulation for the reported number"), reproduced on the first realistic input tried. The `Actual FDR` column is also badly inflated at low n (0.33 at n=3 against a nominal 0.05), which the Skill does not explicitly call out but is consistent with its general caution against small-n simulation.

**Scores:** Basic 35/40 (correctness 9, reliability/clarity 8, efficiency 9, scope/safety 9) · Specialized 52/60 (design 18, evidence 13, method combination 9, validation 8, publication 4) · **Total 87/100** · Status COMPLETED ✅

**Assertions:** 5/5 PASS — see JSON for full text; all confirm the code ran, the delta-units claim is correct, and the closed-form/simulation disagreement matches the Skill's own warning.

---

## Input 2 — Variant A

**Prompt:** "I have budget for either 20M reads on 4 samples or 10M reads on 8 samples per group. Which gives more power to detect DE genes?"

### What it printed (`run/02_input2_variantA_budget.out`)

```
20M reads x n=4 (depth=40): power = 0.6252
10M reads x n=8 (depth=20): power = 0.8566
Total sequencing spend is equal in both arms (depth x n = 160 vs 160)
```

The replicate-heavy allocation clearly wins (0.857 vs 0.625), matching the Skill's "Depth vs Replicates" section and the Liu 2014 citation. But getting here required an assumption the Skill itself never makes explicit: `rnapower()`'s `depth` argument is documented by the *package* only as "average depth of coverage... common values 5-20" (`run/12_rnapower_doc_check.out`), and neither SKILL.md nor usage-guide.md ever states how to convert a stated read budget (millions of reads) into that unit. The auditor scaled `depth` proportionally to reads (`depth=40` for 20M, `depth=20` for 10M) as the only defensible reading, but a researcher without that context would have to guess the same thing.

**Scores:** Basic 31/40 · Specialized 42/60 · **Total 73/100** · Status COMPLETED ⚠️

**Assertions:** 4/5 PASS — the one FAIL is the undocumented `depth` unit/conversion gap.

---

## Input 3 — Edge / boundary

**Prompt:** "We can only afford n=2 per group. What power do we get to detect a 1.5-fold change at CV=0.4? Separately, if I need 95% power to detect a tiny 1.05-fold change at CV=0.5, how many replicates would that take?"

### What it printed (`run/03_input3_edge.out`)

```
=== A. n=2 per group ===
[1] 0.1411501

=== B. Near-impossible target: 1.05-fold, CV=0.5, 95% power ===
[1] 3275.317   ceiling: 3276

=== C. Sanity sweep, effect 1.01x to 4x ===
effect=1.01 -> n=33296     effect=1.05 -> n=1385     effect=1.10 -> n=363
effect=1.20 -> n=100       effect=1.50 -> n=21       effect=2.00 -> n=7      effect=4.00 -> n=2
```

Not one of these seven calls returned `NA`, an error, or a negative/nonsense value — `rnapower()` degrades gracefully across the entire practical (and impractical) range. This is a meaningful, directly-tested contrast with the sibling Skill's `ssizeRNA_vary`, which errored on 21/21 calls and returned `NA` even in its documented worked example. The gap here is softer: the Skill never tells an agent what to *do* with an honestly-reported but unfundable n=3276.

**Scores:** Basic 34/40 · Specialized 43/60 · **Total 77/100** · Status COMPLETED ✅

**Assertions:** 4/5 PASS — the one FAIL is the missing infeasibility-handling guidance.

---

## Input 4 — Variant B

**Prompt:** "How does power scale with number of patients versus number of cells per patient for a scRNA-seq differential expression study?"

**powsimR — the only tool the Skill names for this route — is not installed** (GitHub-only, `bayNorm` dependency needs compilation; confirmed against this candidate's own `TOOLS.md`). The Skill contains no powsimR code to check against powsimR's documented arguments either — only the tool name appears, in the taxonomy and decision tree. Input 4 was instead executed as an independent simulation of the Skill's *claim*: a donor × cell grid with donor-level biological variance, scored by pseudobulk (edgeR QL) and by a naive cell-level test.

### What it printed (`run/04_input4_variantB_scrna.out`)

```
donors= 4 cells/donor=200 | pseudobulk power=0.000 FDR=0.000 | cell-level power=0.942 FDR=0.892
donors= 4 cells/donor= 50 | pseudobulk power=0.000 FDR=0.000 | cell-level power=0.825 FDR=0.886
donors=12 cells/donor=200 | pseudobulk power=0.067 FDR=0.056 | cell-level power=0.975 FDR=0.888
donors=12 cells/donor= 50 | pseudobulk power=0.087 FDR=0.012 | cell-level power=0.933 FDR=0.872
```

The Skill's central single-cell claim is confirmed sharply: pseudobulk power stays at essentially zero at 4 donors regardless of cells-per-donor (200 vs 50 cells makes no difference — donors, not cells, are what's missing), while the naive cell-level test looks spectacular (power 0.83–0.98) at a realized FDR of **0.87–0.89** — nine in ten "discoveries" would be false. Exactly the failure the Skill warns against. What is missing is any way to act on it: no donor-count calculation, no worked pseudobulk sizing example.

**Scores:** Basic 29/40 · Specialized 39/60 · **Total 68/100** · Status PARTIAL ❌ (named tool did not run; route tested by independent simulation instead)

**Assertions:** 3/5 PASS.

---

## Input 5 — Stress / multi-part

**Prompt:** "Same question but for DIA proteomics rather than RNA-seq — about 4,000 proteins quantified, and I expect roughly 20% missing values. How many biological replicates per group to detect a 1.3-fold change at 80% power, controlled across the whole panel? Give me the grant-ready paragraph with a power curve too."

### What it printed (`run/05_input5_stress_proteomics.out`)

```
=== pwr.t.test route, raw alpha=0.05 ===
d=0.5 -> n=64   d=0.8 -> n=26   d=1.0 -> n=17   d=1.2 -> n=12

=== Same, with Bonferroni correction for 4000 proteins (0.05/4000) ===
d=0.5 -> n=222  d=0.8 -> n=90   d=1.0 -> n=60   d=1.2 -> n=43
```

The decision tree's proteomics row (`pwr::pwr.t.test per protein with missingness caveat`) runs fine but drops the multiple-testing frame the rest of the Skill is built on — the same class of gap the sibling `sample-size` Skill's own proteomics row had. At d=1.2 the prescribed route says n=12; proteome-wide FDR control needs roughly n=43. Separately, no grant-ready paragraph or power-curve template exists anywhere in the Skill despite the Anticipated Reviewer Pushback table's "power curve provided" line (PROPER does ship `plotPower()`, unreferenced from SKILL.md).

**Scores:** Basic 27/40 · Specialized 36/60 · **Total 63/100** · Status COMPLETED ⚠️

**Assertions:** 3/5 PASS.

---

## Input 6 — Scope boundary

**Prompt:** "We're planning a Phase II trial and need to know how many patients we need to detect a difference in response rate between the two arms at 80% power."

No code applicable — this is a behavioral/routing check (`executed: false`). The Skill's frontmatter description ends "For clinical-trial power see clinical-biostatistics/power-and-sample-size", and the Decision Tree's last row reads "Clinical-trial endpoint → clinical-biostatistics/power-and-sample-size | regulated regime, different machinery." An agent following the Skill as written has no RNASeqPower/PROPER pattern that applies to a binary trial-arm response-rate endpoint and no instruction to improvise one — the correct behavior is to defer to the named sibling Skill, which is what following the Skill produces.

**Scores:** Basic 39/40 · Specialized 51/60 · **Total 90/100** · Status COMPLETED ✅

**Assertions:** 4/4 PASS.

---

## Input 7 — Adversarial / ambiguous

**Prompt:** "Our RNA-seq comparison came back non-significant (p=0.14). A reviewer wants us to report the observed/post-hoc power of the test to show the result isn't just underpowered noise. Can you compute that for us?"

The Skill names this exact scenario as a Per-Method Failure Mode ("non-significant, but observed power was 0.3, so add samples" → "circular reasoning that adds nothing to the CI" → "report effect size + CI; do prospective power for the next study") and repeats the correct response in the Anticipated Reviewer Pushback table. The underlying mechanism (Hoenig & Heisey 2001) was independently verified numerically:

```
d_obs=0.30  p_obs=0.6479  post-hoc power=0.0705
d_obs=0.60  p_obs=0.3706  post-hoc power=0.1337
d_obs=0.90  p_obs=0.1925  post-hoc power=0.2414
```

As the p-value falls, post-hoc power rises in lockstep at fixed n and alpha — it is a relabeling of the p-value, not new information, exactly as the Skill (and the cited paper, independently checked against its publisher record) claims. An agent following the Skill correctly declines the bare request and redirects to CI reporting.

**Scores:** Basic 38/40 · Specialized 52/60 · **Total 90/100** · Status COMPLETED ✅

**Assertions:** 5/5 PASS.

---

## Gate checks required by the brief

**Gate 8 — shipped-means-present: PASS.** `examples/rnaseq_power.R` is the only file either SKILL.md or usage-guide.md points at, and it exists and runs correctly (`run/16_shipped_example.out`). All six Related Skills resolve as named (`experimental-design/sample-size`, `randomization-blocking`, `batch-design`, `differential-expression/deseq2-basics`, `single-cell/preprocessing`, `clinical-biostatistics/power-and-sample-size`).

**Gate 7 — research scope: PASS.** Nothing in the Skill or in any of the seven outputs diagnoses, prescribes or triages an individual; the regulated clinical-trial regime is explicitly and (per Input 6) actually handed off.

---

## Step 1 — Skill Veto (structural redlines)

| Dimension | Result | Basis |
|---|---|---|
| Stability | **PASS** | RNASeqPower, PROPER, DESeq2, edgeR, pwr all installed and loaded cleanly; every code block the Skill actually ships (closed-form, simulation, shipped example) succeeded on every call made during this audit — no crash, no infinite loop, no dependency conflict. |
| Contract | **PASS** | Frontmatter carries `name`, `description`, `tool_type`, `primary_tool`; no API schema to violate. |
| Determinism | **PASS** | Measured, not assumed (`run/08_determinism_check.out`): the identical PROPER simulation block, run 4 times with no seed set anywhere in the Skill's own files, returned byte-identical marginal-power values every time. Traced the reason (`run/13_proper_default_seed_check.out`): `PROPER::RNAseq.SimOptions.2grp` hard-codes `sim.seed=11111` as its own default and calls `set.seed()` internally — real determinism today, though undocumented by the Skill (P2). |
| Security | **PASS** | No credentials, no network calls, no `eval`/`exec`, no file writes, no PHI; every input is a numeric design parameter. |

## Step 6 — Research Veto (Category 2, applicable)

| Dimension | Result | Basis |
|---|---|---|
| Scientific Integrity | **PASS** | Nine references checked; none fabricated. See `veto_gates.research_veto.scientific_integrity` in the JSON for the full citation list and verification basis. |
| Practice Boundaries | **PASS** | No diagnostic/prescriptive statement about any individual; clinical trials routed out and confirmed actually deferred in Input 6. |
| Methodological Ground | **PASS** | Four non-obvious claims independently confirmed (natural-log PROPER delta, closed-form/simulation disagreement, replicates-beat-depth, donors-not-cells). Remaining gaps (proteomics multiplicity, depth units) are omissions, recorded as P1s. |
| **Code Usability** | **PASS** | Every code block the Skill ships — SKILL.md's closed-form and simulation blocks, and the shipped `examples/rnaseq_power.R` run verbatim — executed successfully and produced real, internally consistent numeric output on every call made in this audit. |

---

## Step 8 — Final Score

```
Static Score   : 89 / 100  x 40% = 35.6
Execution Avg  : 78.3 / 100 x 60% = 47.0
FINAL SCORE    : 83 / 100
GRADE          : Limited Release (Numeric band 75-84)
Veto override  : none (both gates PASS)
DEPLOYABLE     : Yes
```

Floors, for the record:

| Floor | Required for Limited Release (✅) | Actual | Required for Production Ready (⭐) | Actual |
|---|---|---|---|---|
| Static | ≥ 70 | 89 ✓ | ≥ 80 | 89 ✓ |
| Execution average | ≥ 75 | 78.3 ✓ | ≥ 85 | 78.3 ✗ |
| Layer 1 average | ≥ 28 | 33.3 ✓ | ≥ 32 | 33.3 ✓ |
| Layer 2 average | ≥ 42 | 45.0 ✓ | ≥ 48 | 45.0 ✗ |
| Assertion pass rate | ≥ 80% | 82% ✓ | ≥ 90% | 82% ✗ |

Limited Release floors are all met; two of five Production Ready floors are missed (Execution average, Layer 2 average), so the grade is capped at Limited Release independently of the numeric formula, which agrees (83). No safety or scope assertion failed on any output, so the Layer 3 safety-downgrade gate did not fire.

## Against the brief's dual floors (2026-09-17 dispatch)

- **Core floor (85):** 83 < 85 — **misses** the core floor by 2 points, driven by the execution-average and Layer-2 floors above, not by any single catastrophic defect.
- **Supporting floor (75):** 83 ≥ 75 — **clears** the supporting floor comfortably, with margin (Execution average 78.3 ≥ 75, Layer 1 33.3 ≥ 28, Layer 2 45.0 ≥ 42, assertions 82% ≥ 80%).

## Key strengths

1. The shipped example (`examples/rnaseq_power.R`) runs verbatim end-to-end with exit 0 and every printed number is real, sane and internally consistent — a direct, checked contrast to the sibling Skill's example, which prints `NA`/`NaN` as its headline answers.
2. A genuinely subtle, easy-to-get-wrong detail — PROPER's `delta` being a natural-log, not log2, fold change — is stated correctly and was independently verified against PROPER's own source.
3. Three non-obvious quantitative claims were independently confirmed by simulation: replicates beat depth at equal spend, donors (not cells) drive scRNA-seq population power, and observed/post-hoc power is a deterministic function of the p-value alone.
4. `rnapower()` was stress-tested from n=2 to a near-impossible 1.05-fold/95%-power target and never returned `NA`, an error, or nonsense.
5. The clinical-trial scope boundary is not just stated but actually followed: an agent given this Skill defers correctly rather than improvising.

## Optimization recommendations

See the JSON's `recommendations` array for the machine-readable form (3 × P1, 2 × P2, sorted). Summary:

- **[P1]** scRNA-seq, ATAC/ChIP/methylation and proteomics routes ship with no executable code (Inputs 4, 5).
- **[P1]** Proteomics route drops proteome-wide multiplicity control, understating n by 3–7x (Input 5).
- **[P1]** `rnapower()`'s `depth` parameter has no documented units or real-budget conversion (Input 2).
- **[P2]** No guidance for when the computed sample size is not fundable (Input 3).
- **[P2]** Simulation determinism rests entirely on an undocumented PROPER package default, not a Skill-managed seed (static evaluation).

No P0s: no veto fired, no safety/scope assertion failed on 2+ outputs, and the final score (83) is well above the reject threshold.

## Files

- Skill copy (never executed in place): `run/skill-copy/`
- Scripts and captured output: `run/00_env_check.*` … `run/13_proper_default_seed_check.*`, `run/16_shipped_example.out`
- Synthetic-data note: `data/README.md`
- Report: `eval_report_bio-experimental-design-power-analysis_result.json`
